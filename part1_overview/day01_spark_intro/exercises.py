"""
day01 — exercises.py
=====================
Solve these without looking at concepts.py first.
Solutions will be discussed at the start of Day 02.

Run: python part1_overview/day01_spark_intro/exercises.py
"""

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = (
    SparkSession.builder
    .appName("day01_exercises")
    .master("local[*]")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")


# ──────────────────────────────────────────────────────────────────────────────
# EXERCISE 1
# Create a DataFrame of numbers from 1 to 50.
# Filter to keep only numbers divisible by 3.
# Add a column called 'cubed' that contains the cube of each number.
# Show the result.
# Expected: 16 rows (3, 6, 9, ... 48)
# ──────────────────────────────────────────────────────────────────────────────

# YOUR CODE HERE


# ──────────────────────────────────────────────────────────────────────────────
# EXERCISE 2
# Given the data below, find the average salary per city,
# ordered by average salary descending.
# ──────────────────────────────────────────────────────────────────────────────

employees = spark.createDataFrame([
    ("Alice",   "Toronto",  95000),
    ("Bob",     "Montreal", 72000),
    ("Carol",   "Toronto",  88000),
    ("Dave",    "Calgary",  81000),
    ("Eve",     "Montreal", 102000),
    ("Frank",   "Calgary",  76000),
    ("Grace",   "Toronto",  91000),
], schema=["name", "city", "salary"])

# YOUR CODE HERE


# ──────────────────────────────────────────────────────────────────────────────
# EXERCISE 3
# Repartition the employees DataFrame to 4 partitions.
# Print the number of partitions before and after.
# Then coalesce to 2 partitions and print again.
# Question to think about: which operations cause a shuffle and why?
# ──────────────────────────────────────────────────────────────────────────────

# YOUR CODE HERE


# ──────────────────────────────────────────────────────────────────────────────
# EXERCISE 4 (Conceptual — answer in a comment)
# Look at this sequence of operations:
#
#   df = spark.range(1_000_000)
#   df2 = df.filter(df.id > 500_000)
#   df3 = df2.withColumn("doubled", df2.id * 2)
#   df4 = df3.groupBy((df3.doubled % 10).alias("last_digit")).count()
#   df4.show()
#
# Q1: Which of these lines actually execute computation?
# Q2: Which transformations are narrow and which are wide?
# Q3: How many "stages" would you expect in the Spark UI?
#
# YOUR ANSWERS:
# Q1:
# Q2: filter= , withColumn= , groupBy= , count=
# Q3:
# ──────────────────────────────────────────────────────────────────────────────


spark.stop()
