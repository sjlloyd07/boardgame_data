#!python
# main.py

""" 
Iterates through the list of ranked board games on boardgamegeek.com,
collects information about each board game, writes the data to a csv file,
and copies the data to a PostgreSQL database.
"""

import os
import time
import logging

import data_handler
import db_connector


logging.basicConfig(filename='log.log', 
                    filemode='w', 
                    encoding='utf-8', 
                    format='%(asctime)s | %(levelname)s: %(message)s',
                    level=logging.INFO
                    )


# record the program execution time
logging.info('Start program.')
print('Start program.')
start_time = time.perf_counter()


# rank of first list item on page
# used to iterate ranked items pages
rank_count = 1

# base url for page showing list of ranked games
RANK_URL = f'https://boardgamegeek.com/browse/boardgame?sort=rank&rankobjecttype=subtype&rankobjectid=1&rank='

# used to block ids at 1000 per api call
game_ids = []
# used to block returned api call data
data = []

# create new file to store data
time_now = time.strftime('%Y-%m-%d-%H%M', time.localtime()) 
save_file = os.path.join(os.getcwd(),'data', time_now + '.csv')

open(save_file,'w',newline='').close()

logging.info(f'File created: {os.path.basename(save_file)}')

# create new session
s = data_handler.create_session()



# catch block gets data until reaching end of results pages
try:
    # TODO: change rank_count to True for full list of results
    # return first 1000 ranked games
    while rank_count < 1001:
        # create url from base and new rank count
        url = RANK_URL + f'{rank_count}'

        # find and add game ids to list and iterate to next page
        for i in data_handler.get_ids(s, url):
            game_ids.append(i)

        logging.info(f'Ranked game ids {rank_count}-{rank_count+99} added to list.')
        logging.info(f'ID list length: {len(game_ids)}')

        # add 100 to iterate to first item on next page 
        rank_count += 100

        # if there are 1000 list items: write to file
        # if length of list items not a multiple of 100 (end of list): write to file
        if len(game_ids) == 1000 or len(game_ids) % 100 > 0:
            
            # load api with all game data
            logging.info('Retreive data.')
            data = data_handler.get_data(s, game_ids)
            logging.info(f'{len(data)} items to write.')

            # write data to file
            logging.info('Write data to file.')
            data_handler.write_to_file(save_file, data)


            # empty game_ids list before continuing loop
            game_ids = []
            data = []
            logging.info('Clear lists.')
        

        # pause before get next page details to prevent call abuse
        time.sleep(1)

except Exception as e:
    logging.info(f'End of results.\n{e}')



# database connector
db_connector.database_import(save_file)



end_time = time.perf_counter()
logging.info(f'Program run time: {end_time - start_time}')
print(f'Program run time: {end_time - start_time}')

