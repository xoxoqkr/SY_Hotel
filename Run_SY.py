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
global weight


ite_type = 'permutations' #'permutations': 모든 순열,'combinations': 모든 조합
#weight = [1,0] #[route길이 가중치, time penalty 가중치]
customer_num = 168
cal_type2 = 2
#robot_num = 3
run_time = 140
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
    Robots[name] = Robot(name, env, speed, Customers,Operator, end_t = run_time + 10, capacity = 4, cal_type= cal_type2)
    Robots[name].return_t = 0

#3. Run system
#3-1 Customer Generator
Customers[0] = Customer(env, 0, [1,0], type = 1, size = 0)
if input_data == None:
    env.process(OrderGenerator(env, Customers, customer_num = customer_num,lamda = OrderGenLamda))
else:
    env.process(OrderGenerator2(env, Customers, input_data, endless = 0, interval = OrderGenLamda, duration_index = 4 + duration_index, run_time = run_time))
env.process(SystemRunner(env, Robots, Customers, Operator, 'greedy', speed = speed, interval = 0.1, end_t = 800, package_type=package_type,
                         ite_type= ite_type, weight = weight))
env.run(run_time + 10)


f1 = open('결과 저장.txt','a', encoding = 'utf-8')
#input('확인1')
f2 = open('결과 저장2.txt','a', encoding = 'utf-8')
#input('확인2')
r1, r2, ct_data = ResultSave(Customers, Robots, env.now)
f1.write('로봇 수 ;{} cal_type ;{} \n '.format(robot_num, package_type))
ave_service_ct_num = []
ave_idle_t = []
ave_trip_num = []
#input('확인2-2')
for info in r1:
    content = '로봇 이름;{};서비스고객;{};트립수;{};유휴시간;{};유휴시간내용;{}; \n '.format(info[0],info[1],info[3],info[2],info[4])
    #content = 't;{};t;{};t;{};t;{};t;{}; \n '.format(info[0], info[1], info[3], info[2], info[4])
    ave_service_ct_num.append(info[1])
    ave_idle_t.append(info[2])
    ave_trip_num.append(info[3])
    print(content)
    f1.write(content)
#input('확인2-3')

header = '데이터파일;로봇 수;caltype;TW종류;서비스된 고객;발생 후 할당t;할당 후 실림t;실린 후 고객 도착t;' \
         '로봇 당 평균 서비스고객 수;평균 유휴 시간;로봇운행트립수;초과고객t1;초과고객t2;초과고객t3;' \
         '격리고객t1;격리고객t2;격리고객t3;일반고객t1;일반고객t2;일반고객t3;서비스X고객 대기시간;서비스고객중tw초과고객수;' \
         '격리고객수(서비스됨);일반고객수(서비스됨);격리고객수(tw내서비스);일반고객수(tw내서비스);격리고객수(발생);일반고객수(발생);격리고객tw초과시간평균;일반고객tw초과시간평균;permutation type;w1(경로길이);w2(시간 패널티);\n'

if ite_count == 0:
    f2.write(header)
    pass
#f1.write(header)
#print(len(r2))
#print(r2)
#test = [data_file,robot_num, package_type,duration_index,r2[0],r2[1],r2[2],r2[3],
#                                                              sum(ave_service_ct_num)/len(ave_service_ct_num),sum(ave_idle_t)/len(ave_idle_t),
#                                                              sum(ave_trip_num)/len(ave_trip_num),r2[4],r2[5],r2[6],r2[7],r2[8],r2[9],r2[10],r2[11],r2[12],r2[13]]
#print(len(test))
#input('확인1')
content = '{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};'.format(data_file,robot_num, package_type,duration_index,r2[0],r2[1],r2[2],r2[3],
                                                              sum(ave_service_ct_num)/len(ave_service_ct_num),sum(ave_idle_t)/len(ave_idle_t),
                                                              sum(ave_trip_num)/len(ave_trip_num),r2[4],r2[5],r2[6],r2[7],r2[8],r2[9],r2[10],r2[11],r2[12],r2[13],r2[14],
                                                                                              r2[15],r2[16],r2[17],r2[18],r2[19],r2[20],r2[21],r2[22])

content += '{};{};{};{}; \n'.format(ite_type, str(weight[0]),str(weight[1]),str(weight[2]))

f1.write(content)
f2.write(content)
for robotr_name in Robots:
    content = Robots[robotr_name].visited_nodes
    print('{}'.format(content))
    f1.write('{} \n'.format(content))
f1.close()
f2.close()

f1 = open('customer data save.txt','a')

header1 = '데이터;{};로봇수;{};방식;{};\n'.format(data_file,robot_num, package_type)
f1.write(header1)
header2 = '고객이름;생성시점;패키지구성시점;로봇에 실리 시점;고객 도착시점;TW종료 시점;층;호실; \n'
f1.write(header2)
for ct_info in ct_data:
    content = '{};{};{};{};{};{};{};{}; \n'.format(ct_info[0],ct_info[1],ct_info[2],ct_info[3],ct_info[4],ct_info[5],ct_info[6],ct_info[7])
    f1.write(content)
f1.close()

