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
    floor_room_infos = [[1,0],[4,32],[10,32],[14,28],[17,20]] #층 별 라인에 있는 방 수
    res = 0
    line_info = {0:0,1:1,2:1,3:0} #[[0,3],[1,2]]
    if bf == [1,0] and af == [1,0]:
        return 0.1
    if bf[0] == af[0]:#같은 층이라면
        between_room_distance = ValueFinder(bf[0], between_room_distances)
        move_d = 0
        #move_t = ((af[1] - bf[1]) * between_room_distance)
        f1 = ValueFinder(bf[0], floor_room_infos)/2
        #수평이동
        tem = [bf[1], af[1]]
        tem.sort()
        #if 0 in tem:
        #    input(tem)
        if tem[0] // f1 == tem[1]// f1: #같은 쪽이라면
            if tem[1] < f1: #오른쪽
                val = max(tem[1], tem[1] - (f1 / 2))
            else:  # 왼쪽
                val = max(tem[1], tem[1] - f1)
            move_d += val * between_room_distance
        else: #다른 쪽 이라면
            val_right = max(tem[0], tem[0] - (f1 / 2))
            val_left = max(tem[1], tem[1] - f1)
            move_d += (val_right + val_left) * between_room_distance
        if int((tem[0]-1) / (f1/2)) > 3 or int((tem[1]-1) / (f1/2)) > 3:
            print('에러 확인1', bf, af)
            print('에러확인2', tem[0], tem[1], f1, f1 / 2)
            print('에러확인3', int((tem[0] - 1) / (f1 / 2)), int((tem[1] - 1) / (f1 / 2)))
            input('확인필요')
        if line_info[int((tem[0]-1) / (f1/2))] == line_info[int((tem[1]-1) / (f1/2))]:
            pass
        else:
            move_d += 1.5
        res = move_d/speed
    else:
        ev_wait_t = ValueFinder(bf[0], ev_waits) + 4/60 + 1/60 #4는 e/v타고 내리는 시간 1/60 : 복도 0.5m
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
        violated_t = max(0, af.time_info[6]- (now_t + route_t))
        #if af > 0:
        #    route_t += 45 #서비스 시간
        if violated_t > 0 and customers[trip[index]].name > 0:
            TW_violation.append(violated_t)
    return route_t, TW_violation




def ComeBackRobot(now_t, robots, interval):
    robot_names = []
    print('시간 정보', now_t, now_t + interval)
    for robot_name in robots:
        robot = robots[robot_name]
        print('로봇 예상 도착 정보',robot.name, robot.return_t, robot.idle, robot.env.now)
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


def TripBuilderEnumerate(customers, ava_customer_names,  robot_capacity = 5, over_cts = []):
    customer_names = []
    #1 가능한 모든 고객 조합 탐색
    for customer_name in ava_customer_names:
        customer_names.append(customer_name)
    #print('탐색 대상 고객들:', customer_names,'2분 미만 고객:',over_cts)
    raw_trips = copy.deepcopy(list(itertools.combinations(customer_names, robot_capacity)))
    if len(over_cts) > 0:
        rev_raw_trip = []
        for info in raw_trips:
            rev = list(info) + over_cts
            rev_raw_trip.append(rev)
        raw_trips = rev_raw_trip
    #raw_trips += over_cts
    trips = []
    #2탐색한 조합을 경로로 구성
    for trip in raw_trips:
        ct_infos = []
        size = 0
        #print(trip)
        for customer_name in trip:
            #input('확인 {} {}'.format(trip,customer_name))
            ct = customers[customer_name]
            #input('확인 2{}'.format(ct))
            size += ct.size
            ct_infos.append([ct.type,ct.location[0],ct.location[1],ct.name])
        if size > 4 or len(ct_infos) == 0:
            continue
        ct_infos.sort(key = operator.itemgetter(0,1,2)) #todo 0223:고정된 순서가 아닌, TW를 고려한 최단 경로로 수정 할 것.
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


