import logging

from radish import after, world


@after.each_scenario()
def cleanup(scenario):
    """ Kill flask app process """
    try:
        world.config.user_data['process'].kill()
        world.config.user_data['process'].communicate()
    except ProcessLookupError as e:
        logging.warning(e)
