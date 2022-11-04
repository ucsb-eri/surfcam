import requests
import os

def print_hi(name):
    open("./surf/wavedata.txt").close() 
    print('Beginning file download with requests')
    url = 'https://www.ndbc.noaa.gov/data/realtime2/46053.spec'
    r = requests.get(url)
    with open('./surf/wavedata.txt', 'wb') as f:
        f.write(r.content)
    file = open('./surf/wavedata.txt')
    content = file.readlines()
    data = content[0]+content[1]+content[2]
    with open('./surf/wavedata.txt', 'w') as f:
        f.write(data)
    print(data)
    f.close

if __name__ == '__main__':
    print_hi('PyCharm')
