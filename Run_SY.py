# -*- coding: utf-8 -*-

from Class_SY import *
from Basic_Func import SystemRunner
import random
import simpy

Customers = {}
Robots = {}
env = simpy.Environment()
run_time = 100
#1. Gen Operator
Operator = Operator()

#2. Gen data
Customers[0] = Customer(env, 0, [25,25], type = 0, size = 1, service_time = 4, duration = 200) #Information Desk
for name in range(1,10):
    location = [random.randrange(1,50),random.randrange(1,50) ]
    Customers[name] = Customer(env, name, location, type = 1, size = 1, service_time = 1, duration = 60)
#3. Gen Robots
speed = 2
for name in range(1):
    Robots[name] = Robot(name, env, speed, Customers,Operator, end_t = 120, capacity = 4)
    Robots[name].return_t = 0

#3. Run system

env.process(SystemRunner(env, Robots, Customers, Operator, 'greedy', speed = speed, interval = 5, end_t = 800))

env.run(run_time)