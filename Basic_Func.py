# -*- coding: utf-8 -*-
import math
import itertools
import copy
import operator
from TripSelectionProblem import TripSelectionProblem
def distance(x, y):
    return round(math.sqrt((x[0]-y[0])**2 + (x[1]-y[1])**2),4)

def distance2(bf, af, speed = 1, floor_t = 2):
    # x = [floor, Room #]
    # y = [floor, Room #]
    ev_waits = [[1,15],[4,0],[17,6]] #층 별 e/v 기다리는 시간(sec)
    between_room_distances = [[4,3],[10,3],[14,3.5],[17,4]] #층 별 방 사이 이동 시간(sec)
    floor_room_infos = [[1,0],[4,12],[10,12],[14,10],[17,9]] #층 별 라인에 있는 방 수
    res = 0
    if bf[0] == af[0]:
        between_room_distance = ValueFinder(bf[0], between_room_distances)
        move_t = ((af[1] - bf[1]) * between_room_distance) / speed
        f1 = ValueFinder(bf[0], floor_room_infos)
        print('f1',f1,'bf[1]',bf,'af[1]',af)
        try:
            if bf[1] // f1 == af[1] // f1: #같은 라인이라면
                pass
            else:
                move_t += 1.5 #1.5 = 라인 사이 거리
                move_t -= between_room_distance
        except:
            input('에러 확인')
        res = between_room_distance + move_t
    else:
        ev_wait_t = ValueFinder(bf[0], ev_waits) + 4#4는 e/v타고 내리는 시간
        horizontal_move = abs(af[1] - bf[1])*floor_t + ev_wait_t #2 : 층간 이동 시간
        move_t1 = 0
        move_t2 = 0
        #bf에서 e/v까지
        if bf[0] == 1:
            move_t1 += 7 #1층 로비에서 e/v까지
        else:
            bf_between_room_distance = ValueFinder(bf[0], between_room_distances)
            f1 = ValueFinder(bf[0], floor_room_infos)
            if bf[1] <= f1:
                move_t1 = ((f1 - bf[1])*bf_between_room_distance) / speed
            else:
                move_t1 = ((f1*2 - bf[1]) * bf_between_room_distance) / speed
        # e/v에서 af까지
        if af[0] == 1:
            move_t2 += 7 #1층 로비에서 e/v까지
        else:
            af_between_room_distance = ValueFinder(af[0], between_room_distances)
            f2 = ValueFinder(af[0], floor_room_infos)
            if af[1] <= f1:
                move_t2  += ((f2 - af[1])*af_between_room_distance) / speed
            else:
                move_t2 += ((f2*2 - af[1])*af_between_room_distance) / speed
            res = move_t1 + ev_wait_t + horizontal_move + move_t2
    if af[0] > 0:
        res += 45
    return res

def ValueFinder(value, infos):
    res = 0
    for info in infos:
        if value <= info[0]:
            res = info[1]
            break
        else:
            pass
    return res


def RouteTimeWithTimePenalty(trip_data, customers, speed = 1, now_t = 0, cal_type = 1):
    route_t = 0
    TW_violation = []
    if cal_type == 2:
        trip = []
        for info in trip_data:
            trip.append(info[3])
    else:
        trip = trip_data
    print('trip_data',trip_data)
    print('trip',trip)
    for index in range(1,len(trip)):
        bf = customers[trip[index - 1 ]]
        af = customers[trip[index]]
        if cal_type == 1:
            move_t = round(distance(bf.location,af.location)/speed,4)
        else:
            print(customers[trip[index - 1 ]], '->',customers[trip[index]])
            move_t = distance2(bf.location, af.location)
        print('move_t {}'.format(move_t))
        route_t += move_t + af.time_info[5]
        violated_t = now_t + route_t - af.time_info[6]
        #if af > 0:
        #    route_t += 45 #서비스 시간
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


