# -*- coding: utf-8 -*-
import math
import itertools
import copy
import operator
from TripSelectionProblem import TripSelectionProblem
import random


def distance(x, y):
    return round(math.sqrt((x[0]-y[0])**2 + (x[1]-y[1])**2),4)

def distance2_org(bf, af, speed = 3600, floor_t = 2/60):
    # x = [floor, Room #]
    # y = [floor, Room #]
    #speed = m/hr
    ev_waits = [[1,15/60],[4,0],[17,6/60]] #층 별 e/v 기다리는 시간(sec)
    between_room_distances = [[4,3],[10,3],[14,3.5],[17,4]] #층 별 방 사이 이동 거리 (m)
    floor_room_infos = [[1,0],[4,12],[10,12],[14,10],[17,9]] #층 별 라인에 있는 방 수
    res = 0
    if bf[0] == af[0]:
        between_room_distance = ValueFinder(bf[0], between_room_distances)
        move_t = ((af[1] - bf[1]) * between_room_distance)
        f1 = ValueFinder(bf[0], floor_room_infos)
        #print('f1',f1,'bf[1]',bf,'af[1]',af)
        try:
            if bf[1] // f1 == af[1] // f1: #같은 라인이라면
                pass
            else:
                move_t += 1.5 #1.5 = 라인 사이 거리
                move_t -= between_room_distance
        except:
            if bf[0] == 1 and af[0] == 1:
                pass
            else:
                input('에러 확인')
        res = move_t/speed
    else:
        ev_wait_t = ValueFinder(bf[0], ev_waits) + 4/60 #4는 e/v타고 내리는 시간
        horizontal_move = abs(af[1] - bf[1])*floor_t  #2 : 층간 이동 시간
        move_t1 = 0
        move_t2 = 0
        #bf에서 e/v까지
        if bf[0] == 1:
            move_t1 += 7 #1층 로비에서 e/v까지
        else:
            bf_between_room_distance = ValueFinder(bf[0], between_room_distances)
            f1 = ValueFinder(bf[0], floor_room_infos)
            if bf[1] <= f1:
                move_t1 = ((f1 - bf[1])*bf_between_room_distance)
            else:
                move_t1 = ((f1*2 - bf[1]) * bf_between_room_distance)
        # e/v에서 af까지
        if af[0] == 1:
            move_t2 += 7 #1층 로비에서 e/v까지
        else:
            af_between_room_distance = ValueFinder(af[0], between_room_distances)
            f2 = ValueFinder(af[0], floor_room_infos)
            if af[1] <= f2:
                move_t2  += ((f2 - af[1])*af_between_room_distance)
            else:
                move_t2 += ((f2*2 - af[1])*af_between_room_distance)
            res = move_t1/speed + ev_wait_t + horizontal_move + move_t2/speed
    if af[0] > 0: #서비스 시간
        res += 45/60
    if 1 <= bf[0] <= 4 and af[0] == 1: #todo: 격리자 주문 수행 후 1층으로 이동하는 경우, 소독 시간이 추가로 필요함.
        res += 20/60
    return res


