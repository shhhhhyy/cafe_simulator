import argparse
import subprocess
import json
import csv
import os


def run_simulation(w, two, four, alpha):
    cmd = [
        "python", "/content/PythonPDEVS/src/cafe_simulator/main2.py",
        "-w", str(w),
        "-two", str(two),
        "-four", str(four),
        "--alpha", str(alpha),
        "--json"
    ]

    output = subprocess.check_output(cmd)
    data = json.loads(output.decode("utf-8"))
    return data  # {"turnover": x, "net_profit": y, "score": z}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--max_worker", type=int, required=True)
    parser.add_argument("-two", "--max2", type=int, required=True)
    parser.add_argument("-four", "--max4", type=int, required=True)
    parser.add_argument("--save_path", type=str, default="xy_dataset.csv")
    args = parser.parse_args()

    max_w = args.max_worker
    max2 = args.max2
    max4 = args.max4

    save_path = args.save_path
    file_exists = os.path.exists(save_path)

    # CSV header (best_profit 제거!)
    header = [
        "alpha",
        "X_max_worker", "X_max2", "X_max4",
        "Y_best_worker", "Y_best2", "Y_best4"
    ]

    # CSV 파일 없으면 header 먼저 기록
    if not file_exists:
        with open(save_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)

    # ------------------------------
    #   🔥 α = 0,1,2 자동 실행
    # ------------------------------
    for alpha in [0, 1, 2]:

        print(f"\n===============================")
        print(f"▶ α = {alpha} 전체 조합 탐색 시작")
        print(f"===============================\n")

        best_profit = -1e18
        best_combo = (0, 0, 0)

        for w in range(1, max_w + 1):
            for two in range(1, max2 + 1):
                for four in range(1, max4 + 1):

                    result = run_simulation(w, two, four, alpha)
                    profit = result["net_profit"]

                    if profit > best_profit:
                        best_profit = profit
                        best_combo = (w, two, four)

                    print(f"  → α={alpha}, w={w}, 2={two}, 4={four}, profit={profit}")

        # ------------------------------
        #   α 기준 최적 조합 출력
        # ------------------------------
        print("\n===== α =", alpha, "최종 최적 조합(Y) =====")
        print("best_worker =", best_combo[0])
        print("best_2seats =", best_combo[1])
        print("best_4seats =", best_combo[2])
        print("best_profit =", best_profit)

        # ------------------------------
        #     X → Y CSV 저장 (profit 제거)
        # ------------------------------
        X = [max_w, max2, max4]
        Y = list(best_combo)

        # best_profit은 저장 X!
        row = [alpha] + X + Y

        with open(save_path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(row)

        print(f"\n[X→Y] α={alpha} 저장 완료 → {save_path}\n")