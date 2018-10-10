import time


def log(*args, **kwargs):
    # time.time() 返回 unix time
    # strftime 把 unix time 转换为普通人类可以看懂的格式
    time_format = '%Y/%m/%d %H:%M:%S'
    localtime = time.localtime(int(time.time()))
    formatted = time.strftime(time_format, localtime)
    with open('log.txt', 'a', encoding='utf-8') as f:
        print(formatted, *args, **kwargs)
        print(formatted, *args, file=f, **kwargs)

