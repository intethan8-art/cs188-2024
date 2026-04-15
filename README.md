# CS188 Project 1: Search — Summary

## 🔄 Overall Pipeline

```
GameState (full environment)
   ↓ abstraction
SearchProblem.state (your design)
   ↓
Search (DFS / BFS / UCS / A*)
   ↓
action list
   ↓
Agent.getAction executes step-by-step
```

---

## 🔍 Core Algorithms

### Q1–Q2: DFS & BFS (Unweighted)

* **DFS** → Stack / recursion
* **BFS** → Queue
* Both are **graph search** → must track visited states

---

### Q3–Q4: UCS & A*

* **UCS** = Dijkstra
* **A*** = UCS + heuristic
* Use **PriorityQueue (min cost first)**

**Key insight (Dijkstra):**

* Nodes popped from PQ already have the shortest path
* Relaxation only affects nodes still in PQ (edge weights ≥ 0)

---

## 🧩 Q5: Why state can be “freely defined”

* `search.py` is **generic (interface-based)**
* It only relies on:

  * `getStartState()`
  * `getSuccessors(state)`
  * `isGoalState(state)`

❗ It does NOT care about:

* state structure
* internal meaning

👉 **State design = problem modeling**

---

## 🔥 Q6: Heuristic Design (A*)

### Baseline

* Manhattan Distance

### Advanced

* **MST (Minimum Spanning Tree)**

  * True path ≥ MST cost → admissible

**Cut Property:**

> The minimum crossing edge of any cut belongs to the MST

### Algorithms

* **Prim** (preferred): grows from a node (similar to Dijkstra)
* **Kruskal**: sort edges + Union-Find (WQU)

---

## 🚀 Q7: Heuristic Optimization

**Standard high-quality heuristic:**

```
h(state) =
    distance to nearest food
  + MST(remaining food)
```

* Improves accuracy over pure MST
* Can optimize with **k-nearest food subset** (reduce cost)

---

## 🍔 Q8: Greedy Strategy

* Always go to the nearest food (BFS each step)
* Implemented via inheritance (clean code reuse)

⚠️ Not optimal:

> Local optimum ≠ global optimum

---

## ⚠️ Common Pitfalls

* ❌ Confusing `GameState` with `state`
* ❌ No cost tracking in UCS / A*
* ❌ Non-admissible heuristic
* ❌ Running search every step (too slow)

---

## 🎯 Final Takeaway

> **Project 1 = state design + graph search + heuristic design**
