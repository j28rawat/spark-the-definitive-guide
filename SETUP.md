# Environment Setup Guide
## Spark: The Definitive Guide — Hands-On Python Study

> **Why this guide exists:** Python 3.14 (which ships as the default on modern Macs) is too new for stable PySpark usage. This guide installs Python 3.11 in an isolated virtual environment using `pyenv`, leaving your system Python completely untouched.

---

## Prerequisites Overview

| Tool | Version | Purpose |
|------|---------|---------|
| Java (Temurin JDK) | 17 (LTS) | Spark runs on the JVM |
| pyenv | latest | Manage multiple Python versions without breaking your system |
| Python | 3.11.x | Stable, fully supported by PySpark 4.x |
| PySpark | 4.1.2 | Latest stable Apache Spark for Python |
| Git | latest | Version control for this repo |
| VSCode | latest | Editor + Python extension |

---

## Step 1 — Install Homebrew (if not already installed)

Homebrew is the package manager for macOS. Open **Terminal** and run:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Verify it works:
```bash
brew --version
```

---

## Step 2 — Install Java 17 (Temurin LTS)

<br>

> **Why Temurin?** It's the free, open-source, production-grade OpenJDK distribution from Eclipse Adoptium. Oracle JDK requires a license for commercial use.

```bash
# Install the Adoptium tap first, then Java 17
brew install --cask temurin@17
```

Verify Java is installed:
```bash
java -version
# Expected output: openjdk version "17.x.x" ...
```

Set `JAVA_HOME` permanently by adding this to your shell profile (`~/.zshrc` for zsh, which is the default on modern Macs):

```bash
echo 'export JAVA_HOME=$(/usr/libexec/java_home -v 17)' >> ~/.zshrc
source ~/.zshrc
```

Confirm:
```bash
echo $JAVA_HOME
# Should print something like: /Library/Java/JavaVirtualMachines/temurin-17.jdk/Contents/Home
```

---

## Step 3 — Install pyenv

`pyenv` lets you install and switch between multiple Python versions per project. Your system Python 3.14 is never modified.

```bash
brew install pyenv
```

Add `pyenv` initialisation to your shell profile:

```bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
source ~/.zshrc
```

Verify:
```bash
pyenv --version
```

---

## Step 4 — Install Python 3.11 via pyenv

```bash
# This takes 2–3 minutes — it compiles Python from source
pyenv install 3.11.9
```

> **Note:** If the build fails, run `brew install openssl readline sqlite3 xz zlib tcl-tk` first and retry.

---

## Step 5 — Clone (or create) the GitHub Repository

### 5a. Create a new repo on GitHub

