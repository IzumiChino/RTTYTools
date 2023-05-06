import numpy as np
import pyaudio

# RTTY参数
BAUD_RATE = 45.45  # 比特速率
SAMPLE_RATE = 44100  # 采样率
MARK_PHASE = 0  # 标记相位
SPACE_PHASE = np.pi  # 空格相位
BITS_PER_CHAR = 7  # 每个字符的比特数

# 提示用户输入MARK_FREQ和SPACE_FREQ
MARK_FREQ = float(input("请输入标记频率（Hz）："))
SPACE_FREQ = float(input("请输入空格频率（Hz）："))

# 文本输入
text = input("请输入要转换的文本：")

# RTTY编码函数
def rtty_encode(text):
    # ASCII转二进制
    binary = ''.join('{:07b}'.format(ord(c)) for c in text)
    # RTTY编码
    rtty = np.array([])
    for bit in binary:
        if bit == '0':
            rtty = np.append(rtty, np.sin(2 * np.pi * MARK_FREQ * np.arange(0, 1 / BAUD_RATE, 1 / SAMPLE_RATE) + MARK_PHASE))
        else:
            rtty = np.append(rtty, np.sin(2 * np.pi * SPACE_FREQ * np.arange(0, 1 / BAUD_RATE, 1 / SAMPLE_RATE) + SPACE_PHASE))
    return rtty
  
# RTTY信号生成
signal = rtty_encode(text)

# 输出到声卡
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=SAMPLE_RATE, output=True)
stream.write(signal.astype(np.float32).tobytes())
stream.stop_stream()
stream.close()
p.terminate()
