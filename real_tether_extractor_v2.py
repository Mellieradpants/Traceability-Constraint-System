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
        matched_signals = [
            keyword for keyword in CONSTRAINT_KEYWORDS
            if keyword in line_lower
        ]

        if matched_signals:
            anchors.append({
                "line": i + 1,
                "text": line,
                "matchedSignals": matched_signals
            })

    return anchors


def build_analysis(document_path: Path):
    text = document_path.read_text(encoding="utf-8")
    anchors = extract_anchors(text)

    analysis = []

    for anchor in anchors:
        result = {
            "tetherAnchor": {
                "group": "meaning",
                "type": "text_span",
                "sourceSystem": "real_tether_extractor_v2",
                "sourceLocation": f"line_{anchor['line']}",
                "anchorText": anchor["text"],
                "structuredValue": anchor["text"],
                "matchedSignals": anchor["matchedSignals"],
                "traceReason": "Matched explicit constraint language in source text"
            },
            "driftDetected": False,
            "status": "ok"
        }

        analysis.append(result)

    return {
        "document": str(document_path),
        "anchorCount": len(anchors),
        "analysis": analysis
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python real_tether_extractor_v2.py <document>")
        sys.exit(1)

    document_path = Path(sys.argv[1])

    if not document_path.exists():
        print(f"Error: file not found: {document_path}")
        sys.exit(1)

    output = build_analysis(document_path)
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
