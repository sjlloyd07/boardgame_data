#! python
# gamepage_parser.py

'''
Each function returns specific info from the 
game soup element and returns NA if none is found.

'''

import logging


logging.basicConfig(
                    filename='log.log', 
                    filemode='w', 
                    encoding='utf-8', 
                    format='%(asctime)s | %(levelname)s: %(message)s',
                    level=logging.DEBUG
                    )


def get_type(soup_object):
    """Search soup element for game type and return."""    
    try:
        # returns full string from friendlyname attribute
        game_type = soup_object.find('rank', {'type':'family'}).get('friendlyname')        
        # extract first string (game type) from the returned attribute string
        game_type = game_type[:game_type.find(' ')].upper()
    # throw error if no attribute is found and return 'NA'
    except AttributeError as e:
        logging.warning(f'TYPE not found. {e}')
        game_type = 'NA'
    return game_type


def get_rank(soup_object):
    """Search soup element for game rank and return.""" 
    try:
        rank = soup_object.find('rank', {'friendlyname':'Board Game Rank'}).get('value')
    # throw error if no attribute is found and return 'NA'
    except AttributeError as e:
        logging.warning(f'RANK not found. {e}')
        rank = 'NA'
    return rank


def get_name(soup_object):
    """Search soup element for game name and return.""" 
    try:
        name = soup_object.find('name', {'type':'primary'}).get('value')
        # name = name.decode('ANSI')
    # throw error if no attribute is found and return 'NA'
    except AttributeError as e:
        logging.warning(f'NAME not found. {e}')
        name = 'NA'
    return name


def get_publisher(soup_object):
    """Search soup element for game publisher and return.""" 
    try:
        publisher = soup_object.find('link', {'type':'boardgamepublisher'}).get('value')
    # throw error if no attribute is found and return 'NA'
    except AttributeError as e:
        logging.warning(f'PUBLISHER not found. {e}')
        publisher = 'NA'
    return publisher


def get_year_pub(soup_object):
    """Search soup element for game year published and return.""" 
    try:
        year_pub = soup_object.find('yearpublished').get('value')
    # throw error if no attribute is found and return 'NA'
    except AttributeError as e:
        logging.warning(f'YEAR PUB not found. {e}')
        year_pub = 'NA'
    return year_pub


def get_rating(soup_object):
    """Search soup element for game rating and return.""" 
    try:
        # round value to one decimal place
        rating = round(float(soup_object.find('average').get('value')),1)
    # throw error if no attribute is found and return 'NA'
    except AttributeError as e:
        logging.warning(f'RATING not found. {e}')
        rating = 'NA'
    return rating


def get_weight(soup_object):
    """Search soup element for game weight and return.""" 
    try:
        # round value to one decimal place
        weight = round(float(soup_object.find('averageweight').get('value')),1)
    # throw error if no attribute is found and return 'NA'
    except AttributeError as e:
        logging.warning(f'WEIGHT not found. {e}')
        weight = 'NA'
    return weight


def get_min_play(soup_object):
    """Search soup element for game minimum players and return.""" 
    try:
        min_play = soup_object.find('minplayers').get('value')
    # throw error if no attribute is found and return 'NA'
    except AttributeError as e:
        logging.warning(f'MIN PLAY not found. {e}')
        min_play = 'NA'
    return min_play


def get_max_play(soup_object):
    """Search soup element for game max players and return.""" 
    try:
        max_play = soup_object.find('maxplayers').get('value')
    # throw error if no attribute is found and return 'NA'
    except AttributeError as e:
        logging.warning(f'MAX PLAY not found. {e}')
        max_play = 'NA'
    return max_play



def get_play_time(soup_object):
    """Search soup element for estimated game play time and return.""" 
    try:
        play_time = soup_object.find('playingtime').get('value')
    # throw error if no attribute is found and return 'NA'
    except AttributeError as e:
        logging.warning(f'PLAY TIME not found. {e}')
        play_time = 'NA'
    return play_time


def get_min_age(soup_object):
    """Search soup element for recommended minimum age and return.""" 
    try:
        min_age = soup_object.find('minage').get('value')
        # min_age cannot be 0
        if int(min_age) == 0:
            min_age = 'NA'
    # throw error if no attribute is found and return 'NA'
    except AttributeError as e:
        logging.warning(f'MIN AGE not found. {e}')
        min_age = 'NA'
    return min_age


def get_img_link(soup_object):
    """Search soup element for game art image link and return."""
    try:
        img_link = soup_object.find('image').text
    # throw error if no attribute is found and return 'NA'
    except AttributeError as e:
        logging.warning(f'IMG LINK not found. {e}')
        img_link = 'NA'
    return img_link


def get_best_player(soup_object):
    """Search soup element for community poll best player count and return."""
    try:    
        # find poll results
        poll_object = soup_object.find('poll', {'name':'suggested_numplayers'})
        # new dict for best player counts, votes
        player_num_poll = {}

        # find and loop through poll results and add 'Best' votes to dict
        for ro in poll_object.find_all('results'):
            numplayers = ro.get('numplayers') # assign numplayers from results object    
            player_num_poll[numplayers] = {} # create dict for each numplayer
            best = ro.find('result',{'value':'Best'}) # assign 'Best' result object to variable
            player_num_poll[numplayers] = int(best.get('numvotes')) # assign 'Best' numvalue to numplayer in dict
        # loop through 'Best' results and return player count w/ the most votes
        for player, count in player_num_poll.items():
            if count == max(list(player_num_poll.values())):                
                best_player = player                
            else:
                continue
        # try-catch cast best_player as int
        try:
            best_player = int(best_player)
        except ValueError as e:
            logging.warning(f'BEST PLAYER is str: "{best_player}". {e}')
            best_player = 'NA'

    # throw error if no attribute is found or best_player is str and return 'NA'
    except AttributeError as e:
        logging.warning(f'BEST PLAYER not found. {e}')
        best_player = 'NA'

    return best_player



# TODO: get category

# TODO: get mechanic