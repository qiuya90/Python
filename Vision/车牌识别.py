from aip import AipOcr

"""APPID AK SK"""

APP_ID = '15731590'
API_KEY = 'GTAkGyVvGgUNnzp1Z1jsW0Tp'
SECRET_KEY = 'IO8ATkx9c3Dj3IjtnVA7w4RbNbajjlVb'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

"""读取图片"""
def get_file_contnet(filepath):
    with open(filepath, 'rb') as fp:
        return fp.read()

image = get_file_contnet('C:/Users/Administrator/PycharmProjects/爬虫/图像处理/pics/car(15).jpg')

"""调用通用文字车牌识别，图片参数为本地图片"""
print(client.licensePlate(image))