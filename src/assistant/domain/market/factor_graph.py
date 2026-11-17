"""Factor-map graph rules in pure code (no I/O, no LLM): compute each node's tier as the number
of edges on the shortest path to the subject; find the path from a factor down to tier 0;
reject maps with unknown node ids, missing subject or nodes that cannot reach the subject.
"""

# TODO: write the implementation yourself.
