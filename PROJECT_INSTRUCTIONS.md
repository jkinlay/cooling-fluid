# Project instructions — Cooling Fluid Discovery

Read [docs/README.md](docs/README.md), [docs/M0_Feasibility_Study.md](docs/M0_Feasibility_Study.md), and the current v1.1 specification before proposing or dispatching project work. The nine M0 desk procedures are the present planning scope. The study control is still proposed, and the G0 decision has not been made; neither the planning backlog nor the Jira tickets authorize spending, experiments, procurement, or later implementation.

The primary research tool for compound analysis is Mathematica and its Chemistry knowledge base, with relevant chemistry plug-ins where available. Reputable external chemical and regulatory databases and reproducible Python code and libraries may supplement it. Record each source, retrieval date, chemical identity, property conditions, units, method, and uncertainty. Separate measured data, correlations, predictions, and claims. Treat missing decisive evidence as UNKNOWN; do not infer safety or deployability from a molecular identity or a single property.

Jira project CFD has Epic CFD-1 and nine M0 Tasks. AWF's configured Jira scope is empty until an explicit ticket selector and ownership are accepted. Do not make AWF Jira lifecycle writes on that basis alone.

Keep candidate-level publication, outreach, supplier contact, paid computation, and laboratory activity within the accepted study control and publication decision. The repository is public. Protect unpublished formulations and confidential information. Preserve the existing feasibility and specification package as historical evidence; its manifest and ZIP hashes are byte-bound.

The project-owned validation command is `python -B docs/tools/validate_specification_package.py`. It checks planning-document consistency and package integrity, not chemical validity or AWF execution.