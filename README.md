# Spark: The Definitive Guide — Hands-On Python Study

A structured, code-first journey through **Spark: The Definitive Guide** (Chambers & Zaharia).  
Every concept is implemented in Python using PySpark 4.x. Files are **additive** — nothing is ever overwritten.

---

## Environment

| | |
|---|---|
| **Python** | 3.11.9 (via pyenv) |
| **PySpark** | 4.1.2 |
| **Java** | Temurin JDK 17 |
| **Editor** | VSCode |

📖 **See [SETUP.md](SETUP.md) for the full installation guide.**

---

## Study Plan (29 Days)

| Day | Part | Chapter(s) | Topic | Folder |
|-----|------|-----------|-------|--------|
| 01 | I | Ch 1–2 | What is Spark? Gentle intro, SparkSession, RDDs vs DataFrames | `part1_overview/day01_spark_intro` |
| 02 | I | Ch 3 | Tour of the toolset: Datasets, SQL, Streaming, MLlib overview | `part1_overview/day02_toolset` |
| 03 | II | Ch 4 | Structured API overview: execution model, plans, transformations | `part2_structured_apis/day03_api_overview` |
| 04 | II | Ch 5 | Basic structured operations: schemas, columns, rows, expressions | `part2_structured_apis/day04_basic_operations` |
| 05 | II | Ch 6 | Working with types: booleans, numbers, strings, dates, complex | `part2_structured_apis/day05_types_and_formats` |
| 06 | II | Ch 7 | Aggregations: groupBy, window functions, rollup, cube, pivot | `part2_structured_apis/day06_aggregations` |
| 07 | II | Ch 8 | Joins: inner, outer, cross, semi, anti — and the shuffle problem | `part2_structured_apis/day07_joins` |
| 08 | II | Ch 9 | Data sources: CSV, JSON, Parquet, ORC, JDBC | `part2_structured_apis/day08_data_sources` |
| 09 | II | Ch 10 | Spark SQL: views, catalog, JDBC server, subqueries | `part2_structured_apis/day09_spark_sql` |
| 10 | II | Ch 11 | Datasets API (typed API, encoders, UDFs vs typed transformations) | `part2_structured_apis/day10_datasets` |
| 11 | III | Ch 12 | RDD basics: creation, actions, transformations, lineage | `part3_low_level/day11_rdds_intro` |
| 12 | III | Ch 13 | Advanced RDDs: key-value pairs, partitioners, co-grouping | `part3_low_level/day12_advanced_rdds` |
| 13 | III | Ch 14 | Distributed shared variables: broadcast vars, accumulators | `part3_low_level/day13_shared_variables` |
| 14 | IV | Ch 15 | How Spark runs on a cluster: driver, executors, memory model | `part4_production/day14_how_spark_runs` |
| 15 | IV | Ch 16 | Developing Spark apps: packaging, testing, local vs cluster mode | `part4_production/day15_developing_spark` |
| 16 | IV | Ch 17 | Deploying Spark: standalone, YARN, Kubernetes overview | `part4_production/day16_deploying` |
| 17 | IV | Ch 18 | Monitoring & debugging: Spark UI, event logs, metrics, DAG viz | `part4_production/day17_monitoring` |
| 18 | IV | Ch 19 | Performance tuning: partitioning, caching, AQE, skew, spill | `part4_production/day18_performance_tuning` |
| 19 | V | Ch 20 | Stream processing fundamentals: micro-batch vs continuous | `part5_streaming/day19_stream_intro` |
| 20 | V | Ch 21 | Structured Streaming basics: sources, sinks, output modes | `part5_streaming/day20_structured_streaming_basics` |
| 21 | V | Ch 22 | Event-time & stateful processing: watermarks, state store | `part5_streaming/day21_event_time_stateful` |
| 22 | V | Ch 23 | Streaming in production: checkpointing, fault tolerance, triggers | `part5_streaming/day22_streaming_production` |
| 23 | VI | Ch 24 | Advanced analytics intro: MLlib pipeline, transformers, estimators | `part6_ml/day23_advanced_analytics_intro` |
| 24 | VI | Ch 25 | Preprocessing & feature engineering: encoders, scalers, imputers | `part6_ml/day24_preprocessing` |
| 25 | VI | Ch 26 | Classification: Logistic Regression, Decision Trees, Random Forest | `part6_ml/day25_classification` |
| 26 | VI | Ch 27 | Regression: Linear Regression, gradient-boosted trees | `part6_ml/day26_regression` |
| 27 | VI | Ch 28–29 | Recommendation (ALS) + Unsupervised (KMeans, LDA, PCA) | `part6_ml/day27_recommendation_unsupervised` |
| 28 | VI | Ch 30–31 | Graph Analytics (GraphFrames) + Deep Learning overview | `part6_ml/day28_graph_deep_learning` |
| 29 | VII | Ch 32–33 | Python-specific APIs + Ecosystem & community resources | `part7_ecosystem/day29_python_specifics_ecosystem` |

---

## Folder Convention

Every `dayXX_topic/` folder follows the same pattern:

```
dayXX_topic/
├── concepts.py     # Runnable demos of every concept from the chapter(s)
├── exercises.py    # Problems to solve yourself
└── notes.md        # Key internals, mental models, common gotchas
```

---

## Progress

See [PROGRESS.md](PROGRESS.md) for the day-by-day log.

---

## How to Run

```bash
# Activate your environment first
source .venv/bin/activate

# Run a day's concepts
python part1_overview/day01_spark_intro/concepts.py

# Verify your setup at any time
python environment/verify_setup.py
```

---

## Repository Rules

- **Never overwrite** files from previous days — only add new ones
- Each day's folder is self-contained and runnable independently
- Commit at the end of each session with the message format:  
  `day04: basic structured operations — concepts + exercises`
