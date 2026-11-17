"""Evidence rules in pure code (no I/O, no LLM): point-in-time filter (published_at <= as_of);
drop tier >= 2 evidence without a path to tier 0; order conflicting evidence by credibility,
then reliability, then tier; check that every claim cites at least one evidence id.
"""

# TODO: write the implementation yourself.
