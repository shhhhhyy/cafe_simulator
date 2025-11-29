from pypdevs.DEVS import *
from pypdevs.infinity import INFINITY
from pypdevs.simulator import DEVSException
from pypdevs.DEVS import AtomicDEVS
from pypdevs.DEVS import CoupledDEVS
from pypdevs.simulator import Simulator
import random

import generator 
import waiting
import order
import hall
# ----------------------------------------------------------------------
# 카페 coupled 모델
# ----------------------------------------------------------------------
class Welcome(CoupledDEVS):
    def __init__(self, name, max_worker,max2, max4):
        CoupledDEVS.__init__(self,name)

        # ----- Submodels -----
        self.gen = generator.GEN("GEN")
        self.waiting = waiting.HallSeatQueueCM("Hall", max2, max4)
        self.orderworker = order.OrderWorkerCM("OrderWorker", max_worker=max_worker , make_time=5.0)
        self.hall = hall.SeatManager("SeatManager", max2, max4)

        self.addSubModel(self.gen)
        self.addSubModel(self.waiting)
        self.addSubModel(self.orderworker)
        self.addSubModel(self.hall)
        
        # ----- Port Connections -----
        # GEN → HallSeatQueueCM (손님 전달)
        self.connectPorts(self.gen.out_hall12, self.waiting.in_hall12)
        self.connectPorts(self.gen.out_hall34, self.waiting.in_hall34)

        # GEN -> orderworkerCM
        self.connectPorts(self.gen.out_takeout, self.orderworker.in_takeout)

        # HallSeatQueueCM -> orderworkerCM
        self.connectPorts(self.waiting.out_order2, self.orderworker.in_hall2)
        self.connectPorts(self.waiting.out_order4, self.orderworker.in_hall4)
        
        # seat -> HallSeatQueueCM
        self.connectPorts(self.hall.out_exit2, self.waiting.in_exit2)
        self.connectPorts(self.hall.out_exit4, self.waiting.in_exit4)
        
        # order -> seat
        self.connectPorts(self.orderworker.out_serving2, self.hall.in_serving2)
        self.connectPorts(self.orderworker.out_serving4, self.hall.in_serving4)