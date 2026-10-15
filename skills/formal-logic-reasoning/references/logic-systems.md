# Formal Logic Systems Reference

Reference for the formal-logic-reasoning skill. Tenets, notation, and when each system applies.

## 1. Zeroth-order logic (propositional)

Tenets: formulas built from atoms (P, Q, R…) and connectives; truth-functional semantics (each formula's truth fixed by atoms' truth values); validity = no truth assignment makes premises true and conclusion false (semantic entailment).

Connectives (CoT ASCII / standard):

| ASCII | Standard | Meaning |
|-------|----------|---------|
| `~`   | ¬        | not |
| `&`   | ∧        | and |
| `\|`  | ∨        | or (inclusive) |
| `->`  | →        | if … then (material) |
| `<->` | ↔        | iff |

Valid argument forms:

| Name | Form |
|------|------|
| MP (modus ponens) | `P -> Q, P ⊢ Q` |
| MT (modus tollens) | `P -> Q, ~Q ⊢ ~P` |
| HS (hypothetical syllogism) | `P -> Q, Q -> R ⊢ P -> R` |
| DS (disjunctive syllogism) | `P | Q, ~P ⊢ Q` |
| CON (contraposition) | `P -> Q ⊢ ~Q -> ~P` |
| ADD (addition) | `P ⊢ P | Q` |
| SIMP (simplification) | `P & Q ⊢ P` |
| CONJ (conjunction) | `P, Q ⊢ P & Q` |
| ABS (absorption) | `P -> Q ⊢ P -> (P & Q)` |
| CD (constructive dilemma) | `(P -> Q) & (R -> S), P | R ⊢ Q | S` |
| DD (destructive dilemma) | `(P -> Q) & (R -> S), ~Q | ~S ⊢ ~P | ~R` |
| TAUT | any substitution instance of a tautology ⊢ itself |

Common fallacies (INVALID — check with the script):

| Fallacy | Invalid form |
|---------|--------------|
| Affirming the consequent | `P -> Q, Q ⊢ P` |
| Denying the antecedent | `P -> Q, ~P ⊢ ~Q` |
| Undistributed middle | `P -> Q, R -> Q ⊢ P -> R` |

Metalogic facts: decidable (truth tables, 2^n rows); sound and complete for semantic entailment.

## 2. First-order logic (predicate)

Tenets: adds predicates `F(x)`, relations, functions, identity `=`, and quantifiers over objects.

| Symbol | CoT form | Rule | Side condition |
|--------|----------|------|----------------|
| ∀ | `forall x P(x)` | UI: instantiate to any constant | none |
| ∀ | `forall x P(x)` | UG: generalize from `P(c)` | c must be arbitrary (not from an EI) |
| ∃ | `exists x P(x)` | EI: instantiate to fresh constant | constant appears in no earlier premise |
| ∃ | `exists x P(x)` | EG: from `P(t)` infer `exists x P(x)` | none |

Syllogism pattern (Aristotelian, FOL renderings): `forall x (H(x) -> M(x)), H(a) ⊢ M(a)` (Barbara instance); the four figures reduce to UI + MP / MT chains with existential import caveats for particular premises.

Metlogic facts: sound and (Gödel) complete; validity semi-decidable — no truth-table method; resolution enumerates countermodels but may not halt on valid FOL arguments. Practical approach: instantiate to a propositional skeleton, check it, state the caveat.

## 3. Probabilistic / Bayesian logic

Tenets: degrees of belief obeying Kolmogorov axioms (0 ≤ P ≤ 1; P(tautology)=1; additivity for exclusive alternatives). Cox's theorem: any consistent plausibility calculus matching common-sense constraints is isomorphic to probability. Adams' probability logic: deductive validity degrades gracefully — uncertainty accumulates additively.

| Rule | Formula | Note |
|------|---------|------|
| Negation | `P(~A) = 1 − P(A)` | complement |
| Conjunction (general) | `P(A & B) = P(A)·P(B|A)` | chain rule |
| Conjunction (independent) | `P(A & B) = P(A)·P(B)` | independence assumed |
| Conjunction bound | `P(A & B) ≤ min(P(A), P(B))` | always true |
| Disjunction (general) | `P(A | B) = P(A) + P(B) − P(A & B)` | inclusion–exclusion |
| Disjunction bound | `P(A | B) ≥ max(P(A), P(B))` | always true |
| Conditional | `P(A|B) = P(A & B)/P(B)` | requires P(B) > 0 |
| Bayes | `P(H|E) = P(E|H)·P(H)/P(E)` | from conditional rule |
| Adams bound | `C entailed by Pᵢ ⇒ P(C) ≥ 1 − Σ(1 − P(Pᵢ))` | use for every deductive step |

Caveats: the product rule requires independence — when premises depend (share evidence or causes), product overstates certainty; prefer the Adams bound. A valid argument with certain premises preserves certainty: 100% in, 100% out.

## 4. Modal logic

Tenets: operators on propositions — `Box` necessity (□), `Dia` possibility (◇ ≡ `~Box~`). System K: `Box(P -> Q) -> (Box P -> Box Q)`; T adds `Box P -> P` (factivity); S4 adds positive introspection (`Box P -> Box Box P`); S5 adds negative introspection. Epistemic reading: `Box_i P` = agent i knows P. Deontic reading: `O P` obligatory, `Perm P` permitted (`Perm P ≡ ~O ~P`), `F P` forbidden (`F P ≡ O ~P`).

Use when: claims about what must/may be true, knowledge attributions, obligations/permissions. Named forms: necessitation (from ⊢ P infer `Box P`), K for distribution.

## 5. Temporal logic

Tenets: operators over time — LTL: `always P` (all future), `eventually P` (some future), `X P` (next), `P until Q`. CTL adds path quantifiers A (all paths) / E (exists path). Use when: sequencing, recurrence (`always eventually P`), deadlines (`request -> eventually response`).

## 6. Defeasible / non-monotonic logic

Tenets: defaults with exceptions — `Bird(x) & ~Ab(x) / Flies(x)` (Reiter defaults: prerequisite : justification / conclusion). Adding premises can RETRACT conclusions — inductive chains must mark defeasibility: `In:` steps with % < 100% are retractable; new contrary evidence lowers them via Bayes, not deletion.

## 7. Paraconsistent logic

Tenets: contradictions do not explode — `{P, ~P} ⊬ Q` (LP keeps explosion local). Use when: sources conflict. Procedure: flag CONFLICT, quarantine the pair, mark conclusions downstream of the pair ≤ 50%, present branches separately.

## 8. Higher-order logic (brief)

Quantifies over predicates/relations (`forall F ...`). More expressive, still semi-decidable, no complete proof procedure (Gödel incompleteness applies). Use only when a property of properties is genuinely needed; otherwise stay first-order.

## 9. Which system when

| Need | System | % handling |
|------|--------|------------|
| Certain deduction, truth-functional structure | Propositional | Adams bound on steps |
| Objects, classes, quantification | First-order | Instantiate, bound on skeleton |
| Degrees of belief, evidence weighing | Probabilistic/Bayesian | rules in §3 |
| Necessity/possibility, knowledge | Modal/epistemic | % inside `Box`/`Dia` |
| Obligations, permissions | Deontic | % on norm premises |
| Time, sequencing, liveness | Temporal (LTL/CTL) | % per temporal claim |
| Defaults, rules with exceptions | Defeasible | base-rate %, retractable |
| Conflicting sources | Paraconsistent | quarantine, ≤ 50% downstream |
| Properties of properties | Higher-order | prefer FOL if possible |
