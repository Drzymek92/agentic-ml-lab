# Working set (session scope)
_Pinned selectors the design→build→test loop operates on (D3/D5). `decision_tools.py scope`
resolves these into a compact read-plan (the in-play decisions + only the docs that carry them).
Overwrite per session — like `session.md`, this is a cold-start aid, not a history.
Write it by hand or with `decision_tools.py scope <selectors> --pin`._

<!-- selectors: one per line as `- <D#|P#|G#|path|keyword>`; empty = nothing pinned yet -->
