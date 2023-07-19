import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from config import comunity_token, acces_token
from backend import VkTools
from dbinterface import DbTools, engine

class BotFront:

    def __init__(self,comunity_token, acces_token):
        self.interface = vk_api.VkApi(token=comunity_token)
        self.api = VkTools(acces_token)
        self.longpoll = VkLongPoll(self.interface)
        self.db_tools = DbTools(engine)
        self.worksheets = []
        self.params = {}
        self.offset = 0
        

    def message_send(self, user_id, message, attachment=None):
        self.interface.method('messages.send',
                                {'user_id': user_id,
                                'message': message,
                                'attachment': attachment,
                                'random_id': get_random_id()
                                }
                                )
        
    def handler_info(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                return event.text



    def event_handler(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                command = event.text.lower()

                if command == 'привет':
                    self.params = self.api.get_profile_info(event.user_id)
                    self.message_send(event.user_id, f'Здравствуйте {self.params["name"]}')
                 

                    if self.params['age'] is None:
                        self.message_send(event.user_id, f'Укажите свой возраст')
                        age = self.handler_info()
                        while not age.isdigit():
                            self.message_send(event.user_id, f'Введите корректный возраст')
                            age = self.handler_info()
                        self.params['age'] = int(age)

                    if self.params['city'] is None:
                        self.message_send(event.user_id, f'Укажите свой город')
                        self.params['city'] = self.handler_info()

                    if self.params['sex'] is None:
                        self.message_send(event.user_id, f'Укажите пол (м/ж)')
                        sex = self.handler_info()
                        while sex not in 'мж':
                            self.message_send(event.user_id, f'Введите корректный пол м/ж')
                            sex = self.handler_info()
                        self.params['sex'] = 1 if sex == 'ж' else 2

                elif command == 'поиск':
                    
                    if  self.worksheets:
                        worksheet = self.worksheets.pop()

                        photos = self.api.get_photos(worksheet['id'])
                        photo_string = ''
                        for photo in photos:
                            photo_string += f'photo{photo["owner_id"]}_{photo["id"]},'

                    else:
                        self.worksheets = self.api.search_worksheet(self.params, self.offset)

                        worksheet = self.worksheets.pop()

                        # проверка в БД
                        while self.db_tools.find_profile(event.user_id, worksheet['id']) is True:
                            if len(self.worksheets):
                                worksheet = self.worksheets.pop()
                            else:
                                self.message_send(event.user_id, f'Ничего не найдено, попробуйте позднее')   
                                break

                        photos = self.api.get_photos(worksheet['id'])
                        photo_string = ''
                        for photo in photos:
                            photo_string += f'photo{photo["owner_id"]}_{photo["id"]},'
                        self.offset += 30

                    self.message_send(
                        event.user_id,
                        f'Имя: {worksheet["name"]} ссылка: vk.com/id{worksheet["id"]}',
                        attachment = photo_string
                    )
                    # добавление в БД
                    if self.db_tools.find_profile(event.user_id, worksheet["id"]) is False:
                        self.db_tools.add_profile(event.user_id, worksheet["id"])

                elif command == 'пока':
                    self.message_send(event.user_id, 'До встречи.')
                else:
                    self.message_send(event.user_id, 'Неизвестная команда.')



if __name__ == '__main__':
    bot = BotFront(comunity_token, acces_token)
    bot.event_handler()            
