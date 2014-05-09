import time
import praw
import re
import requests
from pprint import pprint
r = praw.Reddit(user_agent='')
r.login()

if r.is_logged_in():
    print "logged in"
already_done = []
def get_soup(url):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-Agent' : user_agent }
    request = requests.get(url, headers=headers)
    print request.text
    return request.text 


while True:
    subreddit = r.get_subreddit('test_2')
    for submission in subreddit.get_new(limit=10): 
        print submission
        kd = get_soup('http://karmadecay.com/r/test_2/comments/'+submission.id)
        mul = re.compile("Found [0-9] very similar images")
        one = re.compile("Found [0-9] very similar image")
        if mul.search(kd) or one.search(kd):
            if submission.id not in already_done:
                print submission.id
                submission.remove(False)
                already_done.append(submission.id) 
    time.sleep(1800)
