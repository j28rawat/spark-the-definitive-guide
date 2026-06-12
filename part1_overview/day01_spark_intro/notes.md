# Day 01 Notes — What is Apache Spark?
**Chapters 1–2 | Book: Spark: The Definitive Guide**

---

## The Core Mental Model

```
Your Python code
      │
      ▼
  SparkSession  ──────────────────────────────────-┐
      │                                            │
      │  builds a logical plan                     │
      ▼                                            │
  Catalyst Optimizer  (rewrites your query)        │  Driver JVM
      │                                            │
      ▼                                            │
  Physical Plan  (how to actually execute)         │
      │                                            │
      ▼                                            │
  DAG Scheduler  (splits into stages + tasks) ─────┘
      │
      │  serialises tasks + sends over network
      ▼
  Executor 1  │  Executor 2  │  Executor N
  (partition) │  (partition) │  (partition)
```

---

## Key Terms

| Term | Definition |
|------|-----------|
| **Driver** | The JVM process running your `SparkSession`. Coordinates everything. |
| **Executor** | JVM workers that run tasks. Each holds partitions in memory/disk. |
| **Partition** | One chunk of data. The unit of parallelism. Lives on one executor. |
| **Task** | One unit of work applied to one partition. |
| **Stage** | A group of tasks that can run without a shuffle. |
| **Job** | One complete computation triggered by an action. May have many stages. |
| **DAG** | The directed graph of all transformations leading to an action. |
| **Shuffle** | Moving data across the network between executors (expensive!). |

---

## Transformation Taxonomy

```
Narrow Transformations          Wide Transformations
(no shuffle)                    (shuffle required)
─────────────────               ──────────────────
filter()                        groupBy() + agg()
select()                        orderBy()
withColumn()                    join()
map()                           repartition()
union()                         distinct()
coalesce()                      pivot()
```

**Why this matters:** every wide transformation creates a new **stage boundary**. Data must be written to disk (shuffle write) and then read back by other executors (shuffle read). This is the #1 performance concern in Spark.

---

## Lazy Evaluation — Why It Exists

Spark records your transformations but doesn't run them. When you finally call an action, Spark:
1. Looks at the full transformation chain
2. Runs it through the **Catalyst Optimizer**
3. May reorder, push down predicates, eliminate redundant steps
4. Then executes the optimised plan

This is why `filter()` before `join()` is often automatically applied by Spark even if you wrote it after — the optimizer pushes the filter down.

---

## SparkSession vs SparkContext

```python
spark = SparkSession.builder...getOrCreate()  # unified API (use this)
sc = spark.sparkContext                        # low-level RDD API (still needed for RDDs)
```

In PySpark 4.x, `SparkSession` is everything you need for DataFrames, SQL, Streaming, and ML. `SparkContext` is only needed when working with raw RDDs (Part III of this series).

---

## Partition Rule of Thumb

- **Default parallelism**: `spark.default.parallelism` (defaults to number of cores)
- **After a shuffle**: controlled by `spark.sql.shuffle.partitions` (default: 200 — often too high for local mode)
- **For local development**: set shuffle partitions to number of CPU cores:
  ```python
  spark.conf.set("spark.sql.shuffle.partitions", "4")
  ```

---

## Common Gotchas

1. **`collect()` on large DataFrames** — pulls ALL data to the driver. OOM risk. Use `show()`, `take(n)`, or write to storage instead.

2. **Counting partitions** — `df.rdd.getNumPartitions()` triggers a job internally. Don't call it in a hot loop.

3. **`spark.stop()` in tests** — always stop the session at the end of a script. A lingering SparkSession will block port 4040 for the next run.

4. **Chaining transformations** — this is idiomatic PySpark (each returns a new DataFrame, original is unchanged):
   ```python
   result = (
       df
       .filter(df.age > 18)
       .select("name", "age")
       .orderBy("age")
   )
   ```

---

## The Spark UI Cheat Sheet

| Tab | What to look for |
|-----|-----------------|
| **Jobs** | How many jobs ran, which succeeded/failed |
| **Stages** | Stage boundaries = shuffle points; look at shuffle read/write bytes |
| **Tasks** | Task duration distribution; outliers = data skew |
| **SQL** | Visual DAG of your DataFrame operations; push-down filters highlighted |
| **Storage** | What's cached and how much memory it uses |
| **Environment** | All Spark configuration properties |
| **Executors** | Memory usage, GC time, task counts per executor |
