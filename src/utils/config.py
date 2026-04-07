import os

from dotenv import load_dotenv

load_dotenv()


def get_config():
    return {
        "clickup": {
            "token": os.getenv("CLICKUP_API_TOKEN"),
            "list_id": os.getenv("CLICKUP_LIST_ID"),
        },
        "plane": {
            "token": os.getenv("PLANE_API_TOKEN"),
            "base_url": os.getenv("PLANE_BASE_URL", "https://app.plane.so/api"),
        },
        "wekan": {
            "api_url": os.getenv("WEKAN_API_URL"),
            "user_id": os.getenv("WEKAN_USER_ID"),
            "token": os.getenv("WEKAN_API_TOKEN"),
        },
        "kanboard": {
            "api_url": os.getenv("KANBOARD_API_URL"),
            "username": os.getenv("KANBOARD_USERNAME"),
            "password": os.getenv("KANBOARD_PASSWORD"),
        },
    }
