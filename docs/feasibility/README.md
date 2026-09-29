# Cooling-fluid candidate screen — 29 September 2026

**32 compounds screened; no coolant qualified.** Thirteen meet the declared boiling-range evidence screen, eight fall outside it, and eleven require resolution of a boundary or conflicting source values. Of the thirteen boiling-range matches, twelve have explicit flammability evidence and one (2,3-pentadiene) lacks a primary fire-property record in this pass.

- [Filterable workbook](Cooling_Fluid_Candidate_Table.xlsx): candidates, individual property observations and a data-gap register.
- [Machine-readable dataset](feasibility_table.json): 32 candidate records, 164 observations and 66 source records, with provenance and missing-value states.
- [Flat table](feasibility_table.csv): one row per compound for import.

The named-compound search covers C1–C6 molecules containing C/H/O/N/S/Cl, with no fluorine, plus adjacent boiling-range controls. It is a purposive family-based search, **not an exhaustive enumeration of NIST or all fluorine-free chemistry**. It excludes mixtures, invented compounds and other element families. Known facts from the earlier review and the first lead searches informed the seed list; this was not a blinded preregistration.

## Results

The table uses the inclusive normal-boiling window **45–55°C**. The NIST column below reports the envelope of the retained values and their reported spreads/uncertainties; this is a conservative source-consistency screen, **not a statistical confidence interval**. Original values remain in the dataset and Evidence worksheet. Widely scattered compilations are flagged rather than silently averaged or discarded. Unqualified supplier boiling points do not independently establish measurement pressure.

Flash points are source-reported product/reference values, not project measurements. Inequalities and methods are preserved. In the workbook and CSV relation columns, `EQ` means the source gives a value without an inequality; it does not imply exact measurement. The selected display value is not an adjudicated best estimate; alternatives are retained. GHS categories are not inferred from NIOSH fire classes or molecular identity.

