from typing import Dict, Any
import uvicorn
import sys
import getopt
import os
import json

"""
MAIN ENTRY OF START_FASTAPI
WHICH LOADS CONFIG FOR UVICORN BUT NOT FOR FASTAPI APP
JUST MODIFY CONFIGS IN config/app IF NEEDED
"""

# load application config
CONFIG: Dict[str, Any] = dict()
CONFIG_ROOT: str = 'config/uvicorn'
DEV_CONFIG_PATH: str = 'dev.json'
PROD_CONFIG_PATH: str = 'prod.json'
APP_MODE: str = 'dev'
APP_KEY: str = 'app'
LOGGER_KEY: str = 'logger'


def __print(*args):
    print(*args, file=sys.stderr)


def __get_cfg_json(*args) -> Dict:
    """
    load json config from specific config path
    :param args: path
    :return: json config
    """
    return json.loads(open(os.path.join(CONFIG_ROOT, *args)).read())


def __load_cfg(mode: str):
    """
    load config from path to _CONFIG
    :param mode: application mode (dev or prod)
    :return: None
    """
    # get application mode
    if not mode == 'prod' and not mode == 'dev':
        raise Exception('Unknown application mode')
    global CONFIG
    global APP_MODE
    APP_MODE = mode
    if APP_MODE == 'dev':
        CONFIG = __get_cfg_json(DEV_CONFIG_PATH)
    else:
        CONFIG = __get_cfg_json(PROD_CONFIG_PATH)
    # check if app config is loaded
    if APP_KEY not in CONFIG.keys():
        raise Exception('Failed to load application config')
    # load logger config
    if LOGGER_KEY in CONFIG.keys():
        log_config = None
        raw_logger_cfg = CONFIG[LOGGER_KEY]
        if isinstance(raw_logger_cfg, dict):
            if 'path' in raw_logger_cfg.keys():
                log_cfg_path = str(raw_logger_cfg['path'])
                try:
                    log_config = __get_cfg_json(log_cfg_path)
                except Exception as e:
                    __print('Failed to load logger config at %s! %s' % (log_cfg_path, e))
            if not log_config and 'content' in raw_logger_cfg.keys():
                log_config = raw_logger_cfg['content']
        if log_config and isinstance(log_config, dict):
            CONFIG[APP_KEY]['log_config'] = log_config


def __preset_eventloop():
    """
    change SelectorEventLoop to ProactorEventLoop
    :return:
    """
    from uvicorn.config import LOOP_SETUPS
    LOOP_SETUPS['asyncio'] = 'application.compat:set_proactor_eventloop'


def main():
    # Windows users may need this for calling some methods in asyncio
    # DO NOT ENABLE RELOAD IF U AIM TO CHANGE THE EVENTLOOP POLICY!!!
    # __preset_eventloop()
    # get application config
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'e:t:', ['env=', 'tag='])  # no error handling here
    except getopt.GetoptError as e:
        raise e
    env = 'dev'
    for o, a in opts:
        if o == '-e':
            if a == 'prod':
                env = 'prod'
        elif o == '-t':
            __print('launch app with tag: %s' % a)
    __load_cfg(env)
    if not CONFIG:
        raise Exception('Failed to load config!')
    # run application
    uvicorn.run('app:app', loop='asyncio', **CONFIG[APP_KEY])


if __name__ == '__main__':
    main()
