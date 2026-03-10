
 import json
from pathlib import Path

document_path = Path("examples/example-policy.txt")
document = document_path.read_text()

anchors = [
    {
        "type": "quote",
        "location": "Section 3",
        "text": "Applicants must submit documentation within 30 days."
    },
    {
        "type": "quote",
        "location": "Section 5",
        "text": "The agency may extend deadlines under exceptional circumstances."
    }
]

analysis = []

def detect_drift(anchor_text: str, operational_meaning: str) -> bool:
    anchor_text = anchor_text.lower()
    operational_meaning = operational_meaning.lower()

    if "30 days" in anchor_text and "30 days" not in operational_meaning:
        return True

    if "extend deadlines" in anchor_text and "extend" not in operational_meaning:
        return True

    return False

for anchor in anchors:
    if "30 days" in anchor["text"]:
        observation = "A strict submission deadline is defined."
        operational = "Applicants must provide documents within 30 days or risk rejection."
    elif "extend deadlines" in anchor["text"]:
        observation = "Deadline extensions are allowed."
        operational = "The agency can extend the deadline under special conditions."
    else:
        observation = "No rule detected."
        operational = "No operational meaning extracted."

    drift_detected = detect_drift(anchor["text"], operational)

    result = {
        "anchor": anchor,
        "observation": observation,
        "operationalMeaning": operational,
        "driftDetected": drift_detected
    }

    if drift_detected:
        result["recoveryAction"] = "Return to tether point before continuing analysis."
    else:
        result["recoveryAction"] = "Tether verified."

    analysis.append(result)

output = {
    "document": str(document_path),
    "analysis": analysis
}

print(json.dumps(output, indent=2))       
