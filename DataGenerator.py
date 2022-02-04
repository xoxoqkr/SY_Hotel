# -*- coding: utf-8 -*-

from Class_SY import *
from Generator import OrderGenerator
import simpy
import random
import numpy as np

for ite in range(10):
    customer_num = 110
    Customers = {}
    Robots = {}
    cal_type = 2
    env = simpy.Environment()
    run_time = 120
    meal_order_ratio = 0.2 #전체 주문 중 식사 주문의 비율
    OrderGenLamda = run_time/customer_num # 전체 고객 수 / 시뮬레이션 시간 = 110/120
    #1. Gen Operator
    #2. Gen data

    Customers[0] = Customer(env, 0, [1,0], type = 0, size = 1, service_time = 4, duration = 200) #Information Desk
    duration_data = np.random.normal(40,10, size = 10000)
    duration_data_bigger_than_20 = []
    for t in duration_data:
        if t > 20:
            duration_data_bigger_than_20.append(t)
    duration_pool = random.sample(duration_data_bigger_than_20, customer_num + 1)
    env.process(OrderGenerator(env, Customers, customer_num = customer_num,lamda = OrderGenLamda, meal_order_ratio = meal_order_ratio, duration = duration_pool))
    env.run(run_time)

    #고객 데이터 저장 부
    f1 = open('CustomerData'+str(ite)+'.txt','a')
    f1.write('number;floor;room#;type;size;service_time;duration;interval;\n')
    f1.write('{};{};{};{};{};{};{};{};\n'.format(0, Customers[0].location[0], Customers[0].location[1], 0, 0, 0, 1000,0))
    for index in range(1, len(Customers)):
        bf = Customers[index-1]
        af = Customers[index]
        content = '{};{};{};{};{};{};{};{}; \n'.format(index, af.location[0],af.location[1],af.type,af.size, af.time_info[5], af.time_info[6], round(af.time_info[0] - bf.time_info[0],4))
        f1.write(content)
    f1.close()