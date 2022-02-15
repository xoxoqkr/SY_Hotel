data_files = ['CustomerData_Case1_ex1']
cal_types = [1,2,3,4]
rider_nums = [3,4,5]
duration_types = [1,2]

ite_count = 0
for data in data_files:
    for rider_num in rider_nums:
        for duration_type in duration_types:
            for cal_type in cal_types:
                #input('시작')
                exec(open('Run_SY.py', encoding='UTF8').read(),globals().update(data_file=data, package_type = cal_type,robot_num = rider_num, duration_index = duration_type, ite_count = ite_count))
                ite_count += 1
            input('결과확인')