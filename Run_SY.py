# -*- coding: utf-8 -*-

from Class_SY import *
from Basic_Func import SystemRunner, ValueFinder, ResultSave
from Generator import OrderGenerator,OrderGenerator2, InputDataTransform
import simpy

global package_type
global data_file
global robot_num
global duration_index
global ite_count

customer_num = 168
cal_type = 2
#robot_num = 3
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
input_data = InputDataTransform('data/'+data_file)
print('data수::',len(input_data))
#3. Gen Robots
speed = 1
for name in range(robot_num):
    Robots[name] = Robot(name, env, speed, Customers,Operator, end_t = 120, capacity = 4, cal_type= cal_type)
    Robots[name].return_t = 0

#3. Run system
#3-1 Customer Generator
Customers[0] = Customer(env, 0, [1,0], type = 1, size = 0)
if input_data == None:
    env.process(OrderGenerator(env, Customers, customer_num = customer_num,lamda = OrderGenLamda))
else:
    env.process(OrderGenerator2(env, Customers, input_data, endless = 0, interval = OrderGenLamda, duration_index = 4 + duration_index))
env.process(SystemRunner(env, Robots, Customers, Operator, 'greedy', speed = speed, interval = 0.1, end_t = 800, package_type=package_type))
env.run(run_time)

f1 = open('결과 저장.txt','a')
f2 = open('결과 저장2.txt','a')
r1, r2 = ResultSave(Customers, Robots)
f1.write('로봇 수 ;{} cal_type ;{} \n '.format(robot_num, package_type))
ave_service_ct_num = []
ave_idle_t = []
ave_trip_num = []
for info in r1:
    content = '로봇 이름;{};서비스고객;{};트립수;{};유휴시간;{};유휴시간내용;{}; \n '.format(info[0],info[1],info[3],info[2],info[4])
    ave_service_ct_num.append(info[1])
    ave_idle_t.append(info[2])
    ave_trip_num.append(info[3])
    print(content)
    f1.write(content)

header = '데이터파일;로봇 수;caltype;TW종류;서비스된 고객;발생 후 할당;할당 후 실림;실린 후 고객 도착;' \
         '로봇 당 평균 서비스고객 수;평균 유휴 시간;로봇운행트립수;초과고객t1;초과고객t2;초과고객t3;초과고객수;\n'
if ite_count == 0:
    f2.write(header)
f1.write(header)
content = '{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};\n'.format(data_file,robot_num, package_type,duration_index,r2[0],r2[1],r2[2],r2[3],
                                                              sum(ave_service_ct_num)/len(ave_service_ct_num),sum(ave_idle_t)/len(ave_idle_t),
                                                              sum(ave_trip_num)/len(ave_trip_num),r2[4],r2[5],r2[6],r2[7])
f1.write(content)
f2.write(content)
for robotr_name in Robots:
    content = Robots[robotr_name].visited_nodes
    print('{}'.format(content))
    f1.write('{} \n'.format(content))
f1.close()
f2.close()
