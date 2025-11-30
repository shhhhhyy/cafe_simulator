import argparse
import csv
import os
import json
import sys

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

    parser.add_argument("-stay", "--max_stay",type=int,required=True,choices=[60, 90, 120],help="Maximum stay duration for customers (60, 120, 180 minutes)")

    parser.add_argument("--save_path", type=str, default="sim_result.csv")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    # ----------------------------
    # Create model
    # ----------------------------
    top = welcome.Welcome(
        "RestaurantSystem",
        max_worker=args.max_worker,
        max2=args.max2,
        max4=args.max4,
        max_stay=args.max_stay
    )

    # ----------------------------
    # JSON 모드면 모든 출력 차단
    # ----------------------------
    if args.json:
        sys.stdout = open(os.devnull, 'w')

    # ----------------------------
    # Simulation
    # ----------------------------
    sim = Simulator(top)
    sim.setClassicDEVS()

    if not args.json:   # JSON 모드 아닐 때만 verbose 출력
        sim.setVerbose()

    sim.setTerminationTime(600)
    sim.simulate()

    # ----------------------------
    # Worker count 조회
    # ----------------------------
    ow = top.orderworker
    total_customers = sum([w.count for w in ow.workers])

    # ----------------------------
    # 회전율 계산
    # ----------------------------
    total_seats = args.max2 * 2 + args.max4 * 4
    turnover_rate = total_customers / total_seats if total_seats > 0 else 0

    # ----------------------------
    # 순수익 계산
    # ----------------------------
    drink_price = 5000
    labor_cost = (args.max_worker -1) * 110000
    seat_cost = args.max2 * 500 + args.max4 * 1000
    revenue = total_customers * drink_price
    net_profit = revenue - labor_cost - seat_cost

    # ----------------------------
    #  α 기반 score 계산 ( α =  1000 )
    # ----------------------------
    score = net_profit + 1000 * turnover_rate

    # ----------------------------
    # JSON 모드: JSON 한 줄만 출력 후 종료
    # ----------------------------
    if args.json:
        sys.stdout = sys.__stdout__  # stdout 복원

        result = {
            "turnover": turnover_rate,
            "net_profit": net_profit,
            "score": score
        }
        print(json.dumps(result))
        exit()

    # ----------------------------
    # CSV 저장 (일반 모드)
    # ----------------------------
    save_path = args.save_path
    file_exists = os.path.exists(save_path)

    header = ["max_worker", "max2", "max4", "maxstay",
              "turnover", "net_profit", "score"]
    row = [
        args.max_worker,
        args.max2,
        args.max4,
        args.max_stay,
        turnover_rate,
        net_profit,
        score
    ]

    with open(save_path, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(header)
        writer.writerow(row)

    print(f"\nCSV 저장 완료 → {save_path}")