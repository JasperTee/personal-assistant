## What

<!-- one or two sentences: what this PR changes -->

## Why

<!-- the problem or the phase-1 step; link the ADR or issue if there is one -->

## How to test

<!-- steps a reviewer can follow, or which tests cover it -->

## Checklist

- [ ] `dotnet format --verify-no-changes`, `dotnet build` and `dotnet test` pass (market: `ruff check .`, `lint-imports`, `pytest`)
- [ ] Tests added or updated for the change
- [ ] Docs updated (README, docs/, ADR) if behaviour or structure changed
- [ ] No secrets or real tenant data
