# -*- coding: utf-8 -*-

from numpy import arange
import locale
from io import open
import sys
import importlib
# sys.setdefaultencoding() does not exist, here!
#importlib.reload()
#importlib.reload(sys)  # Reload does the trick!
#sys.setdefaultencoding('UTF8')

print(locale.getpreferredencoding())

#input('확인')
data_files = []
for i in [13,23,33]:#[13,23,33,43]:
    for j in range(0,2):
        #data_files.append('CustomerData_Case'+str(i)+'_ex'+str(j))
        data_files.append('RC_0_' + str(i) + '_' + str(j))

weights = []
for i in list(arange(0,1,0.2)):
    for j in list(arange(0,1,0.2)):
        weights.append([1-i, i*(1-j) , i*j])
#data_files = ['CustomerData_Case1_ex1']
cal_types = [4]
rider_nums = [2]
duration_types = [1]

ite_count = 0
for data in data_files:
    for rider_num in rider_nums:
        for duration_type in duration_types:
            for cal_type in cal_types:
                for weight in weights:
                    exec(open('Run_SY.py','rt',encoding='utf-8').read(), globals().update(data_file=data, package_type = cal_type,robot_num = rider_num,duration_index = duration_type, ite_count = ite_count, weight = weight))
                    #exec(open('Run_SY.py', encoding='UTF8').read(),
                    #     globals().update(data_file=data, package_type = cal_type,robot_num = rider_num,duration_index = duration_type, ite_count = ite_count, weight = weight))
                    ite_count += 1
                    print(cal_type, weight)
                    #input('연산종료')
                #input('결과확인')