# ==============================
# EEG Demo 项目（可视化 + 实时 + 简单AI）
# 支持 ADS1299 串口接入（期望每行 CSV: ch1,ch2,...）或模拟模式
# ==============================

import argparse
import time
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
from scipy.signal import butter, lfilter
from sklearn.linear_model import LogisticRegression

try:
    import serial
except Exception:
    serial = None

# ------------------------------
# 参数
# ------------------------------
fs = 250
window_size = fs  # 1秒窗口

# 帮助函数：带通滤波（可选）
def bandpass(data, low, high, fs, order=4):
    nyq = 0.5 * fs
    lown = low / nyq
    highn = high / nyq
    b, a = butter(order, [lown, highn], btype='band')
    return lfilter(b, a, data)

# ------------------------------
# 生成训练数据（用于初始模型）
# ------------------------------
X = []
y = []
for _ in range(100):
    t = np.arange(0, 2, 1/fs)
    alpha_amp = np.random.uniform(0.5, 1.5)
    beta_amp = np.random.uniform(0.5, 1.5)
    alpha_wave = alpha_amp * np.sin(2 * np.pi * 10 * t)
    beta_wave = beta_amp * np.sin(2 * np.pi * 20 * t)
    noise = 0.3 * np.random.randn(len(t))
    signal = alpha_wave + beta_wave + noise
    label = 1 if beta_amp > alpha_amp else 0
    for i in range(0, len(signal) - window_size, window_size):
        segment = signal[i:i+window_size]
        yf = fft(segment)
        xf = fftfreq(len(segment), 1/fs)
        xf = xf[:len(segment)//2]
        yf = np.abs(yf[:len(segment)//2])
        alpha_power = np.sum(yf[(xf >= 8) & (xf <= 13)])
        beta_power = np.sum(yf[(xf >= 13) & (xf <= 30)])
        X.append([alpha_power, beta_power])
        y.append(label)
X = np.array(X)
y = np.array(y)

# ------------------------------
# 训练模型
# ------------------------------
model = LogisticRegression()
model.fit(X, y)
print('模型训练完成（基于模拟数据）')


# ------------------------------
# ADS1299 读取封装（串口 CSV 或模拟）
# ------------------------------
class ADSReader:
    def __init__(self, source='sim', port=None, baud=115200, channels=8):
        self.source = source
        self.port = port
        self.baud = baud
        self.channels = channels
        self.fs = fs
        self.window = window_size
        self._ser = None
        if source == 'serial':
            if serial is None:
                raise RuntimeError('pyserial 未安装，无法使用 serial 模式')
            self._ser = serial.Serial(port, baud, timeout=1)

    def read_serial(self):
        line = self._ser.readline().decode(errors='ignore').strip()
        if not line:
            return None
        parts = line.split(',')
        try:
            vals = [float(x) for x in parts[:self.channels]]
        except Exception:
            return None
        return np.array(vals)

    def get_segment(self):
        if self.source == 'sim':
            t = np.arange(0, 1, 1/self.fs)
            alpha_wave = np.sin(2 * np.pi * 10 * t)
            beta_wave = 1.2 * np.sin(2 * np.pi * 20 * t)
            noise = 0.3 * np.random.randn(len(t))
            return alpha_wave + beta_wave + noise
        else:
            buf = []
            start = time.time()
            while len(buf) < self.window:
                row = self.read_serial()
                if row is None:
                    continue
                buf.append(row[0])
                if time.time() - start > 2:
                    break
            if len(buf) < self.window:
                buf = buf + [0.0] * (self.window - len(buf))
            return np.array(buf)


def run_realtime(source='sim', port=None, baud=115200):
    reader = ADSReader(source=source, port=port, baud=baud)
    plt.ion()
    fig, (ax1, ax2) = plt.subplots(2, 1)
    try:
        while True:
            segment = reader.get_segment()
            if segment is None:
                continue
            yf = fft(segment)
            xf = fftfreq(len(segment), 1/fs)
            xf = xf[:len(segment)//2]
            yf = np.abs(yf[:len(segment)//2])
            alpha_power = np.sum(yf[(xf >= 8) & (xf <= 13)])
            beta_power = np.sum(yf[(xf >= 13) & (xf <= 30)])
            pred = model.predict([[alpha_power, beta_power]])[0]
            state = 'Focused' if pred == 1 else 'Relaxed'
            ax1.cla(); ax2.cla()
            ax1.plot(segment); ax1.set_title(f'EEG Signal - {state}')
            ax2.plot(xf, yf); ax2.set_xlim(0, 40); ax2.set_title('Frequency Spectrum')
            plt.pause(0.3)
    except KeyboardInterrupt:
        print('\n退出实时显示')
        plt.close(fig)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', choices=['sim', 'serial'], default='sim')
    parser.add_argument('--port', type=str, default=None, help='串口端口，例如 COM3')
    parser.add_argument('--baud', type=int, default=115200)
    args = parser.parse_args()
    if args.source == 'serial' and args.port is None:
        parser.error('--port 对于 serial 模式是必须的')
    run_realtime(source=args.source, port=args.port, baud=args.baud)
