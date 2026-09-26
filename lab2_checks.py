"""
Answer checks for AM 11B Lab 2: Profit Maximization.

The Lab 2 notebook's setup cell imports `check` from this file, so students see only a
one-line call like  check("lab2_...", answer)  and the feedback it prints, not the
answer key or the comparison code.

This file is self-contained on purpose: each lab has its own checks file, so editing
one lab's checks can't break another lab. Keep it in the same folder as the lab
notebooks (it's deployed with them).

If you change an answer here, change the matching Otter test in grading/Lab2_tests/ too.
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
        "Correct! That's a W. 🏆",
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
    "lab2_step3": ("A", "Check the sign of D first, then the sign of pi_LL, and match them to the rules in Step 3."),
}


def _check_mc(question, answer):
    correct, hint = _MC[question]
    if str(answer).strip().upper() not in _LETTERS:
        print('⚠️ Set your answer to "A", "B", "C", or "D" (with the quotes), then run this cell again.')
    elif str(answer).strip().upper() == correct:
        _right()
    else:
        _wrong(hint)


# ------------------------------------------------------------------ Lab 2
def _lab2_partials(pi_L_hand, pi_K_hand):
    if _blank(pi_L_hand) or _blank(pi_K_hand):
        return _missing("both formulas")
    pi_L = 24 * _K**sp.Rational(3, 10) / _L**sp.Rational(3, 5) - 5
    pi_K = 18 * _L**sp.Rational(2, 5) / _K**sp.Rational(7, 10) - 3
    _report([n for n, y, c in [("d(pi)/dL", pi_L_hand, pi_L), ("d(pi)/dK", pi_K_hand, pi_K)]
             if not same_formula(y, c, [_L, _K])], hint_prefix="Recheck your power-rule work for: ")


def _lab2_your_turn(w_new, Lstar_new, Lstar, D_new, pi_LL_new_val):
    if w_new > 5 and D_new > 0 and pi_LL_new_val < 0 and Lstar_new < Lstar:
        _right()
    else:
        _wrong("Make sure w_new is actually higher than 5 -- a higher wage should still give a maximum, with less labor hired.")


def _lab2_saddle(xstar_hand, ystar_hand, D_hand, classification_hand):
    if any(_blank(v) for v in (xstar_hand, ystar_hand, D_hand, classification_hand)):
        return _missing("all four answers")
    wrong = []
    if not (_close(xstar_hand, 50) and _close(ystar_hand, 20)):
        wrong.append("the critical point")
    if not _close(D_hand, -4):
        wrong.append("D")
    if "saddle" not in str(classification_hand).lower():
        wrong.append("the classification")
    _report(wrong)


_CHECKS = {
    "lab2_partials": _lab2_partials,
    "lab2_your_turn": _lab2_your_turn,
    "lab2_saddle": _lab2_saddle,
}


def check(question, *answers):
    """Print feedback on a student's answer(s) for the named Lab 2 question."""
    if question in _MC:
        return _check_mc(question, *answers)
    if question not in _CHECKS:
        raise ValueError(f"Unknown Lab 2 question id: {question!r}")
    try:
        _CHECKS[question](*answers)
    except Exception:
        _wrong("Make sure every answer above is a number (or, for formulas, text in quotes).")