def distance2(bf, af, speed = 3600, floor_t = 2/60):
    # x = [floor, Room #]
    # y = [floor, Room #]
    #speed = m/hr
    ev_waits = [[1,15/60],[4,0],[17,6/60]] #층 별 e/v 기다리는 시간(sec)
    between_room_distances = [[4,3],[10,3],[14,3.5],[17,4]] #층 별 방 사이 이동 거리 (m)
    floor_room_infos = [[1,0],[4,24],[10,24],[14,20],[17,16]] #층 별 라인에 있는 방 수
    res = 0
    line_info = {0:0,1:1,2:1,3:0} #[[0,3],[1,2]]
    if bf[0] == af[0]:#같은 층이라면
        between_room_distance = ValueFinder(bf[0], between_room_distances)
        move_d = 0
        #move_t = ((af[1] - bf[1]) * between_room_distance)
        f1 = ValueFinder(bf[0], floor_room_infos)/2
        #수평이동
        tem = [bf[1], af[1]]
        tem.sort()
        if tem[0] // f1 == tem[1]// f1: #같은 쪽이라면
            if tem[1] < f1: #오른쪽
                val = (tem[1], tem[1] - (f1 / 2))
            else:  # 왼쪽
                val = (tem[1], tem[1] - f1)
            move_d += val * between_room_distance
        else: #다른 쪽 이라면
            val_right = (tem[0], tem[0] - (f1 / 2))
            val_left = (tem[1], tem[1] - f1)
            move_d += (val_right + val_left) * between_room_distance
        if line_info[tem[0] // (f1/2)] == line_info[tem[1] // (f1/2)]:
        #if (tem[0] // (f1/2) in line_info[0] and tem[0] // (f1/2) in line_info[0]) or tem[0] // (f1/2) in line_info[1] and tem[0] // (f1/2) in line_info[1]):
            #같은 라인임.
            pass
        else:
            move_d += 1.5
        res = move_d/speed
    else:
        ev_wait_t = ValueFinder(bf[0], ev_waits) + 4/60 #4는 e/v타고 내리는 시간
        vertical_move_t = abs(af[0] - bf[0])*floor_t  #2 : 층간 이동 시간
        move_d1 = 0
        move_d2 = 0
        #bf에서 e/v까지
        if bf[0] == 1:
            move_d1 += 7 #1층 로비에서 e/v까지
        else:
            bf_between_room_distance = ValueFinder(bf[0], between_room_distances)
            f1 = ValueFinder(bf[0], floor_room_infos)/2
            if bf[1] <= f1:
                val = max(bf[1], bf[1] - (f1/2))
                #move_d1 = (val*bf_between_room_distance)
            else:
                val = max(bf[1], bf[1] - f1)
                #move_d1 = ((f1*2 - bf[1]) * bf_between_room_distance)
            move_d1 = (val * bf_between_room_distance)
        # e/v에서 af까지
        if af[0] == 1:
            move_d2 += 7 #1층 로비에서 e/v까지
        else:
            af_between_room_distance = ValueFinder(af[0], between_room_distances)
            f2 = ValueFinder(af[0], floor_room_infos)/2
            if af[1] <= f2:
                val = max(af[1], af[1] - (f2 / 2))
                #move_t2  += ((f2 - af[1])*af_between_room_distance)
            else:
                val = max(af[1], af[1] - f2)
                #move_t2 += ((f2*2 - af[1])*af_between_room_distance)
            move_d2 = (val * af_between_room_distance)
            res = move_d1/speed + ev_wait_t + vertical_move_t + move_d2/speed
    if af[0] > 0: #서비스 시간
        res += 45/60
    if 1 <= bf[0] <= 4 and af[0] == 1: #todo: 격리자 주문 수행 후 1층으로 이동하는 경우, 소독 시간이 추가로 필요함.
        res += 20/60
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
    #print('trip_data',trip_data)
    #print('trip',trip)
    for index in range(1,len(trip)):
        bf = customers[trip[index - 1 ]]
        af = customers[trip[index]]
        if cal_type == 1:
            move_t = round(distance(bf.location,af.location)/speed,4)
        else:
            #print(customers[trip[index - 1 ]], '->',customers[trip[index]])
            move_t = distance2(bf.location, af.location)
        #print('move_t {}'.format(move_t))
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
        if now_t <= robot.return_t < interval or robot.idle == True:
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
        size = 0
        for customer_name in trip:
            #input('확인 {} {}'.format(trip,customer_name))
            ct = customers[customer_name]
            #input('확인 2{}'.format(ct))
            size += ct.size
            ct_infos.append([ct.type,ct.location[0],ct.location[1],ct.name])
        if size > 4 or len(ct_infos) == 0:
            continue
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


def InputCalculator2(trip_infos, customer_names):
    D = []
    S = []
    P = []

    for customer_name in customer_names:
        tem = []
        for trip_info in trip_infos:
            trip_customers = []
            for info in trip_info[1]:
                if info[3] > 0:
                    trip_customers.append(info[3])
            if customer_name in trip_customers:
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
                print('선택 됨 {} ; {}'.format(selected_customer_names, trip_info[1]))
            if select_count >= len(robots):
                break
    else: #Assignment Problem
        #D계산
        if cal_type == 1:
            D,S,P = InputCalculator(trip_infos, customers)
        else:
            D,S,P = InputCalculator2(trip_infos, customers)
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

def SystemRunner2(env, Robots, Customers, Operator, assign_type, speed = 1, interval = 5, end_t = 800, cal_type = 2, thres = 0.2):
    print('Start')
    while env.now < end_t:
        available_robot_names = ComeBackRobot(env.now, Robots, interval)
        print('운행가능로봇:',available_robot_names)
        rho = len(Robots)/ len(AvailableCustomer(Customers))
        if len(available_robot_names) == 0:
            continue
        if rho > thres:
            customer_names = AvailableCustomer(Customers)
            all_trips = TripBuilder2(Customers,customer_names, robot_capacity= Robots[available_robot_names[0]].capacity)
            print(all_trips[:10])
            trips = all_trips
            #input('체크')
            trip_infos = TripsScore(trips, Customers, speed=speed, now_t=env.now, cal_type=cal_type)
            print('로봇들',Robots)
            selected_trip_infos = RouteRobotAssignSolver(Robots, trip_infos, Customers, assign_type=assign_type, cal_type=cal_type)
            Operator.Route += selected_trip_infos
        else:
            #로봇 대기 후 출발
            pass
        yield env.timeout(interval)
        print('T {} 인터벌 끝'.format(int(env.now)))

def ResultSave(Customers, Robots):
    #로봇 필요 산출 값
    robot_res = []
    for robot_name in Robots:
        robot = Robots[robot_name]
        robot_res.append([robot.name, len(self.served_customers), self.idle_t])
    #고객 필요 산출 값
    customer_t1 = []
    customer_t2 = []
    customer_t3 = []
    for customer_name in Customers:
        customer = Customers[customer_name]
        robot_res.append([customer.time_info])
        customer_t1.append(customer.time_info[1] - customer.time_info[0])
        customer_t2.append(customer.time_info[2] - customer.time_info[1])
        customer_t3.append(customer.time_info[3] - customer.time_info[2])
    try:
        ave_t1 = sum(customer_t1)/len(customer_t1)
    except:
        ave_t1 = 0
    try:
        ave_t2 = sum(customer_t2)/len(customer_t2)
    except:
        ave_t2 = 0
    try:
        ave_t3 = sum(customer_t3)/len(customer_t3)
    except:
        ave_t3 = 0
    customer_res = [len(customer_t3), ave_t1, ave_t2, ave_t3]
    return robot_res, customer_res