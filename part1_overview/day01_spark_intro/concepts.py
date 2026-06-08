"""
day01 — concepts.py
====================
Book reference: Chapters 1 & 2
Topic: What is Apache Spark? + A Gentle Introduction

Run: python part1_overview/day01_spark_intro/concepts.py
"""

from pyspark.sql import SparkSession
from pyspark.sql import functions as F


# ──────────────────────────────────────────────────────────────────────────────
# 1. CREATING A SPARKSESSION
# ──────────────────────────────────────────────────────────────────────────────
# SparkSession is the single entry point to all Spark functionality.
# In PySpark 4.x, SparkSession.builder is the standard way to create one.
# 'local[*]' means: run locally, use all available CPU cores.

spark = (
    SparkSession.builder
    .appName("day01_spark_intro")
    .master("local[*]")
    .config("spark.driver.memory", "2g")
    .getOrCreate()
)

# Reduce log noise — ERROR only during learning
spark.sparkContext.setLogLevel("ERROR")

print("=" * 60)
print(f"Spark version : {spark.version}")
print(f"Python version: {spark.sparkContext.pythonVer}")
print(f"App name      : {spark.sparkContext.appName}")
print(f"Master        : {spark.sparkContext.master}")
print("=" * 60)


# ──────────────────────────────────────────────────────────────────────────────
# 2. DATAFRAMES: THE FUNDAMENTAL ABSTRACTION
# ──────────────────────────────────────────────────────────────────────────────
# A DataFrame is a distributed collection of rows with named, typed columns.
# It is conceptually like a SQL table or a Pandas DataFrame — but distributed
# across potentially thousands of machines.

print("\n── 2. DataFrames ──")

# range() creates a DataFrame with a single 'id' column (0..999)
# This is a TRANSFORMATION — no data is computed yet (lazy evaluation)
numbers_df = spark.range(1000)

print(f"Type: {type(numbers_df)}")
print(f"Partitions: {numbers_df.rdd.getNumPartitions()}")  # parallelism level

# show() is an ACTION — it triggers execution and displays results
numbers_df.show(5)


# ──────────────────────────────────────────────────────────────────────────────
# 3. TRANSFORMATIONS vs ACTIONS (the most important concept in Spark)
# ──────────────────────────────────────────────────────────────────────────────
# TRANSFORMATIONS: lazy — they define a new DataFrame but do NOT compute it.
#   Examples: filter(), select(), groupBy(), join(), withColumn()
#
# ACTIONS: eager — they trigger actual computation and return a result.
#   Examples: show(), count(), collect(), write(), first()
#
# Spark builds a DAG (Directed Acyclic Graph) of transformations and only
# executes when an action is called. This is how Spark optimises execution.

print("\n── 3. Transformations vs Actions ──")

# These are ALL transformations — nothing runs yet:
evens = numbers_df.filter(numbers_df.id % 2 == 0)          # narrow transformation
with_square = evens.withColumn("square", evens.id ** 2)     # narrow transformation

# .count() is an ACTION — this triggers the full plan above
print(f"Count of even numbers: {with_square.count()}")   # triggers execution

# .explain() shows the physical execution plan (not an action, just prints)
print("\nExecution plan:")
with_square.explain()


# ──────────────────────────────────────────────────────────────────────────────
# 4. NARROW vs WIDE TRANSFORMATIONS
# ──────────────────────────────────────────────────────────────────────────────
# NARROW: each input partition contributes to exactly one output partition.
#   No data shuffled across the network. Fast.
#   Examples: filter, map, withColumn, select
#
# WIDE: input partitions may contribute to multiple output partitions.
#   Data is shuffled across the network. This creates a new "stage" in the DAG.
#   Examples: groupBy, orderBy, join, repartition, distinct

print("\n── 4. Narrow vs Wide transformations ──")

data = [
    ("Alice", "Engineering", 95000),
    ("Bob",   "Marketing",   72000),
    ("Carol", "Engineering", 88000),
    ("Dave",  "Marketing",   81000),
    ("Eve",   "Engineering", 102000),
]
schema = ["name", "department", "salary"]
employees = spark.createDataFrame(data, schema=schema)

# NARROW: filter — each partition is filtered independently
senior = employees.filter(employees.salary > 80000)   # no shuffle

# WIDE: groupBy + avg — data from all partitions must be shuffled to compute
#       the aggregation per department
dept_avg = (
    employees
    .groupBy("department")
    .agg(F.avg("salary").alias("avg_salary"), F.count("*").alias("headcount"))
    .orderBy("department")
)

print("Senior employees (narrow filter):")
senior.show()

print("Department averages (wide aggregation — involves shuffle):")
dept_avg.show()

print("Plan for dept_avg (look for 'Exchange' = shuffle point):")
dept_avg.explain()


# ──────────────────────────────────────────────────────────────────────────────
# 5. PARTITIONS — the unit of parallelism
# ──────────────────────────────────────────────────────────────────────────────
# A partition is a chunk of data that sits on one executor.
# More partitions = more parallelism (up to the number of CPU cores).
# Too few partitions = underutilised cluster.
# Too many partitions = scheduling overhead.
# Rule of thumb: 2–4x the number of CPU cores.

print("\n── 5. Partitions ──")

# Create a DataFrame and repartition it manually
df_8 = spark.range(100).repartition(8)
print(f"Partitions after repartition(8): {df_8.rdd.getNumPartitions()}")

# coalesce reduces partitions WITHOUT a shuffle (can only go smaller)
df_3 = df_8.coalesce(3)
print(f"Partitions after coalesce(3):    {df_3.rdd.getNumPartitions()}")

# repartition can increase OR decrease (always does a full shuffle)
df_12 = df_3.repartition(12)
print(f"Partitions after repartition(12): {df_12.rdd.getNumPartitions()}")


# ──────────────────────────────────────────────────────────────────────────────
# 6. THE SPARK UI (localhost:4040)
# ──────────────────────────────────────────────────────────────────────────────
# Every running SparkSession exposes a web UI at http://localhost:4040
# It shows: Jobs, Stages, Tasks, Storage, Environment, Executors, SQL
# This is your primary debugging tool for understanding what Spark is doing.
#
# To explore the UI:
#   1. Run this file
#   2. Before the script finishes, open http://localhost:4040 in your browser
#   3. Explore the SQL / Jobs / Stages tabs
#
# Uncomment the line below to pause execution so you can explore the UI:
# input("\n🔍 Spark UI is live at http://localhost:4040 — press Enter to exit...")


# ──────────────────────────────────────────────────────────────────────────────
# 7. SPARKSESSION vs SPARKCONTEXT vs SQLCONTEXT
# ──────────────────────────────────────────────────────────────────────────────
# SparkContext   — original low-level entry point (Spark 1.x). Still exists.
# SQLContext     — added SQL support (Spark 1.x). Deprecated.
# SparkSession   — unified entry point since Spark 2.0. Use this always.
#
# SparkSession wraps SparkContext internally.

print("\n── 7. Session hierarchy ──")
print(f"SparkSession     : {spark}")
print(f"SparkContext      : {spark.sparkContext}")
print(f"Conf (app name)  : {spark.sparkContext.getConf().get('spark.app.name')}")

# ──────────────────────────────────────────────────────────────────────────────
# Cleanup
# ──────────────────────────────────────────────────────────────────────────────
spark.stop()
print("\n✅ Day 01 complete.")
