"""
Answer checks for AM 11B Lab 0: Notebook Demo (practice only, not graded).

The Lab 0 notebook's setup cell imports `check` from this file, so students see only a
one-line call like  check("lab0_...", answer)  and the feedback it prints, not the
answer key or the comparison code. Same design as lab1_checks.py ... lab5_checks.py.

Keep it in the same folder as the lab notebooks (it's deployed with them).
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
        "Correct! Big brain energy. 🧠",
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


_x, _y = sp.symbols("x y")


# ------------------------------------------------------------------ multiple choice
_MC = {
    "lab0_linear_approx": ("B", "Use f(1,2) + f_x(1,2)*(1.1 - 1) + f_y(1,2)*(2.1 - 2). Don't forget to multiply by the 0.1 changes."),
}


def _check_mc(question, answer):
    correct, hint = _MC[question]
    if str(answer).strip().upper() not in _LETTERS:
        print('⚠️ Set your answer to "A", "B", "C", or "D" (with the quotes), then run this cell again.')
    elif str(answer).strip().upper() == correct:
        _right()
    else:
        _wrong(hint)


# ------------------------------------------------------------------ Lab 0
def _lab0_warmup(my_answer):
    if _blank(my_answer):
        return _missing("your answer")
    _right() if _close(my_answer, 12) else _wrong("Compute 3 * 4 in your head, then type just the number.")


def _lab0_partials(fx_formula_hand, fy_value_hand):
    if _blank(fx_formula_hand) or _blank(fy_value_hand):
        return _missing("both answers")
    wrong = []
    if not same_formula(fx_formula_hand, 2 * _x * _y, [_x, _y]):
        wrong.append("your formula for f_x (treat y as a constant)")
    if not _close(fy_value_hand, 13):
        wrong.append("f_y(1, 2) (find f_y first, then plug in x = 1, y = 2)")
    _report(wrong)


_CHECKS = {
    "lab0_warmup": _lab0_warmup,
    "lab0_partials": _lab0_partials,
}


def check(question, *answers):
    """Print feedback on a student's answer(s) for the named Lab 0 question."""
    if question in _MC:
        return _check_mc(question, *answers)
    if question not in _CHECKS:
        raise ValueError(f"Unknown Lab 0 question id: {question!r}")
    try:
        _CHECKS[question](*answers)
    except Exception:
        _wrong("Make sure every answer above is a number (or, for formulas, text in quotes).")
