"""Benchmark Test Script

This script runs benchmark tests for both semantic and grammar verification
of Litex code using multiple processors. It loads test cases from CSV files,
processes them, and provides a summary of the verification accuracy.
"""

import multiprocessing as mp
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from utils.csv_utils import load_csv_dicts
from verifier import verify_grammar, verify_semantic


MAX_PROCESSORS = 40
SEMANTIC_CSV_PATH = Path.cwd() / "test" / "semantic_test.csv"
GRAMMAR_CSV_PATH = Path.cwd() / "test" / "grammar_test.csv"


if __name__ == "__main__":
    semantic_test_list = load_csv_dicts(SEMANTIC_CSV_PATH)
    grammar_test_list = load_csv_dicts(GRAMMAR_CSV_PATH)

    with mp.Pool(processes=MAX_PROCESSORS) as pool:
        semantic_result = pool.map(verify_semantic, semantic_test_list)


    t = 0
    f = 0

    tt = 0
    tf = 0
    ft = 0
    ff = 0

    print("Detailed Missed Cases:")

    for r in semantic_result:
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
    print("Semantic Summary:")
    print("======================Total======================")
    print(f"True Positive: {tt} / {t} = {tt/t if t>0 else 0}")
    print(f"True Negative: {ff} / {f} = {ff/f if f>0 else 0}")
    print(f"False Negative: {tf} / {t} = {tf/t if t>0 else 0}")
    print(f"False Positive: {ft} / {f} = {ft/f if f>0 else 0}")

    with mp.Pool(processes=MAX_PROCESSORS) as pool:
        grammar_results = pool.map(verify_grammar, grammar_test_list)

    t = 0
    f = 0

    tt = 0
    tf = 0
    ft = 0
    ff = 0

    print("\nDetailed Missed Cases:")

    for r in grammar_results:
        if r["expect"] == "True":
            t += 1
            if r["actual"]:
                tt += 1
            if not r["actual"]:
                tf += 1
                print(f"Missed True for code:\n{r['code']}\n")
        elif r["expect"] == "False":
            f += 1
            if not r["actual"]:
                ff += 1
            if r["actual"]:
                ft += 1
                print(f"Missed False for code:\n{r['code']}\n")
    
    print("=================================================")
    print("Grammar Summary:")
    print("======================Total======================")
    print(f"True Positive: {tt} / {t} = {tt/t if t>0 else 0}")
    print(f"True Negative: {ff} / {f} = {ff/f if f>0 else 0}")
    print(f"False Negative: {tf} / {t} = {tf/t if t>0 else 0}")
    print(f"False Positive: {ft} / {f} = {ft/f if f>0 else 0}")

# =================================================
# Semantic Summary (One round voting):
# ======================Total======================
# True Positive: 356 / 361 = 0.9861495844875346
# True Negative: 89 / 89 = 1.0
# False Negative: 5 / 361 = 0.013850415512465374
# False Positive: 0 / 89 = 0.0

# =================================================
# Semantic Summary (Two rounds voting):
# ======================Total======================
# True Positive: 356 / 360 = 0.9888888888888889
# True Negative: 89 / 89 = 1.0
# False Negative: 4 / 360 = 0.011111111111111112
# False Positive: 0 / 89 = 0.0

# =================================================
# Grammar Summary:
# ======================Total======================
# True Positive: 2775 / 2775 = 1.0
# True Negative: 109 / 109 = 1.0
# False Negative: 0 / 2775 = 0.0
# False Positive: 0 / 109 = 0.0