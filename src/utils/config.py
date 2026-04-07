import os

from dotenv import load_dotenv

load_dotenv()


def get_config():
    return {
        "clickup": {
            "token": os.getenv("CLICKUP_API_TOKEN"),
            "list_id": os.getenv("CLICKUP_LIST_ID"),
        },
        "trello": {
            "api_key": os.getenv("TRELLO_API_KEY"),
            "token": os.getenv("TRELLO_TOKEN"),
            "board_id": os.getenv("TRELLO_BOARD_ID"),
            "default_list_id": os.getenv("TRELLO_DEFAULT_LIST_ID"),
        },
        "asana": {
            "token": os.getenv("ASANA_TOKEN"),
            "default_project_id": os.getenv("ASANA_DEFAULT_PROJECT_ID"),
        },
        "freedcamp": {
            "api_key": os.getenv("FREEDCAMP_API_KEY"),
            "default_project_id": os.getenv("FREEDCAMP_DEFAULT_PROJECT_ID"),
        },
    }
