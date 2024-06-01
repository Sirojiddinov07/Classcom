"""
New secret key
"""
from django.core.management import utils

from common.env import env

print(utils.get_random_secret_key())
