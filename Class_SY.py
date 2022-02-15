# -*- coding: utf-8 -*-
from Basic_Func import distance, distance2, AvailableCustomer

class Operator(object):
    def __init__(self):
        self.Route = []
        self.history = []

class Customer(object):
    def __init__(self, env, name, location, type = 0, size = 1, service_time = 0, duration = 60):
        self.name = name
        self.env = env
        self.time_info = [round(env.now, 2), None, None, None, None, service_time, round(env.now, 2) + duration, None]
        # [0 :발생시간, 1: 로봇에 할당 시간, 2:로봇에 실린 시간, 3:고객 도착 시간, 4: 고객 서비스 완료 시간, 5: 서비스 시간, 6:주문 종료 시간]
        self.location = location #[Floor , Room #, 층의 절반]
        self.type = type
        self.size = size
        self.history = []
        self.canceal = False
        #env.process(self.Cancelation(env, duration))

    def Cancelation(self, env, t):
        yield env.timeout(t)
        self.canceal == True


class Robot(object):
    def __init__(self, name, env, speed, customers,Operator, end_t = 120, capacity = 4, cal_type = 1):
        self.name = name
        self.env = env
        self.speed = speed
        self.capacity = capacity
        self.visited_nodes = [[1,0]]
        self.end_t = end_t
        self.history = []
        self.return_t = 0
        self.Process = None
        self.idle = True
        self.idle_t = 0
        self.idle_info = []
        self.wait_t = 0.05
        self.served_customers = [0]
        self.trip_num = 0
        env.process(self.Runner(env, Operator, customers, cal_type = cal_type))


    def RunTrip(self, env, trip, customers, cal_type = 2):
        print('T:{}/ 로봇 :{} Trip :{} 시작'.format(int(env.now),self.name,trip))
        for name1 in trip: #로봇에 할당된 시점
            customers[name1].time_info[2] = env.now
        visit_count = 0
        for name in trip:
            customer = customers[name]
            if cal_type == 1:
                move_t = distance(self.visited_nodes[-1], customer.location)
            else:
                print('{}->{}'.format(self.served_customers[-1], customer.name))
                print('{}->{}'.format(self.visited_nodes[-1], customer.location))
                move_t = distance2(self.visited_nodes[-1],customer.location)
            yield env.timeout(move_t)
            customer.time_info[3] = env.now #로봇이 고객에게 도착한 시점
            self.history.append([env.now, customer.name, customer.location, 'C'])
            if customer.time_info[5] > 0:
                yield env.timeout(customer.time_info[5]) #서비스 시간은 이미 이동 시간에서 계산 됨.
                customer.time_info[4] = env.now
            if customer.name > 0:
                self.served_customers.append(customer.name)
            if visit_count == 0: #로봇에 실린 시점
                for name2 in trip:
                    customers[name2].time_info[2] = env.now
            self.visited_nodes.append(customer.location)
            print('T:{} ; 로봇 {} ;고객 {} 도착'.format(env.now, self.name, name))
            visit_count += 1
        self.history.append([env.now, 0, 'Trip End'])
        print('T:{} ; 로봇 {} ;트립 완료'.format(env.now, self.name))


    def Runner(self, env, Operator, Customers, cal_type = 1):
        while self.env.now < self.end_t:
            print(Operator.Route)
            if len(Operator.Route) > 0:
                trip = Operator.Route[0][1]
                trip_names = []
                size = 0
                for info in trip:
                    trip_names.append(info[3])
                    size += Customers[info[3]].size
                print('로봇 {} ; T {} ; 경로 {} 추가됨 : 무게 {}'.format(self.name, int(self.env.now), trip,size))
                Operator.history.append(Operator.Route[0][1])
                self.trip_num += 1
                del Operator.Route[0]
                print('로봇{} 수행 후 경로 {}'.format(self.name, Operator.Route))
                self.idle = False
                if cal_type == 1:
                    yield env.process(self.RunTrip(env, trip, Customers))
                else:
                    yield env.process(self.RunTrip(env, trip_names, Customers))
                #self.Process = env.process(self.RunTrip(trip[1], Customers))
                #yield self.Process
                self.idle = True
                print('로봇{} 지우고 난 후 경로 {}'.format(self.name, Operator.Route))
            else:
                #self.idle = True
                print('T {} ; 로봇 {} '.format(int(self.env.now), self.name))
                self.idle_info.append([env.now, len(Operator.Route), len(AvailableCustomer(Customers))])
                yield self.env.timeout(self.wait_t)
                self.idle_t += self.wait_t
                #self.idle_info.append([env.now,len(Operator.Route),len(AvailableCustomer(Customers))])
                print('T {} ; 로봇 {} ;운행 가능한 경로 없음; {}'.format(int(self.env.now), self.name, len(Operator.Route)))
