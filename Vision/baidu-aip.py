from aip import AipOcr

"""APPID AK SK"""

APP_ID = '15731590'
API_KEY = 'GTAkGyVvGgUNnzp1Z1jsW0Tp'
SECRET_KEY = 'IO8ATkx9c3Dj3IjtnVA7w4RbNbajjlVb'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

"""读取图片"""
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

image = get_file_content('C:/Users/IvanChur/PycharmProjects/01_python/图像处理/pic/id03.png')
# image = get_file_content('C:/Users/IvanChur/PycharmProjects/01_python/图像处理/pic/id07.jpg')

"""调用通用文字识别，图片参数为本地图片"""
print(client.licensePlate(image, {'multi_detect':'true'}))