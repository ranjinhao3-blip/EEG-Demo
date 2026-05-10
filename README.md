# EEG Demo - Real-Time EEG Visualization & Simple AI Classification

## 项目简介

本项目是一个基于 Python 的实时 EEG（脑电）信号可视化与简单 AI 分类 Demo，支持：

* ADS1299 串口脑电数据采集
* 实时 EEG 波形显示
* FFT 频谱分析
* Alpha / Beta 脑电频段分析
* 简单 AI 状态分类（Focused / Relaxed）
* 模拟 EEG 数据运行模式

项目主要用于学习：

* 生物信号处理
* EEG 脑电分析
* FFT 频域分析
* ADS1299 数据采集
* Python 实时可视化
* 基础机器学习分类

---

# 项目功能

## 1. 实时 EEG 波形显示

系统实时显示脑电时域波形。

---

## 2. FFT 频谱分析

对 EEG 信号进行快速傅里叶变换（FFT），显示频域能量分布。

支持观察：

* Alpha 波（8~13Hz）
* Beta 波（13~30Hz）

---

## 3. 简单 AI 状态识别

使用 Logistic Regression 对 EEG 状态进行简单分类：

* Focused（专注）
* Relaxed（放松）

---

## 4. ADS1299 串口接入

支持 ADS1299 通过串口发送 EEG 数据。

数据格式：

```text id="s4p8t1"
ch1,ch2,ch3,...
```

例如：

```text id="4x2n8z"
123.1,120.3,119.8,118.5
```

---

# 技术栈

* Python
* NumPy
* SciPy
* Matplotlib
* Scikit-learn
* PySerial

---

# 系统架构

```text id="m1v5d7"
ADS1299 -> UART Serial -> Python -> FFT -> AI Classification -> Real-time Visualization
```

---

# EEG 信号处理流程

```text id="5p7k1z"
EEG Signal
    ↓
Band-pass Filter
    ↓
FFT Frequency Analysis
    ↓
Alpha/Beta Power Extraction
    ↓
Logistic Regression
    ↓
Focused / Relaxed
```

---

# 安装依赖

## pip 安装

```bash id="8v4h2m"
pip install numpy scipy matplotlib scikit-learn pyserial
```

---

# 运行方式

## 1. 模拟模式（无需硬件）

```bash id="3m9t5x"
python eeg_demo.py
```

系统会自动生成模拟 EEG 数据。

---

## 2. ADS1299 串口模式

```bash id="0k2h7s"
python eeg_demo.py --source serial --port COM3
```

示例：

```bash id="1n8q3z"
python eeg_demo.py --source serial --port COM5
```

---

# 项目截图

## 上位机实时界面

* 上方：EEG 时域波形
* 下方：FFT 频谱图

系统会实时显示：

```text id="2f4x7j"
Focused
```

或：

```text id="7m1c4p"
Relaxed
```

---

# 核心算法

## FFT 频谱分析

使用：

```text id="0n3k8d"
Fast Fourier Transform
```

提取 EEG 频域特征。

---

## Alpha 波

频率范围：

```text id="4j2m8x"
8Hz ~ 13Hz
```

通常表示：

* 放松
* 闭眼
* 冥想

---

## Beta 波

频率范围：

```text id="9x1v6r"
13Hz ~ 30Hz
```

通常表示：

* 专注
* 思考
* 注意力集中

---

# 项目亮点

* 实现实时 EEG 数据可视化
* 支持 ADS1299 脑电采集
* 实现 FFT 频谱分析
* 实现简单 AI 分类
* 支持串口实时数据流
* 具备基础 BCI（脑机接口）系统框架

---

# 后续优化方向

* 多通道 EEG 显示
* CNN / LSTM 深度学习分类
* Qt 上位机界面
* 蓝牙无线传输
* 脑机接口控制
* 实时滤波优化
* ICA 去伪迹算法

---

# 作者

Embedded & EEG Learning Project

Focused on:

* Embedded Systems
* EEG Signal Processing
* ADS1299
* AI + Biomedical Signal
* Real-time Visualization

