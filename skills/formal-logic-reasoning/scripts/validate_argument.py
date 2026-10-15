#!/usr/bin/env python3
"""validate_argument.py — validate the FORM of propositional logic arguments
(semantic entailment via truth tables) and compute probability propagation
mechanically, with calibration guards.

Zero dependencies. Works with ASCII (~ & | -> <->) and Unicode (¬ ∧ ∨ → ↔)
connectives, parentheses, and multi-letter variables (Rain, UserIsAdmin, ...).

Usage:
  validate_argument.py "P -> Q" --prob 95 "P" --prob 98 -c "Q"
      # form check + propagation + guards in ONE shot; paste output into NOTES
  validate_argument.py "P -> Q" "P" --conclusion "Q"
      # form check only
  validate_argument.py --bound 90 75                   # Adams: P(C) >= 1-sum(1-p)
  validate_argument.py --product 90 75                 # independent conjunction
  validate_argument.py --neg 95                        # negation: 100 - p
  validate_argument.py --bayes 40 90 50                # prior p(H), p(E|H), p(E)
  validate_argument.py ... -c "Q" --conclusion-pct 93
      # sanity-check a proposed conclusion % against the propagation cap

Guards (--prob mode): errors on 0%/100% premises that cannot bear weight,
warns on 100% (axioms/definitions/tautologies only), and rejects a proposed
conclusion % above the Adams-bound/max-premise cap.

Exit codes: 0 = valid, 1 = invalid (counterexample printed), 2 = error.
"""

import sys

PRECEDENCE = {'~': 4, '&': 3, '|': 2, '->': 1, '<->': 1}
UNICODE_MAP = str.maketrans({'¬': '~', '∧': '&', '∨': '|', '→': '->', '↔': '<->'})


def tokenize(expr):
    """Tokenize into identifiers, operators, parentheses."""
    expr = expr.translate(UNICODE_MAP)
    tokens, i = [], 0
    while i < len(expr):
        ch = expr[i]
        if ch.isalpha() or ch == '_':
            j = i
            while j < len(expr) and (expr[j].isalnum() or expr[j] == '_'):
                j += 1
            name = expr[i:j]
            i = j
            # predicate application: Ident(args) flattens to ONE atom token,
            # so FOL skeletons like P(a) -> Q(a) validate as propositional atoms
            k = i
            while k < len(expr) and expr[k].isspace():
                k += 1
            if k < len(expr) and expr[k] == '(':
                depth, l = 0, k
                while l < len(expr):
                    if expr[l] == '(':
                        depth += 1
                    elif expr[l] == ')':
                        depth -= 1
                        if depth == 0:
                            break
                    l += 1
                if depth != 0:
                    raise ValueError("unbalanced parentheses in predicate application")
                name = name + '(' + ''.join(expr[k + 1:l].split()) + ')'
                i = l + 1
            tokens.append(name)
        elif ch in '()~&|':
            tokens.append(ch)
            i += 1
        elif expr.startswith('->', i):
            tokens.append('->')
            i += 2
        elif expr.startswith('<->', i):
            tokens.append('<->')
            i += 3
        elif ch.isspace():
            i += 1
        else:
            raise ValueError(f"invalid character {ch!r} at position {i}")
    return tokens


def to_postfix(tokens):
    """Shunting-yard: infix -> postfix, with parentheses."""
    output, stack = [], []
    for tok in tokens:
        if tok in PRECEDENCE:
            while (stack and stack[-1] in PRECEDENCE and
                   PRECEDENCE[tok] <= PRECEDENCE[stack[-1]]):
                output.append(stack.pop())
            stack.append(tok)
        elif tok == '(':
            stack.append(tok)
        elif tok == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if not stack:
                raise ValueError("unbalanced parentheses")
            stack.pop()  # discard '('
        else:  # variable
            output.append(tok)
    while stack:
        if stack[-1] == '(':
            raise ValueError("unbalanced parentheses")
        output.append(stack.pop())
    return output


def evaluate(postfix, assignment):
    """Evaluate postfix expression under a truth assignment."""
    stack = []
    for tok in postfix:
        if tok in PRECEDENCE:
            if tok == '~':
                stack.append(not stack.pop())
            else:
                right, left = stack.pop(), stack.pop()
                if tok == '&':
                    stack.append(left and right)
                elif tok == '|':
                    stack.append(left or right)
                elif tok == '->':
                    stack.append((not left) or right)
                elif tok == '<->':
                    stack.append(left == right)
        else:
            stack.append(assignment[tok])
    if len(stack) != 1:
        raise ValueError("malformed expression")
    return stack[0]


def validate(premises, conclusion):
    """Entailment check: no assignment makes all premises true and conclusion false.
    Returns (is_valid, counterexample_or_None)."""
    variables = sorted({t for e in premises + [conclusion]
                        for t in tokenize(e) if t not in PRECEDENCE and t not in '()'})
    parsed_premises = [to_postfix(tokenize(e)) for e in premises]
    parsed_conclusion = to_postfix(tokenize(conclusion))
    n = len(variables)
    if n > 20:
        raise ValueError(f"{n} variables: truth table needs 2^n rows; too slow")
    for i in range(2 ** n):
        assignment = {v: bool((i >> j) & 1) for j, v in enumerate(variables)}
        if all(evaluate(p, assignment) for p in parsed_premises):
            if not evaluate(parsed_conclusion, assignment):
                return False, assignment  # counterexample
    return True, None


def adams_bound(percents):
    """P(C) >= 1 - sum(1 - P(P_i)) for C entailed by premises P_i."""
    uncertainty = sum((100 - p) / 100 for p in percents)
    return max(0.0, 1.0 - uncertainty)


