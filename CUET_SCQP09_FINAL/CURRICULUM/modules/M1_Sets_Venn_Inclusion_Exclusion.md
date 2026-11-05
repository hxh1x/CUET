# Module M1: Sets, Venn Diagrams & Inclusion–Exclusion Principle

**Module Track:** Track 1 — Mathematics  
**Module ID:** `M1`  
**Priority Status:** Priority `P0` (Critical High-Yield Foundation)  
**Exam Appearances:** 5 Official NTA Questions (2024 Q26, 2025 Q17, 2025 Q19, 2026 Q21, 2026 Q39)  
**Target Speed:** $\le 72$ seconds per question  
**Language Specification:** Strictly English-Only  

---

## 1. Module Identity & Overview

Module M1 establishes the set-theoretic language and combinatorial cardinality rules that underpin probability theory, relational databases, formal logic, and Boolean switching algebra across the CUET-PG SCQP09 examination.

- **Domain:** Discrete Mathematics & Foundation Algebra
- **Exam Weightage:** 2–3 questions per paper directly; foundational prerequisite for an additional 8–10 questions in Probability (M3), Syllogisms (T14), and Logic Gates (G4/G5).
- **Core Invariant:** The Inclusion–Exclusion Principle (IEP) corrects for overlapping intersections to prevent multi-counting elements.

---

## 2. Prerequisites

