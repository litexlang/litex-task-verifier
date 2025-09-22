"""Benchmark Test Script

This script benchmarks the performance of the LaTeX code verifier. It loads test cases from a CSV file, processes them using multiple processors, and exports the results to a new CSV file. It also provides a summary of the verification accuracy for each LLM used.
"""

import multiprocessing as mp
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from utils.csv_utils import export_csv_dicts, load_csv_dicts
from verifier import verify_semantic


MAX_PROCESSORS = 40
CSV_PATH = Path.cwd() / "test" / "test.csv"
EXPORT_CSV_PATH = Path.cwd() / "test" / "test_with_results.csv"


if __name__ == "__main__":
    test_info = load_csv_dicts(CSV_PATH)

    with mp.Pool(processes=MAX_PROCESSORS) as pool:
        results = pool.map(verify_semantic, test_info)

    export_csv_dicts(EXPORT_CSV_PATH, results, write_mode="w")

    t = 0
    f = 0

    tt = 0
    tf = 0
    ft = 0
    ff = 0

    print("Detailed Missed Cases:")

    for r in results:
        if r["expect"] == "TRUE":
            t += 1
            if r["actual"] == "Yes":
                tt += 1
            if r["actual"] == "No":
                tf += 1
                print(f"Missed True for {r['collaboration_title']} \t {r['title']}")
        elif r["expect"] == "FALSE":
            f += 1
            if r["actual"] == "No":
                ff += 1
            if r["actual"] == "Yes":
                ft += 1
                print(f"Missed False for {r['collaboration_title']} \t {r['title']}")

    print("\n")
    print("=================================================")
    print("Summary:")
    print("======================Total======================")
    print(f"True Positive: {tt} / {t} = {tt/t if t>0 else 0}")
    print(f"True Negative: {ff} / {f} = {ff/f if f>0 else 0}")
    print(f"False Negative: {tf} / {t} = {tf/t if t>0 else 0}")
    print(f"False Positive: {ft} / {f} = {ft/f if f>0 else 0}")

# =================================================
# Summary (One round voting):
# ======================Total======================
# True Positive: 356 / 361 = 0.9861495844875346
# True Negative: 89 / 89 = 1.0
# False Negative: 5 / 361 = 0.013850415512465374
# False Positive: 0 / 89 = 0.0

# =================================================
# Summary (Two rounds voting):
# ======================Total======================
# True Positive: 356 / 360 = 0.9888888888888889
# True Negative: 89 / 89 = 1.0
# False Negative: 4 / 360 = 0.011111111111111112
# False Positive: 0 / 89 = 0.0
