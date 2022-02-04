# -*- coding: utf-8 -*-
import random
from Basic_Func import ValueFinder
from Class_SY import Customer


def OrderGenerator(env, Customers, customer_num = 110, lamda = 1, floors= list(range(2, 17)), floor_data = [[4, 24], [10, 24], [14, 20], [17, 16]], meal_order_ratio = 0.2,
                   input_data = None, duration = [60]):
    #고객 생성기
    pool = []
    #floors = list(range(2, 17))
    #floor_data = [[1, 0], [4, 24], [10, 24], [14, 20], [17, 19]]
    for floor in floors:
        rooms = ValueFinder(floor, floor_data)
        for room in range(1, rooms + 1):
            pool.append([floor, room])
    for name in range(1, customer_num + 1):
        if len(duration) == 1:
            duration_t = duration[0]
        else:
            duration_t = duration[name]
        rv = random.random()
        if name % 2 == 0:
            while True:
                if input_data == None:
                    location = list(random.choice(pool))
                else:
                    location = input_data[name][1:3]
                if location[0] <= 4:
                    Customers[name] = Customer(env, name, location, type=1, size=1, service_time=1,
                                               duration=duration_t)  # 자가 격리자
                    print('고객 {}, 타입{}'.format(name, 1))
                    break
        else:
            while True:
                if input_data == None:
                    location = list(random.choice(pool))
                else:
                    location = input_data[name][1:3]
                if location[0] > 4:
                    Customers[name] = Customer(env, name, location, type=0, size=1, service_time=1,
                                               duration=duration_t)  # 자가 격리자
                    print('고객 {}, 타입{}'.format(name, 0))
                    break
            # Customers[name] = Customer(env, name, location, type=0, size=1, service_time=1, duration=60) #일반
        if rv < meal_order_ratio:
            Customers[name].size = 2
        pool.remove(location)
        print('T : {} 고객 수 {}'.format(int(env.now), len(Customers)))
        yield env.timeout(lamda)



def OrderGenerator2(env, Customers, input_data, endless = 0):
    for data in input_data:
        Customers[data[0]] = Customer(env, data[0], data[1:3], type=data[3], size=data[4], service_time=data[5],duration = max(data[6],endless))  # 자가 격리자
        #print('info : {}'.format(data))
        #print('T : {} 고객 수 {}'.format(int(env.now), len(Customers)))
        if data[7] > 0:
            yield env.timeout(data[7])