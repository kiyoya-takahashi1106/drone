import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# データポイント
x_lst = np.array([158.6938776, 246.8571429, 299.755102, 335.0204082, 352.6530612, 370.2857143, 380.8653061, 387.9183673, 416.1306122, 419.6571429, 423.1836735, 426.7102041, 430.2367347, 433.7632653])
y_lst = np.array([0.384615385, 0.555555556, 0.714285714, 0.909090909, 1.111111111, 1.25, 1.428571429, 1.666666667, 1.666666667, 1.818181818, 2, 2.222222222, 2.5, 2.857142857])
test_lst = np.array([78, 54, 42, 33, 27, 24, 21, 18, 18, 16.5, 15, 13.5, 12, 10.5])

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
    print((0.003051 * np.exp(0.015006 * x) + 0.430705)*test)