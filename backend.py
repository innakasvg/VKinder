from datetime import datetime
from pprint import pprint
import vk_api
from vk_api.exceptions import ApiError

from config import acces_token


class VkTools:
    def __init__(self, acces_token):
        self.api = vk_api.VkApi(token=acces_token)

    def _bdate_to_age(self, bdate):
        user_year = bdate.split('.')[2] if bdate else None
        now = datetime.now().year
        return now - int(user_year)

    def get_profile_info(self, user_id):

        try:
            info, = self.api.method('users.get',
                                    {'user_id': user_id,
                                    'fields': 'city,bdate,sex,'
                                    }
                                    )
        except ApiError as e:
            info = {}
            print(f'error = {e}')
        pprint(info)
        #pprint(info['first_name'])
        #pprint(info['home_town'])
        user_info = {'name': info['first_name'] + ' ' + info['last_name'] if
        'first_name' in info and 'last_name' in info else None,
                     'age': self._bdate_to_age(info['bdate']),
                     'city': info['city']['title'],
                     'sex': info.get('sex') if 'sex' in info else None,
                     'id': info.get('id')
                     }
        pprint(user_info)
        return user_info

    def search_worksheet(self, params, offset):

        try:
            users = self.api.method('users.search',
                                   {'count': 50,
                                    'offset': offset,
                                    'age_from': params['age'] - 3,
                                    'age_to': params['age'] + 3,
                                    'has_photo': True,
                                    'sex': 1 if params['sex'] == 2 else 2,
                                    'hometown': params['city']
                                    }
                                    )
        except ApiError as e:
            users = [ ]
            print(f'error = {e}')

        result = [{'name': item['first_name'] + item['last_name'],
                    'id': item['id']
                    } for item in users['items'] if item['is_closed'] is False
                ]

        return result

    def get_photos(self, id):
        try:
            photos = self.vkapi.method('photos.get',
                                       {'owner_id': id,
                                        'album_id': 'profile',
                                        'extended': 1
                                        }
                                       )
            try:
                photos = photos['items']
            except KeyError:
                return []

            result = [{'owner_id': item['owner_id'],
                       'id': item['id'],
                       'likes': item['likes']['count'],
                       'comments': item['comments']['count']
                       }
                      for item in photos['items']
                      ]

            return result
        except ApiError as e:
            photos = []
            print(f'error = {e}')

            photos_dict = dict()
            for photo in photos:
                likes = photo['likes']['count']
                comments = comments['comments']['count']
                photos_dict[db_url] = likes
                top3_photos = sorted(photos_dict.items(), key=lambda x: x[1], reverse=True)[0:3]
            return top3_photos


if __name__ == '__main__':
    user_id = []
    bot = VkTools(acces_token)
    params = bot.get_profile_info(user_id)
    users = bot.search_worksheet(params,30)