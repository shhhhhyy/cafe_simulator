import argparse

# 파일 임포트
import welcome

# pypdevs 임포트
from pypdevs.DEVS import *
from pypdevs.infinity import INFINITY
from pypdevs.simulator import DEVSException
from pypdevs.DEVS import AtomicDEVS
from pypdevs.DEVS import CoupledDEVS
from pypdevs.simulator import Simulator


if __name__ == "__main__":
    # ----------------------------
    # ArgumentParser 추가
    # ----------------------------
    parser = argparse.ArgumentParser()
    parser.add_argument("-w","--max_worker", type=int, default=5, help="총 worker 수")
    parser.add_argument("-two","--max2", type=int, default=2, help="2인석 수")
    parser.add_argument("-four","--ax4", type=int, default=2, help="4인석 수")
    parser.add_argument("-tt","--termination_time", type=float, default=50, help="시뮬레이션 종료 시간")

    args = parser.parse_args()

    # ----------------------------
    # Welcome 모델 생성 (입력 받은 값 활용)
    # ----------------------------
    top = welcome.Welcome(
        "RestaurantSystem",
        max_worker=args.max_worker,
        max2=args.max2,
        max4=args.max4
    )

    # ----------------------------
    # Simulator 실행
    # ----------------------------
    sim = Simulator(top)
    sim.setClassicDEVS()
    sim.setVerbose()
    sim.setTerminationTime(args.termination_time)
    sim.simulate()

    # ----------------------------
    # Worker count 조회
    # ----------------------------
    ow = top.orderworker
    for w in ow.workers:
        print(w.name, "총 만든 잔수 =", w.count)