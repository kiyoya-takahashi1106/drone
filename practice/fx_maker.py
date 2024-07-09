import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# データポイント
x_lst = np.array([185.143, 267.429, 308.571, 329.143, 349.714, 362.057, 370.286, 378.514])
y_lst = np.array([0.384615385, 0.555555556, 0.714285714, 0.909090909, 1.111111111, 1.251, 1.428571429, 1.666666667])
test_lst = np.array([78, 54, 42, 33, 27, 24, 21, 18])

# 関数の定義（指数関数）
def exponential_func(x, a, b, c):
    return a * np.exp(b * x) + c

# 初期パラメータを設定してフィッティング
initial_guess = (1, 0.01, 0)
params, covariance = curve_fit(exponential_func, x_lst, y_lst, p0=initial_guess, maxfev=2000)

# フィッティングしたパラメータ
a, b, c = params

# フィッティングした関数をプロットするためのx値
x_fit = np.linspace(min(x_lst), max(x_lst), 500)
y_fit = exponential_func(x_fit, a, b, c)

# プロット
plt.scatter(x_lst, y_lst, label='Data Points')
plt.plot(x_fit, y_fit, label=f'Fitted Exponential Function: y = {a:.3e} * exp({b:.3e} * x) + {c:.3e}', color='red')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.title('Exponential Fit')
plt.show()

# フィッティングした関数の式を表示
print(f"Fitted Exponential Function: y = {a:.6f} * exp({b:.6f} * x) + {c:.6f}")



# 試してみる
for x, test in zip(x_lst, test_lst):
    print((0.001265 * np.exp(0.018237 * x) + 0.367068) * test)
