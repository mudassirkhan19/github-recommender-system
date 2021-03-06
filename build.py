import requests
import json
import pandas as pd

def get_user_repos_count(username):
    url = 'https://api.github.com/users/'+username+'/repos'
    r = requests.get(url)
    data = json.loads(r.content)
    return len(data) if type(data) == list else -1

def get_user_liked_repos_count(username):
    url = 'https://api.github.com/users/'+username+'/starred'
    r = requests.get(url)
    data = json.loads(r.content)
    return len(data) if type(data) == list else -1

def get_user_liked_repos(username):
    url = 'https://api.github.com/users/'+username+'/starred'
    r = requests.get(url)
    data = json.loads(r.content)
    if type(data) != list:
        return None
    df = pd.DataFrame()
    for item in data:
        df = df.append({'Name': item['full_name'].split('/')[1], 'Url': item['html_url']}, ignore_index=True)
    return df

def get_user_liked_repos_owners(username):
    url = 'https://api.github.com/users/'+username+'/starred'
    r = requests.get(url)
    data = json.loads(r.content)
    if type(data) != list:
        return None
    df = pd.DataFrame()
    for item in data:
        new_r = requests.get(item['url'])

        df = df.append({'Name': item['full_name'].split('/')[0], 'Url': item['url']}, ignore_index=True)
    return df

def get_owners_liked_repos(username):
    url = 'https://api.github.com/users/'+username+'/starred'
    r = requests.get(url)
    data = json.loads(r.content)
    if type(data) != list:
        return None
    df = pd.DataFrame()
    for item in data:
        owner_name = item['full_name'].split('/')[0]
        ##### Making too many requests leads to blocking
        #new_r = requests.get('https://api.github.com/users/'+owner_name+'/starred')
        owner_url = 'https://github.com/'+owner_name
        new_data = json.loads(r.content)
        repo_name = item['full_name'].split('/')[1]
        repo_url = item['html_url']
        for owner_liked in new_data:
            df = df.append({'repo_name': repo_name, 'repo_url': repo_url, 'owner_name': owner_name,
            'owner_profile_url': owner_url, 'repo_liked_by_owner': owner_liked['full_name'].split('/')[1],
            'repo_url_liked_by_owner': owner_liked['html_url']}, ignore_index=True)
    return df

def get_owners_liked_repos_summary(username):
    url = 'https://api.github.com/users/'+username+'/starred'
    r = requests.get(url)
    data = json.loads(r.content)
    if type(data) != list:
        return None
    df = pd.DataFrame()
    for item in data:
        owner_name = item['full_name'].split('/')[0]
        ##### Making too many requests leads to blocking
        #new_r = requests.get('https://api.github.com/users/'+owner_name+'/starred')
        owner_url = 'https://github.com/'+owner_name
        new_data = json.loads(r.content)
        repo_name = item['full_name'].split('/')[1]
        repo_url = item['html_url']
        for owner_liked in new_data:
            df = df.append({'repo_name': repo_name, 'repo_url': repo_url, 'owner_name': owner_name,
            'owner_profile_url': owner_url, 'repo_liked_by_owner': owner_liked['full_name'].split('/')[1],
            'repo_url_liked_by_owner': owner_liked['html_url']}, ignore_index=True)
    l=[]
    for index,row in df['repo_url_liked_by_owner'].value_counts().reset_index().head().iterrows():
        l.append((row['index'],row['repo_url_liked_by_owner']))
    return l
