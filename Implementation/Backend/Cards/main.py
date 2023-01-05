from gada_api.cards_api import start_api
from tools.api_macros import SERVER_PORT
from tools.sqlite_utils import *

if __name__ == '__main__':
    create_table_high_scores()
    # clear_table_high_score()
    start_api(SERVER_PORT)
