import time

"""
该文件主要负责提供其他相关函数
"""


def time_strp(fotmat_time=None, age_min=0):
    """格式化时间转换时间戳"""
    if fotmat_time is None:
        timestamp = (int(time.time() - 60 * age_min) * 1000)
    else:
        time_tuple = time.strptime(fotmat_time, "%Y-%m-%d %H:%M:%S")
        timestamp = int(time.mktime(time_tuple)) * 1000
    return timestamp