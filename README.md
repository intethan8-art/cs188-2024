# CS188 Project 1: Search — Summary

## Overall Pipeline

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

## Core Algorithms

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

## Q5: Why state can be “freely defined”

* `search.py` is **generic (interface-based)**
* It only relies on:

  * `getStartState()`
  * `getSuccessors(state)`
  * `isGoalState(state)`

It does NOT care about:

* state structure
* internal meaning

**State design = problem modeling**

---

## Q6: Heuristic Design (A*)

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

## Q7: Heuristic Optimization

**Standard high-quality heuristic:**

```
h(state) =
    distance to nearest food
  + MST(remaining food)
```

* Improves accuracy over pure MST
* Can optimize with **k-nearest food subset** (reduce cost)

---

## Q8: Greedy Strategy

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

## Final Takeaway

> **Project 1 = state design + graph search + heuristic design**


# CS188 Project 2: Multi-Agent Search — Summary

## Q1: Reflex Agent

* Reflex Agent 是 **reactive（反应式）**，而不是 **planning（规划式）**
* 只考虑 **当前一步（one-step lookahead）**
* Evaluation Function 输入为：

  ```python
  (currentGameState, action)
  ```

### 问题现象

当只剩一个 food 时，Pacman 可能“驻足不前”

### 原因分析

* Evaluation Function 设计过于平滑
* 对距离变化（如 1 → 2）区分不明显
* 对“吃到最后一个 food”奖励不足

---

## Q2: Minimax Agent

* 核心是理解 `getAction()` 的执行逻辑
* 使用递归构建搜索树：

```text
MAX (Pacman) → MIN (Ghost) → MAX → ...
```

### 核心点

* `value(state, agentIndex, depth)`
* agentIndex 控制当前行动者
* depth 在所有 agent 走完一轮后增加

---

## Q3: Alpha-Beta Pruning

### 核心思想

* α / β 不是全局变量
* 而是 **沿当前 path 向下传递的约束**

```text
α = MAX 当前已知的最好下界
β = MIN 当前已知的最好上界
```

---

### 剪枝条件（CS188要求：不在等号处剪枝）

#### 在 MIN 节点：

```text
if v < α → prune
```

#### 在 MAX 节点：

```text
if v > β → prune
```

---

### 关键理解

* α / β 沿递归路径传递
* 每一层局部更新
* 用于剪掉“不可能影响最终决策”的分支

---

### 示例

```text
                 MAX
          /                 \
       MIN                  MIN
     /     \             /     \
   MAX     MAX         MAX     MAX
  /  \    /  \        /  \    /  \
 3    12  8    2      4    6  14   5
```

关键过程：

```text
Root (α=-∞, β=+∞)
↓
Left MIN
↓
MAX → 得到 12 → MIN 更新 β=12
↓
MIN 最终返回 8
↓
Root 更新 α=8
↓
Right MIN（继承 α=8）
↓
看到 6 → β=6
↓
β ≤ α → 剪枝（14, 5 不再探索）
```

---

## Q4: Expectimax

### 假设

* 使用 **uniform distribution（均匀分布）**

```text
P(action) = 1 / len(actions)
```

---

### 计算方式

```text
V(s) = Σ [ P(s'|s) * V(s') ]
```
---

## Q5: Evaluation Function（for Search）

* 用于 **depth-limited minimax / expectimax**
* 本质类似 **heuristic function**

---

### 与 Reflex Evaluation 的区别

|    | Reflex Evaluation | Search Evaluation |
| -- | ----------------- | ----------------- |
| 输入 | (state, action)   | (state)           |
| 作用 | 选择当前动作            | 评估叶子节点            |
| 视野 | 1-step            | multi-step        |
| 本质 | 局部评分              | 全局估计              |

---

## 总结

* Reflex：局部贪心（one-step）
* Minimax：对抗搜索（最坏情况）
* Alpha-Beta：剪枝优化（不改变结果）
* Expectimax：随机对手（期望）
* Evaluation Function：未来价值的启发式估计
