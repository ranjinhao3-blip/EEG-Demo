# Micro-Wheeled_leg-Robot-master
基于ESP32实现双轮腿自平衡机器人，融合MPU6050与编码器构建多状态反馈系统；控 制层基于LQR思想设计多环PID闭环控制，实现动态平衡。底层采用FOC驱动无刷电机输出力 矩，并通过串行舵机实现腿部高度调节与跳跃。基于WiFi + WebSocket实现远程控制与在 线调参 
