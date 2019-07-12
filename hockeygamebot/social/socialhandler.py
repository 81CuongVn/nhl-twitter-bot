"""
A social media wrapper function that handles routing messages to all other defined
social networks in our configuration file.
"""
import logging

from hockeygamebot.helpers import arguments
from hockeygamebot.helpers.config import config
from hockeygamebot.social import discord, slack, twitter


def send(msg, **kwargs):
    """ The handler function that takes a message and a set of key-value arguments
        to be routed to social media functions.

    Args:
        message: The main message to be sent to all social media sites.
        #TODO: **kwargs

    Returns:
        None
    """
    # If for some reason, message is None (or False), just exit the function.
    if not msg:
        return

    args = arguments.get_arguments()
    social_config = config.socials

    if args.notweets:
        logging.info("[SOCIAL] %s", msg)
        # return

    if social_config["twitter"]:
        pass

    if social_config["discord"]:
        discord.send_discord_textonly(msg)

    if social_config["slack"]:
        pass