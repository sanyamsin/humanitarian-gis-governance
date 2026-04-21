#!/usr/bin/env python3
"""
Humanitarian GIS Governance Maturity Assessment Tool
=====================================================
Aligned with DAMA-DMBOK v2 and the Data Management Maturity (DMM) model.

Usage:
    python tools/maturity_assessment.py --config framework/governance_policy.yaml
    python tools/maturity_assessment.py --interactive
    python tools/maturity_assessment.py --report --output reports/maturity_report.html
"""

import argparse
import json
import yaml
import datetime
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass, field, asdict


# ── DATA STRUCTURES ──────────────────────────────────────────────────────────

@dataclass
class MaturityDimension:
    """Single governance dimension with scoring."""
    id: str
    name: str
    dama_chapter: str
    description: str
    levels: Dict[int, str]
    current_score: int = 0
    evidence: str = ""
    priority: str = "medium"  # low / medium / high / critical

    @property
    def level_label(self) -> str:
        labels = {0: "Initial", 1: "Managed", 2: "Defined",
                  3: "Quantitatively Managed", 4: "Optimizing"}
        return labels.get(self.current_score, "Unknown")

    @property
    def score_pct(self) -> float:
        return (self.current_score / 4) * 100


@dataclass
class MaturityAssessment:
    """Full maturity assessment with all dimensions."""
    org_name: str = "Humanitarian GIS Centre"
    assessment_date: str = field(default_factory=lambda: datetime.date.today().isoformat())
    assessor: str = ""
    dimensions: List[MaturityDimension] = field(default_factory=list)
    notes: str = ""

    @property
    def overall_score(self) -> float:
        if not self.dimensions:
            return 0.0
        return sum(d.current_score for d in self.dimensions) / len(self.dimensions)

    @property
    def overall_pct(self) -> float:
        return (self.overall_score / 4) * 100

    @property
    def maturity_label(self) -> str:
        score = self.overall_score
        if score < 1.0:
            return "Initial (Level 0–1)"
        elif score < 2.0:
            return "Managed (Level 1–2)"
        elif score < 3.0:
            return "Defined (Level 2–3)"
        elif score < 4.0:
            return "Quantitatively Managed (Level 3–4)"
        else:
            return "Optimizing (Level 4)"

    def critical_gaps(self) -> List[MaturityDimension]:
        return sorted(
            [d for d in self.dimensions if d.current_score <= 1],
            key=lambda x: x.current_score
        )

    def top_priorities(self, n: int = 3) -> List[MaturityDimension]:
        high = [d for d in self.dimensions if d.priority in ("high", "critical")]
        return sorted(high, key=lambda x: x.current_score)[:n]


# ── FRAMEWORK DEFINITION ─────────────────────────────────────────────────────

