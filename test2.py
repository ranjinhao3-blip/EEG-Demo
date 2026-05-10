import numpy as np

fs = 250  # 采样率

# 生成2秒信号
t = np.linspace(0, 2, 2*fs, endpoint=False)

alpha_wave = np.sin(2 * np.pi * 10 * t)
beta_wave = np.sin(2 * np.pi * 20 * t)

noise = 0.3 * np.random.randn(len(t))

signal = alpha_wave + 0.5 * beta_wave + noise

from scipy.fft import fft, fftfreq

def band_power(xf, yf, low, high):
    idx = (xf >= low) & (xf <= high)
    return sum(yf[idx])

def classify_eeg(signal,fs):

   

    N = len(signal)
    yf = fft(signal)
    xf = fftfreq(N,1/fs)
    xf = xf[:N//2]
    yf = abs(yf[:N//2])

    alpha_power = band_power(xf, yf, 8, 13)
    beta_power = band_power(xf, yf, 13, 30)

    if beta_power > alpha_power:
        return "Focused(专注)"
    else:
        return "Relaxed(放松)"



window_size = fs  # 1秒窗口

for i in range(0, len(signal), window_size):
    segment = signal[i:i+window_size]

    result = classify_eeg(segment, fs)
    print(f"第{i//fs}秒:", result)