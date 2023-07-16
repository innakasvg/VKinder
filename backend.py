from datetime import datetime

import vk_api
from vk_api.exceptions import ApiError

from config import db_url, acces_token


def _bdate_toyear(bdate):
    user_year = bdate.split('.')[2] if bdate else None
    now = datetime.now().year
    return now - int(user_year)


class VkTools:
    def __init__(self, acces_token):
        self.api = vk_api.VkApi(token=acces_token)

    def get_profile_info(self, user_id):

        try:
            info = self.api.method('users.get',
                                    {'user_id': user_id,
                                    'fields': 'city,bdate,sex,relation,home_town'
                                    }
                                    )
        except ApiError as e:
            info = {}
            print(f'error = {e}')

        user_info = {'name': info['first_name'] + ' ' + info['last_name'] if
        'first_name' in info and 'last_name' in info else None,
                     'bdate': info['bdate'] if 'bdate' in info else None,
                     'home_town': info.get('home_town') if 'home_town' in info else None,
                     'sex': info.get('sex') if 'sex' in info else None,
                     'city': info['city']['id'],
                     'id': info.get('id')
                     }

        return user_info

    def search_worksheet(self, params):

        try:
            user = self.api.method('users.search',
                                   {'count': 50,
                                    'offset': 0,
                                    'age_from': params['year'] - 3,
                                    'age_to': params['year'] + 3,
                                    'has_photo': True,
                                    'sex': 1 if params['sex'] == 2 else 2,
                                    'hometown': params['city'],
                                    'status': 6,
                                    'is_closed': False
                                    }
                                    )
            try:
                users = user['items']
            except KeyError:
                return []

            result = []

            for user in users:
                if not user['is_closed']:
                    result.append({'id': user['id'],
                                   'name': user['first_name'] + ' ' + user['last_name']
                                   }
                                  )

            return result
        except ApiError as e:
            user = []
            print(f'error = {e}')

        result = [{'name': item['first_name'] + item['last_name'],
                   'id': item['id']
                   }
                  for item in user['items'] if item['is_closed'] is False
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
    users = bot.search_worksheet(params)