1. Go to [github.com/new](https://github.com/new)
2. Name it: `spark-the-definitive-guide`
3. Set it to **Private** (or Public — your call)
4. Do **not** initialise with a README (we'll push our own)
5. Click **Create repository**

### 5b. Clone it to your machine

```bash
# Replace YOUR_USERNAME with your actual GitHub username
git clone https://github.com/YOUR_USERNAME/spark-the-definitive-guide.git
cd spark-the-definitive-guide
```

Or, if you downloaded this scaffold as a zip and want to push it:
```bash
cd spark-the-definitive-guide   # navigate to the scaffold folder
git init
git remote add origin https://github.com/YOUR_USERNAME/spark-the-definitive-guide.git
```

---

## Step 6 — Set Python 3.11 for this project

Inside the project directory, run:

```bash
# This creates a .python-version file that pins Python 3.11 for this folder only
pyenv local 3.11.9
python --version   # Should print: Python 3.11.9
```

---

## Step 7 — Create and activate the virtual environment

```bash
# Create the venv using the pyenv-managed Python 3.11
python -m venv .venv

# Activate it
source .venv/bin/activate

# Confirm you're inside the venv
which python        # Should point to .venv/bin/python
python --version    # Should print: Python 3.11.9
```

> **Every time you open a new terminal session**, re-activate with:
> ```bash
> cd spark-the-definitive-guide
> source .venv/bin/activate
> ```

---

## Step 8 — Install PySpark and dependencies

```bash
pip install --upgrade pip

pip install \
  pyspark==4.1.2 \
  pyarrow \
  pandas \
  numpy \
  matplotlib \
  jupyter \
  ipykernel
```

This installs:
- **pyspark** — Apache Spark Python API
- **pyarrow** — columnar memory format; required for pandas ↔ Spark conversions and Arrow-optimised UDFs
- **pandas / numpy** — used throughout the book's examples
- **matplotlib** — for visualising results
- **jupyter / ipykernel** — so you can run `.ipynb` notebooks alongside `.py` scripts in VSCode

---

## Step 9 — Verify the full stack works

Run the smoke test:

```bash
python environment/verify_setup.py
```

Expected output:
```
✅ Python version: 3.11.x
✅ PySpark version: 4.1.2
✅ Java home: /Library/Java/JavaVirtualMachines/temurin-17.jdk/...
✅ SparkSession created successfully
✅ Basic DataFrame operation works
✅ Environment is ready. Happy Sparking! 🚀
```

---

## Step 10 — Configure VSCode

1. Open the project folder in VSCode: `code .`
2. Install the **Python** extension (Microsoft) if not already installed
3. Select the interpreter: `Cmd+Shift+P` → **Python: Select Interpreter** → choose `.venv` (the one inside your project folder)
4. Install the **Jupyter** extension for running notebooks inline

### Recommended VSCode extensions for this project

```
ms-python.python
ms-toolsai.jupyter
ms-python.pylint
mechatroner.rainbow-csv       # for viewing CSV data files
```

---

## Step 11 — Create the .gitignore

This prevents committing the venv, Java caches, and Spark temp files:

```bash
cat > .gitignore << 'EOF'
# Python
.venv/
__pycache__/
*.pyc
*.pyo
.python-version

# Jupyter
.ipynb_checkpoints/
*.ipynb_checkpoints

# Spark
derby.log
metastore_db/
spark-warehouse/
/tmp/

# Data (large files)
data/*.csv
data/*.parquet
data/*.json
!data/sample_*.csv
!data/sample_*.json

# macOS
.DS_Store
EOF
```

---

## Project Structure

```
spark-the-definitive-guide/
├── SETUP.md                        ← You are here
├── README.md                       ← Master index + daily progress
├── PROGRESS.md                     ← Day-by-day log of what was covered
├── .gitignore
├── .python-version                 ← Pins Python 3.11 for this folder
├── requirements.txt                ← Pinned dependencies
│
├── environment/
│   └── verify_setup.py             ← Smoke test for the full stack
│
├── data/                           ← Shared sample datasets
│
├── part1_overview/
│   ├── day01_spark_intro/
│   └── day02_toolset/
│
├── part2_structured_apis/
│   ├── day03_api_overview/
│   ├── day04_basic_operations/
│   ├── day05_types_and_formats/
│   ├── day06_aggregations/
│   ├── day07_joins/
│   ├── day08_data_sources/
│   ├── day09_spark_sql/
│   └── day10_datasets/
│
├── part3_low_level/
│   ├── day11_rdds_intro/
│   ├── day12_advanced_rdds/
│   └── day13_shared_variables/
│
├── part4_production/
│   ├── day14_how_spark_runs/
│   ├── day15_developing_spark/
│   ├── day16_deploying/
│   ├── day17_monitoring/
│   └── day18_performance_tuning/
│
├── part5_streaming/
│   ├── day19_stream_intro/
│   ├── day20_structured_streaming_basics/
│   ├── day21_event_time_stateful/
│   └── day22_streaming_production/
│
├── part6_ml/
│   ├── day23_advanced_analytics_intro/
│   ├── day24_preprocessing/
│   ├── day25_classification/
│   ├── day26_regression/
│   ├── day27_recommendation_unsupervised/
│   └── day28_graph_deep_learning/
│
└── part7_ecosystem/
    └── day29_python_specifics_ecosystem/
```

Each `dayXX_topic/` folder contains:
- `concepts.py` — runnable demos of every concept from the chapter
- `exercises.py` — problems to solve yourself (solutions added next day)
- `notes.md` — internals, mental models, gotchas

---

## Daily Workflow

```bash
# 1. Navigate to project
cd ~/path/to/spark-the-definitive-guide

# 2. Activate venv
source .venv/bin/activate

# 3. Work on today's folder
cd part2_structured_apis/day04_basic_operations
python concepts.py

# 4. Commit your work
git add .
git commit -m "day04: basic structured operations — concepts + exercises"
git push
```

---

## Common Issues & Fixes

### `JAVA_HOME not set` error
```bash
export JAVA_HOME=$(/usr/libexec/java_home -v 17)
```

### `pyspark` command not found
Make sure your venv is activated: `source .venv/bin/activate`

### `py4j` or JVM errors on startup
Confirm Java 17 is active: `java -version`. If you have multiple JVMs, `JAVA_HOME` must point to 17.

### Spark UI not loading (localhost:4040)
The Spark UI only runs while a SparkSession is active. Keep your script running (or add `input()` at the end temporarily) and open `http://localhost:4040` in your browser.

### `python --version` still shows 3.14
You're not inside the venv. Run `source .venv/bin/activate` and check again.

---

## Saving dependencies

After adding any new `pip install`, save it:
```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "chore: update requirements.txt"
```

To restore on a new machine:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Working with Notebooks in VSCode

Each day uses **Jupyter notebooks** (`.ipynb`) instead of plain `.py` files for better readability and cell-by-cell execution.

### Open a notebook
1. In VSCode, open the project folder
2. Navigate to e.g. `part1_overview/day01_spark_intro/day01_concepts.ipynb`
3. Click to open — VSCode renders it with the Jupyter extension

### Select the right kernel
When you open a notebook for the first time, VSCode asks which Python kernel to use.  
Click **"Select Kernel"** → **"Python Environments"** → choose the `.venv` interpreter  
(it will say something like `Python 3.11.9 ('.venv': venv)`)

### Each day's files
| File | Purpose |
|------|---------|
| `dayXX_concepts.ipynb` | All concepts from the chapter(s), explained inline |
| `dayXX_exercises.ipynb` | Problems to solve + solutions in the last cell |
| `notes.md` | Reference sheet: mental models, term glossary, gotchas |

### Recommended VSCode extensions (add to your existing list)
```
ms-toolsai.jupyter          # Jupyter notebook support (you likely have this)
ms-toolsai.jupyter-keymap   # Jupyter keyboard shortcuts inside VSCode
```
