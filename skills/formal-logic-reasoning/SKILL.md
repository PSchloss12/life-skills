---
name: formal-logic-reasoning
description: Restricts an agent to formulaic formal-logic chain of thought where every premise, assumption, and inference line carries a truth-likelihood percentage, then emits output in which every statement carries a derived percent likelihood, plus all research premises, assumptions, and starting axioms. Use when the user wants rigorous or formal reasoning, argument validation, proof-style analysis, "prove it", "show the logic", wants to see premises behind a conclusion, or asks for probability-annotated reasoning.
---

# Formal Logic Reasoning

When this skill is active, ALL internal reasoning and ALL output follow this protocol. No prose reasoning. No unquantified claims. The percentage IS the hedge — never write "probably", "it seems", or "likely"; write the number.

## 1. Internal reasoning: formulaic lines only

Every chain-of-thought step is ONE terse line with a fixed schema. Symbols, not sentences. One statement per line. No connective tissue ("so", "as we established", "next we consider"). Tool calls and search queries are exempt; every reasoning line is not.

Schemas (IDs increment; cite IDs, never restate them):

- Premise: `Pn: <formula> <pct>% [<terse source>]` — from research or observation
- Assumption/axiom: `An: <formula> <pct>% [assumed|axiom: <terse why>]`
- Deductive step: `Sn: <formula> <pct>% [= <Form>(<ids>); bound 1-Σ(1-p)]`
- Inductive step: `In: <formula> <pct>% [ind: <basis — sample|analogy|base-rate>]`
- Bayesian update: `Bn: <formula> <pct>% [= Bayes: prior=<pct> P(E|H)=<pct> P(E)=<pct>]`

Formula language (script-compatible ASCII): `~` not, `&` and, `|` or, `->` implies, `<->` iff, `( )` grouping. First-order: `forall x(...)`, `exists x(...)`, predicates like `Fails(deploy)`. Modality flags when applicable: `Box`/`Dia` (necessary/possible), `O`/`Perm` (obligatory/permitted), temporal `always`/`eventually`.

Percentages: whole numbers, honest. 100% only for axioms, definitions, or tautologies.

**Research gate:** an empirical premise (a claim about the world that evidence could check) may only exceed 60% if you gathered its source with a tool during this session; otherwise cap it at 60% and tag `[uncited]`. If the question turns on empirical facts, gather evidence BEFORE assigning percentages — one confidently wrong premise poisons every number downstream of it.

## 2. Named valid forms (use the name, never prose)

- MP (modus ponens): `P -> Q, P ⊢ Q`
- MT (modus tollens): `P -> Q, ~Q ⊢ ~P`
- HS (hypothetical syllogism): `P -> Q, Q -> R ⊢ P -> R`
- DS (disjunctive syllogism): `P | Q, ~P ⊢ Q`
- CON (contraposition): `P -> Q ⊢ ~Q -> ~P`
- ADD (addition): `P ⊢ P | Q`
- CD (constructive dilemma): `(P -> Q) & (R -> S), P | R ⊢ Q | S`
- First-order: UI (`forall x P(x) ⊢ P(c)`), UG (arbitrary-c to `forall`), EI (`exists x P(x) ⊢ P(c)`, fresh c), EG (`P(c) ⊢ exists x P(x)`)

Full schemas, fallacies to avoid, and modal/temporal/deontic/defeasible/paraconsistent extensions: [logic-systems.md](references/logic-systems.md).

**Categorical syllogisms are not propositional implications.** From `All F are S` and `All Sh are S`, `All Sh are F` does NOT follow (undistributed middle) — even when it happens to be true. Instantiating `All F are S` as `F(c) -> S(c)` destroys quantifier scope. Test All-X-are-Y arguments by substitution counterexample (swap a term to force a false conclusion) and name the syllogistic fallacy: undistributed middle, illicit major/minor, existential import. Never label a categorical fallacy with a propositional name (affirming the consequent, etc.).

## 3. Probability propagation (every step)

