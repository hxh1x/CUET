# CUET SCQP09 Multi-Tier Assessment Specification & Rubric

**Artifact:** `CUET_SCQP09_FINAL/CURRICULUM/assessment_spec.md`  
**Purpose:** Formal evaluation framework for verifying candidate mastery across all 92 modules of CUET-PG SCQP09. Aligned with Bloom's Revised Taxonomy and NTA 72-second speed benchmarks.

---

## 1. Exam Structure & Pedagogical Benchmarks

- **Paper Format:** 75 multiple-choice questions in 90 minutes.
- **Time Allocation:** Approximately **72 seconds per question**.
- **Scoring Scheme:** $+4$ marks for each correct response, $-1$ mark for each incorrect response, $0$ for unattempted.
- **Question Typologies (2024–2026 NTA Trend):**
  1. Direct Single-Choice MCQs
  2. Match List-I with List-II (combinatorial matching)
  3. Arrange in Correct Sequence / Chronological Order
  4. Multiple Statements Evaluation ("Which of the following are correct? (A), (B), (C)...")
  5. Assertion–Reason ($A$ and $R$ analysis)

---

## 2. Five-Tier Assessment Hierarchy

Every module must provide progressive assessments categorized into five distinct difficulty and cognitive tiers:

```
[Level 5] Synthesis & Exam-Speed Mastery (≤ 72s, mixed-concept synthesis, high pressure)
   ▲
[Level 4] Analytical Discrimination & Error Diagnosis (Edge cases, bug detection, counterexamples)
   ▲
[Level 3] Procedural Execution & Problem Solving (Standard numerical & algorithmic computation)
   ▲
[Level 2] Conceptual Understanding & Translation (Representation changes, Venn/ASCII diagrams)
   ▲
[Level 1] Recall & Recognition (Definitions, terminology, standard formula identification)
```

---

## 3. Rubric & Evaluation Criteria for the 5 Levels

### Level 1: Recall & Recognition (Remembering)
- **Cognitive Objective:** Retrieve relevant knowledge from long-term memory. Recognize core terminology, standard identities, time complexities, and definitions without computation.
- **Typical Prompts:**
  - "State the formula for..."
  - "Identify which of the following is an idempotent matrix..."
  - "What is the worst-case time complexity of QuickSort?"
- **Mastery Criteria:**
  - Accuracy $\ge 90\%$ on rapid-fire checks.
  - Response time $\le 25$ seconds per item.
  - Zero formula confusion between similar operations.

---

### Level 2: Conceptual Understanding & Representation (Understanding)
- **Cognitive Objective:** Construct meaning from instructional messages; translate representations between verbal descriptions, algebraic notation, set diagrams, and circuit diagrams.
- **Typical Prompts:**
  - "Match each set expression to its corresponding shaded region in a Venn diagram."
  - "Express the condition 'at least one but not both' in formal Boolean / Set notation."
  - "Explain why Banker's Algorithm avoids deadlocks rather than detecting them."
- **Mastery Criteria:**
  - Accuracy $\ge 85\%$.
  - Ability to convert freely between symbolic formulas, graphical diagrams, and English word problems.
  - Response time $\le 45$ seconds.

---

### Level 3: Procedural Execution & Problem Solving (Applying)
- **Cognitive Objective:** Execute routine procedural algorithms, carry out multi-step algebraic derivations, and solve standard single-topic numerical problems.
- **Typical Prompts:**
  - "In a group of 200 students, 120 play football, 50 play cricket, and 30 play both. How many play exactly one sport?"
  - "Compute the inverse of matrix $A$ or evaluate $\det(A)$ using cofactor expansion."
  - "Find the number of page faults for the reference string using FIFO replacement."
- **Mastery Criteria:**
  - Accuracy $\ge 80\%$.
  - Arithmetic and algebraic manipulation verified with zero sign errors.
  - Response time $\le 70$ seconds.

---

### Level 4: Analytical Discrimination & Error Diagnosis (Analyzing)
- **Cognitive Objective:** Break material into constituent parts; determine how parts relate to an overall structure. Discriminate true vs false assertions, identify edge-case traps, and detect faulty reasoning.
- **Typical Prompts:**
  - "Consider statements (A), (B), (C), (D) regarding symmetric matrices. Which combinations are strictly valid?"
  - "Evaluate Assertion (A) and Reason (R): Determine if R is the correct explanation of A."
  - "Given a three-set survey with contradictory totals, identify which constraint is mathematically violated."
- **Mastery Criteria:**
  - Accuracy $\ge 75\%$.
  - Candidate actively verifies each statement independently rather than guessing based on partial matches.
  - Demonstrates awareness of boundary conditions (e.g., empty set, division by zero, cycle in graph).

---

### Level 5: Synthesis & Exam-Speed Mastery (Evaluating & Creating)
- **Cognitive Objective:** Integrate multi-domain concepts under strict NTA exam conditions; optimize solution path for speed; apply heuristics to eliminate distractors within 72 seconds.
- **Typical Prompts:**
  - Real NTA PYQs under strict 72-second countdown timers.
  - Composite questions combining Set Theory cardinality with Probability and Permutations.
  - "Match List-I with List-II" involving 4 independent mathematical evaluations.
- **Mastery Criteria:**
  - Accuracy $\ge 80\%$ under simulated time pressure.
  - Mean latency $\le 72$ seconds per question.
  - Net positive score ($+4$ / $-1$) exceeding $+3.0$ expected value per question attempted.

---

## 4. Mastery Scoring Engine Rules

| Status | Overall Level | Criteria | Next Recommendation |
|---|---|---|---|
| **NOVICE** | Level 0 | Module unstarted or $< 50\%$ on Level 1. | Complete foundational reading and terminology drills. |
| **DEVELOPING**| Level 1–2 | $\ge 80\%$ on L1, but $< 70\%$ on L2–L3. | Practice visual diagrams, worked examples, and basic exercises. |
| **COMPETENT** | Level 3 | $\ge 80\%$ on L1–L3, but $< 70\%$ on L4–L5. | Drill multi-statement, assertion-reason, and standard PYQs. |
| **MASTERED** | Level 4–5 | $\ge 85\%$ on L1–L4, $\ge 80\%$ on L5 under 72s. | Module cleared. Scheduled for spaced repetition review. |
| **REGRESSED** | Any | Fails spaced review after 14/30 days. | Targeted error remediation on failed diagnostic sub-skills. |
