Semantic Tether Point – Design Rules

Rule 1: Interpretation Requires a Tether

All interpretations must reference a verified anchor.

Anchors may include:
- quoted text
- document sections
- page numbers
- timestamps
- structured metadata fields


Rule 2: Anchor Before Interpretation

The system must extract anchors before producing analysis.

Pipeline:

Document
→ Anchor extraction
→ Tethered interpretation
→ Structured output


Rule 3: Traceability

Every interpretation must be traceable back to its anchor.


Rule 4: Drift Prevention

If interpretation becomes detached from its anchor, it must not continue.


Rule 5: Recovery Behavior

When uncertainty occurs, return to the last verified tether point before continuing analysis.


Core System Rule

When in doubt, return to the tether point.