def build_framework() -> List[MaturityDimension]:
    """
    Returns the 10-dimension assessment framework aligned with DAMA-DMBOK v2.
    Each dimension maps to a DAMA knowledge area.
    """
    return [
        MaturityDimension(
            id="D01", name="Data Governance Strategy",
            dama_chapter="DMBOK2 Ch.3",
            description="Existence and operationalization of a formal governance framework with assigned roles.",
            priority="critical",
            levels={
                0: "No governance framework. Ad hoc data practices.",
                1: "Basic policies exist but not enforced. No assigned stewards.",
                2: "Formal framework documented. Stewards assigned. Partial adoption.",
                3: "Framework actively enforced. Stewards accountable. Metrics tracked.",
                4: "Continuous improvement. Governance embedded in all processes. Benchmarked externally."
            }
        ),
        MaturityDimension(
            id="D02", name="Metadata Management",
            dama_chapter="DMBOK2 Ch.12",
            description="Completeness, standardization, and discoverability of dataset metadata.",
            priority="critical",
            levels={
                0: "No metadata records. Datasets discovered informally.",
                1: "Some informal README files. No standard schema.",
                2: "Metadata schema defined (ISO 19115). Partially applied.",
                3: "All production datasets have complete metadata. Catalogue operational.",
                4: "Automated metadata generation. Machine-readable. Cross-system interoperability."
            }
        ),
        MaturityDimension(
            id="D03", name="Data Quality Management",
            dama_chapter="DMBOK2 Ch.13",
            description="Automated quality monitoring, incident management, and quality KPIs.",
            priority="critical",
            levels={
                0: "No quality checks. Issues discovered by end users.",
                1: "Manual spot checks. No systematic process.",
                2: "Quality dimensions defined. Some automated checks on key datasets.",
                3: "Automated quality pipeline covering all production datasets. SLAs defined.",
                4: "Predictive quality management. Root cause analysis. Continuous improvement loop."
            }
        ),
        MaturityDimension(
            id="D04", name="Data Lineage & Provenance",
            dama_chapter="DMBOK2 Ch.11",
            description="Traceability of data origin, transformations, and downstream usage.",
            priority="high",
            levels={
                0: "No lineage documentation. Origins unknown for most datasets.",
                1: "Informal notes on some datasets. No structured lineage.",
                2: "Lineage documented manually for key datasets.",
                3: "Automated lineage tracking in ETL pipelines. Visual lineage graphs available.",
                4: "End-to-end automated lineage. Impact analysis capability. Regulatory compliance."
            }
        ),
        MaturityDimension(
            id="D05", name="Data Architecture & Integration",
            dama_chapter="DMBOK2 Ch.5",
            description="Standardization of spatial data models, ETL pipelines, and API integrations.",
            priority="high",
            levels={
                0: "Fragmented storage. Multiple incompatible formats and schemas.",
                1: "Some standard formats used. No enterprise geodatabase.",
                2: "PostGIS/enterprise geodatabase in use. Basic ETL scripts.",
                3: "Standardized data models. Automated ETL pipelines. API integrations active.",
                4: "Event-driven architecture. Real-time data integration. Full API ecosystem."
            }
        ),
        MaturityDimension(
            id="D06", name="Data Security & Classification",
            dama_chapter="DMBOK2 Ch.7",
            description="Classification of sensitive geospatial data and enforcement of access controls.",
            priority="critical",
            levels={
                0: "No classification. All data accessible to all staff.",
                1: "Informal sensitivity awareness. No formal classification scheme.",
                2: "Classification policy defined. Partially implemented.",
                3: "All datasets classified. Access controls enforced. Audit logs active.",
                4: "Automated classification. Dynamic access control. Regular security audits."
            }
        ),
        MaturityDimension(
            id="D07", name="Reference & Master Data Management",
            dama_chapter="DMBOK2 Ch.10",
            description="Management of authoritative reference datasets (admin boundaries, CODs, etc.).",
            priority="high",
            levels={
                0: "Multiple conflicting versions of reference datasets in circulation.",
                1: "Single authoritative source identified but not enforced.",
                2: "MDM process for key reference data. Version control applied.",
                3: "Golden record management. Change notification to consumers. Full versioning.",
                4: "Automated synchronization with upstream authoritative sources (OCHA, GADM, OSM)."
            }
        ),
        MaturityDimension(
            id="D08", name="Data Catalogue & Discovery",
            dama_chapter="DMBOK2 Ch.12",
            description="Availability of a searchable, maintained catalogue for dataset discovery.",
            priority="high",
            levels={
                0: "No catalogue. Staff rely on word-of-mouth to find datasets.",
                1: "Shared spreadsheet or SharePoint list. Incomplete and outdated.",
                2: "Formal catalogue deployed (CKAN or equivalent). Partially populated.",
                3: "Catalogue actively maintained. All datasets discoverable. Search functional.",
                4: "Semantic search. Automated enrichment. Federated with external catalogues (HDX)."
            }
        ),
        MaturityDimension(
            id="D09", name="Data Lifecycle Management",
            dama_chapter="DMBOK2 Ch.9",
            description="Defined retention policies, archiving procedures, and disposal governance.",
            priority="medium",
            levels={
                0: "No retention policy. Data accumulates indefinitely.",
                1: "Informal retention awareness. No documented policy.",
                2: "Retention policy documented per domain. Partially enforced.",
                3: "Lifecycle stages actively managed. Disposal requires steward approval.",
                4: "Automated lifecycle transitions. Compliance reporting. Legal hold capability."
            }
        ),
        MaturityDimension(
            id="D10", name="Governance Culture & Training",
            dama_chapter="DMBOK2 Ch.3",
            description="Staff awareness, training, and cultural adoption of governance practices.",
            priority="medium",
            levels={
                0: "No governance awareness. Data management seen as purely technical.",
                1: "Some staff aware of governance importance. No formal training.",
                2: "Training materials available. Stewards onboarded. Limited field reach.",
                3: "Mandatory onboarding. Regular training. Governance champions in field teams.",
                4: "Self-reinforcing governance culture. Community of practice. External knowledge sharing."
            }
        ),
    ]


