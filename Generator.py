# -*- coding: utf-8 -*-
import random
from Basic_Func import ValueFinder
from Class_SY import Customer


def OrderGenerator(env, Customers, customer_num = 110, lamda = 1, floors= list(range(2, 17)), floor_data = [[4, 24], [10, 24], [14, 20], [17, 19]], meal_order_ratio = 0.2):
    #고객 생성기
    pool = []
    #floors = list(range(2, 17))
    #floor_data = [[1, 0], [4, 24], [10, 24], [14, 20], [17, 19]]
    for floor in floors:
        rooms = ValueFinder(floor, floor_data)
        for room in range(1, rooms + 1):
            pool.append([floor, room])
    for name in range(1, customer_num + 1):
        rv = random.random()
        if name % 2 == 0:
            while True:
                location = list(random.choice(pool))
                if location[0] <= 4:
                    Customers[name] = Customer(env, name, location, type=1, size=1, service_time=1,
                                               duration=60)  # 자가 격리자
                    print('고객 {}, 타입{}'.format(name, 1))
                    break
        else:
            while True:
                location = list(random.choice(pool))
                if location[0] > 4:
                    Customers[name] = Customer(env, name, location, type=0, size=1, service_time=1,
                                               duration=60)  # 자가 격리자
                    print('고객 {}, 타입{}'.format(name, 0))
                    break
            # Customers[name] = Customer(env, name, location, type=0, size=1, service_time=1, duration=60) #일반
        if rv < meal_order_ratio:
            Customers[name].size = 2
        pool.remove(location)
        print('T : {} 고객 수 {}'.format(int(env.now), len(Customers)))
        yield env.timeout(lamda)