def product(percents):
    """Independent conjunction estimate."""
    result = 1.0
    for p in percents:
        result *= p / 100
    return result


def bayes(prior, p_e_given_h, p_e):
    """P(H|E) = P(E|H) * P(H) / P(E)."""
    if p_e == 0:
        raise ValueError("P(E) = 0: the evidence itself is impossible")
    return p_e_given_h * prior / p_e


def parse_prob_pairs(args):
    """Split arg list into [(formula, pct), ...]; --prob N attaches to the
    preceding formula. Returns (pairs, index of -c/--conclusion in args)."""
    pairs, pending = [], None
    i = 0
    while i < len(args):
        a = args[i]
        if a in ('-c', '--conclusion'):
            break
        if a == '--prob':
            if pending is None:
                raise ValueError('--prob must follow a premise formula')
            pairs.append((pending, float(args[i + 1])))
            pending, i = None, i + 2
            continue
        if pending is not None:
            raise ValueError(f'premise {pending!r} has no --prob; give one per premise')
        pending, i = a, i + 1
    if pending is not None:
        raise ValueError(f'premise {pending!r} has no --prob; give one per premise')
    return pairs, i


def run_prob_mode(args):
    """Form check + mechanical propagation + guards in one shot."""
    pairs, idx = parse_prob_pairs(args)
    if args[idx:idx + 1] not in (['-c'], ['--conclusion']):
        raise ValueError('missing --conclusion')
    conclusion = args[idx + 1]
    if not pairs:
        raise ValueError('need at least one premise with --prob')
    percents = [p for _, p in pairs]
    for pct in percents:
        if pct >= 100:
            print(f'WARNING: premise at {pct:g}% — 100% only for axioms/definitions/tautologies')
        if pct <= 0:
            print(f'WARNING: premise at {pct:g}% — cannot bear weight; restate or drop it')

    valid, counterexample = validate([f for f, _ in pairs], conclusion)
    if not valid:
        print('INVALID: counterexample —')
        for v in sorted(counterexample):
            print(f'  {v} = {str(counterexample[v]).lower()}')
        print('DO NOT present the conclusion as following. Fix the form, add a premise, '
              'or report the argument invalid; if the premises are still EVIDENCE '
              '(e.g. affirming the consequent), estimate via --bayes as an inductive step.')
        return 1

    bound = adams_bound(percents) * 100
    prod = product(percents) * 100
    ceiling = min(percents)  # cannot be surer of C than of the weakest premise it rests on
    print(f'VALID: bound (Adams floor) = {bound:g}%, product (independent conj.) = {prod:g}%')
    print(f'HONEST RANGE for the conclusion: {bound:g}%-{ceiling:g}% (floor = bound; ceiling = weakest premise)')
    print(f'SUGGESTED (conservative, per skill convention): {bound:g}%')
    print(f"NOTES line: form check: VALID; bound {bound:g}% "
          f"(premises {', '.join(f'{p:g}%' for p in percents)})")
    return 0


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2
    try:
        if args[0] == '--bound':
            percents = [float(a) for a in args[1:]]
            if not percents:
                raise ValueError("--bound needs at least one percent")
            print(f"{adams_bound(percents) * 100:g}%")
            return 0
        if args[0] == '--product':
            percents = [float(a) for a in args[1:]]
            if not percents:
                raise ValueError("--product needs at least one percent")
            print(f"{product(percents) * 100:g}%")
            return 0
        if args[0] == '--neg':
            if len(args) != 2:
                raise ValueError("--neg needs exactly one percent")
            print(f"{100 - float(args[1]):g}%")
            return 0
        if args[0] == '--bayes':
            if len(args) != 4:
                raise ValueError("--bayes needs: prior, p(E|H), p(E)")
            prior, p_eh, p_e = (float(a) for a in args[1:])
            print(f"{bayes(prior, p_eh, p_e):g}%")
            return 0
        # Combined mode: formula --prob N ... -c conclusion [--conclusion-pct N]
        if '--prob' in args:
            if '--conclusion-pct' in args:
                cidx = args.index('--conclusion-pct')
                proposed = float(args[cidx + 1])
                trimmed = args[:cidx] + args[cidx + 2:]
                pairs, _ = parse_prob_pairs(trimmed)
                if not pairs:
                    raise ValueError('need at least one premise with --prob')
                floor = adams_bound([p for _, p in pairs]) * 100
                ceiling = min(p for _, p in pairs)  # cannot be surer than the weakest premise it rests on
                if proposed > ceiling + 1e-9:
                    print(f'ERROR: proposed conclusion {proposed:g}% exceeds {ceiling:g}% '
                          f'(weakest cited premise). Recompute — do not eyeball.',
                          file=sys.stderr)
                    return 2
                if proposed < floor - 1e-9:
                    print(f'NOTE: proposed {proposed:g}% is below the Adams floor {floor:g}% — '
                          'pessimistic but not wrong; the bound is a lower bound.')
                print(f'conclusion {proposed:g}% OK (honest range {floor:g}%-{ceiling:g}%)')
            return run_prob_mode(args)
        # Entailment mode: premises..., --conclusion <c> (or -c <c>)
        if '--conclusion' in args:
            idx = args.index('--conclusion')
        elif '-c' in args:
            idx = args.index('-c')
        else:
            raise ValueError("missing --conclusion")
        premises = args[:idx]
        conclusion = args[idx + 1]
        if not premises:
            raise ValueError("need at least one premise")
        valid, counterexample = validate(premises, conclusion)
        if valid:
            print("VALID: conclusion follows from premises (no counterexample exists)")
            return 0
        print("INVALID: counterexample —")
        for v in sorted(counterexample):
            print(f"  {v} = {str(counterexample[v]).lower()}")
        return 1
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
