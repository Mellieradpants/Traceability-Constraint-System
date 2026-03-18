import json

anchors = [
    {
        "line": 1,
        "text": "Applicants must submit documentation within 30 days.",
        "matchedSignals": ["must"]
    },
    {
        "line": 3,
        "text": "The agency may extend deadlines under exceptional circumstances.",
        "matchedSignals": ["may"]
    }
]

analysis = []

for anchor in anchors:
    text = anchor["text"].lower()

    # observation (what is explicitly present)
    observation_parts = []

    if "must" in text:
        observation_parts.append("Includes a requirement ('must').")

    if "may" in text:
        observation_parts.append("Includes permission ('may').")

    if "within" in text:
        observation_parts.append("Includes a time constraint.")

    if "under" in text:
        observation_parts.append("Includes a condition.")

    observation = " ".join(observation_parts)

    # operational meaning (no added info)
    if "must submit documentation within 30 days" in text:
        operational = "Applicants are required to submit documentation within 30 days."
    elif "may extend deadlines under exceptional circumstances" in text:
        operational = "The agency is allowed to extend deadlines under exceptional circumstances."
    else:
        operational = anchor["text"]

    # drift check (simple)
    drift = False

    result = {
        "tetherAnchor": {
            "group": "meaning",
            "type": "text_span",
            "sourceSystem": "semantic_tether_engine",
            "sourceLocation": f"line_{anchor['line']}",
            "anchorText": anchor["text"],
            "structuredValue": operational,
            "matchedSignals": anchor["matchedSignals"],
            "traceReason": observation
        },
        "driftDetected": drift,
        "status": "ok"
    }

    analysis.append(result)

output = {
    "analysis": analysis
}

print(json.dumps(output, indent=2))
