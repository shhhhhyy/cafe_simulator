from pypdevs.DEVS import *
from pypdevs.simulator import Simulator
from pypdevs.infinity import INFINITY
import random

# ------------------------------------------
# 상태 클래스 정의
# ------------------------------------------
class SeatStatus:
    def __init__(self, current="IDLE"):
        self.set(current)

    def set(self, value):
        self.__state = value
        return self.__state

    def get(self):
        return self.__state

    def __str__(self):
        return self.get()

# ------------------------------------------
# 2인석 좌석 배치 모델
# ------------------------------------------
class SeatPlacement2AM(AtomicDEVS):
    def __init__(self, name, max2):
        super().__init__(name)
        self.max2 = max2  # 최대 좌석 수

        # 입력/출력 포트
        self.in_serving = self.addInPort("in_serving")
        self.in_stop = self.addInPort("in_stop")
        self.out_exit2 = self.addOutPort("out_exit2")

        # 상태 변수
        self.status = SeatStatus("IDLE")  # 상태: IDLE or ACTIVE
        self.phase = "IDLE"
        self.timers = []
        self.m2 = 0
        self.elapsed = 0  # 한 턴마다의 경과 시간
        self.total_elapsed = 0 # 총 누적경과 시간

        # 체류시간 범위
        self.min_stay = 30
        self.max_stay = 60

    def timeAdvance(self):
        return min(self.timers) if self.status.get() == "ACTIVE" else INFINITY

    def outputFnc(self):
        if self.status.get() == "ACTIVE" and self.timers:
            #print(f"[outputFnc] Customer leaving. m2: {len(self.timers)}")
            return {self.out_exit2: "exit2"}
        return {}

    def intTransition(self):
        if self.status.get() == "ACTIVE":
          min_t = min(self.timers)

          # 누적 경과 시간 갱신
          self.total_elapsed += min_t
          print()
          print(f"[intTransition] Elapsed: {min_t:.2f} (총 경과시간={self.total_elapsed:.2f})")

          # 타이머 업데이트
          self.timers = [t - min_t for t in self.timers]
          formatted_timers = [f"{t:.2f}" for t in self.timers]
          print(f"[timers] 현재 타이머 리스트 (경과 반영): {formatted_timers}")

          # 고객 제거
          # float 오차 때문에 정확히 0.0이 아닐 수도 있음 → 가장 작은 값 제거
          to_remove = min(self.timers, key=lambda x: abs(x))
          self.timers.remove(to_remove)
          self.m2 -= 1

          formatted_timers2 = [f"{t:.2f}" for t in self.timers]
          print(f"[intTransition] Removed customer. timers: {formatted_timers2}")
          print(f"[outputFnc] Customer leaving. m2: {len(self.timers)}")

          # 상태 업데이트
          self.status.set("ACTIVE" if len(self.timers) > 0 else "IDLE")
        return self


    def extTransition(self, inputs):
        e = self.elapsed
        self.total_elapsed += e  # 누적 경과시간 업데이트

        print(f"[extTransition] Elapsed: {e:.2f} (총 경과시간={self.total_elapsed:.2f})")

        if self.status.get() == "ACTIVE":
            self.timers = [t - e for t in self.timers]

        if self.in_serving in inputs:
            msg = inputs[self.in_serving]
            _, n = msg
            if n <= 2 and self.m2 < self.max2:
                stay_time = random.uniform(self.min_stay, self.max_stay)
                self.timers.append(stay_time)
                self.m2 += 1
                print(f"[extTransition] New customer's stay_time={stay_time:.2f}, m2: {self.m2}")

        # 타이머 리스트 출력 (경과시간 반영된 상태)
        formatted_timers = [f"{t:.2f}" for t in self.timers]
        print(f"[timers] 현재 타이머 리스트 (경과 반영): {formatted_timers}")

        if len(self.timers) > 0:
            self.status.set("ACTIVE")
        else:
            self.status.set("IDLE")

        return self