| Operation | Rule |
|-----------|------|
| Deductive step (valid form) | conclusion ≥ `1 − Σ(1 − pᵢ)` (Adams bound; Adams' probability logic) |
| Conjunction, independent | product of `pᵢ` |
| Conjunction, general | ≤ min(pᵢ) |
| Disjunction, general | ≥ max(pᵢ) |
| Negation | `100 − p` |
| Bayes update | `P(H|E) = P(E|H)·P(H)/P(E)` |
| Inductive step | assign from basis; never above strongest supporting evidence |
| Dependent premises | treat product as upper estimate; prefer the Adams bound |

If a bound falls below 50%, say so in reasoning and either gather stronger premises or report the weakness honestly.

**Mechanical rule — never eyeball a number.** Every deductive step's % comes from the validator (below), not judgment. A valid deduction licenses an honest RANGE: floor = Adams bound `1-Σ(1-p)`, ceiling = the weakest cited premise (you cannot be surer of a conclusion than of what it rests on). Conclusions outside the range get recalculated, not defended. `0%` and `100%` are reserved for contradictions and axioms/definitions/tautologies — nothing else, ever. An INVALID form with informative premises is an *inductive* situation: estimate with `--bayes` and label the step `In`/`Bn` — never emit the conclusion as `Sn` at 0%.

## 4. Validate before answering (deterministic check)

The validator lives beside this file at `scripts/validate_argument.py` — resolve the path from this SKILL.md's own location (the harness reports it when the skill loads; if lost, `find ~ -path '*formal-logic-reasoning/scripts/validate_argument.py' 2>/dev/null | head -1`).

Run it on the propositional skeleton of EVERY deductive argument, with percentages attached:

1. Quantified formulas: instantiate (`forall x` → representative instances per UI; `exists x` → witness per EI) to a propositional skeleton.
2. One shot per argument:
   `python3 <skill-dir>/scripts/validate_argument.py "<P1>" --prob 98 "<P2>" --prob 95 -c "<C>"`
   → `VALID` + Adams floor + product + honest range + a ready-to-paste NOTES line; or `INVALID` + counterexample.
3. **Paste the validator's NOTES line into NOTES verbatim.** A form check with no pasted validator output is `unchecked`, and `unchecked` on a deductive argument is a protocol failure, not a shortcut.
4. The script guards calibration: it errors on conclusion %s above the weakest cited premise, flags 0%/100% premises, and refuses a proposed `--conclusion-pct` outside the honest range. Treat its verdict as final — recompute, never defend.
5. Other operations: `--bayes <prior> <p(E|H)> <p(E)>`, `--neg <p>`, `--bound <p...>`, `--product <p...>`.

Limits: propositional skeletons only; ≤ 20 atoms (2^n rows); FOL is semi-decidable — a valid skeleton is necessary but not sufficient for UG steps. State these caveats in NOTES when they apply.

**Pre-output checklist (mechanical, every run):**
- CONFLICT scan: any premise or note asserts `~C` at ≥50% while `C` is ≥50% → apply §6; never ship both unflagged.
- Calibration scan: no assertive line at 0%/100% (except axioms/tautologies/contradictions); every deductive % sits inside its honest range; every empirical premise obeys the research gate.
- Categorical scan: All-X-are-Y arguments were checked by substitution counterexample, not propositional forms.

## 5. Output format (to user)

Fixed sections, this order. EVERY assertive statement carries `(pct%)` taken from the reasoning — premise %s, step bounds, products. Section labels exempt.

```
PREMISES
- <statement> (<pct>%) [<source>]
ASSUMPTIONS & AXIOMS
- <statement> (<pct>%, assumed|axiom) [<why>]
CONCLUSION
- <answer to the user's question> (<pct>%)
NOTES
- form check: VALID|INVALID|unchecked (skeleton caveat if FOL)
- conflicts, limitations, stronger-evidence needs (<pct>% on any assertive note)
```

If the user's question decomposes into multiple conclusions, list each with its own %. Terse output: no greetings, no filler, no recap. Combined claims get a computed % (product/bound), never an eyeballed blend.

## 6. Conflicts

If reasoning yields both `X` and `~X` at ≥ 50%: flag `CONFLICT` in NOTES. Do NOT infer anything from the pair (paraconsistent — no explosion). Mark directly affected conclusions ≤ 50%, or present both branches with their %s. Never silently drop either.

## Example

Query: "Will the deploy fail if the config file is missing?"

```
P1: ReadsConfig(deploy) 98% [docs: deploy.md]
P2: ReadsConfig(deploy) -> Fails(deploy) 95% [docs: fail-fast on missing config]
S1: Fails(deploy) 93% [= MP(P1,P2); bound 1-(2+5)=93]
```

Validate: `validate_argument.py "ReadsConfig(deploy) -> Fails(deploy)" --prob 98 "ReadsConfig(deploy)" --prob 95 -c "Fails(deploy)"` → VALID, bound 93%, NOTES line printed.

```
PREMISES
- Deploy reads the config file (98%) [deploy.md]
- Deploy is fail-fast when config is missing (95%) [deploy.md]
ASSUMPTIONS & AXIOMS
- none
CONCLUSION
- The deploy fails if the config file is missing (93%)
NOTES
- form check: VALID (MP, propositional skeleton verified)
```
