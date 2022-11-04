from datetime import datetime
import requests
import re

tlreg = re.compile(r"  DEWP  VIS PTDY  TIDE")
mlreg = re.compile(r"  degC  nmi  hPa    ft")
blreg = re.compile(r"    MM   MM .*    MM")

def print_hi(name):
    open("/surf/gendata.txt").close()
    print('Beginning file download with requests')
    url = 'https://www.ndbc.noaa.gov/data/realtime2/46053.txt'
    r = requests.get(url)
    with open('/surf/gendata.txt', 'wb') as f:
        f.write(r.content)
    file = open('/surf/gendata.txt')
    content = file.readlines()
    data = content[0]+content[1]+content[2]
    timestamp = datetime.now().strftime("%m/%d/%y %H:%M")
    data = re.sub(tlreg, '  TIMESTAMP', data)
    data = re.sub(mlreg, '  MM/DD/YY hh:mm TZ', data)
    data = re.sub(blreg, f'  {timestamp} PST', data)  # datetime.now() returns local time, so assume PST
    with open('/surf/gendata.txt', 'w') as f:
        f.write(data)
    print(data)
    f.close

if __name__ == '__main__':
    print_hi('PyCharm')


