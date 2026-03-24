Traceability Constraint System — Architecture

Goal

Ensure all outputs are directly traceable to explicit source text.

The system only produces outputs supported by a specific anchor.

Problem

Many systems produce summaries or explanations without linking outputs to source text.

This breaks traceability and allows meaning to drift from the source.

Core Rule

Every output must:

reference a specific source anchor
include only what the anchor supports

If the source does not support it, it is not included.

Core Flow

Document → Anchor Extraction → Feature Detection → Constrained Restatement → Structured Output

Anchor Types

An anchor is a direct reference to source content.

Examples:

quoted text
document sections
page numbers
timestamps
metadata fields

Output Structure

Each result includes three parts:

Anchor
Source text or location

Observation
What is explicitly present in the text

Operational Meaning
Plain-language restatement of the same content without adding or altering information

System Behavior

anchors are identified before any output is produced
all outputs must link to an anchor
no output may include information not present in the anchor
if no valid anchor exists, no output is produced

Design Principle

If it cannot be traced to the source, it is not included.

aligned language with README + DESIGN + PIPELINE

