datas = list(range(10))
cal_types = [1,2,3]
rider_nums = [2,3]
for rider_num in rider_nums:
    for data_index in datas:
        for cal_type in cal_types:
            exec(open('Run_SY.py', encoding='UTF8').read(),globals().update(data_num=data_index, package_type = cal_type,robot_num = rider_num))
            #input('확인')