def TripBuilderHeuristic(customers, ava_customer_names, K = 1, sort_type = 1, robot_capacity = 5, now_t = 0):
    #sort_type = 1 :선입선출
    #sort_type = 2: LT가 작은 고객 부터 정렬
    customer_infos = []
    #1 가능한 모든 고객 조합 탐색
    for customer_name in ava_customer_names:
        customer_infos.append([customer_name, customers[customer_name].time_info[0], customers[customer_name].time_info[6] - now_t])
        print(customer_infos[-1])
        #[고객 이름, 고객 생성 시간, 남은 여유 시간]
    customer_infos.sort(key = operator.itemgetter(sort_type))
    trips = []
    for k in range(K):
        print('k',k)
        ct_count = 0
        try:
            size = 0
            trip = []
            for info in customer_infos[ct_count:]:
                print('info',info)
                ct = customers[info[0]]
                size += ct.size
                if size > robot_capacity:
                    print('break2?')
                    break
                trip.append([ct.type, ct.location[0], ct.location[1], ct.name])
                print('info2',trip[-1])
                ct_count += 1
            trip.sort(key=operator.itemgetter(0, 1, 2))
            trip.insert(0, [0, 1, 0, 0])
            trip.append([0, 1, 0, 0])
            trips.append(trip)
        except:
            break
        if ct_count >= len(customer_infos):
            break
    print('trips', trips)
    return trips


def TripsScore(trips, customers, speed = 1, now_t = 0, cal_type = 1):
    scores = []
    index = 0
    for trip in trips:
        #input('정보1 {}'.format(trip))
        route_time, tw_penalty = RouteTimeWithTimePenalty(trip, customers, speed = speed, now_t = now_t, cal_type = cal_type)
        trip_len = len(trip)-2
        scores.append([index, trip, route_time/trip_len, round(sum(tw_penalty),4)/trip_len,len(tw_penalty)]) #[index, trip, 라우트 시간, tw남은시간,tw위반 고객 수, trip고객 수]
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
        if customer.name > 0 and customer.time_info[1] == None and customer.canceal == False:
            res.append(customer.name)
    return res


def RouteRobotAssignSolver(robots, trip_infos, customers, assign_type = 'greedy', cal_type = 1, now_t = 0):
    selected_trip_infos = []
    if assign_type == 'greedy':
        selected_customer_names = []
        # [index, trip, 라우트 시간, tw 남은시간,tw위반 고객 수]
        # 2 : 경로가 짧은 순 / 3: 남은 시간이 촉박한 것.
        #trip_infos.sort(key=operator.itemgetter(5), reve)  # 경로 길이가 짧은 순으로 수행
        trip_infos.sort(key=operator.itemgetter(2)) #경로 길이가 짧은 순으로 수행
        print('현재 trip_info수{}'.format(len(trip_infos)))
        #input(trip_infos[:5])
        select_count = 0
        for trip_info in trip_infos:
            if cal_type == 1:
                test_names = trip_info[1][1:len(trip_info[1])-1]
            else:
                test_names = []
                for info in trip_info[1][1:len(trip_info[1])-1]:
                    test_names.append(info[3])
            #print('{};{};{};{}'.format(selected_customer_names, type(selected_customer_names),trip_info[1],type(trip_info[1])))
            if len(set(selected_customer_names) & set(test_names)) == 0:
                selected_trip_infos.append(trip_info)
                selected_customer_names += test_names
                for name in test_names:
                    customers[name].time_info[1] = now_t
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


def InsertMinCost(route, insert_customer):
    scores = []
    ava_seq = [[0,0,0],[0,1,1],[1,0,0],[1,1,0],[1,1,1]]
    all0_para = True
    for info in route:
        if info[0] == 1:
            all0_para == False
            break
    for pos in range(1,len(route)):
        seq = [route[pos-1][0], insert_customer.type,route[pos][0]]
        if seq in [ava_seq]:
            dist1 = distance(route[pos-1][1:3],insert_customer.location)
            dist2 = distance(insert_customer.location, route[pos][1:3])
            scores.append([dist1 + dist2, pos])
        elif seq == [0, 1, 0] and all0_para == True:
            dist1 = distance(route[pos-1][1:3],insert_customer.location)
            dist2 = distance(insert_customer.location, route[pos][1:3])
            add_t = 45
            scores.append([dist1+dist2+add_t, pos])
        else:
            pass
    scores.sort()
    pos = scores[0][0]
    rev_route = copy.deepcopy(route)
    rev_route.insert(pos, [insert_customer.type, insert_customer.location[0],insert_customer.location[1], insert_customer.name])
    return rev_route



