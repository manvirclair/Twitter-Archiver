from __future__ import print_function
import twitter
import os
import json
import time
from collections import  deque
from datetime import datetime



class TList:



    def __init__(self, list_name):
        self.list_name = list_name
        self.last_tweets_a = [None for i in range(100)]

        time_sn = 'saved_json' + time.ctime().replace(' ', '_').replace(':', '') + '.json'
        new_tweets = api.GetListTimeline(owner_screen_name=config['owner_screen_name'], slug=list_name, include_rts=True,
                                         count=200, return_json=True)
        std_tweets = sorted(new_tweets, key=lambda x: datetime.strptime(x['created_at'], '%a %b %d %H:%M:%S %z %Y'))

        fd = open(os.path.abspath(data_path + list_name + "_" + time_sn), 'w')
        fd.write(json.dumps(std_tweets))
        fd.close()
        self.saved_till = datetime.strptime(std_tweets[-1]['created_at'], '%a %b %d %H:%M:%S %z %Y')
        self.last_last_dt = datetime.strptime(std_tweets[-1]['created_at'], '%a %b %d %H:%M:%S %z %Y')
        self.save_mark = 0
    def api_store_list(self):
        iter_save_mark = 0
        time_sn = 'saved_json' + time.ctime().replace(' ', '_').replace(':', '') + '.json'
        new_tweets = api.GetListTimeline(owner_screen_name=config['owner_screen_name'], slug=self.list_name, include_rts=True,
                                         count=200, return_json=True)

        nt_l = sorted(new_tweets, key=lambda x: datetime.strptime(x['created_at'], '%a %b %d %H:%M:%S %z %Y'))
        new_last_index = 0
        for i, pj_dic in enumerate(nt_l):
            if datetime.strptime(pj_dic['created_at'], '%a %b %d %H:%M:%S %z %Y') == self.last_last_dt:
                new_last_index =  i 
                break

        new_tbs = nt_l[new_last_index + 1:]
        print('new ones:(' + self.list_name + ') \n')
        for pj_dic in new_tbs:
            print(' ' + pj_dic['text'] + '\n')
            self.last_tweets_a[self.save_mark] = pj_dic
            self.save_mark += 1
            if self.save_mark == 100:
                st_name = self.saved_till.strftime("%Y-%b-%d_%H%M%S")
                last_last_dt_name = self.last_last_dt.strftime("%Y-%b-%d_%H%M%S")
                fd = open(os.path.abspath(data_path + self.list_name + "_" \
                                        + st_name + 'to' + last_last_dt_name + '.json'), 'w')
                fd.write(json.dumps(list(self.last_tweets_a)))
                fd.close()
                print('saved {0} tweets from list {1} at'.format(self.save_mark, self.list_name) + time.ctime() + '\n')
                self.saved_till = self.last_last_dt
                self.save_mark = 0
        print('save_mark: (' + self.list_name + ') ' +  str(self.save_mark) + '\n')


        self.last_last_dt = datetime.strptime(nt_l[-1]['created_at'], '%a %b %d %H:%M:%S %z %Y')
        

def load_files(path):
    files =  os.listdir(path)



def get_list_tls():
    tlists = []

    for list_name in config['lists']:
        tlists.append(TList(list_name))
    for tlist in tlists:
        tlist.api_store_list()
    while 1:
        for tlist in tlists:
            tlist.api_store_list()
        print('checked at' + time.ctime())
        time.sleep(100)


def load_config(config_file, path):
    global config
    global data_path
    with open(config_file) as cf:
        config = json.load(cf)[0]
    data_path = path
    
    
def create_api_instance():
    global CONSUMER_KEY
    global CONSUMER_SECRET
    global ACCESS_TOKEN
    global ACCESS_TOKEN_SECRET

    CONSUMER_KEY = config['auth']['CONSUMER_KEY']
    CONSUMER_SECRET = config['auth']['CONSUMER_SECRET']
    ACCESS_TOKEN = config['auth']['ACCESS_TOKEN']
    ACCESS_TOKEN_SECRET = config['auth']['ACCESS_TOKEN_SECRET']

    global api
    api = twitter.Api(consumer_key=CONSUMER_KEY,
                      consumer_secret=CONSUMER_SECRET,
                      access_token_key=ACCESS_TOKEN,
                      access_token_secret=ACCESS_TOKEN_SECRET)