# ------------------------------------------
# 4인석 좌석 배치 모델
# ------------------------------------------
class SeatPlacement4AM(AtomicDEVS):
    def __init__(self, name, max4):
        super().__init__(name)
        self.max4 = max4  # 최대 좌석 수

        # 입력/출력 포트
        self.in_serving = self.addInPort("in_serving")
        self.in_stop = self.addInPort("in_stop")
        self.out_exit4 = self.addOutPort("out_exit4")

        # 상태 변수
        self.status = SeatStatus("IDLE")  # 상태: IDLE or ACTIVE
        self.phase = "IDLE"
        self.timers = []
        self.m4 = 0
        self.elapsed = 0  # 한 턴마다의 경과 시간
        self.total_elapsed = 0 # 총 누적경과 시간

        # 체류시간 범위
        self.min_stay = 30
        self.max_stay = 60

    def timeAdvance(self):
        return min(self.timers) if self.status.get() == "ACTIVE" else INFINITY

    def outputFnc(self):
        if self.status.get() == "ACTIVE" and self.timers:
            #print(f"[outputFnc] Customer leaving. m2: {len(self.timers)}")
            return {self.out_exit4: "exit4"}
        return {}

    def intTransition(self):
        if self.status.get() == "ACTIVE":
          min_t = min(self.timers)

          # 누적 경과 시간 갱신
          self.total_elapsed += min_t
          print()
          print(f"[intTransition] Elapsed: {min_t:.2f} (총 경과시간={self.total_elapsed:.2f})")

          # 타이머 업데이트
          self.timers = [t - min_t for t in self.timers]
          formatted_timers = [f"{t:.2f}" for t in self.timers]
          print(f"[timers] 현재 타이머 리스트 (경과 반영): {formatted_timers}")
    

          # 고객 제거
          # float 오차 때문에 정확히 0.0이 아닐 수도 있음 → 가장 작은 값 제거
          to_remove = min(self.timers, key=lambda x: abs(x))
          self.timers.remove(to_remove)
          self.m4 -= 1

          formatted_timers2 = [f"{t:.2f}" for t in self.timers]
          print(f"[intTransition] Removed customer. timers: {formatted_timers2}")
          print(f"[outputFnc] Customer leaving. m4: {len(self.timers)}")

          # 상태 업데이트
          self.status.set("ACTIVE" if len(self.timers) > 0 else "IDLE")
        return self


    def extTransition(self, inputs):
        e = self.elapsed
        self.total_elapsed += e  # 누적 경과시간 업데이트

        print(f"[extTransition] Elapsed: {e:.2f} (총 경과시간={self.total_elapsed:.2f})")

        if self.status.get() == "ACTIVE":
            self.timers = [t - e for t in self.timers]

        if self.in_serving in inputs:
            msg = inputs[self.in_serving]
            _, n = msg
            if n >= 3 and self.m4 < self.max4:
                stay_time = random.uniform(self.min_stay, self.max_stay)
                self.timers.append(stay_time)
                self.m4 += 1
                print(f"[extTransition] New customer's stay_time={stay_time:.2f}, m4: {self.m4}")

        # 타이머 리스트 출력 (경과시간 반영된 상태)
        formatted_timers = [f"{t:.2f}" for t in self.timers]
        print(f"[timers] 현재 타이머 리스트 (경과 반영): {formatted_timers}")

        if len(self.timers) > 0:
            self.status.set("ACTIVE")
        else:
            self.status.set("IDLE")

        return self
    
    
# ------------------------------------------
# SeatManager Coupled Model
# ------------------------------------------
class SeatManager(CoupledDEVS):
    def __init__(self, name, max2, max4):
        super().__init__(name)
        
        self.seat2 = self.addSubModel(SeatPlacement2AM("Seat2", max2))
        self.seat4 = self.addSubModel(SeatPlacement4AM("Seat4", max4))
        
        self.in_serving2 = self.addInPort("in_serving2")
        self.in_serving4 = self.addInPort("in_serving4")

        self.out_exit2 = self.addOutPort("out_exit2")
        self.out_exit4 = self.addOutPort("out_exit4")
        
        
        self.connectPorts(self.in_serving2, self.seat2.in_serving)
        self.connectPorts(self.in_serving4, self.seat4.in_serving)

        self.connectPorts(self.seat2.out_exit2, self.out_exit2)
        self.connectPorts(self.seat4.out_exit4, self.out_exit4)

    def select(self, imm):
        if self.seat2 in imm:
            return self.seat2
        if self.seat4 in imm:
            return self.seat4

