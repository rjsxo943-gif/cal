"""Compare representative Python and C++ calculator results."""
from __future__ import annotations

import math
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "python_calculator"))
from core.calculator_engine import CalculatorEngine  # noqa: E402
from core.calculator_state import AngleMode, CalculatorState  # noqa: E402

CASES = [
    "2+3*4", "(2+3)*4", "2^3^2", "-2^2", "5!", "50%",
    "sqrt(81)", "sin(30)", "cos(60)", "tan(45)",
    "asin(0.5)", "log(1000)", "ln(e)", "root(3,-8)",
    "npr(10,3)", "ncr(10,3)", "gcd(84,30)", "lcm(12,18)",
    "quot(-7,3)", "rem(-7,3)", "pi*2", "1.2E3+4",
]


def cpp_value(executable: pathlib.Path, expression: str) -> float:
    result = subprocess.run(
        [str(executable), "--eval", expression, "--angle", "DEG", "--format", "NORM"],
        check=False, capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"C++ failed for {expression}: {result.stdout}{result.stderr}")
    return float(result.stdout.strip())


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python compare_with_python.py <scientific_calculator executable>")
        return 2
    executable = pathlib.Path(sys.argv[1]).resolve()
    state = CalculatorState(angle_mode=AngleMode.DEG)
    engine = CalculatorEngine(state)
    failures = 0
    for expression in CASES:
        expected = engine.evaluate(expression)
        actual = cpp_value(executable, expression)
        ok = math.isclose(actual, expected, rel_tol=1e-9, abs_tol=1e-10)
        print(f"{'PASS' if ok else 'FAIL'}  {expression:<18} py={expected:.12g} cpp={actual:.12g}")
        failures += int(not ok)
    print(f"\n{len(CASES) - failures}/{len(CASES)} parity cases passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