# ── INTERACTIVE ASSESSMENT ────────────────────────────────────────────────────

def run_interactive_assessment() -> MaturityAssessment:
    """Guides the assessor through each dimension interactively."""
    print("\n" + "="*65)
    print("  HUMANITARIAN GIS GOVERNANCE MATURITY ASSESSMENT")
    print("  Aligned with DAMA-DMBOK v2")
    print("="*65)

    org = input("\nOrganization name [Humanitarian GIS Centre]: ").strip()
    assessor = input("Assessor name: ").strip()

    assessment = MaturityAssessment(
        org_name=org or "Humanitarian GIS Centre",
        assessor=assessor
    )

    dimensions = build_framework()
    total = len(dimensions)

    print(f"\n{'─'*65}")
    print(f"  You will be scored on {total} governance dimensions.")
    print(f"  Scale: 0 (Initial) → 4 (Optimizing)")
    print(f"{'─'*65}\n")

    for i, dim in enumerate(dimensions, 1):
        print(f"\n[{i}/{total}] {dim.id} — {dim.name}")
        print(f"  DAMA Reference: {dim.dama_chapter}")
        print(f"  {dim.description}")
        print()
        for level, desc in dim.levels.items():
            print(f"  Level {level}: {desc}")
        print()

        while True:
            try:
                score_input = input(f"  Score (0–4): ").strip()
                score = int(score_input)
                if 0 <= score <= 4:
                    break
                print("  Please enter a number between 0 and 4.")
            except ValueError:
                print("  Please enter a valid integer.")

        evidence = input(f"  Evidence / notes (optional): ").strip()
        dim.current_score = score
        dim.evidence = evidence
        dimensions[i-1] = dim

    assessment.dimensions = dimensions
    assessment.notes = input("\nOverall assessment notes (optional): ").strip()

    return assessment


# ── REPORT GENERATION ─────────────────────────────────────────────────────────

