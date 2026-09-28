"""Validate planning-document consistency only; no science or AWF execution.

Run: python3 docs/tools/validate_specification_package.py
Use --write-report before rebuilding the manifest/archive after an intentional edit.
"""
from pathlib import Path
import argparse
import collections
import hashlib
import json
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
checks = []

def check(name, condition, detail):
    checks.append({'check': name, 'passed': bool(condition), 'detail': detail})
    if not condition:
        raise AssertionError(name + ': ' + str(detail))

def sha(data):
    return hashlib.sha256(data).hexdigest()

def run(write_report=False):
    checks.clear()
    backlog=json.loads((ROOT/'FDE_Requirements_and_Backlog.json').read_text())
    specpath=ROOT/backlog['specification_file']; spec=specpath.read_text()
    reqs=backlog['requirements']; work=backlog['work_packages']; epics=backlog['epics']
    byid={w['work_package_id']:w for w in work}
    byreq={w['requirement_ids'][0]:w for w in work}
    reqids={r['id'] for r in reqs}; epicids={e['epic_id'] for e in epics}
    check('version_and_counts',backlog['document_version']=='1.1' and len(reqs)==73 and len(work)==73 and len(epics)==16,{'requirements':len(reqs),'packages':len(work),'epics':len(epics)})
    check('unique_identifiers',len(byid)==len(work) and len(reqids)==len(reqs) and len(epicids)==len(epics),'IDs are unique within each catalogue')
    check('one_package_per_requirement',len(byreq)==len(work) and set(byreq)==reqids and all(len(w['requirement_ids'])==1 for w in work),'Complete one-to-one planning coverage')
    check('epic_membership',all(w['epic_id'] in epicids for w in work) and all(set(e['work_package_ids'])=={w['work_package_id'] for w in work if w['epic_id']==e['epic_id']} for e in epics),'Epics exactly cover their packages')
    check('dependency_references',all(d in byid for w in work for d in w['depends_on']),'All predecessors resolve')
    ancestors={}
    def visit(k,stack):
        if k in stack:raise AssertionError('Dependency cycle: '+k)
        if k in ancestors:return ancestors[k]
        out=set()
        for d in byid[k]['depends_on']:out.add(d);out.update(visit(d,stack|{k}))
        ancestors[k]=out;return out
    for k in byid:visit(k,set())
    check('acyclic_graph',True,'All 73 packages visited without a dependency cycle')
    m0=[w for w in work if w['release_increment']=='M0']
    m1=[w for w in work if w['release_increment']=='M1']
    check('m0_nine_tasks_without_software',len(m0)==9 and all(byid[d]['release_increment']=='M0' for w in m0 for d in ancestors[w['work_package_id']]),'M0 dependencies are exclusively desk procedures')
    check('later_work_requires_g0',all('FDE-E15-W09' in ancestors[w['work_package_id']] for w in work if w['release_increment']!='M0'),'Every conditional package has the desk decision as an ancestor')
    check('m1_independent_of_optional_stages',all(byid[d]['release_increment'] in ('M0','M1') for w in m1 for d in ancestors[w['work_package_id']]),'No M1 package depends on M2, M3 or EXT')
    check('runtime_choice_precedes_core','FDE-E01-W07' in ancestors[byreq['FDE-RUN-001']['work_package_id']],'Core headless implementation requires the bounded runtime decision')
    check('models_and_policy_are_optional',all(w['release_increment']!='M1' for rid,w in byreq.items() if rid.startswith(('FDE-ML-','FDE-VAL-')) or rid=='FDE-AL-002'),'Model/benchmark/policy comparison requirements are outside M1')
    ledger=byreq['FDE-AL-005']['work_package_id']
    check('external_actions_require_ledger',all(ledger in ancestors[byreq[r]['work_package_id']] for r in ['FDE-SIM-001','FDE-EXP-001']),'Compute dispatch and physical campaign design retain accounting prerequisites')
    check('ledger_independent_of_policy_research',byid[ledger]['release_increment']=='M2_ACTIONS' and all(byid[d]['release_increment'] in ('M0','M1','M2_ACTIONS') for d in ancestors[ledger]),'Action accounting can operate without ML training or policy-superiority research')
    cases=[c for w in m0 for c in w['validation_plan']['cases']]
    check('m0_concrete_cases',len(cases)==27 and len({c['id'] for c in cases})==27 and len({c['procedure_and_expected_result'] for c in cases})==27 and all(len(c['procedure_and_expected_result'])>100 for c in cases),'Nine distinct positive/negative/boundary triads')
    check('manual_validation_honesty',all(w['validation_plan']['kind']=='MANUAL_EVIDENCE_PROCEDURE' and w['validation_plan']['commands']==[] for w in m0),'No invented runtime commands for desk procedures')
    check('risk_tier_differentiation',{w['proposed_risk_tier'] for w in m0}=={1,2},dict(collections.Counter(w['proposed_risk_tier'] for w in m0)))
    check('planning_not_runtime',all(w['runtime_contract'] is False and w['planning_status']=='DRAFT_NOT_DISPATCHABLE' for w in work) and backlog['artifact_type']=='PROJECT_PLANNING_SIDECAR_NOT_AWF_RUNTIME_RECORD','No READY contracts or completed scientific gates asserted')
    check('later_acceptance_explicitly_deferred',all(w['validation_plan'].get('readiness')=='DEFERRED_NOT_EXECUTABLE' for w in work if w['release_increment']!='M0'),'Implementation acceptance still requires actual scope and commands')
    check('input_dependency_consistency',all({i['work_package_id'] for i in w['inputs']}==set(w['depends_on']) for w in work),'Input records match graph edges')
    check('specification_hash',sha(specpath.read_bytes())==backlog['specification_sha256'],'Backlog binds exact operative specification bytes')
    check('requirement_text_consistency',all('| '+r['id']+' | '+r['title']+' | '+r['acceptance']+' |' in spec for r in reqs),'All normative requirement rows match the JSON catalogue')
    check('map_coverage',all(w['work_package_id'] in (ROOT/'FDE_Jira_Epic_and_Work_Package_Map.md').read_text() for w in work),'Every package appears in the readable map')
    awf=backlog['awf_compatibility']; source=json.loads((ROOT/'AWF_1.9.1_Source_Inspection.json').read_text())
    check('awf_pin_unchanged',awf['version']=='1.9.1' and awf['source_commit']==source['commit']=='e7d80a691e2ae0a0b55e54f4e5e91e95e5ca7fe5' and awf['ticket_schema_revision']==3 and awf['source_manifest_sha256']==source['manifest_sha256'],'Requested compatibility baseline retained; no adoption claimed')
    check('actual_repository_binding',backlog['project_bindings']['product_repository']=='jkinlay/cooling-fluid' and backlog['project_bindings']['repository_id']==1393836050 and backlog['project_bindings']['jira_project_key'] is None,'Observed GitHub identity bound; unknown Jira/policy fields remain unresolved')
    control=json.loads((ROOT/'M0_Study_Control_Template.json').read_text()); decision=json.loads((ROOT/'Feasibility_Decision_Template.json').read_text())
    check('unaccepted_control_and_decision',control['status']=='PROPOSED_NOT_STARTED' and control['owner_accepted'] is False and control['actual_start_date'] is None and control['authorized_external_spend_gbp']==0 and decision['status']=='NOT_DECIDED' and decision['authorized_work_package_ids']==[] and decision['physical_work_authorized'] is False,'Templates do not assert approval, study completion or paid commitments')
    external=(ROOT/'reviews/Red_Team_04_External.md').read_text(); disposition=(ROOT/'reviews/Red_Team_04_Disposition.md').read_text()
    check('supplied_review_byte_integrity',sha((ROOT/backlog['external_review']['path']).read_bytes())==backlog['external_review']['sha256'],'Supplied review retained at its recorded input hash')
    expected={f'R4-A{i:02d}' for i in range(1,9)}|{f'R4-B{i:02d}' for i in range(1,6)}|{f'R4-C{i:02d}' for i in range(1,7)}
    check('external_findings_covered',set(re.findall(r'\| (R4-[ABC]\d\d) \|',disposition))==expected and all(x in external for x in expected),'All 19 external findings have explicit dispositions')
    historical=[]
    with zipfile.ZipFile(ROOT/'Cooling_Fluid_Discovery_Specification_Package_v1.0.zip') as old:
        oldbacklog=json.loads(old.read('FDE_Requirements_and_Backlog.json'))
        check('original_identifiers_preserved',all(r['id'] in reqids for r in oldbacklog['requirements']) and all(w['work_package_id'] in byid and byid[w['work_package_id']]['requirement_ids']==w['requirement_ids'] for w in oldbacklog['work_packages']),'All original 63 requirement/package identities retained')
        for name in old.namelist():
            if name.startswith(('revisions/','reviews/')) or name=='AWF_1.9.1_Source_Inspection.json':
                historical.append(name);check('historical_bytes:'+name,(ROOT/name).read_bytes()==old.read(name),'Unchanged historical evidence')
    check('superseded_entrypoint','Superseded specification' in (ROOT/'Cooling_Fluid_Discovery_Project_Specification_v1.0.md').read_text() and 'v1.1' in (ROOT/'README.md').read_text(),'Current entrypoints route to v1.1')
    check('no_template_markers','{{REQUIREMENTS}}' not in spec and '{{EPICS}}' not in spec,'Generated tables expanded')
    active=[p for p in ROOT.glob('*.md')]+[ROOT/'reviews/Red_Team_04_Disposition.md']
    missing=[]
    for p in active:
        for dest in re.findall(r'\]\(([^)]+)\)',p.read_text()):
            if '://' in dest or dest.startswith('#'):continue
            dest=dest.split('#')[0]
            if dest=='Cooling_Fluid_Discovery_Specification_Package_v1.1.zip' and write_report:continue
            if not (p.parent/dest).exists():missing.append((p.name,dest))
    check('operative_local_links',not missing,missing or 'Current document links resolve; historical snapshots retain their original context')
    result={'document_version':'1.1','validation_scope':'Planning-document structure, traceability and preserved history; not chemistry, runtime, laboratory, buyer or AWF execution.','all_checks_pass':True,'check_count':len(checks),'counts':{'epics':len(epics),'requirements':len(reqs),'work_packages':len(work),'m0_procedures':len(m0),'m0_acceptance_cases':len(cases),'increments':dict(collections.Counter(w['release_increment'] for w in work))},'checks':checks,'scientific_work_executed':False,'independent_professional_reviews_obtained':False,'awf_adoption_performed':False}
    if write_report:
        (ROOT/'Specification_Package_Validation.json').write_text(json.dumps(result,indent=2)+'\n')
    else:
        manifest=json.loads((ROOT/'PACKAGE_MANIFEST.json').read_text())
        for f in manifest['files']:
            data=(ROOT/f['path']).read_bytes()
            assert len(data)==f['bytes'] and sha(data)==f['sha256'],f['path']
        archive=ROOT/'Cooling_Fluid_Discovery_Specification_Package_v1.1.zip'
        with zipfile.ZipFile(archive) as z:
            assert z.testzip() is None
            assert set(z.namelist())=={f['path'] for f in manifest['files']}|{'PACKAGE_MANIFEST.json'}
            for f in manifest['files']:assert z.read(f['path'])==(ROOT/f['path']).read_bytes(),f['path']
            assert z.read('PACKAGE_MANIFEST.json')==(ROOT/'PACKAGE_MANIFEST.json').read_bytes()
        result['manifest_and_zip_verified']=True
    print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--write-report',action='store_true')
    run(parser.parse_args().write_report)
