import os

def cam_find():
    # ~/dev에서 device가 몇번인지 보고 할당해줌
    os.system('ls /dev | grep video > result.txt')
    with open('/home/orin/final_run/result.txt', 'r') as f:
        str = f.read()
    f.close()
    return int(str[5]), int(str[19])
