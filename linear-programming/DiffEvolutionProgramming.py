import numpy as np
import pandas as pd
from scipy.optimize import LinearConstraint, Bounds, rosen, differential_evolution, NonlinearConstraint

# 加载数据
dict_data = {'pcvr': [0.026, 0.109, 0.042, 0.020, 0.095],
             'pcvr': [0.040, 0.011, 0.005, 0.043, 0.006],
             'wp':   [0.180, 0.209, 0.454, 0.434, 0.927],
             'ecpm': [0.021, 0.024, 0.005, 0.017, 0.011]}
df = pd.DataFrame(dict_data)

n = 10000000 #样本量
N = 50 #近似函数参数
interval = n #每隔多少样本用一套参数
m = int(n / interval * 2)
B = 100000.0
C = 2

def sigmoidN(x):
    return 1.0 / (1 + np.exp(-N * x))

def obj_func(x):
    datas = df.values
    total = 0.0
    for i in range(int(n / interval)):
        block = datas[i*interval: i*interval+interval, :]