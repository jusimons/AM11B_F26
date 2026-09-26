"""
Answer checks for AM 11B Lab 5: Present Value.

The Lab 5 notebook's setup cell imports `check` from this file, so students see only a
one-line call like  check("lab5_...", answer)  and the feedback it prints, not the
answer key or the comparison code.

This file is self-contained on purpose: each lab has its own checks file, so editing
one lab's checks can't break another lab. Keep it in the same folder as the lab
notebooks (it's deployed with them).

If you change an answer here, change the matching Otter test in grading/Lab5_tests/ too.
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
        "Correct, no cap. 🧢",
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
    "lab5_step2": ("B", "Evaluate your Step 1 antiderivative at t=5 and at t=0, then subtract."),
    "lab5_q5_2": ("C", "This is just the integral of (1000+50t) from 0 to 5, with no discount factor -- recheck the power rule integration."),
    "lab5_q5_3": ("B", "Evaluate the Step 1 antiderivative at t=10 and at t=0, then subtract -- don't just double the 5-year answer."),
}


def _check_mc(question, answer):
    correct, hint = _MC[question]
    if str(answer).strip().upper() not in _LETTERS:
        print('⚠️ Set your answer to "A", "B", "C", or "D" (with the quotes), then run this cell again.')
    elif str(answer).strip().upper() == correct:
        _right()
    else:
        _wrong(hint)


# ------------------------------------------------------------------ Lab 5
def _lab5_antiderivative(F_hand):
    if _blank(F_hand):
        return _missing("your antiderivative")
    if same_formula(F_hand, (1000 + 50 * _t) * sp.exp(-_t / 20), [_t], antiderivative=True):
        _right()
    else:
        _wrong("Double check your u, dv split and the sign when you substitute v back in.")


_CHECKS = {
    "lab5_antiderivative": _lab5_antiderivative,
}


def check(question, *answers):
    """Print feedback on a student's answer(s) for the named Lab 5 question."""
    if question in _MC:
        return _check_mc(question, *answers)
    if question not in _CHECKS:
        raise ValueError(f"Unknown Lab 5 question id: {question!r}")
    try:
        _CHECKS[question](*answers)
    except Exception:
        _wrong("Make sure every answer above is a number (or, for formulas, text in quotes).")
