# Release Checklist

Use this before tagging a release.

- [ ] `python scripts/quality_gate.py` passes locally.
- [ ] GitHub Actions passes on all supported matrix versions.
- [ ] No generated clean data or validation reports are staged.
- [ ] Notebook code cells execute in learning order.
- [ ] Historical Phase 2/3/4 behavior remains reproducible.
- [ ] `README.md` matches the actual feature set.
- [ ] `CHANGELOG.md` contains the release.
- [ ] `pyproject.toml` version is correct.
- [ ] No secrets, tokens, private datasets, or local absolute paths are committed.
- [ ] Resume/portfolio claims use measured evidence only.
- [ ] Create the Git tag only after the repository quality gates are green.
