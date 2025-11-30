import argparse
import subprocess
import json
import csv
import os
from itertools import product

def run_simulation(w, two, four):
    cmd = [
        "python", "/content/PythonPDEVS/src/cafe_simulator/main2.py",
        "-w", str(w),
        "-two", str(two),
        "-four", str(four),
        "--json"
    ]
    output = subprocess.check_output(cmd)
    data = json.loads(output.decode("utf-8"))
    return data

def append_with_header(path, header, row):
    write_header = not os.path.exists(path)
    with open(path, "a", newline="") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(header)
        writer.writerow(row)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--save_path", type=str, default="master_results.csv")
    args = parser.parse_args()

    csv_path = args.save_path

    header = ["w","two","four","turnover","net_profit"]

    # 실행 범위 = (5,10,10)
    max_w, max2, max4 = 4, 10, 10

    for w, two, four in product(range(1,max_w+1), range(1,max2+1), range(1,max4+1)):
        result = run_simulation(w,two,four)

        row = [
            w, two, four,
            result["turnover"],
            result["net_profit"]
        ]
        append_with_header(csv_path, header, row)

        print(f"[OK] ({w},{two},{four}) 저장됨.")