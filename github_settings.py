#pip install pygithub

from github import Github
import os
import requests
import json
import yaml
from pprint import pprint


GITHUB_API_URL = "https://api.github.com/"
ORG_NAME = "TestForSettings"

file = open("Token.txt", "r")
token = file.readline()

file.close()

g = Github(token)

# Here are saved the names of the repos that have as a topic "testing"
repo_names = []
# print(repo_names)

for repo in g.get_user().get_repos():
    # print(repo.name)
    for topic in repo.topics:
        if topic == 'testing':
            repo_names.append(repo.name)
            break

print(repo_names)
headers = {"Authorization" : "token {}".format(token)}

# read the settings from the yaml file
with open("settings.yaml", "r") as file:
    target_settings = yaml.load(file, Loader=yaml.FullLoader)


no_repos_updated = 0

for repo in repo_names: 
    # print(repo)
    res = requests.get(GITHUB_API_URL + "repos/{}/{}".format(ORG_NAME,repo), headers = headers)
    res_dict = res.json()

    # iterate over the keys of the settings dictionary and updading
    # the settings of the repos when the values of the keys
    for key in target_settings:
        # pprint(res_dict)
        if res_dict.get(key) != target_settings.get(key):
            no_repos_updated += 1
            settings = {key: target_settings.get(key)}
            update = requests.patch(GITHUB_API_URL + "repos/{}/{}".format(ORG_NAME, repo), headers = headers, data = json.dumps(settings))
            #print(update.status_code)
            if update.status_code == 200:
                print("The value of key {} of repo {} has been updated successfully".format(key,repo))
            else:
                print("No need to update")

print("The number of repos that have been updated is: {}".format(no_repos_updated))


