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
    "status": "blocked" if drift else "ok"
}
