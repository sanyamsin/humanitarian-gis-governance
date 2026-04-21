# humanitarian-gis-governance

**A production-grade GIS data governance framework for humanitarian organizations**  
Aligned with DAMA-DMBOK v2 | ISO 19115 | INSPIRE Directive

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org)
[![DAMA-DMBOK v2](https://img.shields.io/badge/framework-DAMA--DMBOK%20v2-darkblue.svg)](https://www.dama.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## Overview

Humanitarian GIS operations generate complex, multi-source geospatial datasets under time pressure, in low-connectivity environments, and with high operational stakes. Without a structured governance framework, data quality degrades, datasets become undiscoverable, and decision-making suffers.

This repository provides a **practical, deployable governance framework** covering:

- **Policy & stewardship** — formal roles, data domains, classification, lifecycle rules
- **Governance maturity assessment** — CLI tool aligned with DAMA-DMBOK v2, with HTML reporting
- **Metadata standards** — ISO 19115 schema adapted for humanitarian GIS contexts
- **Data quality dimensions** — automated check specifications and KPI definitions
- **Documentation & training** — onboarding guides, steward checklists, governance templates

Designed for the realities of distributed GIS teams supporting field operations across multiple countries.

---

## Repository Structure

```
humanitarian-gis-governance/
├── framework/
│   ├── governance_policy.yaml      # Master policy: principles, domains, lifecycle, bodies
│   ├── stewardship_register.yaml   # Role definitions and domain assignments
│   ├── data_standards.yaml         # ISO 19115 metadata schema + naming conventions
│   └── data_lifecycle.yaml         # Retention policies and disposal procedures
│
├── tools/
│   ├── maturity_assessment.py      # CLI: DAMA-DMBOK maturity assessment + HTML report
│   ├── metadata_validator.py       # Validates dataset metadata against ISO 19115 schema
│   └── steward_dashboard.py        # Streamlit dashboard for governance monitoring
│
├── data/
│   ├── sample_datasets/            # Sample geospatial datasets for testing
│   └── metadata/                   # Sample metadata records (JSON)
│
├── docs/
│   ├── DAMA_DMBOK_alignment.md     # Mapping framework components to DAMA knowledge areas
│   ├── stewardship_guide.md        # Practical guide for Data Stewards
│   └── governance_maturity_model.md # The 10-dimension maturity model explained
│
├── reports/                        # Generated maturity reports (HTML, JSON)
├── tests/                          # Unit tests for governance tools
├── notebooks/                      # Jupyter: maturity trends, gap analysis
└── requirements.txt
```

---

## Quick Start

### 1. Install dependencies

```bash
git clone https://github.com/sanyamsin/humanitarian-gis-governance.git
cd humanitarian-gis-governance
pip install -r requirements.txt
```

### 2. Run a demo maturity assessment

```bash
python tools/maturity_assessment.py --demo --output reports/demo_report.html
```

Opens a pre-populated assessment based on a realistic baseline scenario. Generates:
- `reports/demo_report.html` — styled HTML report with scoring and roadmap
- `reports/demo_report.json` — machine-readable export for integration

### 3. Run an interactive assessment

```bash
python tools/maturity_assessment.py --interactive --output reports/my_org_report.html
```

Guides you through all 10 governance dimensions. Score your organization on a 0–4 scale for each, provide evidence, and generate a full maturity report.

---

## Governance Framework

### 5 Data Domains

| Domain | Scope | Classification |
|--------|-------|----------------|
| DD01 | Reference Geospatial Data (admin boundaries, base maps) | Public / Restricted |
| DD02 | Operational Field Data (beneficiary locations, intervention zones) | Restricted / Confidential |
| DD03 | Health & Epidemiological Data | Confidential |
| DD04 | Logistics & Supply Chain Data | Restricted |
| DD05 | Context & Security Data | Confidential / Sensitive |

### 10 Maturity Dimensions (DAMA-DMBOK v2)

| ID | Dimension | DAMA Chapter |
|----|-----------|-------------|
| D01 | Data Governance Strategy | Ch. 3 |
| D02 | Metadata Management | Ch. 12 |
| D03 | Data Quality Management | Ch. 13 |
| D04 | Data Lineage & Provenance | Ch. 11 |
| D05 | Data Architecture & Integration | Ch. 5 |
| D06 | Data Security & Classification | Ch. 7 |
| D07 | Reference & Master Data Management | Ch. 10 |
| D08 | Data Catalogue & Discovery | Ch. 12 |
| D09 | Data Lifecycle Management | Ch. 9 |
| D10 | Governance Culture & Training | Ch. 3 |

Each dimension is scored 0–4:

| Score | Level | Description |
|-------|-------|-------------|
| 0 | Initial | Ad hoc. No governance processes. |
| 1 | Managed | Basic awareness. Informal practices. |
| 2 | Defined | Formal policies documented. Partial adoption. |
| 3 | Quantitatively Managed | Enforced. Metrics tracked. SLAs defined. |
| 4 | Optimizing | Continuous improvement. Benchmarked externally. |

---

## Maturity Report Example

```
=====================================================
  RESULTS — Demo Humanitarian GIS Centre
=====================================================
  Overall Score  : 1.50 / 4.00
  Maturity Level : Managed (Level 1–2)
  Critical Gaps  : 6
=====================================================

  D01 █░░░  1/4  Data Governance Strategy
  D02 █░░░  1/4  Metadata Management
  D03 ██░░  2/4  Data Quality Management
  D04 █░░░  1/4  Data Lineage & Provenance
  D05 ██░░  2/4  Data Architecture & Integration
  ...
```

Full HTML report generated at `reports/maturity_report.html`.

---

## DAMA-DMBOK v2 Alignment

This framework implements the following DAMA-DMBOK v2 knowledge areas:

- **Data Governance (Ch. 3)** → governance_policy.yaml, stewardship_register.yaml
- **Data Architecture (Ch. 5)** → data_standards.yaml (schema and integration)
- **Data Security (Ch. 7)** → classification levels, access control policies
- **Data Lifecycle Management (Ch. 9)** → data_lifecycle.yaml
- **Reference & Master Data (Ch. 10)** → domain DD01, naming conventions
- **Data Warehousing & BI (Ch. 11)** → lineage documentation patterns
- **Metadata Management (Ch. 12)** → ISO 19115 schema, catalogue integration
- **Data Quality (Ch. 13)** → quality dimensions, automated check specifications

---

## Humanitarian Context Adaptations

Standard enterprise governance frameworks assume stable connectivity, permanent staff, and predictable data flows. This framework adapts for:

- **Field connectivity constraints** — lightweight YAML configs, offline-capable tools
- **High staff turnover** — role-based (not person-based) stewardship assignments
- **Do No Harm principle** — mandatory classification of population-sensitive data
- **Multi-organization coordination** — open standards (ISO 19115, OGC) for interoperability
- **Emergency response mode** — tiered governance allowing rapid data publication with post-hoc documentation

---

## Related Projects

| Project | Description |
|---------|-------------|
| [geodata-quality-pipeline](https://github.com/sanyamsin/geodata-quality-pipeline) | Automated PostGIS quality monitoring pipeline |
| [humanitarian-geo-catalogue](https://github.com/sanyamsin/humanitarian-geo-catalogue) | ISO 19115 data catalogue for humanitarian datasets |
| [sahel-program-monitor](https://github.com/sanyamsin/sahel-program-monitor) | Geospatial program monitoring — Sahel region |

---

## Author
**Serge-Alain NYAMSIN** — GIS Data Governance & Humanitarian Data Engineering  
[github.com/sanyamsin](https://github.com/sanyamsin) | [huggingface.co/Lokozu](https://huggingface.co/Lokozu)

12+ years of field data management experience across Sub-Saharan Africa (RCA, Mauritania, Senegal).  
MSc Data Science & AI — DSTI Paris.

---

## License

MIT License — see [LICENSE](LICENSE)
