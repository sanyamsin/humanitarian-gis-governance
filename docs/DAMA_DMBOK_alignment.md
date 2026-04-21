# DAMA-DMBOK v2 Alignment Documentation

## How This Framework Maps to DAMA-DMBOK v2 Knowledge Areas

This document provides explicit traceability between the humanitarian-gis-governance
framework components and the DAMA Data Management Body of Knowledge (DMBOK) v2.

---

## Knowledge Area Mapping

### Chapter 3 — Data Governance

**DAMA Scope:** Establishing authority, management, and control over data assets.

| DMBOK Concept | Framework Implementation |
|--------------|--------------------------|
| Governance Operating Model | `framework/governance_policy.yaml` → Section: governance_bodies |
| Data Stewardship Roles | `framework/stewardship_register.yaml` → role_definitions |
| Data Policies | `framework/governance_policy.yaml` → principles, compliance |
| Governance Maturity | `tools/maturity_assessment.py` → Dimensions D01, D10 |
| Stewardship Council | `framework/stewardship_register.yaml` → Stewardship Council definition |

**Humanitarian adaptation:**  
Standard DMBOK assumes a single organization. This framework supports federated
governance across national offices, partner organizations, and field teams —
with role-based (not person-based) accountability to handle high staff turnover.

---

### Chapter 5 — Data Architecture

**DAMA Scope:** Design and maintenance of master blueprints for data assets.

| DMBOK Concept | Framework Implementation |
|--------------|--------------------------|
| Data Models | `framework/data_standards.yaml` → spatial data model definitions |
| Integration Architecture | `framework/data_standards.yaml` → format standards (GeoPackage, PostGIS) |
| Enterprise Geodatabase | Referenced in data_standards.yaml and governance_policy.yaml |
| API Standards | `framework/data_standards.yaml` → OGC WMS/WFS standards |

---

### Chapter 7 — Data Security

**DAMA Scope:** Ensuring appropriate access and protection of data assets.

| DMBOK Concept | Framework Implementation |
|--------------|--------------------------|
| Data Classification | `framework/governance_policy.yaml` → data_classification |
| Access Control | Classification levels drive access policies (Public/Restricted/Confidential/Sensitive) |
| Do No Harm | Sensitive classification for population/staff location data |
| Security Incident Response | `framework/governance_policy.yaml` → compliance → non_compliance_process |

**Humanitarian adaptation:**  
The "Sensitive" classification level extends standard DMBOK to address the specific
risk of geospatial data exposing vulnerable populations, staff locations in conflict
zones, or enabling targeting by hostile actors.

---

### Chapter 9 — Data Lifecycle Management

**DAMA Scope:** Management of data through its full lifecycle from creation to disposal.

| DMBOK Concept | Framework Implementation |
|--------------|--------------------------|
| Lifecycle Stages | `framework/governance_policy.yaml` → data_lifecycle |
| Retention Policy | `framework/data_lifecycle.yaml` (per domain) |
| Disposal Governance | Requires steward approval, audit trail maintained |
| Archiving | Version history preserved per naming convention |

---

### Chapter 10 — Reference & Master Data Management

**DAMA Scope:** Managing shared data to ensure consistency across systems.

| DMBOK Concept | Framework Implementation |
|--------------|--------------------------|
| Reference Data | Domain DD01 — OCHA CODs, GADM, OSM as authoritative sources |
| Master Data | Golden record management for administrative boundaries |
| Version Control | Naming convention `_v01, _v02` + PostGIS version history |
| Change Notification | Steward responsibilities in stewardship_register.yaml |

---

### Chapter 11 — Data Warehousing & Business Intelligence

**DAMA Scope (adapted for GIS):** Data lineage and transformation documentation.

| DMBOK Concept | Framework Implementation |
|--------------|--------------------------|
| Lineage Documentation | `framework/data_standards.yaml` → provenance fields |
| ETL Documentation | `optional_fields` → processing_scripts |
| Traceability | Maturity Dimension D04 |

---

### Chapter 12 — Metadata Management

**DAMA Scope:** Defining, maintaining, and managing metadata.

| DMBOK Concept | Framework Implementation |
|--------------|--------------------------|
| Business Metadata | title, abstract, domain, topic_category |
| Technical Metadata | CRS, geometry_type, format, spatial_resolution |
| Operational Metadata | date_created, update_frequency, data_steward |
| Metadata Standards | ISO 19115:2014, INSPIRE, Dublin Core, OCHA HDX |
| Data Catalogue | Maturity Dimension D08; implemented in humanitarian-geo-catalogue |

---

### Chapter 13 — Data Quality

**DAMA Scope:** Defining, monitoring, and improving data quality.

| DMBOK Concept | Framework Implementation |
|--------------|--------------------------|
| Quality Dimensions | `framework/data_standards.yaml` → quality_dimensions (6 dimensions) |
| Quality Monitoring | Maturity Dimension D03; implemented in geodata-quality-pipeline |
| Incident Management | `framework/governance_policy.yaml` → compliance |
| SLAs | Defined in geodata-quality-pipeline project |

---

## Maturity Dimension to DAMA Chapter Crosswalk

| Dimension | Name | DAMA Chapter(s) |
|-----------|------|-----------------|
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

---

## References

- DAMA International. *DAMA-DMBOK: Data Management Body of Knowledge*, 2nd Edition. 2017.
- ISO 19115:2014 — Geographic Information — Metadata
- OCHA. *Common Operational Datasets (CODs) Guidelines*. 2021.
- INSPIRE Directive 2007/2/EC — European spatial data infrastructure
