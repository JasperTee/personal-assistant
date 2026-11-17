"""Indicator trust rules in pure code (no I/O, no LLM), ADR-24: decayed score of past calls per
indicator, regime and horizon; trust = that score shrunk toward the average by the number of
scored calls; a new indicator starts at the average.
"""

# TODO: write the implementation yourself.
