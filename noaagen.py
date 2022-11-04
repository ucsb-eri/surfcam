import requests
import re

tlreg = re.compile(r"  DEWP  VIS PTDY  TIDE")
mlreg = re.compile(r"  degC  nmi  hPa    ft")
blreg = re.compile(r"    MM   MM .*    MM")

def print_hi(name):
    open("./surf/gendata.txt").close()
    print('Beginning file download with requests')
    url = 'https://www.ndbc.noaa.gov/data/realtime2/46053.txt'
    r = requests.get(url)
    with open('./surf/gendata.txt', 'wb') as f:
        f.write(r.content)
    file = open('./surf/gendata.txt')
    content = file.readlines()
    data = content[0]+content[1]+content[2]
    data = re.sub(tlreg, '', data)
    data = re.sub(mlreg, '', data)
    data = re.sub(blreg, '', data)
    with open('./surf/gendata.txt', 'w') as f:
        f.write(data)
    print(data)
    f.close

if __name__ == '__main__':
    print_hi('PyCharm')