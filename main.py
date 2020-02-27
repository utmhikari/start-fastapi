from typing import Dict, Any
import uvicorn
import sys
import getopt
import os
import json

# load application config
_CONFIG: Dict[str, Any] = dict()
_CONFIG_ROOT: str = 'config/app'
_DEV_CONFIG_PATH: str = 'dev.json'
_PROD_CONFIG_PATH: str = 'prod.json'
_APP_MODE: str = 'dev'
_APP_KEY: str = 'fastapi'
_LOGGER_KEY: str = 'logger'


def _get_cfg_json(*args) -> Dict:
    """
    load json config from specific config path
    :param args: path
    :return: json config
    """
    return json.loads(open(os.path.join(_CONFIG_ROOT, *args)).read())


def _load_cfg(mode: str):
    """
    load config from path to _CONFIG
    :param mode: application mode (dev or prod)
    :return: None
    """
    # get application mode
    if not mode == 'prod' and not mode == 'dev':
        raise Exception('Unknown application mode')
    global _CONFIG
    global _APP_MODE
    _APP_MODE = mode
    if _APP_MODE == 'dev':
        _CONFIG = _get_cfg_json(_DEV_CONFIG_PATH)
    else:
        _CONFIG = _get_cfg_json(_PROD_CONFIG_PATH)
    # check if app config is loaded
    if _APP_KEY not in _CONFIG.keys():
        raise Exception('Failed to load application config')
    # load logger config
    if _LOGGER_KEY in _CONFIG.keys():
        log_config = None
        raw_logger_cfg = _CONFIG[_LOGGER_KEY]
        if isinstance(raw_logger_cfg, dict):
            if 'path' in raw_logger_cfg.keys():
                log_cfg_path = str(raw_logger_cfg['path'])
                try:
                    log_config = _get_cfg_json(log_cfg_path)
                except Exception as e:
                    print('Failed to load logger config at %s! %s' % (log_cfg_path, e))
            if not log_config and 'content' in raw_logger_cfg.keys():
                log_config = raw_logger_cfg['content']
        if log_config and isinstance(log_config, dict):
            _CONFIG[_APP_KEY]['log_config'] = log_config


def main():
    # get application config
    # TODO: 解决config复用问题
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'e:', ['env='])  # no error handling here
    except getopt.GetoptError as e:
        raise e
    for o, a in opts:
        if o == '-e':
            if a == 'prod':
                _load_cfg('prod')
    if not _CONFIG:
        _load_cfg('dev')
        if not _CONFIG:
            raise Exception('Failed to load config!')
    # run application
    uvicorn.run('app:app', **_CONFIG[_APP_KEY])


if __name__ == '__main__':
    main()
