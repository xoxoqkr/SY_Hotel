# -*- coding: utf-8 -*-
from Basic_Func import distance


class Operator(object):
    def __init__(self):
        self.Route = []
        self.history = []

class Customer(object):
    def __init__(self, env, name, location, type = 0, size = 1, service_time = 0, duration = 60):
        self.name = name
        self.env = env
        self.time_info = [round(env.now, 2), None, None, None, None, service_time, round(env.now, 2) + duration]
        # [0 :발생시간, 1: 로봇에 할당 시간, 2:로봇에 실린 시간, 3:고객 도착 시간, 4: 고객 서비스 완료 시간, 5: 서비스 시간, 6:주문 종료 시간]
        self.location = location #[Floor , Room #, 층의 절반]
        self.type = type
        self.size = size
        self.history = []

class Robot(object):
    def __init__(self, name, env, speed, customers,Operator, end_t = 120, capacity = 4, cal_type = 1):
        self.name = name
        self.env = env
        self.speed = speed
        self.capacity = capacity
        self.visited_nodes = [[1,1]]
        self.end_t = end_t
        self.history = []
        self.return_t = 0
        self.Process = None
        env.process(self.Runner(env, Operator, customers, cal_type = cal_type))


    def RunTrip(self, env, trip, customers):
        print(self.name, ';RunTrip 시작',trip)
        for name in trip:
            customer = customers[name]
            move_t = distance(self.visited_nodes[-1],customer.location)
            yield env.timeout(move_t)
            customer.time_info[3] = env.now
            self.history.append([env.now, customer.name, customer.location, 'C'])
            if customer.time_info[5] > 0:
                yield env.timeout(customer.time_info[5])
                customer.time_info[4] = env.now
            self.visited_nodes.append(customer.location)
            input('T:{} ; 로봇 {} ;고객 {} 도착'.format(env.now, self.name, name))
        self.history.append([env.now, 0, 'Trip End'])
        input('T:{} ; 로봇 {} ;트립 완료'.format(env.now, self.name))


    def Runner(self, env, Operator, Customers, cal_type = 1):
        while self.env.now < self.end_t:
            print(Operator.Route)
            if len(Operator.Route) > 0:
                trip = Operator.Route[0][1]
                trip_names = []
                for info in trip:
                    trip_names.append(info[3])
                input('로봇 {} ; T {} ; 경로 {}추가'.format(self.name, int(self.env.now), trip))
                Operator.history.append(Operator.Route[0][1])
                del Operator.Route[0]
                print('로봇{} 수행 후 경로 {}'.format(self.name, Operator.Route))
                if cal_type == 1:
                    yield env.process(self.RunTrip(env, trip, Customers))
                else:
                    yield env.process(self.RunTrip(env, trip_names, Customers))
                #self.Process = env.process(self.RunTrip(trip[1], Customers))
                #yield self.Process
                print('로봇{} 지우고 난 후 경로 {}'.format(self.name, Operator.Route))
            else:
                input('T {} ; 로봇 {} '.format(int(self.env.now), self.name))
                yield self.env.timeout(2)
                input('T {} ; 로봇 {} ;운행 가능한 경로 없음; {}'.format(int(self.env.now), self.name, len(Operator.Route)))


    def RunTrigger(self,customers, Operator):
        try:
            route = Operator.Route[-1][1]
            self.Process = self.env.process(self.Run(route, customers))
        except:
            yield self.timeout(3)
            input('T {} ; 운행 가능한 경로 없음; {}'.format(int(self.env.now), len(Operator.Route)))
