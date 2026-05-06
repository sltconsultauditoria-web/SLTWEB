$env:RUN_RENDER_SMOKE="1"
python -m pytest tests/test_render_public_smoke.py -q
exit $LASTEXITCODE
