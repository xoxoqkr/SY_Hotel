# -*- coding: utf-8 -*-

from Class_SY import *
from Basic_Func import SystemRunner, ValueFinder, ResultSave
from Generator import OrderGenerator,OrderGenerator2
import random
import simpy


customer_num = 110
cal_type = 2
robot_num = 3
run_time = 120
meal_order_ratio = 0.2 #전체 주문 중 식사 주문의 비율
OrderGenLamda = run_time/customer_num # 전체 고객 수 / 시뮬레이션 시간 = 110/120
#1. Gen Operator
Operator = Operator()
Customers = {}
Robots = {}
env = simpy.Environment()
#2. Gen data
"""
Customers[0] = Customer(env, 0, [25,25], type = 0, size = 1, service_time = 4, duration = 200) #Information Desk
for name in range(1,10):
    location = [random.randrange(1,50),random.randrange(1,50) ]
    Customers[name] = Customer(env, name, location, type = 1, size = 1, service_time = 1, duration = 60)
"""
data_num = 0
input_data = []
file = open("data/CustomerData"+str(data_num)+".txt",'r')
data = file.readlines()
for org_info in data[1:]:
    info = org_info.split(';')
    tem = []
    for ele in info[:5]:
        tem.append(int(ele))
    for ele in info[5:8]:
        tem.append(float(ele))
    input_data.append(tem)
#for info in input_data:
#    print(info)
#input('데이터 확인')
#3. Gen Robots
speed = 1
for name in range(robot_num):
    Robots[name] = Robot(name, env, speed, Customers,Operator, end_t = 120, capacity = 4, cal_type= cal_type)
    Robots[name].return_t = 0

#3. Run system
#3-1 Customer Generator
Customers[0] = Customer(env, 0, [1,0], type = 1, size = 1)
if input_data == None:
    env.process(OrderGenerator(env, Customers, customer_num = customer_num,lamda = OrderGenLamda))
else:
    env.process(OrderGenerator2(env, Customers, input_data))
env.process(SystemRunner(env, Robots, Customers, Operator, 'greedy', speed = speed, interval = 5, end_t = 800, package_type=2))
env.run(run_time)

f1 = open('결과 저장.txt','a')
r1, r2 = ResultSave(Customers, Robots)
for info in r1:
    content = '로봇 이름;{};서비스고객;{};유휴시간;{} \n '.format(info[0],info[1],info[2])
    print(content)
    f1.write(content)
content = '서비스된 고객;{};발생 후 할당;{};할당 후 실림;{};실린 후 고객 도착;{}'.format(r2[0],r2[1],r2[2],r2[3])
print(content)
f1.write(content)
for robotr_name in Robots:
    content = Robots[robotr_name].visited_nodes
    print(content)
    f1.write(content)
f1.close()
