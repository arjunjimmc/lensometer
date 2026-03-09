# Testing Guide (Kaise test kare)

## 1) Environment setup

```bash
python -m venv .venv
source .venv/bin/activate
```

## 2) Run CLI demo (quick smoke test)

```bash
PYTHONPATH=src python app/prototype_cli.py --demo
```

Expected output me yeh headings dikhni chahiye:
- `=== Lensometer Prototype Output ===`
- Sphere / Cylinder / Axis / Confidence
- `Pass quality:  True` (demo data ke liye)

## 3) Run automated unit tests

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

Aapko 2 tests `ok` dikhne chahiye.

## 4) Optional: run through pytest (if installed)

```bash
PYTHONPATH=src pytest -q
```

> Note: project ke core tests `unittest` ke saath bhi fully run ho jate hain, isliye pytest mandatory nahi hai.

## 5) Common issues

- `ModuleNotFoundError: lensometer`
  - Ensure command me `PYTHONPATH=src` prefix ho.
- Virtual env active nahi hai
  - `source .venv/bin/activate` rerun karein.
