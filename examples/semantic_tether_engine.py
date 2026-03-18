import sys
import json
from pathlib import Path


CONSTRAINT_KEYWORDS = [
    "must",
    "shall",
    "required",
    "prohibited",
    "cannot",
    "may"
]


def extract_anchors(document_text: str):
    anchors = []
    lines = [line.strip() for line in document_text.splitlines()]

    for i, line in enumerate(lines):
        if not line:
            continue

        line_lower = line.lower()

        matched = [k for k in CONSTRAINT_KEYWORDS if k in line_lower]

        if matched:
            anchors.append({
                "line": i + 1,
                "text": line,
                "matchedSignals": matched
            })

    return anchors


def build_observation(anchor_text: str):
    text = anchor_text.lower()
    features = []

    if "must" in text:
        features.append("Includes a requirement ('must').")

    if "shall" in text:
        features.append("Includes a requirement ('shall').")

    if "may" in text:
        features.append("Includes permission ('may').")

    if "within" in text:
        features.append("Includes a time constraint.")

    if "if" in text or "under" in text:
        features.append("Includes a condition.")

    if not features:
        return "No explicit feature detected."

    return " ".join(features)


def build_operational_meaning(anchor_text: str):
    text = anchor_text.lower()

    # strict restatement rules (no additions)
    if "must submit documentation within 30 days" in text:
        return "Applicants are required to submit documentation within 30 days."

    if "may extend deadlines under exceptional circumstances" in text:
        return "The agency is allowed to extend deadlines under exceptional circumstances."

    return anchor_text  # fallback = original text (safe, no drift)


def detect_drift(anchor_text: str, operational: str):
    # simple strict check: output must not introduce new phrases
    anchor_words = set(anchor_text.lower().split())
    output_words = set(operational.lower().split())

    return not output_words.issubset(anchor_words.union({"are", "is", "to", "the"}))


def run(document_path: Path):
    text = document_path.read_text(encoding="utf-8")

    anchors = extract_anchors(text)

    analysis = []

    for anchor in anchors:
        observation = build_observation(anchor["text"])
        operational = build_operational_meaning(anchor["text"])
        drift = detect_drift(anchor["text"], operational)

        result = {
            "anchor": anchor,
            "observation": observation,
            "operationalMeaning": operational,
            "driftDetected": drift,
            "status": "blocked" if drift else "ok"
        }

        analysis.append(result)

    return {
        "document": str(document_path),
        "anchorCount": len(anchors),
        "analysis": analysis
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python semantic_tether_engine.py <document>")
        sys.exit(1)

    path = Path(sys.argv[1])

    if not path.exists():
        print(f"Error: file not found: {path}")
        sys.exit(1)

    output = run(path)

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
