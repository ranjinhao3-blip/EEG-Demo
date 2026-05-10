  

import numpy as np
import matplotlib.pyplot as plt

# 采样率（每秒采多少点）
fs = 250  

# 时间轴（2秒）
t = np.arange(0, 2, 1/fs)

# 模拟脑电信号
alpha_wave = np.sin(2 * np.pi * 10 * t)  # α波（10Hz，放松）
beta_wave = np.sin(2 * np.pi * 20 * t)   # β波（20Hz，专注）

# 加一点随机噪声（更像真实信号）
noise = 0.3 * np.random.randn(len(t))

# 合成信号
signal = alpha_wave + 0.5 * beta_wave + noise

# 画图
plt.plot(t, signal)
plt.title("Simulated EEG Signal")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.show()
from scipy.fft import fft, fftfreq

# 信号长度
N = len(signal)



# 做FFT
yf = fft(signal)
xf = fftfreq(N, 1/fs)

# 只取一半（正频率）
xf = xf[:N//2]
yf = abs(yf[:N//2])

# 画频谱图
plt.plot(xf, yf)
plt.title("Frequency Spectrum")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Power")
plt.show()
# 定义一个函数：计算某个频段的能量
def band_power(xf, yf, low, high):
    idx = (xf >= low) & (xf <= high)
    return sum(yf[idx])

# 计算α和β能量
alpha_power = band_power(xf, yf, 8, 13)
beta_power = band_power(xf, yf, 13, 30)

print("Alpha Power:", alpha_power)
print("Beta Power:", beta_power)
if beta_power > alpha_power:
    state = "Focused（专注）"
else:
    state = "Relaxed（放松）"

print("State:", state)
import matplotlib.pyplot as plt

labels = ['Alpha', 'Beta']
values = [alpha_power, beta_power]

plt.bar(labels, values)
plt.title("EEG Band Power")
plt.show()