# 
import requests

#
def rocket_reach_by_linkedin_url(linkedin_profile_url):
    url = 'https://api.rocketreach.co/v2/api/person/lookup'
    api_key = 'd0be2fk8018675b76a58153852362fc5809dab9'
    headers = {
    'Api-Key': api_key
    }
    params = {
        'li_url': linkedin_profile_url
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()


#
def process_data(data, domain):
    try:
        for email_data in data['emails']:
            if domain in email_data['email']:
                return email_data['email']
        return data['current_work_email']
    except:
        return False
