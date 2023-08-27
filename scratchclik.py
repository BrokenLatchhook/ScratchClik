import requests

class User:
  def __init__(self, username):
    self.username = username
    self._api_data = requests.get(f'https://api.scratch.mit.edu/users/{username}').json()
    self._db_data = requests.get(f'https://scratchdb.lefty.one/v3/user/info/{username}').json()
    self.data = {'api': self._api_data, 'db': self._db_data}
  
  def id(self):
    return self._api_data['id']

  def scratch_team(self):
    return self._api_data['scratchteam']

  def join_timestamp(self):
    return self._api_data['history']['joined']

  def pfp_url(self, size=90):
    return f'https://uploads.scratch.mit.edu/get_image/user/{self.id()}_{size}x{size}.png'

  def about_me(self):
    return self._api_data['profile']['bio']

  def wiwo(self):
    return self._api_data['profile']['status']

  def what_im_working_on(self):
    return self.wiwo()

  def country(self):
    return self._api_data['profile']['country']

  def status(self):
    return self._db_data['status']

  def follower_count(self):
    return self._db_data['statistics']['followers']

  def following_count(self):
    return self._db_data['statistics']['following']

class Project:
  def __init__(self, id):
    self.id = id
    self._api_data = requests.get(f'https://api.scratch.mit.edu/projects/{id}').json()
    self._db_data = requests.get(f'https://scratchdb.lefty.one/v3/project/info/{id}').json()
    self.data = {'api': self._api_data, 'db': self._db_data}

  def title(self):
    return self._api_data['title']

  def notes_and_credits(self):
    return self._api_data['description']

  def instructions(self):
    return self._api_data['instructions']

  def is_shared(self):
    return self._api_data['is_published']

  def commmenting_on(self):
    return self._api_data['comments_allowed']

  def creator(self):
    return User(self._api_data['author']['username'])

  def thumbnail_url(self, dimensions=(282, 218)):
    return f'https://uploads.scratch.mit.edu/get_image/project/{self.id}_{dimensions[0]}x{dimensions[1]}.png'

  def creation_timestamp(self):
    return self._api_data['history']['created']

  def modification_timestamp(self):
    return self._api_data['history']['modified']

  def share_timestamp(self):
    return self._api_data['history']['shared']

  def view_count(self):
    return self._api_data['stats']['views']

  def love_count(self):
    return self._api_data['stats']['loves']

  def favorite_count(self):
    return self._api_data['stats']['favorites']

  def remix_count(self):
    return self._api_data['stats']['remixes']

  def is_remix(self):
    return self._api_data['remix']['parent'] is not None

  def asset_count(self):
    return self._db_data['metadata']['assets']

  def block_count(self):
    return self._db_data['metadata']['blocks']

  def costume_count(self):
    return self._db_data['metadata']['costumes']

  def variable_count(self):
    return self._db_data['metadata']['variables']

  def hash(self):
    return self._db_data['metadata']['hash']

  def project_json(self):
    return requests.get(f'https://scratchdb.lefty.one/v3/project/source/{self.hash()}').json()

class Studio:
  def __init__(self, id):
    self.id = id
    self.data = requests.get(f'https://api.scratch.mit.edu/studios/{id}').json()

  def title(self):
    return self.data['title']

  def comments_on(self):
    return self.data['comments_allowed']

  def description(self):
    return self.data['description']

  def thumbnail(self):
    return self.data['image']

  def anyone_can_add(self):
    return self.data['open_to_all']

  def follower_count(self):
    return self.data['stats']['followers']

  def manager_count(self):
    return self.data['stats']['managers']

  def creator(self):
    return User(requests.get(f'https://api.scratch.mit.edu/studios/{self.id}/managers/?limit=1').json()[0]['username'])
  
  def managers(self, limit=24, offset=0):
    return [User(user['username']) for user in requests.get(f'https://api.scratch.mit.edu/studios/{self.id}/managers/?limit={limit}&offset={offset}').json()]

  def curators(self, limit=24, offset=0):
    return [User(user['username']) for user in requests.get(f'https://api.scratch.mit.edu/studios/{self.id}/curators/?limit={limit}&offset={offset}').json()]

class ForumPost:
  def __init__(self, id):
    self.id = id
    self.data = requests.get(f'https://scratchdb.lefty.one/v3/forum/post/info/{self.id}').json()

  def bbcode(self):
    return self.data['content']['bb']

  def html(self):
    return self.data['content']['html']

  def creator(self):
    return User(self.data['username'])

  def post_timestamp(self):
    return self.data['time']['posted']

  def topic(self):
    return ForumTopic(self.data['topic']['id'])

class ForumTopic:
  def __init__(self, id):
    self.id = id
    self.data = requests.get(f'https://scratchdb.lefty.one/v3/forum/topic/info/{self.id}').json()

  def title(self):
    return self.data['title']
  
  def category(self):
    return self.data['category']

  def is_closed(self):
    return bool(self.data['closed'])

  def post_count(self):
    return self.data['post_count']

def favor():
  print('Follow @Tech-Wire on Scratch!')


