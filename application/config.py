from typing import Dict, Any
import json
import os


_CONFIG: Dict[str, Any] = dict()
_CONFIG_ROOT: str = 'config'
_DEV_CONFIG_PATH: str = 'dev.json'
_PROD_CONFIG_PATH: str = 'prod.json'
_APP_MODE: str = 'dev'
_APP_KEY: str = 'fastapi'


def _get_cfg_json(*args) -> Dict:
    """
    load json config from specific config path
    :param args: path
    :return: json config
    """
    return json.loads(open(os.path.join(_CONFIG_ROOT, *args)).read())


def load_cfg(mode: str):
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
    if not get_app_cfg():
        raise Exception('Failed to load application config')
    # load logger config
    if 'logger' in _CONFIG.keys():
        log_config = None
        raw_logger_cfg = _CONFIG['logger']
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


def get_instance() -> Dict[str, Any]:
    """
    get config instance
    :return: _CONFIG
    """
    return _CONFIG


def get_cfg(key: str) -> Dict:
    """
    get config
    :param key: config key
    :return: config
    """
    return _CONFIG.get(key, None)


def get_app_cfg() -> Dict:
    """
    load config path to global CONFIG
    :return: None
    """
    return _CONFIG.get(_APP_KEY, None)