def generate_html_report(assessment: MaturityAssessment, output_path: str) -> None:
    """Generates a styled HTML maturity report."""

    bar_color = {0: "#E74C3C", 1: "#E67E22", 2: "#F1C40F", 3: "#2ECC71", 4: "#27AE60"}

    dim_rows = ""
    for d in assessment.dimensions:
        color = bar_color.get(d.current_score, "#999")
        width = d.score_pct
        evidence_html = f'<div class="evidence">{d.evidence}</div>' if d.evidence else ""
        dim_rows += f"""
        <tr>
          <td><strong>{d.id}</strong></td>
          <td>{d.name}<br><small style="color:#888">{d.dama_chapter}</small></td>
          <td>
            <div class="bar-track">
              <div class="bar-fill" style="width:{width}%;background:{color};"></div>
            </div>
          </td>
          <td style="text-align:center;font-weight:bold;color:{color};">{d.current_score}/4</td>
          <td style="color:{color};font-size:12px;">{d.level_label}</td>
          <td class="priority {d.priority}">{d.priority.upper()}</td>
        </tr>
        {f'<tr><td colspan="6">{evidence_html}</td></tr>' if d.evidence else ''}
        """

    gaps = assessment.critical_gaps()
    gap_items = "".join(f"<li><strong>{g.id} — {g.name}</strong> (Level {g.current_score}): {g.levels[g.current_score]}</li>" for g in gaps)

    recommendations = []
    for d in sorted(assessment.dimensions, key=lambda x: x.current_score):
        if d.current_score < 4:
            next_level = d.current_score + 1
            recommendations.append(
                f"<li><strong>{d.id} {d.name}</strong> → Target Level {next_level}: {d.levels[next_level]}</li>"
            )

    overall_color = bar_color.get(int(assessment.overall_score), "#999")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>GIS Governance Maturity Report — {assessment.org_name}</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: Arial, sans-serif; font-size: 14px; color: #2c3e50; background: #f8f9fa; padding: 2rem; }}
  .container {{ max-width: 960px; margin: 0 auto; background: #fff; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); padding: 2.5rem; }}
  h1 {{ font-size: 24px; color: #1A3C5E; border-bottom: 3px solid #2E6DA4; padding-bottom: 0.75rem; margin-bottom: 0.5rem; }}
  h2 {{ font-size: 18px; color: #1A3C5E; margin: 2rem 0 1rem; }}
  .meta {{ font-size: 13px; color: #777; margin-bottom: 2rem; }}
  .score-card {{ display: flex; gap: 1.5rem; margin-bottom: 2rem; flex-wrap: wrap; }}
  .card {{ flex: 1; min-width: 180px; padding: 1.25rem; border-radius: 8px; background: #f0f5fb; border: 1px solid #d0e0f0; text-align: center; }}
  .card .num {{ font-size: 36px; font-weight: bold; color: {overall_color}; }}
  .card .lbl {{ font-size: 12px; color: #888; margin-top: 4px; }}
  table {{ width: 100%; border-collapse: collapse; margin-top: 1rem; }}
  th {{ background: #1A3C5E; color: #fff; padding: 0.6rem 0.8rem; text-align: left; font-size: 13px; }}
  td {{ padding: 0.6rem 0.8rem; border-bottom: 1px solid #eee; font-size: 13px; vertical-align: middle; }}
  tr:hover {{ background: #f8fbff; }}
  .bar-track {{ background: #eee; border-radius: 4px; height: 8px; width: 120px; }}
  .bar-fill {{ height: 100%; border-radius: 4px; transition: width 0.3s; }}
  .evidence {{ font-size: 11px; color: #666; padding: 4px 8px; background: #f9f9f9; border-left: 3px solid #2E6DA4; margin: 2px 0 6px; }}
  .priority {{ font-size: 11px; padding: 2px 6px; border-radius: 4px; font-weight: bold; }}
  .critical {{ background: #fde8e8; color: #C0392B; }}
  .high {{ background: #fef3e2; color: #D68910; }}
  .medium {{ background: #e8f8f5; color: #1E8449; }}
  .low {{ background: #eaf0fb; color: #2E6DA4; }}
  ul.gaps {{ padding-left: 1.2rem; line-height: 2; }}
  ul.gaps li {{ margin-bottom: 0.3rem; }}
  .footer {{ margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #eee; font-size: 12px; color: #aaa; text-align: center; }}
</style>
</head>
<body>
<div class="container">
  <h1>GIS Data Governance Maturity Report</h1>
  <div class="meta">
    Organization: <strong>{assessment.org_name}</strong> &nbsp;|&nbsp;
    Date: <strong>{assessment.assessment_date}</strong> &nbsp;|&nbsp;
    Assessor: <strong>{assessment.assessor or 'N/A'}</strong> &nbsp;|&nbsp;
    Framework: <strong>DAMA-DMBOK v2</strong>
  </div>

  <div class="score-card">
    <div class="card">
      <div class="num">{assessment.overall_score:.1f}<span style="font-size:18px;color:#aaa">/4</span></div>
      <div class="lbl">Overall Maturity Score</div>
    </div>
    <div class="card">
      <div class="num">{assessment.overall_pct:.0f}<span style="font-size:18px;color:#aaa">%</span></div>
      <div class="lbl">Maturity Percentage</div>
    </div>
    <div class="card">
      <div class="num" style="font-size:18px;padding-top:8px;">{assessment.maturity_label}</div>
      <div class="lbl">Maturity Level</div>
    </div>
    <div class="card">
      <div class="num" style="color:#E74C3C;">{len(assessment.critical_gaps())}</div>
      <div class="lbl">Critical Gaps (Level ≤ 1)</div>
    </div>
  </div>

  <h2>Dimension Scores</h2>
  <table>
    <thead>
      <tr>
        <th>ID</th><th>Dimension</th><th>Progress</th>
        <th>Score</th><th>Level</th><th>Priority</th>
      </tr>
    </thead>
    <tbody>{dim_rows}</tbody>
  </table>

  <h2>Critical Gaps</h2>
  <ul class="gaps">{gap_items or "<li>No critical gaps identified. Well done!</li>"}</ul>

  <h2>Improvement Roadmap</h2>
  <ul class="gaps">{"".join(recommendations[:8])}</ul>

  {"<h2>Notes</h2><p>" + assessment.notes + "</p>" if assessment.notes else ""}

  <div class="footer">
    Generated by humanitarian-gis-governance v1.0 &nbsp;|&nbsp;
    github.com/sanyamsin/humanitarian-gis-governance &nbsp;|&nbsp;
    DAMA-DMBOK v2 aligned
  </div>
</div>
</body>
</html>"""

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"\nReport saved to: {output_path}")


def generate_json_export(assessment: MaturityAssessment, output_path: str) -> None:
    """Exports assessment as JSON for programmatic use."""
    data = {
        "org_name": assessment.org_name,
        "assessment_date": assessment.assessment_date,
        "assessor": assessment.assessor,
        "overall_score": round(assessment.overall_score, 2),
        "overall_pct": round(assessment.overall_pct, 1),
        "maturity_label": assessment.maturity_label,
        "critical_gaps": [d.id for d in assessment.critical_gaps()],
        "dimensions": [
            {
                "id": d.id, "name": d.name, "dama_chapter": d.dama_chapter,
                "score": d.current_score, "level_label": d.level_label,
                "score_pct": round(d.score_pct, 1), "priority": d.priority,
                "evidence": d.evidence,
                "next_level_target": d.levels.get(d.current_score + 1, "Already at maximum")
            }
            for d in assessment.dimensions
        ],
        "notes": assessment.notes
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"JSON export saved to: {output_path}")


# ── DEMO / SAMPLE ASSESSMENT ──────────────────────────────────────────────────

def run_demo_assessment() -> MaturityAssessment:
    """Returns a realistic sample assessment for demo/testing purposes."""
    dims = build_framework()
    scores = [1, 1, 2, 1, 2, 1, 2, 1, 1, 2]
    evidences = [
        "Basic policy document exists but not reviewed since 2023. No stewards formally assigned.",
        "Some datasets have README files. No ISO 19115 schema applied.",
        "Manual quality checks on CODs only. No automated pipeline.",
        "Source documented for CODs. No lineage for field data.",
        "PostGIS in use for reference data. Field data in scattered shapefiles.",
        "Sensitive data flagged informally. No access control enforcement.",
        "OCHA CODs used as reference. Multiple versions of admin boundaries in circulation.",
        "SharePoint list exists but last updated 8 months ago.",
        "No formal retention policy. Archived data mixed with active data.",
        "Stewards aware of governance needs. No formal training materials."
    ]
    for dim, score, ev in zip(dims, scores, evidences):
        dim.current_score = score
        dim.evidence = ev

    return MaturityAssessment(
        org_name="Demo — Humanitarian GIS Centre",
        assessor="T. [Nom] — Data Governance Specialist",
        dimensions=dims,
        notes="Baseline assessment. Priority: establish formal stewardship and automated quality pipeline."
    )


# ── CLI ENTRY POINT ───────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Humanitarian GIS Governance Maturity Assessment Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tools/maturity_assessment.py --demo
  python tools/maturity_assessment.py --interactive
  python tools/maturity_assessment.py --demo --output reports/baseline.html
        """
    )
    parser.add_argument("--interactive", action="store_true", help="Run interactive assessment")
    parser.add_argument("--demo", action="store_true", help="Run with demo data")
    parser.add_argument("--output", default="reports/maturity_report.html", help="Output HTML report path")
    parser.add_argument("--json", default="reports/maturity_report.json", help="Output JSON path")

    args = parser.parse_args()

    if args.demo:
        print("\nRunning demo assessment...")
        assessment = run_demo_assessment()
    elif args.interactive:
        assessment = run_interactive_assessment()
    else:
        parser.print_help()
        return

    print(f"\n{'='*55}")
    print(f"  RESULTS — {assessment.org_name}")
    print(f"{'='*55}")
    print(f"  Overall Score  : {assessment.overall_score:.2f} / 4.00")
    print(f"  Maturity Level : {assessment.maturity_label}")
    print(f"  Critical Gaps  : {len(assessment.critical_gaps())}")
    print(f"{'='*55}\n")

    for d in assessment.dimensions:
        bar = "█" * d.current_score + "░" * (4 - d.current_score)
        print(f"  {d.id} {bar} {d.current_score}/4  {d.name}")

    generate_html_report(assessment, args.output)
    generate_json_export(assessment, args.json)


if __name__ == "__main__":
    main()
