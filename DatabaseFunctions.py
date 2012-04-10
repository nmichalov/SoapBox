#!/usr/bin/env python

from pymongo import Connection
import string
import random

"""
Contains the code used to generate and manage the mongo database containing the unique download keys.
"""

def connect_to_db(database, collection):
    """
    A function for connecting to the appropriate collection.
    """
    connection = Connection()
    db = connection[unicode(database)]
    return db[unicode(collection)]



def create_download_database(number_downloads, target_database, target_collection):
    """
    A function for creating the database which contains the unique set of keys for the download,
    and which tracks who those keys are assigned to, and if they're been used.
    """
    urls = []
    while len(urls) < int(number_downloads):
        new_url = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(20))
        if new_url not in urls:
            urls.append(new_url)
        collection = connect_to_db(target_database, target_collection)
    for url in urls:
        download_key = {'key'   : url, 
                        'user'  : 0,
                        'cashed': 0 }
        collection.save(download_key)



def authorize_user(facebook_check, facebook_url, target_database, target_collection):
    """
    A function for assigning keys to users who've earned them.
    """
    if facebook_check:
        collection = connect_to_db(target_database, target_collection)
        if list(collection.find({'user': facebook_url})):
            return 'sorry, only one download per user'
        else:
            download_key = list(collection.find({'user': 0}).limit(1))
            if download_key:
                collection.update({'user': 0}, {'$set': {'user': facebook_url}})
                for i in download_key:
                    return i['key']
            else:
                return 'Sorry, no downloads available'
    else:
        return 'You\'ve got something else to do before you can claim your download'

            



if __name__ == '__main__':
    create_download_database(10, 'downloadDB', 'downloads')
    print authorize_user(True, 'guy', 'downloadDB', 'downloads')

