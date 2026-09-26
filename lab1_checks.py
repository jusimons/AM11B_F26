"""
Answer checks for AM 11B Lab 1: Linear Approximation.

The Lab 1 notebook's setup cell imports `check` from this file, so students see only a
one-line call like  check("lab1_...", answer)  and the feedback it prints, not the
answer key or the comparison code.

This file is self-contained on purpose: each lab has its own checks file, so editing
one lab's checks can't break another lab. Keep it in the same folder as the lab
notebooks (it's deployed with them).

If you change an answer here, change the matching Otter test in grading/Lab1_tests/ too.
"""
import random

import sympy as sp
from sympy.parsing.sympy_parser import (convert_xor, implicit_multiplication_application,
                                        parse_expr, standard_transformations)

__all__ = ["check", "same_formula"]

_L, _K = sp.symbols("L K", positive=True)
_t = sp.symbols("t", positive=True)
_LETTERS = ["A", "B", "C", "D"]


# ------------------------------------------------------------------ feedback helpers
def _right():
    emoji = random.choice(["✅", "🚀", "⭐"])
    msg = random.choice([
        "You're right! Nice work.",
        "Great job! You nailed it.",
        "You did it!",
        "Yes! That's exactly right.",
        "Correct! You're crushing this.",
        "Correct! You ate that — no crumbs. 🍽️",
        "Correct! It's giving… economist. 📈",
    ])
    print(f"{emoji} {msg}")


def _wrong(hint=""):
    print("❌ Not quite. Try again!" + (f" {hint}" if hint else ""))


def _missing(what):
    print(f"⚠️ Enter {what} in the cell above, run it, then run this cell again.")


def _blank(value):
    return value is None or (isinstance(value, str) and not value.strip())


def _close(yours, correct, tol=0.01):
    try:
        return abs(float(yours) - float(correct)) <= tol
    except (TypeError, ValueError):
        return False


def _report(wrong, hint_prefix="Recheck your hand work for: ", extra=""):
    if wrong:
        _wrong(hint_prefix + ", ".join(wrong) + "." + (f" {extra}" if extra else ""))
    else:
        _right()


def same_formula(typed, correct, variables, antiderivative=False):
    """True if a formula typed as text (e.g. "24*K^0.3/L^0.6 - 5") matches `correct`.
    Compares values at several test points, so any equivalent form counts.
    With antiderivative=True, checks that the typed formula's derivative equals `correct`
    (so any +C is fine)."""
    try:
        names = {str(v): v for v in variables}
        names.update({"e": sp.E, "exp": sp.exp, "sqrt": sp.sqrt, "ln": sp.log})
        expr = parse_expr(str(typed), local_dict=names,
                          transformations=standard_transformations
                          + (implicit_multiplication_application, convert_xor))
        if antiderivative:
            expr = sp.diff(expr, variables[0])
        for vals in [(1.3, 2.1), (4.0, 0.7), (9.5, 12.0)]:
            point = dict(zip(variables, vals))
            yours, right = complex(expr.subs(point)), complex(correct.subs(point))
            if abs(yours - right) > 1e-6 * max(1, abs(right)):
                return False
        return True
    except Exception:
        return False


def _eval_at(expr, value):
    """Evaluate a one-variable sympy expression at `value`, whatever its variable is called."""
    return float(expr.subs({s: value for s in expr.free_symbols}))


# ------------------------------------------------------------------ multiple choice
_MC = {

}


def _check_mc(question, answer):
    correct, hint = _MC[question]
    if str(answer).strip().upper() not in _LETTERS:
        print('⚠️ Set your answer to "A", "B", "C", or "D" (with the quotes), then run this cell again.')
    elif str(answer).strip().upper() == correct:
        _right()
    else:
        _wrong(hint)


# ------------------------------------------------------------------ Lab 1
def _lab1_warmup(R_prime):
    try:
        ok = (abs(_eval_at(R_prime, 0) - 200) < 1e-9 and abs(_eval_at(R_prime, 40) - 40) < 1e-9
              and abs(_eval_at(R_prime, 60) + 40) < 1e-9)
    except Exception:
        ok = False
    _right() if ok else _wrong("Double check R_prime is set to sp.diff(R, x).")


def _lab1_step1(Q0_hand, MPL_hand, MPK_hand):
    if any(_blank(v) for v in (Q0_hand, MPL_hand, MPK_hand)):
        return _missing("your hand-computed values")
    _report([n for n, y, c in [("Q0", Q0_hand, 1000), ("MP_L", MPL_hand, 5), ("MP_K", MPK_hand, 20)]
             if not _close(y, c)])


def _lab1_step2(approx_hand):
    if _blank(approx_hand):
        return _missing("your hand-computed estimate")
    _right() if _close(approx_hand, 1065) else _wrong("Recheck your arithmetic: Q0 + MP_L*(105 - 100) + MP_K*(27 - 25).")


def _lab1_your_turn(L1_new, K1_new, pct_error_new, pct_error):
    # The point must be farther from (100, 25) than the (105, 27) example, AND the error must grow.
    dist_new = ((L1_new - 100) ** 2 + (K1_new - 25) ** 2) ** 0.5
    dist_example = ((105 - 100) ** 2 + (27 - 25) ** 2) ** 0.5
    if dist_new <= dist_example:
        _wrong(f"({L1_new}, {K1_new}) is no farther from (100, 25) than the (105, 27) example was. "
               "Pick a point much farther away, like (200, 10) or (60, 40).")
    elif pct_error_new <= pct_error:
        _wrong("Your point is farther away, but the error didn't grow! Points where L is exactly 4 times K "
               "lie on a line where this production function is perfectly straight, so the tangent plane "
               "matches it exactly there. Try a point off that line, like (200, 10) or (60, 40).")
    else:
        _right()


_CHECKS = {
    "lab1_warmup": _lab1_warmup,
    "lab1_step1": _lab1_step1,
    "lab1_step2": _lab1_step2,
    "lab1_your_turn": _lab1_your_turn,
}


def check(question, *answers):
    """Print feedback on a student's answer(s) for the named Lab 1 question."""
    if question in _MC:
        return _check_mc(question, *answers)
    if question not in _CHECKS:
        raise ValueError(f"Unknown Lab 1 question id: {question!r}")
    try:
        _CHECKS[question](*answers)
    except Exception:
        _wrong("Make sure every answer above is a number (or, for formulas, text in quotes).")
