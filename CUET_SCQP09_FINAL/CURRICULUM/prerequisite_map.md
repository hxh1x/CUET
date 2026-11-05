# CUET SCQP09 Module Prerequisite & Dependency Map

**Artifact:** `CUET_SCQP09_FINAL/CURRICULUM/prerequisite_map.md`  
**Purpose:** Defines the strict prerequisite hierarchy, progression pathways, and cross-domain knowledge bridges across the 92 modules of CUET-PG SCQP09.

---

## 1. Global Learning Architecture & Domain Progression

The curriculum is structured around four interconnected knowledge tiers:
1. **Foundational Toolkits (Tier 1):** Unlocks mathematical thinking and discrete symbol manipulation (Sets M1, Indices/Logs M5, Number Systems G1-G3).
2. **Structural Core (Tier 2):** Linear data structures, matrices, counting, and logic minimization (M2, M6, M9, G4-G6, D1-D3, T1-T6).
3. **Algorithmic & System Mechanics (Tier 3):** Non-linear structures, calculus, sequential circuits, OS scheduling, and concurrency (M17-M22, D4-D13, G11-G14, O1-O5).
4. **Integration & Advanced Reasoning (Tier 4):** Virtual memory, dynamic programming, formal deduction, and full exam-speed mock synthesis (O6-O8, D14-D17, T14-T17, R1-R3).

---

## 2. Track Dependency Specifications

### 2.1 Track 1: Mathematics
```
M1 (Sets & Venn) ──────────────► M2 (Permutations & Combinations) ──► M3 (Probability) ──► M4 (Statistics)
 │
 ├──► M5 (Logarithms) ──────────► M6 (Quadratics & Inequalities) ────► M7 (Functions & Range) ──► M8 (Sequences & Series)
 │                                                                       │
 └──► M9 (Matrix Algebra) ──────► M10 (Determinants & Linear Systems)    │
                                                                         ▼
 M11 (Straight Lines) ──────────► M12 (Circles) ──────────────────────► M13 (Parabola) ──► M14 (Conics) ──► M15-M16 (Conic Props)
                                                                         │
                                                                         ▼
                                                                 M17 (Limits) ──────────► M18 (Continuity) ──► M19-M20 (Derivatives)
                                                                                                                   │
                                                                                                                   ▼
                                                                                                           M21-M22 (Integration & Area)
```

| Target Module | Direct Prerequisites | Rationale & Concepts Required |
|---|---|---|
| **M1: Sets & Venn** | *None* | Root foundational module; establishes union, intersection, set complement, and universal sets. |
| **M2: Permutations** | M1 | Relies on set partitioning, disjoint sets, and fundamental counting principles. |
| **M3: Probability** | M1, M2 | Sample spaces are sets; event spaces require $nCr$ and $nPr$ combinations and partitions. |
| **M4: Statistics** | M3 | Probability distributions, expectation, variance, and standard deviation calculations. |
| **M6: Quadratics & Inequalities** | M5 | Requires index laws, algebraic manipulation, and logarithmic transformations. |
| **M7: Functions & Range** | M1, M6 | Functions are relations between sets; domain/range requires solving quadratic inequalities. |
| **M8: Progressions (AP/GP)** | M5, M6 | Sequences require solving index equations and quadratic relations for common ratios. |
| **M10: Determinants & Systems** | M9 | Determinants, matrix inverses, and Cramer's Rule build upon basic matrix operations. |
| **M12-M16: Coordinate Conics**| M11 | Tangents, normals, intersections, and radii build upon slope-intercept line geometry. |
| **M17-M18: Limits & Continuity**| M7 | Limits evaluate behaviour of functions as $x \to a$; continuity tests function definitions. |
| **M19-M20: Differentiation** | M17, M18| Derivative is defined as $\lim_{h \to 0} [f(x+h)-f(x)]/h$. |
| **M21-M22: Integration & Area** | M19, M20| Anti-differentiation relies on reverse derivative rules; area requires definite integrals. |

---

### 2.2 Track 2: Thinking & Decision Making (TDM)
TDM operates on an independent daily habit track with lightweight internal hierarchies:
- **T1 (Number Series) & T2 (Letter Series):** Foundation for all symbol-manipulation questions.
- **T3 (Direction Sense) & T4 (Ranking/Order):** Coordinate and comparative spatial reasoning.
- **T5 (Word Analogy) & T6 (Number Analogy):** Semantic classification and mathematical relations.
- **T7 (Blood Relations) & T8 (Seating Arrangements):** Multi-constraint relational networks.
- **T9 (Coding-Decoding):** Shift cipher and mapping mechanics.
- **T14 (Syllogisms) & T15-T17 (Deductive / Critical Reasoning):** Formal logic requiring set-Euler diagram thinking (connected to M1).

---

### 2.3 Track 3: Digital Fundamentals
```
G1 (Number Systems) ──► G2 (Signed/Complements) ──► G3 (Floating-Point)
 │
 └──► G4 (Logic Gates) ──► G5 (Boolean Algebra) ──► G6 (Karnaugh Maps)
                             │
                             ├──► G7-G10 (Combinational: Adders, MUX, Decoders)
                             │       │
                             │       ▼
                             └──► G11-G14 (Sequential: Flip-Flops, Counters, Registers)
                                     │
                                     ▼
                                  G15-G17 (Memory, Buses, CPU Organization)
```

