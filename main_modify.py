import argparse
import csv
import os

# 파일 임포트
import welcome

# pypdevs 임포트
from pypdevs.simulator import Simulator


if __name__ == "__main__":
    # ----------------------------
    # ArgumentParser
    # ----------------------------
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--max_worker", type=int, default=5)
    parser.add_argument("-two", "--max2", type=int, default=2)
    parser.add_argument("-four", "--max4", type=int, default=2)
    parser.add_argument("--save_path", type=str, default="sim_result.csv")

    args = parser.parse_args()

    # ----------------------------
    # Create model
    # ----------------------------
    top = welcome.Welcome(
        "RestaurantSystem",
        max_worker=args.max_worker,
        max2=args.max2,
        max4=args.max4,
    )

    sim = Simulator(top)
    sim.setClassicDEVS()
    sim.setVerbose()
    sim.setTerminationTime(50)  # sim_time 제거 → 고정값 50
    sim.simulate()

    # ----------------------------
    # Worker count 조회
    # ----------------------------
    ow = top.orderworker
    total_customers = 0

    for w in ow.workers:
        print(w.name, "총 만든 잔수 =", w.count)
        total_customers += w.count

    # ----------------------------
    # 회전율 계산
    # ----------------------------
    total_seats = args.max2 * 2 + args.max4 * 4
    turnover_rate = total_customers / total_seats if total_seats > 0 else 0

    # ----------------------------
    # 순수익 계산
    # ----------------------------
    drink_price = 5000
    labor_cost = args.max_worker * 10000
    seat_cost = total_seats * 1000

    revenue = total_customers * drink_price
    net_profit = revenue - labor_cost - seat_cost

    print("\n===== 시뮬레이션 요약 =====")
    print("회전율 =", turnover_rate)
    print("순수익 =", net_profit)

    # ----------------------------
    # CSV 저장 (없으면 생성, 있으면 append)
    # ----------------------------
    save_path = args.save_path
    file_exists = os.path.exists(save_path)

    header = ["max_worker", "max2", "max4", "turnover", "net_profit"]
    row = [
        args.max_worker,
        args.max2,
        args.max4,
        turnover_rate,
        net_profit
    ]

    with open(save_path, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(header)
        writer.writerow(row)

    print(f"\nCSV 저장 완료 → {save_path}")