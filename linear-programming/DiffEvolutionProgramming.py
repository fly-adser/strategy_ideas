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
        pctr = block[:,0]
        pcvr = block[:,1]
        wp   = block[:,2]
        alpha = x[i]
        beta  = x[i+int(n/inteval)]
        bid_wp = alpha * pctr * pcvr + beta * C * pctr - wp
        xij = sigmoidN(bid_wp)
        val = pctr * pcvr * xij
        total += np.sum(val)
    return -total

def constraint_ueq(x):
    datas = df.values
    cost = 0.0
    click = 0.0
    for i in range(int(n / inteval)):
        block = datas[i*inteval:i*inteval+inteval, :]
        pctr = block[:,0]
        pcvr = block[:,1]
        wp   = block[:,2]
        alpha = x[i]
        beta  = x[i+int(n/inteval)]
        bid_wp = alpha * pctr * pcvr + beta * C * pctr - wp
        xij = sigmoidN(bid_wp)
        
        click += np.sum(xij*pctr)
        cost += np.sum(xij*wp)
        
    return [cost-B, cost-C*click]

def calc(x):
    datas = df.values
    cost = 0.0
    click = 0.0
    total = 0.0
    xlist = []
    for i in range(int(n / inteval)):
        block = datas[i*inteval:i*inteval+inteval, :]
        pctr = block[:,0]
        pcvr = block[:,1]
        wp   = block[:,2]
        alpha = x[i]
        beta  = x[i+int(n/inteval)]
        bid_wp = alpha * pctr * pcvr + beta * C * pctr - wp
        xij = sigmoidN(bid_wp)
        xlist += xij.tolist()
        val = pctr * pcvr * xij
        total += np.sum(val)
        click += np.sum(xij*pctr)
        cost += np.sum(xij*wp)
        
    return total, cost, cost/click, np.sum(xlist)

bounds = Bounds([0. for i in range(m)], [10000.0 for i in range(int(m/2))] + [1.0 for i in range(int(m/2))])
nlc = NonlinearConstraint(constraint_ueq, [-np.inf, -np.inf], [0.0,0.0])
result = differential_evolution(obj_func,bounds,constraints=(nlc),seed=1)
x = result.x

print(calc(x))
print(x)
