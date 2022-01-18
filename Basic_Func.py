# -*- coding: utf-8 -*-
import math
import itertools
import copy
import operator
from TripSelectionProblem import TripSelectionProblem
def distance(x, y):
    return round(math.sqrt((x[0]-y[0])**2 + (x[1]-y[1])**2),4)


def RouteTimeWithTimePenalty(trip, customers, speed = 1, now_t = 0):
    route_t = 0
    TW_violation = []
    for index in range(1,len(trip)):
        bf = customers[trip[index - 1 ]]
        af = customers[trip[index]]
        move_t = round(distance(bf.location,af.location)/speed,4)
        route_t += move_t + af.time_info[5]
        violated_t = now_t + route_t - af.time_info[6]
        if violated_t > 0:
            TW_violation.append(violated_t)
    return route_t, TW_violation




def ComeBackRobot(now_t, robots, interval):
    robot_names = []
    for robot_name in robots:
        robot = robots[robot_name]
        if now_t <= robot.return_t < interval:
            robot_names.append(robot.name)
    return robot_names


def TripValidationChecker(route, customers, type_thres = 5):
    #1조건 #todo : 작동 방식 다시 확인 할 것.
    type1_indexs = []
    type2_indexs = []
    index = 0
    for name in route:
        customer = customers[name]
        if int(customer.type / type_thres) == 0:
            type1_indexs.append(index)
        else:
            type2_indexs.append(index)
        index += 1
    if len(type1_indexs) > 0 and len(type2_indexs) > 0:
        if max(type1_indexs) > min(type2_indexs):
            return False, None
        else:
            return True, 1
    elif len(type1_indexs) == 0:
        return True , 0
    else:
        return True , 1


def TripBuilder(customers, robot_capacity = 5):
    customer_names = []
    for customer_name in customers:
        customer_names.append(customer_name)
    raw_trips = copy.deepcopy(list(itertools.permutations(customer_names, robot_capacity)))
    trips = []
    for info in raw_trips:
        test = list(info)
        trips.append(test)
    for trip in trips:
        trip.insert(0,0)
        trip.append(0)
        #input('계산된 경로 {}'.format(trip))
    return trips


def TripsScore(trips, customers, speed = 1, now_t = 0):
    scores = []
    index = 0
    for trip in trips:
        route_time, tw_penalty = RouteTimeWithTimePenalty(trip, customers, speed = speed, now_t = now_t)
        scores.append([index, trip, route_time, round(sum(tw_penalty),4),len(tw_penalty)]) #[index, trip, 라우트 시간, tw시간,tw위반 고객 수]
        index += 1
    return scores #[[trip,score],...]

def InputCalculator(trip_infos, customer_names):
    D = []
    S = []
    P = []
    for customer_name in customer_names:
        tem = []
        for trip_info in trip_infos:
            if customer_name in trip_info[1]:
                tem.append(trip_info[0])
        D.append(tem)
    for trip_info in trip_infos:
        S.append(trip_info[2])
        P.append(trip_info[3])
    return D,S,P


def AvailableCustomer(customers):
    res = []
    for customer_name in customers:
        customer = customers[customer_name]
        if customer.name > 0 and customer.time_info[1] == None:
            res.append(customer.name)
    return res


def RouteRobotAssignSolver(robots, trip_infos, customers, assign_type = 'greedy'):
    selected_trip_infos = []
    if assign_type == 'greedy':
        selected_customer_names = []
        trip_infos.sort(key=operator.itemgetter(2))
        select_count = 0
        for trip_info in trip_infos:
            #input('{};{};{};{}'.format(selected_customer_names, type(selected_customer_names),trip_info[1],type(trip_info[1])))
            if len(set(selected_customer_names) & set(trip_info[1][1:len(trip_info[1])-1])) == 0:
                selected_trip_infos.append(trip_info)
                selected_customer_names += trip_info[1]
                select_count += 1
                input('선택 됨 {} ; {}'.format(selected_customer_names, trip_info[1]))
            if select_count > len(robots):
                break
    else: #Assignment Problem
        #D계산
        D,S,P = InputCalculator(trip_infos, customers)
        trip_names = TripSelectionProblem(D, S, P, len(robots))
        for trip_name in trip_names:
            selected_trip_infos.append(trip_infos[trip_name])
    return selected_trip_infos


def SystemRunner(env, Robots, Customers, Operator, assign_type, speed = 1, interval = 5, end_t = 800):
    print('Start')
    while env.now < end_t:
        available_robot_names = ComeBackRobot(env.now, Robots, interval)
        print('운행가능로봇:',available_robot_names)
        if len(available_robot_names) > 0:
            customer_names = AvailableCustomer(Customers)
            all_trips = TripBuilder(customer_names, robot_capacity= Robots[available_robot_names[0]].capacity)
            print(all_trips[:10])
            trips = []
            for trip in all_trips:
                print('경로{}검토 시작'.format(trip))
                feasibility, trip_type = TripValidationChecker(trip, Customers, type_thres=5)
                if feasibility == True:
                    print('성공')
                    trips.append(trip)
            trip_infos = TripsScore(trips, Customers, speed=speed, now_t=env.now)
            print('로봇들',Robots)
            selected_trip_infos = RouteRobotAssignSolver(Robots, trip_infos, Customers, assign_type=assign_type)
            Operator.Route += selected_trip_infos
        yield env.timeout(interval)
        input('T {} 인터벌 끝'.format(int(env.now)))
