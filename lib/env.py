from dotenv import load_dotenv
from os import getenv

load_dotenv()


def env(env_variable_name):
    return getenv(env_variable_name)