def TripBuilder2(customers, ava_customer_names,  robot_capacity = 5):
    customer_names = []
    #1 가능한 모든 고객 조합 탐색
    for customer_name in ava_customer_names:
        customer_names.append(customer_name)
    raw_trips = copy.deepcopy(list(itertools.combinations(customer_names, robot_capacity)))
    trips = []
    #2탐색한 조합을 경로로 구성
    for trip in raw_trips:
        ct_infos = []
        for customer_name in trip:
            #input('확인 {} {}'.format(trip,customer_name))
            ct = customers[customer_name]
            #input('확인 2{}'.format(ct))
            ct_infos.append([ct.type,ct.location[0],ct.location[1],ct.name])
        ct_infos.sort(key = operator.itemgetter(0,1,2))
        route = ct_infos
        #route = sorted(ct_infos, key=lambda x: x[2])
        route.insert(0,[0,0,0,0])
        route.append([0,0,0,0])
        trips.append(route)
        #input('경로 확인{}'.format(route))
    #res = sorted(trips, key=lambda x: x[2])
    res = trips
    #input('경로 확인{}'.format(res[:5]))
    return res



def TripsScore(trips, customers, speed = 1, now_t = 0, cal_type = 1):
    scores = []
    index = 0
    for trip in trips:
        #input('정보1 {}'.format(trip))
        route_time, tw_penalty = RouteTimeWithTimePenalty(trip, customers, speed = speed, now_t = now_t, cal_type = cal_type)
        scores.append([index, trip, route_time, round(sum(tw_penalty),4),len(tw_penalty)]) #[index, trip, 라우트 시간, tw시간,tw위반 고객 수]
        index += 1
        #input('정보2 {}'.format(scores[-1]))
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


def RouteRobotAssignSolver(robots, trip_infos, customers, assign_type = 'greedy', cal_type = 1):
    selected_trip_infos = []
    if assign_type == 'greedy':
        selected_customer_names = []
        trip_infos.sort(key=operator.itemgetter(2))
        select_count = 0
        for trip_info in trip_infos:
            if cal_type == 1:
                test_names = trip_info[1][1:len(trip_info[1])-1]
            else:
                test_names = []
                for info in trip_info[1][1:len(trip_info[1])-1]:
                    test_names.append(info[3])
            print('{};{};{};{}'.format(selected_customer_names, type(selected_customer_names),trip_info[1],type(trip_info[1])))
            if len(set(selected_customer_names) & set(test_names)) == 0:
                selected_trip_infos.append(trip_info)
                selected_customer_names += test_names
                select_count += 1
                input('선택 됨 {} ; {}'.format(selected_customer_names, trip_info[1]))
            if select_count >= len(robots):
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

def SystemRunner2(env, Robots, Customers, Operator, assign_type, speed = 1, interval = 5, end_t = 800):
    print('Start')
    while env.now < end_t:
        available_robot_names = ComeBackRobot(env.now, Robots, interval)
        print('운행가능로봇:',available_robot_names)
        if len(available_robot_names) > 0:
            customer_names = AvailableCustomer(Customers)
            all_trips = TripBuilder2(Customers,customer_names, robot_capacity= Robots[available_robot_names[0]].capacity)
            print(all_trips[:10])
            trips = all_trips
            input('체크')
            """
            trips = []
            for trip in all_trips:
                print('경로{}검토 시작'.format(trip))
                feasibility, trip_type = TripValidationChecker(trip, Customers, type_thres=5)
                if feasibility == True:
                    print('성공')
                    trips.append(trip)            
            """
            trip_infos = TripsScore(trips, Customers, speed=speed, now_t=env.now, cal_type=2)
            print('로봇들',Robots)
            selected_trip_infos = RouteRobotAssignSolver(Robots, trip_infos, Customers, assign_type=assign_type, cal_type=2)
            Operator.Route += selected_trip_infos
        yield env.timeout(interval)
        input('T {} 인터벌 끝'.format(int(env.now)))