# CUET SCQP09 Spaced Repetition & Revision Guide

**Artifact:** `CUET_SCQP09_FINAL/LEARNING_SYSTEM/revision_schedule.md`  
**Purpose:** Mathematical spacing model to guarantee long-term retention of 92 modules and 225 core patterns through the CUET-PG exam date.

---

## 1. The Forgetting Curve & The Need for Spaced Recall

Without active recall, human memory retention of mathematical formulas and algorithm steps decays according to Ebbinghaus's exponential model:
$$R(t) = e^{-\frac{t}{S}}$$
where $R$ is memory retention, $t$ is elapsed time, and $S$ is memory stability.

Attempting to "cram" all 92 modules in the final 3 weeks results in severe interference between similar formulas (e.g., confusing 2-set vs 3-set IEP terms, or QuickSort vs MergeSort recurrence relations). By introducing timed, expanding recall sessions, memory stability $S$ multiplies, flattening the decay curve.

---

## 2. Expanding Spaced Repetition Intervals

When a candidate achieves `MASTERED` status on any module, the engine schedules reviews according to the following cadence:

| Review Cycle | Interval | Focus of Review Session | Time Required |
|---|---|---|---|
| **R1 (Consolidation)** | **Day 1** (24 hrs later) | Review Formula Card; solve 3 rapid-fire Level 1–2 items. | 5 minutes |
| **R2 (Stabilization)** | **Day 3** (72 hrs later) | Solve 2 Level 3 procedural exercises without notes. | 5 minutes |
| **R3 (Reinforcement)** | **Day 7** (1 week later) | Solve 2 Level 4 statement/matching questions. | 5 minutes |
| **R4 (Integration)** | **Day 14** (2 weeks later) | Solve 1 timed Level 5 PYQ under $\le 72$ seconds. | 3 minutes |
| **R5 (Mastery Anchor)**| **Day 30** (1 month later) | Cumulative diagnostic drill mixed with adjacent tracks. | 5 minutes |
| **R6 (Pre-Exam Sprint)**| **Final 10 Days** | Flashcard formula verification + speed mock test. | 2 minutes |

---

## 3. Daily Revision Architecture (The 3-Block System)

To balance learning new topics while systematically reviewing older material, candidates should divide daily study time into three non-overlapping blocks:

```
+-------------------------------------------------------------------+
| BLOCK 1: Daily Habit (30 mins)                                    |
| Track 2: Thinking & Decision Making (TDM)                         |
| - 15 mins: Number/Letter Series or Direction Sense or Blood Rel.  |
| - 15 mins: Syllogisms or Seating Arrangement drill                |
+-------------------------------------------------------------------+
| BLOCK 2: Deep Core Study (90 mins)                                |
| Track 1 / Track 3 / Track 4 / Track 5                             |
| - Conceptual learning of 1 new module card                        |
| - Working step-by-step examples                                   |
| - Completing Tier A & Tier B progressive exercises                |
+-------------------------------------------------------------------+
| BLOCK 3: Spaced Repetition & Error Drill (30 mins)                |
| - Clear all modules currently flagged as [REVISION_DUE]           |
| - 5-question rapid diagnostic quiz                                |
| - Log any missteps into error log for targeted remediation        |
+-------------------------------------------------------------------+
```

---

## 4. 16-Week Mastery Roadmap

| Phase | Timeline | Core Modules Covered | Target Status |
|---|---|---|---|
| **Phase I: Foundations** | Weeks 1–4 | M1–M6, T1–T6, G1–G6, D1–D3, O1–O2 | 25 modules Mastered |
| **Phase II: Core Systems** | Weeks 5–8 | M7–M12, T7–T11, G7–G12, D4–D8, O3–O6 | 50 modules Mastered |
| **Phase III: Advanced Structures**| Weeks 9–12 | M13–M18, T12–T15, G13–G17, D9–D13, O7–O10 | 75 modules Mastered |
| **Phase IV: Capstone & Polish** | Weeks 13–15| M19–M22, T16–T17, D14–D17, O11–O16, R1–R3 | All 92 modules Mastered |
| **Phase V: Sprint Mocks** | Week 16 | Full 75-question timed mock papers (90 mins) | $\ge 99$th Percentile |
