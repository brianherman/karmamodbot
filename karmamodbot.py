import time
import praw
import re
import requests
import yaml

#grab stuff from config file
config_file = open('config.yaml')
yaml        = yaml.safe_load(config_file)
username    = yaml['username']
password    = yaml['password']
subreddit_to_mod   = yaml['subreddit']
reply       = yaml['disclaimer']

reply = reply.replace("{{subreddit}}",subreddit_to_mod) 

r = praw.Reddit(user_agent=username)

r.login(username, password)

if r.is_logged_in():
    print "logged in"

already_done = []

def check_kd(url):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-Agent' : user_agent }
    request = requests.get(url, headers=headers)
    print request.text
    return request.text 

while True:
    subreddit = r.get_subreddit(subreddit_to_mod)
    for submission in subreddit.get_new(limit=10): 
        kd = check_kd('http://karmadecay.com/r/'+subreddit_to_mod+'/comments/'+submission.id)
        mul = re.compile("Found [0-9] very similar images")
        one = re.compile("Found [0-9] very similar image")
        if mul.search(kd) or one.search(kd):
            if submission.id not in already_done:
                print submission.id
                submission.add_comment(reply)
                submission.remove(False)
                already_done.append(submission.id) 
    time.sleep(1800)