def SystemRunner(env, Robots, Customers, Operator, assign_type, speed = 1, interval = 5, end_t = 800, cal_type = 2, thres = 0, package_type = 5, wait_t = 0, urgent_ratio = 0.2):
    #package_type = 1 :선입선출
    #package_type = 2 : LT가 작은 고객 부터 정렬
    #package_type = 5 : 가능한 모든 경로 구해보기
    print('Start')
    while env.now < end_t:
        available_robot_names = ComeBackRobot(env.now, Robots, interval)
        if len(available_robot_names) > 1:
            print('로봇 대수가 2대인 상황')
        if len(available_robot_names) > 0:
            print('운행가능로봇:',available_robot_names)
        if len(available_robot_names) == 0:
            yield env.timeout(interval)
            continue
        rho = len(AvailableCustomer(Customers)) /len(available_robot_names)
        if rho > thres:
            customer_names = AvailableCustomer(Customers)
            print('탐색시작::고객수', len(customer_names))
            robot_capa = Robots[available_robot_names[0]].capacity
            urgent_ct_names = []
            for customer_name in customer_names:
                customer = Customers[customer_name]
                q_para = 0.2
                if 0 < customer.location[0] < 5: #격리고객의 경우 더 우선적으로 급한 고객에 할당되도록
                    q_para = 0.5
                    urgent_ct_names.append(customer.name)
                #if customer.time_info[6] - env.now < customer.duration *urgent_ratio * q_para:
                #    urgent_ct_names.append(customer_name)
                #    pass
            if package_type in [1,2]: #휴리스틱
                print('휴리스틱')
                all_trips = TripBuilderHeuristic(Customers, customer_names, K=len(available_robot_names), sort_type=package_type, robot_capacity=robot_capa, now_t=env.now)
                #input('all_trips{}'.format(all_trips))
            elif package_type == 3: #긴급한 주문이 존재시, 해당 주문을 먼저 집어 넣는 경우
                #input('확인1')
                all_trips = []
                if len(urgent_ct_names) == 0:
                    #input('확인2')
                    for length in range(1,robot_capa):
                        tem = TripBuilderEnumerate(Customers,customer_names, robot_capacity= length)
                        all_trips += tem
                else:
                    rev_ava_customer_names = [elem for elem in customer_names if elem not in urgent_ct_names]
                    #input(rev_ava_customer_names)
                    if robot_capa - len(urgent_ct_names) > 0:
                        #input('확인3')
                        for length in range(1,robot_capa - len(urgent_ct_names)):
                            #input(length1)
                            tem = TripBuilderEnumerate(Customers,rev_ava_customer_names, robot_capacity= length, over_cts= urgent_ct_names)
                            all_trips += tem
                    else:
                        for length in range(1,robot_capa):
                            tem = TripBuilderEnumerate(Customers, urgent_ct_names, robot_capacity=length)
                            all_trips += tem
            elif package_type == 4: #경로 효율성만을 고려하는 경우
                all_trips = []
                for length in range(1, robot_capa):
                    tem = TripBuilderEnumerate(Customers, customer_names, robot_capacity=length)
                    all_trips += tem
            else:
                pass
            trip_infos = TripsScore(all_trips, Customers, speed=speed, now_t=env.now, cal_type=cal_type)
            #print('trip_infos',trip_infos)
            print('T {}::로봇 수 {} :: 고객 수{}'.format(int(env.now),len(available_robot_names),len(customer_names)))
            selected_trip_infos = RouteRobotAssignSolver(Robots, trip_infos, Customers, assign_type=assign_type, cal_type=cal_type, now_t= env.now)
            Operator.Route += selected_trip_infos
        else:
            if wait_t > 0:
                for robot_name in available_robot_names:
                    Robots[robot_name].wait_t = wait_t #todo: t 시간 동안 들어온 로봇은 대기 후 출발시키는 기능
        print('P대기 시작 {}'.format(env.now))
        yield env.timeout(interval)
        print('P대기 끝 {}'.format(env.now))
        for trip in Operator.Route:
            for info in trip[1]:
                if type(info) != list:
                    print('구성 확인',info)
                    input(trip)
                #print('구성 확인', info)
                if info[3] > 0:
                    Customers[info[3]].time_info[1] = None
                    Customers[info[3]].time_info[7] = env.now
        Operator.Route = []
        #input('T {} 인터벌 끝'.format(int(env.now)))

