# CUET SCQP09 Mastery Engine Specification

**Artifact:** `CUET_SCQP09_FINAL/LEARNING_SYSTEM/mastery_engine.md`  
**Target:** Candidate Skill Evaluation & Intelligent Progression Model  
**Date:** November 2026  

---

## 1. Pedagogical Philosophy

The CUET SCQP09 examination tests both mathematical precision and rapid decision-making (75 questions in 90 minutes $\approx 72$ seconds per question). Passive reading does not produce exam competence. The **Mastery Engine** enforces an active, criteria-gated progression model ensuring candidates do not advance to complex modules until prerequisite competencies are empirically demonstrated.

---

## 2. Mastery State Machine

Every module in the 92-module syllabus occupies one of five discrete operational states:

```
[NOT_STARTED] ──(Start Module Reading)──► [IN_PROGRESS]
                                             │
                                   (Pass Level 1-3 >=80%)
                                             ▼
                                        [COMPETENT]
                                             │
                            (Pass Level 4-5 >=85% in <=72s)
                                             ▼
                                         [MASTERED]
                                             │
                                   (Spaced Interval Expires)
                                             ▼
                                       [REVISION_DUE]
                                       /            \
                       (Pass Review >=85%)        (Fail Review <75%)
                                     /                \
                                    ▼                  ▼
                               [MASTERED]         [REGRESSED]
```

### State Transition Rules:
1. **NOT_STARTED → IN_PROGRESS:**
   - Candidate opens the module card and completes initial reading of concepts and worked examples.
2. **IN_PROGRESS → COMPETENT:**
   - Score $\ge 80\%$ on Level 1 (Recall) and Level 2 (Conceptual Representation).
   - Score $\ge 75\%$ on Level 3 (Procedural Exercises).
   - Average speed $\le 90$ seconds per question.
3. **COMPETENT → MASTERED:**
   - Score $\ge 85\%$ on Level 4 (Analytical Discrimination).
   - Score $\ge 80\%$ on Level 5 (Synthesis Mock / PYQs) under timed examination conditions ($\le 72$ seconds per question).
   - Error log contains zero unresolved conceptual misunderstandings.
4. **MASTERED → REVISION_DUE:**
   - Triggered automatically when the calendar date reaches `next_review_due` (scheduled via spaced repetition intervals).
5. **REVISION_DUE → MASTERED:**
   - Candidate scores $\ge 85\%$ on a 5-question mixed diagnostic drill. Retention streak increments by $+1$.
6. **REVISION_DUE → REGRESSED:**
   - Candidate scores $< 75\%$ on review drill. Mastery tier is decremented to Tier 2 (Developing), and the system recommends targeted error remediation.

---

## 3. Five-Tier Mastery Rubric

| Tier Level | Designation | Required Gate Criteria | Latency Ceiling |
|---|---|---|---|
| **Tier 0** | Uninitiated | Module not yet attempted. | N/A |
| **Tier 1** | Recall Ready | $\ge 90\%$ on Level 1 rapid-fire terminologies and formulas. | $\le 30$ seconds |
| **Tier 2** | Representational | $\ge 80\%$ on converting word problems into Venn/symbolic forms. | $\le 50$ seconds |
| **Tier 3** | Procedural Competent | $\ge 80\%$ on standard algebraic/numerical calculations. | $\le 75$ seconds |
| **Tier 4** | Analytical Master | $\ge 85\%$ on statement matching, error detection, edge cases. | $\le 72$ seconds |
| **Tier 5** | Exam Speed Synthesizer | $\ge 85\%$ on mixed PYQs with $+4$/$-1$ scoring simulated under exam clock. | $\le 65$ seconds |

---

## 4. Remediation Loops

When a candidate fails an assessment gate:
1. **Sign Error / Calculation Slip:** The engine schedules a 5-minute procedural drill focusing purely on arithmetic accuracy.
2. **Formula Misapplication:** The engine returns the candidate to the Quick-Reference Formula Card and tests term-by-term derivation.
3. **Conceptual Misunderstanding:** The engine flags the module as `IN_PROGRESS` and redirects candidate to the worked examples and ASCII Venn diagrams before unlocking re-assessment.
4. **Time Pressure Rush:** The engine generates untimed variations of the same question template, allowing the candidate to establish procedural fluency before re-introducing countdown timers.
