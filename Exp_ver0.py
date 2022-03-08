from numpy import arange
data_files = []
for i in [13,23,33,43]:#[13,23,33,43]:
    for j in range(0,2):
        #data_files.append('CustomerData_Case'+str(i)+'_ex'+str(j))
        data_files.append('RC_0_' + str(i) + '_' + str(j))
weights = []
for i in list(arange(0,1,0.2)):
    weights.append([1-i, i])
#data_files = ['CustomerData_Case1_ex1']
cal_types = [3]
rider_nums = [3]
duration_types = [1]

ite_count = 0
for data in data_files:
    for rider_num in rider_nums:
        for duration_type in duration_types:
            for cal_type in cal_types:
                for weight in weights:
                    print(cal_type, weight)
                    #input('연산 시작')
                    exec(open('Run_SY.py', encoding='UTF8').read(),globals().update(data_file=data, package_type = cal_type,robot_num = rider_num,
                                                                                    duration_index = duration_type, ite_count = ite_count, weight = weight))
                    ite_count += 1
                    print(cal_type, weight)
                    #input('연산종료')
                #input('결과확인')