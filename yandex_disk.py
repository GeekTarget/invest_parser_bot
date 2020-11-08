import yadisk
from config import months
from datetime import datetime
import pytz

# AgAAAABCD7_EAAaviX7eQsZI7kQGtirnk07dMeg
tz = pytz.timezone('Europe/Moscow')

class YaDisk:
    token = 'AgAAAABIcQPSAAayEbHbnk3wPkFJt-A7HIHByGE'
    y = yadisk.YaDisk(token=token)

    def get_len_disk(self, path):
        if path == True:
            path = months[str(datetime.now(tz).month)]
        else:
            path = f'{months[str(datetime.now(tz).month)]}/{self.get_name()}'
        return list(self.y.listdir('disk:/Телеграм/' + path + '/'))

    def get_name(self):
        number = datetime.now(tz).day
        if len(str(number)) == 1:
            return '00' + str(datetime.now(tz).day)
        elif len(str(number)) == 2:
            return '0' + str(datetime.now(tz).day)
        else:
            return str(datetime.now(tz).day)

    def len_image(self):
        img = []
        len_disk = len(
            list(self.y.listdir('disk:/Телеграм/' + f'{months[str(datetime.now(tz).month)]}/{self.get_name()}' + '/')))
        for i in range(len_disk):
            l = list(self.y.listdir('disk:/Телеграм/' + f'{months[str(datetime.now(tz).month)]}/{self.get_name()}' + '/'))[
                i].name.split('.')
            if l[-1] == 'jpg':
                img.append(l[-1])
        return len(img)

    def create_folder(self, type):
        if type == True:
            self.y.mkdir('/Телеграм/' + months[str(datetime.now(tz).month)])
        else:
            self.y.mkdir('/Телеграм/' + months[str(datetime.now(tz).month)] + '/' + self.get_name())

    def add_file(self, filename):
        self.y.upload(filename, f'/Телеграм/{months[str(datetime.now(tz).month)]}/{self.get_name()}/{filename}')

    def remove_file(self, filename):
        self.y.remove(f'disk:/Телеграм/{months[str(datetime.now(tz).month)]}/' + self.get_name() + '/' + filename)

# y = YaDisk()
# y.create_folder(True)
# print(y.len_image())
# print(y.get_name())
# y.create_folder(type=True)
# y.create_folder(False)
