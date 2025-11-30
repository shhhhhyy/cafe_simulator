import argparse
import subprocess
import json
import csv
import os
from itertools import product

def run_simulation(w, two, four, max_stay):
    cmd = [
        "python", "/content/PythonPDEVS/src/cafe_simulator/main2.py",
        "-w", str(w),
        "-two", str(two),
        "-four", str(four),
        "--max_stay", str(max_stay),
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
    parser.add_argument("--stays", nargs="+", type=int, default=[60,90,120])
    parser.add_argument("--save_path", type=str, default="master_results.csv")
    args = parser.parse_args()

    stays = args.stays
    csv_path = args.save_path

    header = ["w","two","four","max_stay","turnover","net_profit","score"]

    # 실행 범위 = (5,10,10)
    max_w, max2, max4 = 4, 10, 10

    for stay in stays:
        for w, two, four in product(range(1,max_w+1), range(1,max2+1), range(1,max4+1)):
            result = run_simulation(w,two,four,stay)

            row = [
                w, two, four, stay,
                result["turnover"],
                result["net_profit"],
                result["score"]
            ]
            append_with_header(csv_path, header, row)

            print(f"[OK] max_stay={stay}, ({w},{two},{four}) 저장됨.")