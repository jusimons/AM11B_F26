"""
Answer checks for AM 11B Lab 3: Marginal to Total.

The Lab 3 notebook's setup cell imports `check` from this file, so students see only a
one-line call like  check("lab3_...", answer)  and the feedback it prints, not the
answer key or the comparison code.

This file is self-contained on purpose: each lab has its own checks file, so editing
one lab's checks can't break another lab. Keep it in the same folder as the lab
notebooks (it's deployed with them).

If you change an answer here, change the matching Otter test in grading/Lab3_tests/ too.
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
        "Correct! Understood the assignment. 💯",
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
    "lab3_stop": ("B", "Solve 500-20t=0 for t, then integrate the marginal profit from 0 up to that t."),
}


def _check_mc(question, answer):
    correct, hint = _MC[question]
    if str(answer).strip().upper() not in _LETTERS:
        print('⚠️ Set your answer to "A", "B", "C", or "D" (with the quotes), then run this cell again.')
    elif str(answer).strip().upper() == correct:
        _right()
    else:
        _wrong(hint)


# ------------------------------------------------------------------ Lab 3
def _lab3_riemann(n2_sum_hand):
    if _blank(n2_sum_hand):
        return _missing("your hand-computed sum")
    _right() if _close(n2_sum_hand, 4500) else _wrong("Heights should be pi'(0) and pi'(5), each times a width of 5.")


def _lab3_ftc(F_hand, total_profit_10_hand):
    if _blank(F_hand) or _blank(total_profit_10_hand):
        return _missing("your antiderivative and total")
    wrong = []
    if not same_formula(F_hand, 500 - 20 * _t, [_t], antiderivative=True):
        wrong.append("your antiderivative F(t)")
    if not _close(total_profit_10_hand, 4000):
        wrong.append("F(10) - F(0)")
    _report(wrong)


_CHECKS = {
    "lab3_riemann": _lab3_riemann,
    "lab3_ftc": _lab3_ftc,
}


def check(question, *answers):
    """Print feedback on a student's answer(s) for the named Lab 3 question."""
    if question in _MC:
        return _check_mc(question, *answers)
    if question not in _CHECKS:
        raise ValueError(f"Unknown Lab 3 question id: {question!r}")
    try:
        _CHECKS[question](*answers)
    except Exception:
        _wrong("Make sure every answer above is a number (or, for formulas, text in quotes).")
