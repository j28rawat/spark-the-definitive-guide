# Day 02 Notes — A Tour of Spark's Toolset
**Chapter 3 | Book: Spark: The Definitive Guide**

---

## Quick Reference: The Toolset Map

```
                        SparkSession
                             │
        ┌──────────┬─────────┼─────────┬──────────────┐
        ▼          ▼         ▼          ▼              ▼
   DataFrames  Structured   MLlib    GraphFrames   RDDs (low-level)
   / SQL       Streaming    (Day23-28) (Day28)     (Day11-13)
   (Day3-10)   (Day19-22)
```

In Python: **DataFrame = Dataset[Row]**. No separate typed Dataset API exists in PySpark — you get the same Catalyst/Tungsten engine either way.

---

## spark-submit vs Notebook

| | Notebook | `spark-submit script.py` |
|-|----------|---------------------------|
| SparkSession | Created once, reused across cells | Created once, dies with script |
| Best for | Exploration, learning, debugging | Scheduled/production jobs |
| UI after completion | Dies when kernel restarts | Dies when process exits (use History Server for post-mortem) |

---

## MLlib Vocabulary (we'll live in this for Days 23-28)

| Term | Has `.fit()`? | Has `.transform()`? | Example |
|------|--------------|---------------------|---------|
| **Transformer** | No | Yes | `VectorAssembler`, `StandardScalerModel` |
| **Estimator** | Yes | No (until fitted) | `LinearRegression`, `StandardScaler` |
| **Model** | No | Yes | Result of `.fit()` — IS a Transformer |
| **Pipeline** | Yes (chains stages) | Yes (after fit) | `Pipeline(stages=[...])` |

---

# 🔍 Spark UI Field Guide (Living Document)

This section grows every day we discover something new about the UI. Treat it as your personal reference.

## Tabs Covered So Far

### Jobs tab (`/jobs/`)
- **One job per action.** `.show()`, `.count()`, `.collect()`, `.write()` each = 1 job.
- Job description usually names the triggering operation (e.g. `showString`, `count at ...`)
- "Stages: X/Y" tells you immediately how many shuffle boundaries exist

### Stages tab (`/stages/`)
- **One stage per shuffle boundary.** N shuffles = N+1 stages.
- Click a stage → **Tasks table**:
  - Number of tasks = number of partitions for that stage
  - **Duration column**: look for outliers → signals **data skew** (covered deeply in Day 18)
  - **Shuffle Read / Shuffle Write columns**: bytes moved across the network

### SQL tab (`/SQL/`)
- Visual DAG of the *physical plan*
- **Exchange** node = a shuffle (= stage boundary)
- **BroadcastExchange** = a broadcast join, NOT a full shuffle (preview of Day 7)
- Nodes are colour/grouped by stage — matches the Stages tab

### Storage tab (`/storage/`)
- Lists all `.cache()`'d / `.persist()`'d DataFrames
- Shows: fraction cached, size in memory, size on disk
- Empty until you call `.cache()` AND trigger an action

## Tabs Not Yet Covered
- **Environment** — all Spark config properties (Day 14)
- **Executors** — per-executor memory/CPU/GC stats (Day 14, Day 18)

---

## Key Debugging Workflow (build this habit now)

1. Run your code
2. Open **Jobs** → find the job that took longest
3. Click into it → **Stages** → find the stage with the most shuffle read/write
4. Click into that stage → **Tasks** → sort by Duration descending
5. If one task takes 10x longer than others → **data skew** (Day 18 topic)
6. Cross-reference with **SQL tab** to see WHERE in your query this stage corresponds to

This 6-step loop is how real Spark debugging works. We'll apply it to increasingly complex queries as we go.

---

## Caching Quick Reference

```python
df.cache()        # = df.persist(StorageLevel.MEMORY_AND_DISK)
df.persist()      # same as cache()
df.unpersist()    # release from memory — ALWAYS do this when done
```

**Effect on UI:**
- First action after `.cache()`: computes AND stores (no speedup yet)
- Subsequent actions: Storage tab shows the cached data; Stages tab shows fewer/skipped stages for the cached portion

**When NOT to cache:** if a DataFrame is used only once, caching adds overhead with no benefit. Cache when reusing the SAME DataFrame across MULTIPLE actions.
