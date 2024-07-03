from environs import Env

env = Env()
env.read_env()

QUART_HOST = env.str("QUART_HOST")
QUART_PORT = env.int("QUART_PORT")
QUART_DEBUG = env.bool("QUART_DEBUG")

VERSION = "0.1.0"