| ID | Compound | CAS | NIST evidence envelope, °C | Boiling screen | Selected flash point, °C | Fire evidence |
|---|---|---|---:|---|---:|---|
| CF001 | Cyclopentane | 287-92-3 | [48.95–49.55](https://webbook.nist.gov/cgi/cbook.cgi?ID=C287923&Mask=4) | PASS | [-20.00](https://www.sigmaaldrich.com/US/en/product/sigald/459747) | GHS Flam. Liq. 2 |
| CF002 | 2,2-Dimethylbutane | 75-83-2 | [49.65–49.85](https://webbook.nist.gov/cgi/cbook.cgi?ID=C75832&Mask=4) | PASS | [-29.00](https://www.sigmaaldrich.com/US/en/product/sial/39730) | GHS Flam. Liq. 2 |
| CF003 | 3-Methyl-1-pentene | 760-20-3 | [53.25–54.65](https://webbook.nist.gov/cgi/cbook.cgi?ID=C760203&Mask=2C) | PASS | [-27.00](https://www.sigmaaldrich.com/VN/en/product/aldrich/111147) | GHS Flam. Liq. 2 |
| CF004 | 4-Methyl-1-pentene | 691-37-2 | [53.55–54.15](https://webbook.nist.gov/cgi/cbook.cgi?ID=C691372&Mask=4) | PASS | [-32.00](https://www.tcichemicals.com/SG/en/p/M0392) | Supplier H225 |
| CF005 | 3-Methyl-1-pentyne | 922-59-8 | [56.85–58.10](https://webbook.nist.gov/cgi/inchi?ID=C922598&Mask=4) | FAIL | UNKNOWN | Unresolved |
| CF006 | 2,3-Pentadiene | 591-96-8 | [47.80–48.60](https://webbook.nist.gov/cgi/cbook.cgi?ID=C591968&Mask=4) | PASS | UNKNOWN | Unresolved |
| CF007 | 1,2-Pentadiene | 591-95-7 | [43.85–47.85](https://webbook.nist.gov/cgi/cbook.cgi?ID=C591957&Mask=4) | UNKNOWN | [-37.00](https://www.tcichemicals.com/US/en/p/P0805) | Supplier H225 |
| CF008 | Ethyl formate | 109-94-4 | [52.85–54.85](https://webbook.nist.gov/cgi/cbook.cgi?ID=C109944&Mask=4) | PASS | [-20.00](https://www.sigmaaldrich.com/US/en/product/sial/112682) | GHS Flam. Liq. 2 |
| CF009 | Propanal | 123-38-6 | [46.85–50.85](https://webbook.nist.gov/cgi/cbook.cgi?ID=C123386&Mask=4) | PASS | [-30.00](https://b2b.sigmaaldrich.com/US/en/product/sigald/538124) | GHS Flam. Liq. 2 |
| CF010 | Acrolein | 107-02-8 | [26.85–86.85](https://webbook.nist.gov/cgi/cbook.cgi?ID=C107028&Mask=4) | UNKNOWN | [-26.11](https://www.cdc.gov/niosh/npg/npgd0011.html) | NIOSH Class IB |
| CF011 | Oxetane | 503-30-0 | [46.75–50.05](https://webbook.nist.gov/cgi/cbook.cgi?ID=C503300&Mask=4) | PASS | [-28.00](https://www.tcichemicals.com/US/en/p/T0473) | Supplier H225 |
| CF012 | Ethyl isopropyl ether | 625-54-7 | [52.85–95.75](https://webbook.nist.gov/cgi/cbook.cgi?ID=C625547&Mask=4) | UNKNOWN | [-24.00](https://www.tcichemicals.com/US/en/p/E0416) | Supplier H225 |
| CF013 | 2,2-Dimethyloxirane | 558-30-5 | [34.85–74.85](https://webbook.nist.gov/cgi/cbook.cgi?ID=C558305&Mask=4) | UNKNOWN | [-32.50](https://www.sigmaaldrich.com/US/en/product/aldrich/531537) | GHS Flam. Liq. 2 |
| CF014 | trans-2,3-Epoxybutane | 21490-63-1 | [53.85–60.00](https://webbook.nist.gov/cgi/cbook.cgi?ID=C21490631&Mask=4) | UNKNOWN | [-27.00](https://www.sigmaaldrich.com/US/en/product/aldrich/w527408) | GHS Flam. Liq. 2 |
| CF015 | Carbon disulfide | 75-15-0 | [45.45–46.65](https://webbook.nist.gov/cgi/cbook.cgi?ID=C75150&Mask=4) | PASS | [-30.00](https://www.sigmaaldrich.com/US/en/product/mm/102210) | GHS Flam. Liq. 2 |
| CF016 | 2-Propanethiol | 75-33-2 | [49.85–59.85](https://webbook.nist.gov/cgi/cbook.cgi?ID=C75332&Mask=4) | UNKNOWN | [-31.00](https://www.sigmaaldrich.com/US/en/product/mm/807532) | GHS Flam. Liq. 2 |
| CF017 | n-Propylamine | 107-10-8 | [46.85–50.85](https://webbook.nist.gov/cgi/cbook.cgi?ID=C107108&Mask=4) | PASS | [<-35.00](https://www.sigmaaldrich.com/US/en/product/aldrich/109819) | GHS Flam. Liq. 2 |
| CF018 | trans-1,2-Dichloroethylene | 156-60-5 | [45.85–49.85](https://webbook.nist.gov/cgi/cbook.cgi?ID=C156605&Mask=4) | PASS | [6.00](https://www.sigmaaldrich.com/KR/en/product/aldrich/d62209) | GHS Flam. Liq. 2 |
| CF019 | 1-Chloropropane | 540-54-5 | [45.85–47.85](https://webbook.nist.gov/cgi/cbook.cgi?ID=C540545&Mask=4) | PASS | [-18.00](https://www.sigmaaldrich.com/US/en/product/mm/818841) | GHS Flam. Liq. 2 |
| CF020 | tert-Butyl chloride | 507-20-0 | [50.05–51.85](https://webbook.nist.gov/cgi/cbook.cgi?ID=C507200&Mask=4) | PASS | [-26.00](https://www.sigmaaldrich.com/US/en/product/aldrich/c56352) | GHS Flam. Liq. 2 |
| CF021 | Methyl tert-butyl ether | 1634-04-4 | [54.85–55.25](https://webbook.nist.gov/cgi/cbook.cgi?ID=C1634044&Mask=4) | UNKNOWN | [-28.00](https://www.sigmaaldrich.com/US/en/product/sial/306975) | GHS Flam. Liq. 2 |
| CF022 | Diethylamine | 109-89-7 | [54.75–56.35](https://webbook.nist.gov/cgi/cbook.cgi?ID=C109897&Mask=4) | UNKNOWN | [-26.00](https://www.sigmaaldrich.com/US/en/product/aldrich/110000) | GHS Flam. Liq. 2 |
| CF023 | Aziridine | 151-56-4 | [53.85–57.85](https://webbook.nist.gov/cgi/cbook.cgi?ID=C151564&Mask=4) | UNKNOWN | [-11.11](https://www.cdc.gov/niosh/npg/npgd0274.html) | NIOSH Class IB |
| CF024 | Acetone | 67-64-1 | [55.85–56.45](https://webbook.nist.gov/cgi/cbook.cgi?ID=C67641&Mask=4) | FAIL | [-17.00](https://www.sigmaaldrich.com/US/en/product/sigald/179124) | GHS Flam. Liq. 2 |
| CF025 | Methyl acetate | 79-20-9 | [55.95–57.75](https://webbook.nist.gov/cgi/cbook.cgi?ID=C79209&Mask=4) | FAIL | [-13.00](https://www.sigmaaldrich.com/US/en/product/mm/589593) | GHS Flam. Liq. 2 |
| CF026 | Cyclopentene | 142-29-0 | [41.85–45.85](https://webbook.nist.gov/cgi/cbook.cgi?ID=C142290&Mask=4) | UNKNOWN | [-34.40](https://www.sigmaaldrich.com/GB/en/product/aldrich/344508) | GHS Flam. Liq. 2 |
| CF027 | 2-Pentyne | 627-21-4 | [54.95–56.75](https://webbook.nist.gov/cgi/cbook.cgi?ID=C627214&Mask=4) | UNKNOWN | [-31.00](https://www.sigmaaldrich.com/US/en/product/aldrich/271357) | GHS Flam. Liq. 2 |
| CF028 | 2,3-Dimethyl-1-butene | 563-78-0 | [55.25–56.45](https://webbook.nist.gov/cgi/cbook.cgi?ID=C563780&Mask=4) | FAIL | [-18.00](https://www.sigmaaldrich.com/US/en/product/aldrich/190403) | GHS Flam. Liq. 2 |
| CF029 | 1,1-Dichloroethane | 75-34-3 | [56.85–57.85](https://webbook.nist.gov/cgi/cbook.cgi?ID=C75343&Mask=4) | FAIL | [-10.00](https://www.sigmaaldrich.com/US/en/product/sial/36967) | GHS Flam. Liq. 2 |
| CF030 | Dichloromethane | 75-09-2 | [38.85–40.85](https://webbook.nist.gov/cgi/cbook.cgi?ID=C75092&Mask=4) | FAIL | UNKNOWN | Unresolved |
| CF031 | cis-1,2-Dichloroethylene | 156-59-2 | [57.85–61.85](https://webbook.nist.gov/cgi/cbook.cgi?ID=C156592&Mask=4) | FAIL | [6.00](https://www.sigmaaldrich.com/CL/en/product/supelco/48597) | GHS Flam. Liq. 2 |
| CF032 | 2,3-Dimethylbutane | 79-29-8 | [57.85–58.25](https://webbook.nist.gov/cgi/cbook.cgi?ID=C79298&Mask=4) | FAIL | [-29.00](https://www.sigmaaldrich.com/US/en/product/aldrich/d151602) | GHS Flam. Liq. 2 |

**The review's predicted zero count above 0°C is contradicted by CF018:** trans-1,2-dichloroethylene has an in-range boiling point and a supplier-reported +6°C closed-cup flash point, while remaining GHS Flammable Liquid Category 2. The alternate Enviro Tech SDS reports 36°F (about +2.22°C), and inconsistently names ASTM D56 and TAG OPEN CUP in different sections. Both descriptions are retained. Chlorine was not excluded by the fluorine-free screen. This compound is not a coolant recommendation.

CF031, the cis isomer, is a separate identity and lies outside the boiling window. CF001 and CF002 have conflicting reported flash points across sources. Missing numerical flash-point values remain for CF005, CF006 and CF030; CF005 and CF030 already fail this boiling-window screen. NIOSH's unspecified flash-point entry for dichloromethane is not converted into a safety pass.

No application-specific fire requirement has been adopted. Overall qualification therefore remains UNKNOWN except where the boiling constraint fails. The JSON includes a separate, explicitly hypothetical screen rejecting reported flammable liquids; this is not an owner/OEM requirement. The current result does not support a universal STOP_DOMAIN or a CONTINUE to platform/physical implementation.

## How much more can be retrieved?

Many later properties are **not yet collected**, rather than proven unavailable. The current source audit distinguishes those states:

| Data | What is established in this pass | Next retrieval route |
|---|---|---|
| Boiling point | Records found for 32/32; 11 boundary/conflict cases | Inspect the underlying measurements, purity and pressure; cross-check independent records. |
| Flash point | Numerical source reports found for 29/32 | Primary SDS/test-method evidence for CF006 first; resolve conflicting methods before using a single value. |
| Vaporization enthalpy | Data located on 30/32 retrieved NIST pages; not yet extracted | Extract temperature-specific values and references; do not equate a 298 K value with latent heat at operating temperature. |
| Vapour pressure | Antoine sections found for 19/32; reported fit ranges span all of 45–55°C for 11/32 | Extract coefficients and units; validate fit range. CF006's retrieved fit is 213.14–247.10 K and must not be extrapolated to 50°C. |
| Density, heat capacity, viscosity, thermal conductivity | Candidate-level coverage not audited | Wolfram, NIST/ThermoML, suitable equation-of-state packages and original papers. |
| Electrical properties | Candidate-level coverage not audited | Published resistivity/permittivity data and supplier test reports; dielectric breakdown is a distinct property. |
| Compatibility, ageing and practical heat transfer | Unassessed for actual grades and hardware | Transferable supplier/OEM evidence, followed by targeted measurements if the application survives. |

**Wolfram is a useful additional retrieval layer.** Its documented `ChemicalData` interface accepts CAS identifiers and lists `BoilingPoint`, `Density`, `DielectricConstant`, `Resistivity`, `VaporPressure`, `Viscosity`, `ThermalConductivity` and `VaporizationHeat`; unavailable properties return `Missing[...]`. `ThermodynamicData` supports condition-dependent properties for its supported substance set. These capabilities do not demonstrate that each property exists for each of the 32 compounds. No Wolfram kernel or candidate-level Wolfram queries were executed for this release. No numerical coverage percentage is claimed.

Use [ChemicalData documentation](https://reference.wolfram.com/language/ref/ChemicalData.html) and [ThermodynamicData documentation](https://reference.wolfram.com/language/ref/ThermodynamicData.html) to run a CAS-by-property coverage audit, preserving raw returned quantities, missing states, conditions, source attribution where available, retrieval date and software version. Match the exact isomer. Wolfram Alpha is useful for spot checks; Mathematica is preferable for a repeatable batch audit. A repeated value may share an upstream source with NIST and is not automatically independent confirmation.

Other concrete routes are the [NIST ThermoML archive](https://www.nist.gov/mml/acmd/trc/thermoml/thermoml-archive) for experimental data and metadata, [NIST fluid systems](https://webbook.nist.gov/chemistry/fluid/) and [CoolProp](https://coolprop.org/fluid_properties/PurePseudoPure.html) for supported fluids, and [Dortmund Data Bank](https://www.ddbst.com/ddb-transport-prp.html) for transport/electrical-property literature coverage. DDB's [public search](https://www.ddbst.com/ddb-search.html) does not itself expose the underlying numerical data. [ECHA CHEM information](https://echa.europa.eu/en/information-on-chemicals) and current manufacturer SDS are routes for substance-specific hazard evidence.

For the remaining gaps, first decide whether the property could change the shortlist. Recover a primary record or clarify its method before commissioning a measurement. Calibrated correlations or molecular models can prioritize experiments, but their outputs remain predictions; do not impute a hard safety pass. Permittivity does not establish electrical resistivity or breakdown strength. Actual fluid grade, water/ionic contamination, wetted materials and ageing conditions matter. [OCP's Material Compatibility in Immersion Cooling, revision 1.0 (2022)](https://www.opencompute.org/documents/material-compatibility-in-immersion-cooling-document-version-1-0-nov-28-2022-1-pdf) provides application-specific context and test-method guidance.

The practical order is: resolve the intended fire requirement; clarify CF006's missing fire evidence and decision-relevant source conflicts; retrieve the remaining thermophysical data for survivors; obtain transferable supplier evidence; then measure only the gaps that could change the decision. Flash-point, electrical and compatibility measurements should be performed by an appropriately equipped laboratory. No outreach, expenditure or experiments have been undertaken.

## Record status

This is a public-source evidence addition to planning baseline `2628c5a`, not a specification rewrite or acceptance of the proposed ten-day M0 controls. Published content consists of known-compound records and cited source facts, with no novel formulation. The v1.1 planning archive and its manifest remain historical snapshots of that planning release; this evidence folder is a subsequent addition.

Checks performed: 32 unique CAS identities and check digits; formula element bounds; source-reference resolution; Kelvin/Fahrenheit conversions; missing-value and inequality preservation; range/status reconciliation; the trans/cis counterexample distinction; workbook summary recalculation and filter-table export. This is an extraction/self-check, not independent chemical or thermal qualification.
