"""
environment/verify_setup.py
---------------------------
Run this after completing SETUP.md to confirm your entire stack is working.
Usage: python environment/verify_setup.py
"""

import sys
import os

REQUIRED_PYTHON = (3, 11)
REQUIRED_PYSPARK = "4.1.2"


def check(label: str, ok: bool, detail: str = "") -> bool:
    status = "✅" if ok else "❌"
    msg = f"{status} {label}"
    if detail:
        msg += f": {detail}"
    print(msg)
    return ok


def main() -> None:
    all_ok = True

    # --- Python version ---
    major, minor = sys.version_info[:2]
    version_str = f"{major}.{minor}.{sys.version_info[2]}"
    ok = (major, minor) >= REQUIRED_PYTHON
    all_ok &= check("Python version", ok, version_str)
    if not ok:
        print(f"   ⚠️  Need Python {REQUIRED_PYTHON[0]}.{REQUIRED_PYTHON[1]}+. "
              f"Follow SETUP.md Step 3–6 to install via pyenv.")

    # --- JAVA_HOME ---
    java_home = os.environ.get("JAVA_HOME", "")
    all_ok &= check("JAVA_HOME set", bool(java_home), java_home or "not set")

    # --- PySpark import ---
    try:
        import pyspark
        pyspark_version = pyspark.__version__
        ok = pyspark_version == REQUIRED_PYSPARK
        all_ok &= check("PySpark version", ok, pyspark_version)
        if not ok:
            print(f"   ⚠️  Expected {REQUIRED_PYSPARK}. Run: pip install pyspark=={REQUIRED_PYSPARK}")
    except ImportError:
        all_ok &= check("PySpark import", False, "not installed")
        print("   Run: pip install pyspark==4.1.2")
        return  # No point continuing

    # --- SparkSession ---
    try:
        from pyspark.sql import SparkSession

        spark = (
            SparkSession.builder
            .master("local[2]")
            .appName("verify_setup")
            .config("spark.driver.memory", "1g")
            .config("spark.ui.enabled", "false")   # suppress UI during smoke test
            .getOrCreate()
        )
        spark.sparkContext.setLogLevel("ERROR")
        all_ok &= check("SparkSession created", True)

        # --- Basic DataFrame operation ---
        data = [("Alice", 30), ("Bob", 25), ("Carol", 35)]
        df = spark.createDataFrame(data, schema=["name", "age"])
        count = df.filter(df.age > 28).count()
        all_ok &= check("DataFrame filter + count", count == 2, f"got {count}, expected 2")

        # --- SQL ---
        df.createOrReplaceTempView("people")
        result = spark.sql("SELECT name FROM people WHERE age = (SELECT MIN(age) FROM people)")
        youngest = result.collect()[0]["name"]
        all_ok &= check("Spark SQL query", youngest == "Bob", f"youngest={youngest}")

        # --- PyArrow (Arrow-based optimisations) ---
        try:
            import pyarrow  # noqa: F401
            all_ok &= check("PyArrow available", True, pyarrow.__version__)
        except ImportError:
            all_ok &= check("PyArrow available", False, "run: pip install pyarrow")

        # --- Pandas ---
        try:
            import pandas as pd
            pdf = df.toPandas()
            all_ok &= check("Pandas conversion (toPandas)", len(pdf) == 3, f"{len(pdf)} rows")
        except ImportError:
            all_ok &= check("Pandas available", False, "run: pip install pandas")

        spark.stop()

    except Exception as exc:
        all_ok &= check("SparkSession created", False, str(exc))

    # --- Final verdict ---
    print()
    if all_ok:
        print("🚀 Environment is ready. Happy Sparking!")
    else:
        print("🔧 Some checks failed. Follow the fixes above, then re-run this script.")
        sys.exit(1)


if __name__ == "__main__":
    main()
