from scipy.optimize import linprog
import numpy as np
import pandas as pd

# 加载数据
dict_data = {'pcvr': [0.026, 0.109, 0.042, 0.020, 0.095],
             'pcvr': [0.040, 0.011, 0.005, 0.043, 0.006],
             'wp':   [0.180, 0.209, 0.454, 0.434, 0.927],
             'ecpm': [0.021, 0.024, 0.005, 0.017, 0.011]}
df = pd.DataFrame(dict_data)

n = 100000000 # 样本数量
B = 100000.0  # 广告预算
C = 2         # 点击单价约束

obj = (-df.pctr * df.pcvr).tolist()
bnd = [(0, 1.0) for i in range(n)]

lhs_linq = [df.wp.tolist(), (df.wp - C*df.ctr).tolist()]
rhs_linq = [B, 0]

opt = linprog(c=obj, A_ub=lhs_linq, b_ub=rhs_linq, bounds=bnd, method="highs-ipm")

df['dot']   = df.pctr * df.pcvr * opt.x
df['price'] = df.wp - C * df.pctr
print("成本： ", np.sum(opt.x * df.wp) / np.sum(opt.x * df.pctr))
print("消耗： ", np.sum(opt.x * df.wp))
print("竞价成功数：", np.sum(opt.x))
print("最终转化量：", np.sum(df['dot']))