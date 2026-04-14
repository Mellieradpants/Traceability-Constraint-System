from typing import Dict, Any, List, Optional


def build_working_set(structure_output: Dict[str, Any]) -> Dict[str, Any]:
    """
    Layer 3 — Selection

    Purpose:
    Select structurally eligible nodes from Structure output.

    Rules:
    - deterministic only
    - preserve order
    - do not modify node content
    - do not interpret meaning
    """

    document_id = structure_output.get("documentId")
    input_type = structure_output.get("inputType")
    nodes = structure_output.get("nodes", [])

    if not structure_output.get("canProceed", False):
        return _fail(document_id, input_type, ["Structure layer failed"])

    if not isinstance(nodes, list) or not nodes:
        return _fail(document_id, input_type, ["No nodes available for selection"])

    selected_nodes: List[Dict[str, Any]] = []
    drop_reasons: List[Dict[str, str]] = []

    for node in nodes:
        reason = _get_drop_reason(node)
        if reason is None:
            selected_nodes.append(node)
        else:
            drop_reasons.append({
                "nodeId": str(node.get("nodeId", "")),
                "reason": reason,
            })

    if not selected_nodes:
        return {
            "documentId": document_id,
            "inputType": input_type,
            "selectedNodes": [],
            "selectionMetadata": {
                "totalInputNodes": len(nodes),
                "totalSelectedNodes": 0,
                "droppedNodeIds": [item["nodeId"] for item in drop_reasons],
                "dropReasons": drop_reasons,
            },
            "selectionErrors": ["No nodes passed selection rules"],
            "canProceed": False,
        }

    return {
        "documentId": document_id,
        "inputType": input_type,
        "selectedNodes": selected_nodes,
        "selectionMetadata": {
            "totalInputNodes": len(nodes),
            "totalSelectedNodes": len(selected_nodes),
            "droppedNodeIds": [item["nodeId"] for item in drop_reasons],
            "dropReasons": drop_reasons,
        },
        "selectionErrors": [],
        "canProceed": True,
    }


def _get_drop_reason(node: Dict[str, Any]) -> Optional[str]:
    """
    Structural eligibility checks only.
    Returns a reason string if node should be dropped.
    Returns None if node is eligible.
    """

    node_id = node.get("nodeId")
    text = node.get("text")
    order = node.get("order")
    path = node.get("path")
    source_ref = node.get("sourceRef")

    if not node_id:
        return "missing_node_id"

    if text is None:
        return "missing_text"

    if not isinstance(text, str):
        return "invalid_text_type"

    if not text.strip():
        return "empty_text"

    if order is None:
        return "missing_order"

    if not path:
        return "missing_path"

    if not isinstance(source_ref, dict):
        return "missing_source_ref"

    if not source_ref.get("type"):
        return "missing_source_ref_type"

    if not source_ref.get("locator"):
        return "missing_source_ref_locator"

    return None


def _fail(document_id: str, input_type: str, messages: List[str]) -> Dict[str, Any]:
    return {
        "documentId": document_id,
        "inputType": input_type,
        "selectedNodes": [],
        "selectionMetadata": {
            "totalInputNodes": 0,
            "totalSelectedNodes": 0,
            "droppedNodeIds": [],
            "dropReasons": [],
        },
        "selectionErrors": messages,
        "canProceed": False,
    }
   

