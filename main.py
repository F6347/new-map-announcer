# Instructions:
# Create a webhook (doesnt matter username nor avatar), and assign it for the channel it will send messages whenever there is a new map. Copy the webhook link, and define it at line 21.
# Create a new role. Copy its id, and define it at line 22. This is the role which will be pinged once there is a new map.
# You can test it now with changing everything bellow line 102 with the instructions put in the comments.




import time
import requests

# Variables
mapCounter = 0 

# MODIO Settings Variables

url = 'https://mod.io/v1/games/@gorilla-tag/mods?_limit=1&_offset=0&_sort=-date_live'
headers = {'x-modio-origin': 'web'}


# Discord Settings Variables

webhookUrl = 'Put your webhook link in here, no need for username, nor profile picture, put the channel whathever channel it will announce new maps, and DO NOT SHARE THE WEBHOOK LINK WITH NOBODY!'
newMapRole = 'Change this for the role ID that the bot will ping whenever there is a new map.'  # this is the role id for the role that will be pinged when there is a new map

# Functions


def sendAMessage(latestMod):
  global mapCounter
  
  hasImages = True

  title = latestMod['name']
  description = latestMod['description_plaintext']
  urlToMap = latestMod['profile_url']
  urlToMapLogo = latestMod['logo']['original']
  
  author = latestMod['submitted_by']['username']
  authorAvatar = latestMod['submitted_by']['avatar']['original']
  urlToProfile = latestMod['submitted_by']['profile_url']
  urlToMapMedia = latestMod['media']['images']
  urlToMapImages = []
  
  data = {
    'username': author,
    'avatar_url': authorAvatar,
    'content': f"<@&{newMapRole}>, new map has dropped!",
    'embeds': [{
        'title': title,
        'description': description,
        'url': urlToMap,
        'color': 16711680,  # Red color in decimal (use RGB)
        'author': {
            'name': f'Made by {author}',
            'url': urlToProfile,
            'icon_url': authorAvatar
        },
      'thumbnail': {
        'url': urlToMapLogo
      },
        
    }]
  }
  
  for images in urlToMapMedia:
    if images['original'][:-5]!=urlToMapLogo[:-3]:
      if mapCounter<4:
        urlToMapImages.append(images['original'])
      mapCounter+=1
    else:
      hasImages = False
      break

  if hasImages:
    for currentImage in urlToMapImages:
      
      data['embeds'].append({
          'url': urlToMap,
          'image': {
              'url': currentImage
          }
        })

    data['embeds'][0]['footer'] = {
      'text': f'Currently displaying {len(urlToMapImages)} out of {mapCounter} images.'
    }
  


  mapCounter = 0
  return requests.post(webhookUrl, json=data)

def getLatestMod():
  return requests.get(url, headers=headers).json()['data'][0]

# Code

while True:
  LatestMod = getLatestMod()

  time.sleep(120)                                      # Change 120 to 5 when testing

  if getLatestMod()['id']!=LatestMod['id']:            # Change != to == when testing  
    print(sendAMessage(LatestMod))
  #exit()                             # Uf testing, uncomment this line.