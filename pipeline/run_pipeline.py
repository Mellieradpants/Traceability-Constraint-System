from typing import Dict, Any
from uuid import uuid4

from input.intake import prepare_input
from structure.parser import build_structure
from selection.filter import build_working_set


def run_pipeline(raw_text: str) -> Dict[str, Any]:
    """
    Full system pipeline (Layers 1–3 wired)

    Flow:
    Input → Structure → Selection

    No meaning, no AI yet.
    """

    # Layer 1 — Input
    prepared = prepare_input(raw_text)

    document_id = str(uuid4())
    input_type = prepared.get("input_type", "xml")  # default for now

    # Layer 2 — Structure
    structure_output = build_structure(
        document_id=document_id,
        raw_text=prepared["raw_text"],
        input_type=input_type,
    )

    if not structure_output.get("canProceed"):
        return structure_output

    # Layer 3 — Selection
    selection_output = build_working_set(structure_output)

    if not selection_output.get("canProceed"):
        return selection_output

    return selection_output
