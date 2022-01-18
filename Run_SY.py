# -*- coding: utf-8 -*-

from Class_SY import *
from Basic_Func import SystemRunner, SystemRunner2, ValueFinder
import random
import simpy



customer_num = 20
Customers = {}
Robots = {}
cal_type = 2
env = simpy.Environment()
run_time = 100
#1. Gen Operator
Operator = Operator()

#2. Gen data
"""
Customers[0] = Customer(env, 0, [25,25], type = 0, size = 1, service_time = 4, duration = 200) #Information Desk
for name in range(1,10):
    location = [random.randrange(1,50),random.randrange(1,50) ]
    Customers[name] = Customer(env, name, location, type = 1, size = 1, service_time = 1, duration = 60)
"""

Customers[0] = Customer(env, 0, [0,0,0], type = 1, size = 1)
pool = []
floors = list(range(2,17))
floor_data = [[1,0],[4,24],[10,24],[14,20],[17,19]]
for floor in floors:
    rooms = ValueFinder(floor, floor_data)
    for room in range(1, rooms + 1):
        pool.append([floor, room])

for name in range(1, customer_num + 1):
    if name % 2 == 0:
        while True:
            location = list(random.choice(pool))
            if location[0] <= 4:
                Customers[name] = Customer(env, name, location, type = 1, size = 1, service_time = 1, duration = 60) #자가 격리자
                print('고객 {}, 타입{}'.format(name, 1))
                break
    else:
        while True:
            location = list(random.choice(pool))
            if location[0] > 4:
                Customers[name] = Customer(env, name, location, type = 0, size = 1, service_time = 1, duration = 60) #자가 격리자
                print('고객 {}, 타입{}'.format(name, 0))
                break
        #Customers[name] = Customer(env, name, location, type=0, size=1, service_time=1, duration=60) #일반
    pool.remove(location)


#3. Gen Robots
speed = 1
for name in range(1):
    Robots[name] = Robot(name, env, speed, Customers,Operator, end_t = 120, capacity = 4, cal_type= cal_type)
    Robots[name].return_t = 0

#3. Run system

#env.process(SystemRunner(env, Robots, Customers, Operator, 'greedy', speed = speed, interval = 5, end_t = 800))
env.process(SystemRunner2(env, Robots, Customers, Operator, 'greedy', speed = speed, interval = 5, end_t = 800))
env.run(run_time)