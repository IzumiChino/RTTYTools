import numpy as np
import pyaudio

# RTTY参数
BAUD_RATE = 45.45  # 比特速率
SAMPLE_RATE = 44100  # 采样率
MARK_FREQ = 2125  # 标记频率
SPACE_FREQ = 2295  # 空格频率
MARK_PHASE = 0  # 标记相位
SPACE_PHASE = np.pi  # 空格相位
BITS_PER_CHAR = 7  # 每个字符的比特数

# RTTY解码函数
def rtty_decode(signal):
    # 预处理信号
    signal = signal / np.max(np.abs(signal))
    window_size = int(SAMPLE_RATE / BAUD_RATE) // 2 * 2  # 窗口大小为一个符号时间的一半
    signal = signal[:len(signal) // window_size * window_size]  # 确保长度为窗口大小的整数倍
    signal = signal.reshape((-1, window_size))  # 分割信号

    # 解调信号
    mark_signal = np.sin(2 * np.pi * MARK_FREQ * np.arange(0, window_size / SAMPLE_RATE, 1 / SAMPLE_RATE) + MARK_PHASE)
    space_signal = np.sin(2 * np.pi * SPACE_FREQ * np.arange(0, window_size / SAMPLE_RATE, 1 / SAMPLE_RATE) + SPACE_PHASE)
    mark_corr = np.abs(np.dot(signal, mark_signal))
    space_corr = np.abs(np.dot(signal, space_signal))
    bits = mark_corr > space_corr

    # 解码二进制字符串
    binary = ''.join(str(int(b)) for b in bits)
    padding = '0' * (BITS_PER_CHAR - len(binary) % BITS_PER_CHAR) if len(binary) % BITS_PER_CHAR != 0 else ''
    binary += padding
    text = ''
    for i in range(0, len(binary), BITS_PER_CHAR):
        char_binary = binary[i:i+BITS_PER_CHAR]
        char_code = int(char_binary, 2)
        text += chr(char_code)

    return text

# 实时获取麦克风输入并解码
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=SAMPLE_RATE, input=True, frames_per_buffer=1024)

while True:
    data = stream.read(1024)
    signal = np.frombuffer(data, dtype=np.float32)
    text = rtty_decode(signal)
    print(text)

stream.stop_stream()
stream.close()
p.terminate()