| Target Module | Direct Prerequisites | Rationale & Concepts Required |
|---|---|---|
| **G1: Number Systems** | *None* | Root of digital computation (binary, octal, hex, decimal bases). |
| **G2: Complements** | G1 | 1's and 2's complement representations of signed binary integers. |
| **G4: Logic Gates** | G1 | Fundamental binary gate primitives (AND, OR, NOT, NAND, NOR, XOR). |
| **G5: Boolean Algebra** | G4, M1 | Boolean algebra axioms reflect set union/intersection laws (De Morgan's). |
| **G6: K-Maps** | G5 | SOP / POS minimization using Gray codes and adjacency grouping. |
| **G7-G10: Combinational** | G5, G6 | Implementation of adders, MUX, and decoders using minimized gate networks. |
| **G11-G14: Sequential** | G4, G7 | Clocked memory elements (SR, JK, D, T flip-flops, state excitation tables). |
| **G15-G17: Organization** | G2, G8, G13| Register transfer, ALU busses, control units, and RAM/ROM address decoding. |

---

### 2.4 Track 4: Data Structures & Algorithms
```
D1 (Arrays) ──────────► D2 (Linked Lists) ──► D3 (Stacks & Queues)
 │                       │                     │
 ├──► D8 (Complexity) ───┼─────────────────────┼──► D9 (Sorting & Searching)
 │                       │                     │
 └──► D4 (Binary Trees) ─┴─────────────────────┴──► D5 (BST & AVL) ──► D6 (Heaps)
        │
        ▼
      D10 (Graphs: BFS/DFS) ──► D11-D13 (MST & Shortest Paths) ──► D14-D17 (DP & Advanced)
```

| Target Module | Direct Prerequisites | Rationale & Concepts Required |
|---|---|---|
| **D1: Arrays** | *None* | Contiguous memory allocation, random indexing, address calculation. |
| **D2: Linked Lists** | D1 | Dynamic pointer node allocation vs contiguous arrays; pointer manipulation. |
| **D3: Stacks & Queues**| D1, D2 | LIFO and FIFO abstraction implemented over arrays and linked lists. |
| **D4: Binary Trees** | D2, D3 | Recursive node structures, tree traversals (pre/in/post/level-order via queue).|
| **D5: BST & AVL** | D4 | Ordered tree invariant, balanced tree rotations, search complexity. |
| **D6: Heaps** | D1, D4 | Complete binary tree representation in contiguous array; priority queues. |
| **D8: Asymptotics** | M5, M8 | Big-O, Theta, Omega bounds; recurrence relations using log properties. |
| **D9: Sorting** | D1, D8 | Quicksort, mergesort, heapsort, bubble/insertion/selection analysis. |
| **D10: Graphs** | D1, D2, D3 | Adjacency matrix/list representation; BFS (queue) and DFS (stack/recursion).|
| **D11-D13: Greedy/Paths**| D6, D10 | Dijkstra, Prim, Kruskal using priority queues over graph representations. |
| **D14-D15: DP & Divide**| D8 | Optimal substructure, overlapping subproblems, memoization vs iteration. |

---

### 2.5 Track 5: Operating Systems
```
O1 (OS Concepts & Processes) ──► O2 (CPU Scheduling)
 │
 ├──► O3 (Synchronization & Semaphores) ──► O4 (Deadlocks & Banker's) ──► O5 (Classical IPC)
 │
 └──► O6 (Paging & Address Translation) ──► O7 (Virtual Memory & Replacement) ──► O8 (Segmentation)
       │
       ▼
     O9-O12 (File Systems & Disk Scheduling) ──► O13-O16 (Protection & Advanced)
```

| Target Module | Direct Prerequisites | Rationale & Concepts Required |
|---|---|---|
| **O1: OS Concepts** | *None* | Process states, PCB, fork(), context switching, and user/kernel mode. |
| **O2: CPU Scheduling** | O1, D3 | FCFS, SJF, Priority, Round Robin; ready queues implemented via FIFO queues. |
| **O3: Synchronization**| O1 | Race conditions, critical sections, Peterson's algorithm, mutex, semaphores. |
| **O4: Deadlocks** | O3 | Mutual exclusion, hold-and-wait, no-preemption, circular wait, Banker's algorithm.|
| **O6: Paging** | G1, G2, O1 | Logical to physical address translation, page tables, frame sizes in powers of 2. |
| **O7: Virtual Memory** | O6 | Page faults, Effective Access Time (EAT), TLB hit ratios, FIFO/LRU/Optimal replacement.|
| **O11: Disk Scheduling**| O1 | FCFS, SSTF, SCAN, C-SCAN, LOOK disk head movement calculations. |

---

## 3. High-Leverage Cross-Disciplinary Linkages

1. **Sets (M1) ↔ Boolean Logic (G4, G5):**
   - Union ($\cup$) is Boolean OR ($+$).
   - Intersection ($\cap$) is Boolean AND ($\cdot$).
   - Complement ($A'$) is Boolean NOT ($\overline{A}$).
   - De Morgan's Laws are mathematically identical in both domains.
2. **Logarithms & Sequences (M5, M8) ↔ Algorithm Complexity (D8):**
   - Binary search tree heights: $h = \lfloor \log_2 n \rfloor$.
   - Master Theorem recurrences: $T(n) = aT(n/b) + f(n)$ evaluate critical exponents using $\log_b a$.
3. **Queue / Stack Data Structures (D3) ↔ Operating Systems (O2, O6):**
   - Ready queue in CPU scheduling uses FIFO Queue (D3).
   - LRU page replacement stack uses doubly linked list + hash map (D2, D7).
4. **Number Systems (G1, G2) ↔ OS Address Translation (O6, O7):**
   - Splitting virtual addresses into Page Number ($p$) and Offset ($d$) requires bitwise bit-shift and masking based on powers of 2.
5. **Set Inclusion-Exclusion (M1) ↔ Syllogisms & Venn Logic (T14):**
   - Categorical propositions ("All A are B", "Some A are not B") are solved via Venn set partitions.