- **Direct Prerequisites:** None (*Foundational Module 1*).
- **Subsequent Modules Dependent on M1:**
  - `M2` (Permutations & Combinations)
  - `M3` (Probability Theory & Bayes' Theorem)
  - `M7` (Functions, Domain & Range)
  - `T14` (Syllogisms & Categorical Logic)
  - `G4`–`G5` (Boolean Algebra & Logic Gates)
  - `D17` (Disjoint Set Union)

---

## 3. Learning Objectives

By the conclusion of this module, a candidate will be able to:
1. **Represent Sets:** Formulate arbitrary mathematical collections interchangeably in roster form, descriptive form, and set-builder notation.
2. **Execute Operations:** Compute unions ($A \cup B$), intersections ($A \cap B$), relative complements ($A \setminus B$), and symmetric differences ($A \Delta B$) for finite and infinite sets.
3. **Partition Venn Spaces:** Map verbal survey constraints into distinct, non-overlapping atomic Venn regions for 2-set and 3-set universes.
4. **Apply IEP for Two Sets:** Calculate cardinalities for union, intersection, "only one", and "neither" under strict 72-second speed constraints.
5. **Apply IEP for Three Sets:** Deconstruct complex 3-variable system constraints and solve for unknown boundary intersections using system equations.
6. **Apply De Morgan's Laws:** Transform complement expressions $(A \cup B)' = A' \cap B'$ and $(A \cap B)' = A' \cup B'$ to solve match-the-list and event-description exam problems.
7. **Discriminate Finite vs. Infinite Collections:** Evaluate infinite bounds and cardinality conditions without falling for distractor traps.

---

## 4. Required Prior Knowledge

Learners are expected to be familiar with:
- Standard number sets: Natural numbers $\mathbb{N} = \{1, 2, 3, \dots\}$, Whole numbers $\mathbb{W} = \{0, 1, 2, \dots\}$, Integers $\mathbb{Z} = \{\dots, -2, -1, 0, 1, 2, \dots\}$, Rational numbers $\mathbb{Q}$, and Real numbers $\mathbb{R}$.
- Basic linear algebraic solving: Solving single and two-variable linear equations.
- Elementary inequalities and interval notation: $[a, b]$, $(a, b)$, $[a, b)$.

---

## 5. Detailed Concept Explanations

### 5.1 Set Representation
A **set** is an unordered collection of distinct, well-defined objects called elements or members.
1. **Roster / Tabular Form:** Elements are explicitly enumerated within curly braces, separated by commas.
   - Example: $V = \{a, e, i, o, u\}$.
   - Invariant: Order does not matter ($\{1, 2\} = \{2, 1\}$), and duplicate elements are redundant ($\{1, 2, 2, 3\} = \{1, 2, 3\}$).
2. **Set-Builder Form:** Characterizes elements by a defining mathematical predicate $P(x)$.
   - Notation: $S = \{x \in U \mid P(x)\}$, read as "the set of all $x$ in universe $U$ such that property $P(x)$ holds true."
   - Example: $E = \{x \in \mathbb{N} \mid x \text{ is prime and } x < 10\} = \{2, 3, 5, 7\}$.

### 5.2 Set Classifications
- **Empty / Null Set ($\emptyset$ or $\{\}$):** The unique set containing zero elements. Cardinality $n(\emptyset) = 0$. Note: $\{\emptyset\}$ is NOT empty; it is a singleton containing the empty set.
- **Universal Set ($U$ or $\xi$):** The overarching contextual domain containing all possible objects under study.
- **Finite vs. Infinite Sets:** A set is finite if its cardinality can be equated to some non-negative integer $k \in \mathbb{W}$; otherwise it is infinite.
  - *Exam Signal (2025 Q19):* $\{x \in \mathbb{N} \mid x \text{ is prime and } x < 199\}$ is finite (bounded by 199), whereas $\{x \in \mathbb{N} \mid x > 5\}$ is infinite.
- **Subsets ($\subseteq$) and Proper Subsets ($\subset$):**
  - $A \subseteq B \iff (\forall x)(x \in A \implies x \in B)$.
  - $A \subset B \iff A \subseteq B \text{ and } A \neq B$.
  - Total subsets of set with $n$ elements: $2^n$.
  - Total proper subsets: $2^n - 1$.
  - Total non-empty proper subsets: $2^n - 2$.
- **Power Set ($\mathcal{P}(A)$):** The set containing all subsets of $A$.
  - If $n(A) = k$, then $n(\mathcal{P}(A)) = 2^k$.
  - If $A = \emptyset$, $\mathcal{P}(\emptyset) = \{\emptyset\}$, and $n(\mathcal{P}(\emptyset)) = 2^0 = 1$.

### 5.3 Fundamental Set Operations
- **Union ($A \cup B$):** Elements belonging to $A$, or $B$, or both.
  $$A \cup B = \{x \mid x \in A \text{ or } x \in B\}$$
- **Intersection ($A \cap B$):** Elements belonging simultaneously to both $A$ and $B$.
  $$A \cap B = \{x \mid x \in A \text{ and } x \in B\}$$
  - Two sets are **disjoint** or mutually exclusive if $A \cap B = \emptyset$.
- **Difference / Relative Complement ($A \setminus B$ or $A - B$):** Elements belonging to $A$ but strictly NOT belonging to $B$.
  $$A \setminus B = \{x \mid x \in A \text{ and } x \notin B\} = A \cap B'$$
- **Absolute Complement ($A'$ or $A^c$):** Elements of universal set $U$ not in $A$.
  $$A' = U \setminus A = \{x \in U \mid x \notin A\}$$
- **Symmetric Difference ($A \Delta B$):** Elements in exactly one of the sets.
  $$A \Delta B = (A \setminus B) \cup (B \setminus A) = (A \cup B) \setminus (A \cap B)$$

### 5.4 Algebraic Laws of Set Operations
1. **Identity Laws:** $A \cup \emptyset = A$, $A \cap U = A$.
2. **Domination / Annihilation Laws:** $A \cup U = U$, $A \cap \emptyset = \emptyset$.
3. **Idempotent Laws:** $A \cup A = A$, $A \cap A = A$.
4. **Involution Law:** $(A')' = A$.
5. **Commutative Laws:** $A \cup B = B \cup A$, $A \cap B = B \cap A$.
6. **Associative Laws:** $(A \cup B) \cup C = A \cup (B \cup C)$, $(A \cap B) \cap C = A \cap (B \cap C)$.
7. **Distributive Laws:**
   - $A \cup (B \cap C) = (A \cup B) \cap (A \cup C)$
   - $A \cap (B \cup C) = (A \cap B) \cup (A \cap C)$
8. **De Morgan's Laws:**
   - $(A \cup B)' = A' \cap B'$ (The complement of a union is the intersection of complements)
   - $(A \cap B)' = A' \cup B'$ (The complement of an intersection is the union of complements)
9. **Complement Laws:** $A \cup A' = U$, $A \cap A' = \emptyset$, $U' = \emptyset$, $\emptyset' = U$.

---

## 6. Terminology & Formal Definitions

- **Cardinality ($n(A)$ or $|A|$):** The number of unique elements in finite set $A$.
- **Atomic Venn Region:** A minimal, non-overlapping subset of the universe formed by the intersection of each set or its complement. For $k$ sets, the universe partitions into exactly $2^k$ disjoint atomic regions.
- **Inclusion–Exclusion Principle (IEP):** A theorem that expresses the cardinality of the union of multiple sets by adding the cardinalities of the individual sets, subtracting pairwise intersections, adding triple intersections, and so on alternating in signs.

---

## 7. Mathematical Foundations & Term-by-Term Formulas

### 7.1 Two-Set Cardinality Relations
Let $U$ be the universal set, and $A, B \subseteq U$:
1. **Union Cardinality:**
   $$n(A \cup B) = n(A) + n(B) - n(A \cap B)$$
   - *Explanation:* Adding $n(A)$ and $n(B)$ counts the shared overlap $n(A \cap B)$ twice. Subtracting $n(A \cap B)$ once yields the exact count.
2. **Rearranged Intersection Formula:**
   $$n(A \cap B) = n(A) + n(B) - n(A \cup B)$$
3. **Elements in Exactly One Set ("Only A or Only B"):**
   $$n(\text{Exactly One}) = n(A \setminus B) + n(B \setminus A) = n(A \cup B) - n(A \cap B) = n(A) + n(B) - 2n(A \cap B)$$
   - *Explanation:* $n(A) - n(A \cap B)$ is "Only A", $n(B) - n(A \cap B)$ is "Only B". Summing them gives the result.
4. **Neither Set:**
   $$n(\text{Neither } A \text{ nor } B) = n((A \cup B)') = n(U) - n(A \cup B) = n(U) - [n(A) + n(B) - n(A \cap B)]$$

### 7.2 Three-Set Cardinality Relations
Let $A, B, C \subseteq U$:
1. **Three-Set Union IEP Formula:**
   $$n(A \cup B \cup C) = [n(A) + n(B) + n(C)] - [n(A \cap B) + n(B \cap C) + n(C \cap A)] + n(A \cap B \cap C)$$
   - *Explanation:*
     - Single sets sum elements belonging to 1 region once, 2 regions twice, and 3 regions thrice ($+1, +2, +3$).
     - Pairwise intersections subtract 2-region elements once and 3-region elements thrice ($-0, -1, -3$).
     - Net count before final term: 1-region ($1$), 2-region ($2-1=1$), 3-region ($3-3=0$).
     - The central region $n(A \cap B \cap C)$ was reduced to 0! Adding $+n(A \cap B \cap C)$ restores it to exactly 1.
2. **Sum of Pairwise Intersections:**
   $$\sum n(A \cap B) = n(A \cap B) + n(B \cap C) + n(C \cap A)$$
3. **Elements in Exactly One Set:**
   $$n(\text{Exactly One}) = [n(A) + n(B) + n(C)] - 2[n(A \cap B) + n(B \cap C) + n(C \cap A)] + 3n(A \cap B \cap C)$$
4. **Elements in Exactly Two Sets:**
   $$n(\text{Exactly Two}) = [n(A \cap B) + n(B \cap C) + n(C \cap A)] - 3n(A \cap B \cap C)$$
5. **Elements in At Least Two Sets:**
   $$n(\text{At Least Two}) = [n(A \cap B) + n(B \cap C) + n(C \cap A)] - 2n(A \cap B \cap C)$$

---

## 8. Visual Explanations (ASCII Venn Diagrams)

### Two-Set Partition: 4 Mutually Exclusive Atomic Regions
```
+-------------------------------------------------------------+
| Universal Set U                                             |
|                                                             |
|           Set A                           Set B             |
|       /-----------\                   /-----------\         |
|      /             \                 /             \        |
|     /    Region I   \   Region II   /   Region III  \       |
|    |     Only A      |   A and B   |     Only B      |      |
|    |  n(A) - n(AnB)  |   n(A n B)  |  n(B) - n(AnB)  |      |
|     \               /               \               /       |
|      \             /                 \             /        |
|       \-----------/                   \-----------/         |
|                                                             |
|                         Region IV                           |
|                    Neither A nor B:                         |
|                    n(U) - n(A u B)                          |
+-------------------------------------------------------------+
```

### Three-Set Partition: 8 Mutually Exclusive Atomic Regions
```
+-------------------------------------------------------------+
| Universal Set U                                             |
|                     /-----------------\                     |
|                    /      Set A        \                    |
|                   /       Region 1      \                   |
|                  |        (Only A)       |                  |
|                 / \                     / \                 |
|                /   \     Region 4      /   \                |
|               /     \   (A n B only)  /     \               |
|              / Set B \---------------/ Set C \              |
|             / Region 2 \  Region 7  / Region 3\             |
|            |  (Only B)  | (AnBnC)   | (Only C) |            |
|            |            |           |          |            |
|             \          / \         /          /             |
|              \ Region 5   \       / Region 6 /              |
|               \(BnC only)  \-----/ (AnC only)               |
|                \-----------------------------/              |
|                                                             |
|                    Region 8: None of A, B, C                |
|                    n(U) - n(A u B u C)                      |
+-------------------------------------------------------------+
```

---

## 9. Worked Examples (Step-by-Step with Full Computations)

### Example 1: Two-Set Inclusion–Exclusion & "Exactly One" [SOURCE: 2024 Q26 / DERIVED]
**Problem Statement:**  
There are 200 students in a school out of which 120 students play football, 50 students play cricket, and 30 students play both football and cricket. Find the number of students who play **one game only**.

**Step-by-Step Solution:**
1. *Identify given parameters:*
   - Universal set $n(U) = 200$
   - Students playing Football $n(F) = 120$
   - Students playing Cricket $n(C) = 50$
   - Students playing both $n(F \cap C) = 30$
2. *Decompose into mutually exclusive atomic regions:*
   - Students playing **Football only**:
     $$n(\text{Only } F) = n(F) - n(F \cap C) = 120 - 30 = 90$$
   - Students playing **Cricket only**:
     $$n(\text{Only } C) = n(C) - n(F \cap C) = 50 - 30 = 20$$
3. *Compute "one game only":*
   $$n(\text{One game only}) = n(\text{Only } F) + n(\text{Only } C) = 90 + 20 = 110$$
4. *Alternative algebraic verification via IEP:*
   $$n(F \cup C) = n(F) + n(C) - n(F \cap C) = 120 + 50 - 30 = 140$$
   $$n(\text{One game only}) = n(F \cup C) - n(F \cap C) = 140 - 30 = 110$$
5. *Check total universe:*
   - Students playing neither sport: $n(U) - n(F \cup C) = 200 - 140 = 60$.
   - Total sum check: $90 (\text{only } F) + 20 (\text{only } C) + 30 (\text{both}) + 60 (\text{neither}) = 200$. **Verified.**

**Final Answer:** **110** (Option 1 in 2024 paper).

---

### Example 2: Three-Set Missing Region & "Neither" [SOURCE: 2026 Q21 / DERIVED]
**Problem Statement:**  
In a university of 100 students:
- 15 offered Mathematics only;
- 12 offered Statistics only;
- 8 offered Physics only;
- 40 offered Physics and Mathematics;
- 20 offered Physics and Statistics;
- 10 offered Mathematics and Statistics;
- 65 offered Physics.

What is the number of students who did not offer any of the three subjects?

**Step-by-Step Solution:**
1. *Define sets and variables:*
   - Let $M$, $S$, $P$ denote Mathematics, Statistics, and Physics students.
   - Total students $n(U) = 100$.
   - $n(\text{Only } M) = 15$
   - $n(\text{Only } S) = 12$
   - $n(\text{Only } P) = 8$
   - Pairwise totals: $n(P \cap M) = 40$, $n(P \cap S) = 20$, $n(M \cap S) = 10$.
   - Total in Physics $n(P) = 65$.
2. *Deconstruct the central triple intersection:*
   - Let $x = n(M \cap S \cap P)$ (students taking all three subjects).
   - In terms of $x$, the pairwise *exclusive* regions are:
     - Physics and Mathematics *only* $= n(P \cap M) - x = 40 - x$
     - Physics and Statistics *only* $= n(P \cap S) - x = 20 - x$
     - Mathematics and Statistics *only* $= n(M \cap S) - x = 10 - x$
3. *Formulate equation for set $P$:*
   Set $P$ consists of 4 disjoint regions: (Only $P$) + ($P \cap M$ only) + ($P \cap S$ only) + ($M \cap S \cap P$).
   $$n(P) = 8 + (40 - x) + (20 - x) + x = 65$$
   $$68 - x = 65 \implies x = 3$$
   Therefore, exactly **3** students offered all three subjects.
4. *Calculate all 7 non-empty disjoint regions:*
   - Only $M = 15$
   - Only $S = 12$
   - Only $P = 8$
   - $P \cap M$ only $= 40 - 3 = 37$
   - $P \cap S$ only $= 20 - 3 = 17$
   - $M \cap S$ only $= 10 - 3 = 7$
   - All three $= 3$
5. *Compute total offering at least one subject $n(M \cup S \cup P)$:*
   $$n(M \cup S \cup P) = 15 + 12 + 8 + 37 + 17 + 7 + 3 = 99$$
6. *Calculate students offering neither subject:*
   $$n(\text{None}) = n(U) - n(M \cup S \cup P) = 100 - 99 = 1$$

**Final Answer:** **1** student offered none of the three subjects.

---

### Example 3: Match Event Description to Set-Theoretic Notation [SOURCE: 2026 Q39 / DERIVED]
**Problem Statement:**  
Match the verbal description of events in List-I with the corresponding set-theoretic notation in List-II:

| List-I (Event Description) | List-II (Set Notation) |
|---|---|
| (A) Neither $A$ nor $B$ | (I) $(A \cap B') \cup (A' \cap B)$ |
| (B) At least one of $A, B$, or $C$ | (II) $A' \cap B'$ |
| (C) Exactly one of $A$ and $B$ | (III) $A \cup B \cup C$ |
| (D) All three of $A, B$, and $C$ | (IV) $A \cap B \cap C$ |

**Step-by-Step Solution:**
1. *(A) "Neither $A$ nor $B$":*
   - By definition, an element is not in $A$ AND not in $B$.
   - Symbolically: $x \in A'$ and $x \in B' \iff x \in A' \cap B'$.
   - By De Morgan's Law: $A' \cap B' = (A \cup B)'$. Matches with **(II)**.
2. *(B) "At least one of $A, B$, or $C$":*
   - Belonging to at least one set is the formal definition of the set union: $A \cup B \cup C$. Matches with **(III)**.
3. *(C) "Exactly one of $A$ and $B$":*
   - Belongs to $A$ but not $B$ ($A \cap B'$), OR belongs to $B$ but not $A$ ($B \cap A'$).
   - Symbolically: $(A \cap B') \cup (A' \cap B)$. Matches with **(I)**.
4. *(D) "All three of $A, B$, and $C$":*
   - Belongs to $A$ AND $B$ AND $C$: $A \cap B \cap C$. Matches with **(IV)**.

**Final Matching Code:** **(A)-(II), (B)-(III), (C)-(I), (D)-(IV)**.

---

## 10. Common Misconceptions

1. **Misconception: $n(A \cup B) = n(A) + n(B)$ always.**  
   *Reality:* This equation only holds if sets $A$ and $B$ are strictly disjoint ($A \cap B = \emptyset$). If they overlap, adding them counts the common elements twice.
2. **Misconception: The complement of an intersection is the intersection of complements ($(A \cap B)' = A' \cap B'$).**  
   *Reality:* De Morgan's Law reverses the operator: $(A \cap B)' = A' \cup B'$. "Not both" means you are outside at least one of them.
3. **Misconception: "At least one" is the same as "Exactly one".**  
   *Reality:* "At least one" is the entire union ($A \cup B$), which includes elements that belong to both. "Exactly one" is the symmetric difference ($A \Delta B$), which explicitly removes the intersection.
4. **Misconception: $\{\emptyset\}$ is the empty set.**  
   *Reality:* $\emptyset$ has cardinality 0. $\{\emptyset\}$ is a set containing one element (the empty set itself), so $n(\{\emptyset\}) = 1$.

---

## 11. Common Mistakes & Exam Pitfalls

1. **Confusing "Pairwise Given" with "Pairwise Exclusive":**  
   When an NTA problem states "40 offered Physics and Math", this is $n(P \cap M)$, which includes students taking all three subjects! It is NOT the "Physics and Math only" region. To find the exclusive region, you MUST subtract the triple intersection $x$.
2. **Double Subtracting the Intersection in "Only One":**  
   Students often write $n(\text{Only } A \text{ or Only } B) = n(A) + n(B) - n(A \cap B)$. This is wrong; that formula is $n(A \cup B)$. For "Only one", you must subtract $2n(A \cap B)$.
3. **Sign Errors in 3-Set Inclusion–Exclusion:**  
   Students frequently forget that the signs alternate: $+ \text{singles} - \text{pairs} + \text{triples}$. Forgetting to add the triple intersection back at the end will corrupt the entire survey count.

---

## 12. Progressive Exercises (12 Structured Drills)

### Tier A: Basic Competence (Level 1–2)
1. **[SUPPLEMENTARY]** Let $A = \{x \in \mathbb{N} \mid x \text{ divides } 24\}$ and $B = \{x \in \mathbb{N} \mid x \text{ divides } 36\}$. Find $n(A \cap B)$.  
   *Answer:* Divisors of 24: $\{1, 2, 3, 4, 6, 8, 12, 24\}$. Divisors of 36: $\{1, 2, 3, 4, 6, 9, 12, 18, 36\}$. Common divisors: $\{1, 2, 3, 4, 6, 12\}$. Cardinality $= 6$.
2. **[SUPPLEMENTARY]** If $n(A) = 25$, $n(B) = 35$, and $n(A \cup B) = 45$, compute $n(A \cap B)$.  
   *Answer:* $n(A \cap B) = 25 + 35 - 45 = 15$.
3. **[SUPPLEMENTARY]** Set $S$ has 6 elements. Determine the number of proper subsets of $S$.  
   *Answer:* Total subsets $= 2^6 = 64$. Proper subsets $= 64 - 1 = 63$.
4. **[SUPPLEMENTARY]** Simplify $[(A \cup B)' \cup (A' \cap B)]'$.  
   *Answer:* By De Morgan's: $(A \cup B)' = A' \cap B'$. Then $(A' \cap B') \cup (A' \cap B) = A' \cap (B' \cup B) = A' \cap U = A'$. Taking the outer complement: $(A')' = A$.

### Tier B: Standard Exam Level (Level 3)
5. **[DERIVED]** In a cohort of 150 computer science applicants, 85 know Python, 60 know Java, and 35 know both languages. How many applicants know neither Python nor Java?  
   *Answer:* $n(P \cup J) = 85 + 60 - 35 = 110$. Applicants knowing neither $= 150 - 110 = 40$.
6. **[DERIVED]** In a class of 60 students, 30 play badminton, 25 play table tennis, and 12 play both games. Find the number of students who play exactly one game.  
   *Answer:* $n(\text{Only B}) = 30 - 12 = 18$. $n(\text{Only TT}) = 25 - 12 = 13$. Exactly one $= 18 + 13 = 31$.
7. **[DERIVED]** If $n(U) = 1000$, $n(A) = 400$, $n(B) = 500$, and $n(A \cap B) = 150$, find $n(A' \cap B')$.  
   *Answer:* By De Morgan's, $A' \cap B' = (A \cup B)'$. $n(A \cup B) = 400 + 500 - 150 = 750$. $n((A \cup B)') = 1000 - 750 = 250$.
8. **[DERIVED]** If $A$ and $B$ are two sets such that $n(A \setminus B) = 24$, $n(B \setminus A) = 19$, and $n(A \cap B) = 11$, find $n(A)$ and $n(B)$.  
   *Answer:* $n(A) = n(A \setminus B) + n(A \cap B) = 24 + 11 = 35$. $n(B) = n(B \setminus A) + n(A \cap B) = 19 + 11 = 30$.

### Tier C: Advanced Synthesis (Level 4–5)
9. **[DERIVED]** In an inspection of 120 faulty microchips, 48 had solder faults, 52 had trace faults, and 45 had component defects. 18 had both solder and trace faults, 15 had trace and component faults, and 20 had solder and component faults. If 8 microchips had all three defects, how many had exactly two defects?  
   *Answer:* $n(\text{Exactly Two}) = [n(S \cap T) + n(T \cap C) + n(S \cap C)] - 3n(S \cap T \cap C) = [18 + 15 + 20] - 3(8) = 53 - 24 = 29$.
10. **[DERIVED]** For the same microchip cohort in Exercise 9, how many microchips had exactly one defect?  
    *Answer:* $n(\text{Exactly One}) = [48 + 52 + 45] - 2[18 + 15 + 20] + 3(8) = 145 - 2(53) + 24 = 145 - 106 + 24 = 63$.
11. **[DERIVED]** A survey of 100 students revealed: 28 read Book A, 30 read Book B, 42 read Book C, 8 read A and B, 10 read A and C, 5 read B and C, and 3 read all three. Determine how many students read none of the books.  
    *Answer:* $n(A \cup B \cup C) = (28 + 30 + 42) - (8 + 10 + 5) + 3 = 100 - 23 + 3 = 80$. Students who read none $= 100 - 80 = 20$.
12. **[DERIVED]** If $n(A) = 70$, $n(B) = 60$, and universal set $n(U) = 100$, what is the minimum possible value of $n(A \cap B)$?  
    *Answer:* $n(A \cup B) \le n(U) \implies n(A) + n(B) - n(A \cap B) \le 100 \implies 70 + 60 - n(A \cap B) \le 100 \implies 130 - 100 \le n(A \cap B) \implies n(A \cap B) \ge 30$. Minimum value $= 30$.

---

## 13. Practical Assignment: University Course Enrollment Survey

**Scenario:**  
The Department of Computer Science surveyed 500 first-year postgraduate students regarding registration for three elective modules:
- Module A: Machine Learning
- Module B: Distributed Cloud Systems
- Module C: Cryptography & Network Security

The survey produced the following raw telemetry:
- 230 students registered for Module A
- 210 students registered for Module B
- 220 students registered for Module C
- 90 registered for both A and B
- 80 registered for both B and C
- 100 registered for both A and C
- 40 registered for all three electives

**Required Candidate Deliverables:**
1. Compute the number of students taking **Module A only**.
   - *Computation:* $n(\text{Only } A) = n(A) - n(A \cap B) - n(A \cap C) + n(A \cap B \cap C) = 230 - 90 - 100 + 40 = 80$.
2. Compute the number of students taking **exactly two electives**.
   - *Computation:* $[(90 - 40) + (80 - 40) + (100 - 40)] = 50 + 40 + 60 = 150$.
3. Compute the number of students taking **at least one elective**.
   - *Computation:* $n(A \cup B \cup C) = (230 + 210 + 220) - (90 + 80 + 100) + 40 = 660 - 270 + 40 = 430$.
4. Determine the number of students who registered for **no electives**.
   - *Computation:* $n(U) - n(A \cup B \cup C) = 500 - 430 = 70$.

---

## 14. Knowledge-Check Questions (5 MCQs with Explanations)

### MCQ 1 [Level 1 Recall]
Let $S = \{x \in \mathbb{R} \mid x^2 + 1 = 0\}$. The set $S$ is:  
(1) An infinite set  
(2) A singleton set  
(3) An empty set  
(4) A universal set  
- **Correct Answer:** (3)  
- **Explanation:** For any real number $x \in \mathbb{R}$, $x^2 \ge 0$, so $x^2 + 1 \ge 1 > 0$. There are no real solutions to $x^2 + 1 = 0$. Hence $S = \emptyset$.

### MCQ 2 [Level 2 Representation]
If $X$ and $Y$ are any two sets, then $X \cap (X \cup Y)'$ equals:  
(1) $X$  
(2) $Y$  
(3) $\emptyset$  
(4) $X \cap Y$  
- **Correct Answer:** (3)  
- **Explanation:** By De Morgan's Law, $(X \cup Y)' = X' \cap Y'$. Thus $X \cap (X' \cap Y') = (X \cap X') \cap Y'$. Since $X \cap X' = \emptyset$, $\emptyset \cap Y' = \emptyset$.

### MCQ 3 [Level 3 Procedural Execution]
In a class of 80 students, 45 like Mathematics and 35 like Computer Science. If 15 like neither, how many like both subjects?  
(1) 15  
(2) 20  
(3) 25  
(4) 10  
- **Correct Answer:** (1)  
- **Explanation:** Students who like at least one $= n(U) - n(\text{neither}) = 80 - 15 = 65$. Then $n(M \cap CS) = n(M) + n(CS) - n(M \cup CS) = 45 + 35 - 65 = 80 - 65 = 15$.

### MCQ 4 [Level 4 Analytical Discrimination]
Which of the following identities is FALSE for arbitrary sets $A, B, C$?  
(1) $A \setminus (B \cup C) = (A \setminus B) \cap (A \setminus C)$  
(2) $A \setminus (B \cap C) = (A \setminus B) \cup (A \setminus C)$  
(3) $A \cup (B \cap C) = (A \cup B) \cap (A \cup C)$  
(4) $(A \setminus B) \setminus C = A \setminus (B \setminus C)$  
- **Correct Answer:** (4)  
- **Explanation:** Set difference is NOT associative. Let $A = \{1, 2\}$, $B = \{2\}$, $C = \{2\}$. Left side: $(A \setminus B) \setminus C = \{1\} \setminus \{2\} = \{1\}$. Right side: $B \setminus C = \emptyset$, so $A \setminus \emptyset = \{1, 2\} \neq \{1\}$.

### MCQ 5 [Level 5 Speed Synthesis]
If set $A$ has $m$ elements and set $B$ has $n$ elements ($m > n$), and the total number of subsets of $A$ is 112 more than the total number of subsets of $B$, what are the values of $m$ and $n$?  
(1) $m = 7, n = 4$  
(2) $m = 8, n = 5$  
(3) $m = 6, n = 3$  
(4) $m = 7, n = 5$  
- **Correct Answer:** (1)  
- **Explanation:** The number of subsets are $2^m$ and $2^n$. We have $2^m - 2^n = 112$. Factor out $2^n$: $2^n(2^{m-n} - 1) = 112$. Prime factorizing 112 gives $16 \times 7 = 2^4 \times 7$. Thus $2^n = 2^4 \implies n = 4$, and $2^{m-n} - 1 = 7 \implies 2^{m-4} = 8 = 2^3 \implies m - 4 = 3 \implies m = 7$.

---

## 15. Independent Mastery Assessment (10 Exam-Level Questions)

1. **[Q1]** If $A = \{x \in \mathbb{N} \mid x \text{ is a multiple of 3, } x \le 30\}$ and $B = \{x \in \mathbb{N} \mid x \text{ is a multiple of 4, } x \le 30\}$, find $n(A \Delta B)$.  
   *(Answer: $n(A) = 10, n(B) = 7, A \cap B = \{12, 24\} \implies n(A \cap B) = 2$. $n(A \Delta B) = 10 + 7 - 2(2) = 13$.)*
2. **[Q2]** For any two non-empty sets $A$ and $B$, $(A \setminus B) \cup (B \setminus A) \cup (A \cap B)$ simplifies to:  
   *(Answer: $A \cup B$. The three parts form a disjoint partition of the union.)*
3. **[Q3]** In a group of 70 people, 37 like coffee, 52 like tea, and each person likes at least one of the two drinks. How many people like both coffee and tea?  
   *(Answer: $n(C \cap T) = 37 + 52 - 70 = 19$.)*
4. **[Q4]** Let $n(U) = 700, n(A) = 200, n(B) = 300$, and $n(A \cap B) = 100$. Find $n(A' \cap B)$.  
   *(Answer: $n(A' \cap B) = n(B \setminus A) = n(B) - n(A \cap B) = 300 - 100 = 200$.)*
5. **[Q5]** In an examination, 80% of candidates passed in English, 70% in Mathematics, and 10% failed in both subjects. If 360 candidates passed in both, find the total number of candidates.  
   *(Answer: Passed at least one $= 100\% - 10\% = 90\%$. $\%$ passing both $= 80\% + 70\% - 90\% = 60\%$. If $0.60 N = 360$, then $N = 360 / 0.60 = 600$.)*
6. **[Q6]** A set contains $k$ elements. If adding one element to the set doubles the number of subsets, what happens to the number of proper subsets?  
   *(Answer: The number of proper subsets changes from $2^k - 1$ to $2^{k+1} - 1 = 2(2^k - 1) + 1$.)*
7. **[Q7]** Given three sets $A, B, C$ such that $n(A) = 20, n(B) = 25, n(C) = 30$, $n(A \cap B) = 10, n(B \cap C) = 8, n(A \cap C) = 7$, and $n(A \cap B \cap C) = 3$. Find $n(A \cup B \cup C)$.  
   *(Answer: $(20 + 25 + 30) - (10 + 8 + 7) + 3 = 75 - 25 + 3 = 53$.)*
8. **[Q8]** In the above problem, how many elements belong to **exactly one** of the sets?  
   *(Answer: $75 - 2(25) + 3(3) = 75 - 50 + 9 = 34$.)*
9. **[Q9]** If $P(A)$ denotes the power set of $A$, and $A = \{1, 2\}$, determine $n(\mathcal{P}(\mathcal{P}(A)))$.  
   *(Answer: $n(A) = 2 \implies n(\mathcal{P}(A)) = 2^2 = 4 \implies n(\mathcal{P}(\mathcal{P}(A))) = 2^4 = 16$.)*
10. **[Q10]** Which of the following collections is not a well-defined set?  
    (A) The set of all prime numbers less than $10^{12}$  
    (B) The set of difficult problems in this textbook  
    (C) The set of all vowels in the English alphabet  
    (D) The set of roots of $x^3 - x = 0$  
    *(Answer: (B). "Difficult" is subjective and not mathematically well-defined.)*

---

## 16. Assessment Rubric & Mastery Criteria

| Mastery Tier | Score Target | Time Benchmark | Qualitative Competence Demonstrated |
|---|---|---|---|
| **NOVICE** | $< 60\%$ (0–5 / 10) | $> 120$ sec / item | Fails on basic set difference or forgets to subtract intersections. |
| **PRACTICING**| $60\%–79\%$ (6–7 / 10) | $80–120$ sec / item | Solves 2-set IEP correctly; stumbles on 3-set system algebra. |
| **COMPETENT** | $80\%–89\%$ (8 / 10) | $60–80$ sec / item | Accurately solves both 2-set and 3-set problems with minimal scratchwork. |
| **EXAM READY**| $\ge 90\%$ (9–10 / 10)| $\le 72$ sec / item | Effortless mastery of De Morgan's laws, Venn region equations, and NTA traps. |

---

## 17. Revision Material: Quick-Reference Formula Card

```
================================================================================
                    CUET-PG SCQP09 :: MODULE M1 CHEAT SHEET
================================================================================
1. POWER SET CARDINALITY:
   |P(A)| = 2^n,   Proper Subsets = 2^n - 1,   Non-empty Proper = 2^n - 2

2. TWO-SET INCLUSION-EXCLUSION:
   n(A u B)          = n(A) + n(B) - n(A n B)
   n(A n B)          = n(A) + n(B) - n(A u B)
   n(Only A)         = n(A) - n(A n B)
   n(Exactly One)    = n(A u B) - n(A n B) = n(A) + n(B) - 2*n(A n B)
   n(Neither)        = n(U) - n(A u B)

3. THREE-SET INCLUSION-EXCLUSION:
   n(A u B u C)      = Sum[n(A)] - Sum[n(A n B)] + n(A n B n C)
   n(Exactly Two)    = Sum[n(A n B)] - 3*n(A n B n C)
   n(At Least Two)   = Sum[n(A n B)] - 2*n(A n B n C)
   n(Exactly One)    = Sum[n(A)] - 2*Sum[n(A n B)] + 3*n(A n B n C)

4. DE MORGAN'S LAWS:
   (A u B)' = A' n B'
   (A n B)' = A' u B'

5. EXAM SPEED HEURISTIC:
   In 3-set word problems, ALWAYS label the central triple intersection x first.
   Express all double-intersections as (Given - x).
================================================================================
```

---

## 18. Source References

1. **[SOURCE] 2024 Shift 3, Question 26:** 200 students school survey (120 football, 50 cricket, 30 both → exactly one game $= 110$).
2. **[SOURCE] 2025 Shift 2, Question 17:** Match List-I with List-II: Cardinality identities for union, intersection, and power sets.
3. **[SOURCE] 2025 Shift 2, Question 19:** Set-builder representations and identification of infinite sets.
4. **[SOURCE] 2026 Shift 2, Question 21:** 3-set university subject survey (100 students, Math, Stats, Physics → students offering none $= 1$).
5. **[SOURCE] 2026 Shift 2, Question 39:** Event description matching with set-theoretic notation.

---

## 19. Source Category Labels

- `[SOURCE]`: Official NTA exam questions and verbatim problem parameters extracted from 2024, 2025, and 2026 examination papers.
- `[DERIVED]`: Step-by-step mathematical solutions, derivations, proofs, and computed regional counts verified by algebraic evaluation.
- `[SUPPLEMENTARY]`: Foundational theory, illustrative diagrams, diagnostic misconceptions, and progressive practice exercises authored to complete syllabus mastery.
