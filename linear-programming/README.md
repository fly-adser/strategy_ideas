## 优化问题
问题描述：预算和点击单价约束下，最大化转化量  

$$
\begin{aligned}
\max_{x_{i}} & \sum_{i=1,...,N}x_{i}\cdot CTR_{i} \cdot CVR_{i} \\
s.t. & \sum_{i=1,...,N}x_{i} \cdot wp_{i} \leq B \\
& \frac{\sum_{i=1,...,N}x_{i}\cdot wp_{i}}{\sum_{i=1,...,N}x_{i}\cdot CTR_{i}} \leq C \\
& 0 \leq x_{i} \leq 1, \forall i
\end{aligned}
$$

## 线性规划直接求解
文件名：LinearProgramming    
API使用说明：  
```python
def linprog(c, A_ub=None, b_ub=None, A_eq=None, b_eq=None,
            bounds=None, method='highs-ds', callback=None,
            options=None)

c：目标函数的决策变量对应的系数向量。这里指的是 -CTR * CVR 
A_ub：不等式约束组成的决策变量系数矩阵。当不等式中含有分式时，需要将分式转化为不含
      分式的不等式  
b_ub：由A_ub对应不等式顺序的阈值向量
A_eq：等式约束组成的决策变量系数矩阵
b_eq：由A_ub对应等式顺序的阈值向量
bounds：表示决策变量x连续的定义域的n×2维矩阵，None表示无穷
method：求解方法，建议选择'highs', 'highs-ds', 'highs-ipm'中的一个  
callback：回调函数。如果提供了回调函数，则每次迭代至少调用一次(非必选项)
options：可选择的求解器字典(非必选项)
```

## 差分进化近似求解  
文件名：DiffEvolutionProgramming  
近似问题推导。其核心是通过函数逼近 $x_{i}$ ，其推导过程如下：  
- 根据对偶理论推导出其最优出价公式为： $bid = \alpha * pctr * pcvr + \beta * C * pctr$
- 将优化问题中的 $x_{i}$ 表示为：  $x_{i}=S(bid_{i} - wp_{i})$
- 找到一个可微函数逼近示性函数 $S$

[差分进化算法](https://zhuanlan.zhihu.com/p/462522469)    
[API介绍文档](https://vimsky.com/examples/usage/python-scipy.optimize.differential_evolution.html)
