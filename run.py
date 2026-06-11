"""Single-command entry point for the Chronis Behavioral Insight Engine."""
import argparse
import json
from pathlib import Path

from src.data_loader import load_data
from src.insight_generator import generate_insights


def render_markdown(report: dict) -> str:
    lines = ["# Behavioral Insight Report\n"]
    by_user = {}
    for ins in report["insights"]:
        by_user.setdefault(ins["user_id"], []).append(ins)

    for user_id, items in sorted(by_user.items()):
        lines.append(f"## {user_id}")
        for ins in items:
            lines.append(f"- **Insight:** {ins['insight']} (Confidence: {ins['confidence']})")
            evidence_str = ", ".join(f"{k}={v}" for k, v in ins["evidence"].items())
            lines.append(f"  - Evidence: {evidence_str}")
        lines.append("")

    if report["abstentions"]:
        lines.append("## Abstentions")
        for a in report["abstentions"]:
            lines.append(f"- {a['user_id']} / {a['metric']} / {a['type']}: {a['reason']}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Chronis Behavioral Insight Engine")
    parser.add_argument("--data", default="data/Chronis_TaskA_Data_v2-2.csv")
    parser.add_argument("--out", default="outputs/")
    args = parser.parse_args()

    df = load_data(args.data)
    report = generate_insights(df)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    (out_dir / "insights_report.json").write_text(json.dumps(report, indent=2))
    (out_dir / "insights_report.md").write_text(render_markdown(report))

    print(f"Generated {len(report['insights'])} insights, "
          f"abstained on {len(report['abstentions'])} checks.")
    print(f"Reports written to {out_dir}/")


if __name__ == "__main__":
    main()
