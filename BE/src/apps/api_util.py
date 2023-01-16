
import requests
from utils.util import config

client_id = config["app_client_id"]
client_secret = config["app_client_secret"]
redirect_url = 'https://k-army-project-irpqk.run.goorm.io/'
access_url = 'https://www.facebook.com/v13.0/dialog/oauth?response_type=token&display=popup&client_id=your_client_id&redirect_uri=your_redirect_uri&auth_type=rerequest&scope=user_location%2Cuser_photos%2Cuser_friends%2Cuser_gender%2Cpages_show_list%2Cinstagram_basic%2Cinstagram_manage_comments%2Cinstagram_manage_insights%2Cpages_read_engagement%2Cpublic_profile'
graph_url = 'https://graph.facebook.com/v15.0/'

def func_get_long_lived_access_token(access_token = ''):
    url = graph_url + 'oauth/access_token'
    param = dict()
    param['grant_type'] = 'fb_exchange_token'
    param['client_id'] = client_id
    param['client_secret'] = client_secret
    param['fb_exchange_token'] = access_token
    response = requests.get(url = url,params=param)
    response =response.json()
    long_lived_access_tokken = response['access_token']
    return long_lived_access_tokken
  
def func_get_page_id(access_token = ''):
    url = graph_url + 'me/accounts'
    param = dict()
    param['access_token'] = access_token
    response = requests.get(url = url,params=param)
    response = response.json()
    page_id = response['data'][0]['id']
    print("\n page_id",page_id)
    return page_id

def func_get_instagram_business_account(page_id = '',access_token = ''):
    url = graph_url + page_id
    param = dict()
    param['fields'] = 'instagram_business_account'
    param['access_token'] = access_token
    response = requests.get(url = url,params=param)
    response = response.json()
    print("\n response", response)
    try:
        instagram_account_id = response['instagram_business_account']['id']
    except:
        return {'error':'Instagram account not linked'}
    return instagram_account_id