def ResultSave(Customers, Robots, now_t):
    #로봇 필요 산출 값
    robot_res = []
    for robot_name in Robots:
        robot = Robots[robot_name]
        robot_res.append([robot.name, len(robot.served_customers), robot.idle_t, robot.trip_num, robot.idle_info])
    #고객 필요 산출 값
    customer_t1 = []
    customer_t2 = []
    customer_t3 = []
    customer_t4 = []
    customer_t5 = []
    customer_t6 = []
    q_customer_t1 = []
    q_customer_t2 = []
    q_customer_t3 = []
    n_customer_t1 = []
    n_customer_t2 = []
    n_customer_t3 = []
    unserved_customer_t = []
    served_count = 0
    tw_over_customer_count = 0
    q_served = 0
    n_served = 0
    customer_type = [-1,0] #0을 빼야하기 때문
    tw_satified_customer = [0,0]
    saved_ct_data = []
    for customer_name in Customers:
        customer = Customers[customer_name]
        saved_ct_data.append([customer.name] + customer.time_info[:4] +[customer.time_info[6]]+ customer.location)
        if customer.location[0] < 5:
            customer_type[0] += 1
        else:
            customer_type[1] += 1
        if customer.name == 0:
            continue
        if customer.time_info[3] != None:
            print('결과확인', customer.name, customer.time_info)
            if customer.time_info[1] == None:
                input('고객{} 시간정보{}'.format(customer.name, customer.time_info))
            else:
                #robot_res.append([customer.time_info])
                customer_t1.append(customer.time_info[1] - customer.time_info[0])
                customer_t2.append(customer.time_info[2] - customer.time_info[1])
                customer_t3.append(customer.time_info[3] - customer.time_info[2])
            if customer.time_info[3] > customer.time_info[6]:
                customer_t4.append(customer.time_info[3] - customer.time_info[6])
                customer_t5.append(customer.time_info[2] - customer.time_info[1])
                customer_t6.append(customer.time_info[3] - customer.time_info[2])
                tw_over_customer_count += 1
            else:
                pass
            if 1 < customer.location[0] <= 4 :
                q_customer_t1.append(customer.time_info[1] - customer.time_info[0])
                q_customer_t2.append(customer.time_info[2] - customer.time_info[1])
                q_customer_t3.append(customer.time_info[3] - customer.time_info[2])
                q_served += 1
                if customer.time_info[3] < customer.time_info[6]:
                    tw_satified_customer[0] += 1
            else:
                n_customer_t1.append(customer.time_info[1] - customer.time_info[0])
                n_customer_t2.append(customer.time_info[2] - customer.time_info[1])
                n_customer_t3.append(customer.time_info[3] - customer.time_info[2])
                n_served += 1
                if customer.time_info[3] < customer.time_info[6]:
                    tw_satified_customer[1] += 1
            served_count += 1
        else:
            unserved_customer_t.append(now_t - customer.time_info[0])
    print('서비스된 고객 수 :',served_count)
    res = []
    infos = [customer_t1,customer_t2,customer_t3,customer_t4,customer_t5,customer_t6,q_customer_t1,q_customer_t2,q_customer_t3,n_customer_t1,n_customer_t2,n_customer_t3,unserved_customer_t]
    for info in infos:
        ave_val = 0
        if len(info) > 0:
            ave_val = sum(info)/len(info)
        res.append(ave_val)
    customer_res = [len(customer_t3)] + res + [tw_over_customer_count, q_served, n_served] + tw_satified_customer + customer_type
    return robot_res, customer_res, saved_ct_data