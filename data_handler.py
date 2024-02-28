#! python
# game_data.py



import requests
import os
import csv
import logging

from bs4 import BeautifulSoup as bs 
from requests.adapters import HTTPAdapter, Retry 

import gamepage_parser as gpp



logging.basicConfig(filename='log.log', 
                    filemode='w', 
                    encoding='utf-8', 
                    format='%(asctime)s | %(levelname)s: %(message)s',
                    level=logging.INFO
                    )



# Creates custom session object w/ Retry configuration included.
def create_session():
    """Create and return custom session object to navigate urls."""    
    #instantiate Session
    session = requests.Session()
    
    # Configure Retry to apply to session
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[ 429, 502, 503, 504 ]) 

    # mount HTTPAdapter w/ Retry configuration to session
    session.mount('https://', HTTPAdapter(max_retries=retries)) 
    
    # return custom configured session object
    return session




def get_ids(session, url) -> list:
    """
    Parse ranked games page and search
    for game ids.
    Return list of game ids.
    
    Args:
        session object: custom session object
        url: page w/ list of ranked games
    
    Returns:
        list: game ids
    """

    # get response
    try:
        res = session.get(url)      
    except Exception as e:
        logging.error(f'Connection Error: {e}')
    
    # parse response object
    try:
        soup = bs(res.text, 'lxml')
    except Exception as e:
        logging.error(f'Parsing Error: {e}')

    # define holding list
    id_list = []
    
    # loop through page row elements that contain game details
    for i in soup.find_all(id='row_'):
        # find game id in element and add to id_list
        id_string = i.find('td', {'class':'collection_thumbnail'}).a.get('href')
        game_id = id_string.split('/')[2]
        
        id_list.append(game_id)

    return id_list




def get_data(s, id_list) -> list:
    """
    Create api url from list of game ids.
    Parse api response content and return data about every game.
    Add data to list.

    Args:
        session object: custom session object
        id_list: list of game ids
    
    Returns:
        details_list: list of dictionaries that contain game data
    """
    # join ids for use in api url
    ids_joined = ','.join(id_list)    
    
    # define list to hold details
    details_list = []

    # base url for api page with game data in xml format
    API_URL = 'https://boardgamegeek.com/xmlapi2/thing?stats=1&id='

    # attempt to get api response w/ joined ids list
    # contains all game data
    try:
        # create response object from game api page (bgg xmlapi2)
        api_ro = s.get(API_URL + ids_joined)
        api_ro.raise_for_status() # check res object status
        logging.info('API connection successful.')

    except requests.exceptions.HTTPError as e:
        logging.error(f'Error connecting to API: {e}')  


    # create soup element from response
    api_soup = bs(api_ro.text, features="lxml-xml")

    # iterate through page 'boardgame' elements that contain data
    # input game data into dictionary and add to list
    for i in api_soup.find_all(type='boardgame'):        
        game_details = {}
        game_details['rank'] = gpp.get_rank(i)
        game_details['name'] = gpp.get_name(i)
        game_details['publisher'] = gpp.get_publisher(i)
        game_details['year_pub'] = gpp.get_year_pub(i)
        game_details['game_type'] = gpp.get_type(i)
        game_details['rating'] = gpp.get_rating(i)
        game_details['weight'] = gpp.get_weight(i)
        game_details['min_players'] = gpp.get_min_play(i)
        game_details['max_players'] = gpp.get_max_play(i)
        game_details['best_players'] = gpp.get_best_player(i)
        game_details['play_time'] = gpp.get_play_time(i)
        game_details['min_age'] = gpp.get_min_age(i)
        game_details['game_pg_url'] = ('https://boardgamegeek.com/boardgame/' + i['id'])
        game_details['game_img'] = gpp.get_img_link(i)

        details_list.append(game_details)

    logging.info(f'Data items added: {len(details_list)}')

    return details_list
    
    


def write_to_file(save_file, data_list):
    """
    Write game data to csv file.
     
    Args:
        save_file: filepath of csv file to save to
        data_list: list of dictionaries containing game details
        
    """
    # establish csv headers for retrieved data
    HEADERS = ['rank', 'name', 'publisher', 'year_pub', 
               'game_type', 'rating', 'weight', 'min_players', 
               'max_players', 'best_players', 'play_time', 
               'min_age', 'game_pg_url', 'game_img']

    # save game list to save file
    with open(save_file, 'a', newline='', encoding='utf-8') as csv_object:
        csv_writer = csv.DictWriter(csv_object, fieldnames=HEADERS)
        
        if os.path.getsize(save_file) == 0:
            csv_writer.writeheader()

        for row in data_list:
            csv_writer.writerow(row)

    logging.info(f'{len(data_list)} data items written to file.')



