"""
Answer checks for the AM 11B lab notebooks.

Each notebook's setup cell imports `check` from this file, so students see only a
one-line call like  check("lab1_step1", Q0_hand, MPL_hand, MPK_hand)  and the feedback
it prints, not the answer key or the comparison code.

Keep this file in the same folder as the lab notebooks (it's deployed with them).
The Otter tests in grading/ are separate and don't depend on these answer keys,
except that Labs 2, 3 and 5 use `same_formula` from this file.
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
    "lab3_stop": ("B", "Solve 500-20t=0 for t, then integrate the marginal profit from 0 up to that t."),
    "lab4_q4_3": ("C", "Re-integrate (D - S) from 0 to 5 -- it should land on the same number as CS + PS."),
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


def _lab1_your_turn(pct_error_new, pct_error):
    if pct_error_new > pct_error:
        _right()
    else:
        _wrong("Try a point even farther from (100,25) so the error grows more clearly.")


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


# ------------------------------------------------------------------ Lab 4
def _lab4_equilibrium(qstar_hand, pstar_hand):
    if _blank(qstar_hand) or _blank(pstar_hand):
        return _missing("your hand-computed q* and p*")
    _report([n for n, y, c in [("q*", qstar_hand, 5), ("p*", pstar_hand, 75)] if not _close(y, c)],
            extra="Solve 100-q^2=3q^2 for q, then plug back in for p.")


def _lab4_surplus(CS_hand, PS_hand):
    if _blank(CS_hand) or _blank(PS_hand):
        return _missing("your hand-computed CS and PS")
    _report([n for n, y, c in [("CS", CS_hand, 250 / 3), ("PS", PS_hand, 250)] if not _close(y, c)],
            hint_prefix="Recheck your antiderivative and evaluation for: ")


# ------------------------------------------------------------------ Lab 5
def _lab5_antiderivative(F_hand):
    if _blank(F_hand):
        return _missing("your antiderivative")
    if same_formula(F_hand, (1000 + 50 * _t) * sp.exp(-_t / 20), [_t], antiderivative=True):
        _right()
    else:
        _wrong("Double check your u, dv split and the sign when you substitute v back in.")


_CHECKS = {
    "lab1_warmup": _lab1_warmup, "lab1_step1": _lab1_step1, "lab1_step2": _lab1_step2,
    "lab1_your_turn": _lab1_your_turn,
    "lab2_partials": _lab2_partials, "lab2_your_turn": _lab2_your_turn, "lab2_saddle": _lab2_saddle,
    "lab3_riemann": _lab3_riemann, "lab3_ftc": _lab3_ftc,
    "lab4_equilibrium": _lab4_equilibrium, "lab4_surplus": _lab4_surplus,
    "lab5_antiderivative": _lab5_antiderivative,
}


def check(question, *answers):
    """Print feedback on a student's answer(s) for the named question."""
    if question in _MC:
        return _check_mc(question, *answers)
    if question not in _CHECKS:
        raise ValueError(f"Unknown question id: {question!r}")
    try:
        _CHECKS[question](*answers)
    except Exception:
        _wrong("Make sure every answer above is a number (or, for formulas, text in quotes).")
