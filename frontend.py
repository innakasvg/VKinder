
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from config import comunity_token, acces_token
from core import VkTools

class BotFront():

    def __init__(self,comunity_token, acces_token):
        self.interface = vk_api.VkApi(token=comunity_token)
        self.api = VkTools(acces_token)
        self.worksheets = []
        self.params = {}
        self.offset = 0
        self.longpoll = VkLongPoll(self.interface)


    def message_send(self, user_id, message, attachment=None):
        self.interface.method('messages.send',
                                {'user_id': user_id,
                                'message': message,
                                'attachment': attachment,
                                'random_id': get_random_id()
                                }
                                )



    def event_handler(self):
        longpoll = VkLongPoll(self.interface)

        
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                command = event.text.lower()

                if command == 'привет':
                    self.params = self.api.get_profile_info(event.user_id)
                    self.message_send(event.user_id, f'Здравствуйте {self.params["name"]}')
                elif command == 'поиск':
                    users = self.api.serch_users(self.params)
                    user = users.pop()

            if self.worksheets:
                worksheets = self.worksheets.pop()
                photos_user = self.api.get_photos(worksheets['id'])

                self.message_send(event.user_id, f'имя: {worksheets["name"]} ссылка: vk.com/{worksheets["id"]}'),
                attachment = ''

                for num, photo in enumerate(photos_user):
                    attachment += f'photo{photo["owner_id"]}_{photo["id"]},'
                else:
                    self.worksheets = self.api.search_worksheet(self.params, self.offset)
                    worksheet = self.worksheets.pop()
                    photos_user = self.api.get_photos(worksheet['id'])

                    self.message_send(event.user_id, f'имя: {worksheet["name"]} ссылка: vk.com/{worksheet["id"]}'),
                    attachment = ''

                    for num, photo in enumerate(photos_user):
                        attachment += f'photo{photo["owner_id"]}_{photo["id"]},'
                        if num == 2:
                            break

                        self.message_send(event.user_id,
                                          f'познакомтесь: {event.user_id["name"]}',
                                          attachment=attachment
                                          )
                    self.offset += 10

                    try:
                        connection = psycopg2.connect(db_url)
                        cursor = connection.cursor()

                        record_to_insert = ()
                        cursor.execute(record_to_insert)

                        connection.commit()
                    except (Exception, Error) as error:
                        print('Ошибка базы данных', error)

                    photos_attachment = ",".join(photos_user)
                    user_answer = []
                    user_number = []
                    session = db_url.Session()
                    if user_answer == '1':
                        dating_user = db_url.DatingUser(['id'], user_number['first_name'],
                                                        user_number['last_name'], user_number['bdate'],
                                                        user_number['sex'], user_number['city'], photos_attachment,
                                                        user_number['domain'], event.user_id)
                        session.add(dating_user)
                    elif user_answer == '2':
                        black_list_item = db_url.BlackList(user_number['id'], user_number['first_name'],
                                                            user_number['last_name'], user_number['bdate'],
                                                            user_number['sex'], user_number['city'],
                                                            photos_attachment, user_number['domain'], event.user_id)
                        session.add(black_list_item)
                    elif user_answer == '3':
                        self.write_msg(user_id=event.user_id,
                                        message=dictionaries_vk.options_messages['users_end_search'])
                        return False
                    session.commit()

                elif command == 'пока':
                    self.message_send(event.user_id, 'До встречи.')
                else:
                    self.message_send(event.user_id, 'Неизвестная команда.')



if __name__ == '__main__':
    bot = BotFront(comunity_token, acces_token)
    bot.event_handler()
            
