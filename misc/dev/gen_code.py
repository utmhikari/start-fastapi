"""
generate code for handlers, model and services
"""
import os

from core.lib.util import ENCODING


def snake_to_camel(word: str) -> str:
    """
    snake case to camel case
    see https://www.w3resource.com/python-exercises/re/python-re-exercise-37.php
    :param word: word string
    :return: camel case workd
    """
    return ''.join(x.capitalize() or '_' for x in word.split('_'))


# handler template
HANDLER_TEMPLATE = \
    '''"""
{handler_name_camel} Handlers
"""
from typing import List, Dict, Any, Tuple, Optional, Union, Callable

from fastapi import APIRouter, BackgroundTasks

from core.model.handler import Resp
from core.lib import util, logger
from core.service import trans as trans_service


LOGGER = logger.for_handler('{handler_name}')
ROUTER = APIRouter()


@ROUTER.get('/api/v1/{handler_name}s')
def get_{handler_name}s():
    """
    get {handler_name}s
    :return: None
    """
    pass


@ROUTER.get('/api/v1/{handler_name}s/{{{handler_name}_id}}')
def get_{handler_name}({handler_name}_id: int):
    """
    get {handler_name} by id
    :param {handler_name}_id: {handler_name} ID
    :return: None
    """
    pass


@ROUTER.post('/api/v1/{handler_name}s')
def create_{handler_name}(body: Dict[str, Any]):
    """
    create {handler_name} instance
    replace body with your own model
    :param body: post body
    :return: None
    """
    pass


@ROUTER.put('/api/v1/{handler_name}s')
def update_{handler_name}(body: Dict[str, Any]):
    """
    update {handler_name} instance
    replace body with your own model
    :param body: put body
    :return: None
    """
    pass


@ROUTER.delete('/api/v1/{handler_name}s')
def delete_{handler_name}():
    """
    update {handler_name} instance
    :return: None
    """
    pass
'''


def gen_handler(handler_name: str):
    """
    generate handler
    :param handler_name: handler name
    :return: None
    """
    handler_path = os.path.join('app', 'handler', '%s.py' % handler_name)
    if os.path.isfile(handler_path):
        print('cannot generate handler %s! file already exists: %s' %
              (handler_name, handler_path))
        return
    handler_code = HANDLER_TEMPLATE.format(
        handler_name=handler_name,
        handler_name_camel=snake_to_camel(handler_name)
    )
    with open(handler_path, mode='w', encoding=ENCODING) as f:
        f.write(handler_code)
        f.close()


# model template
MODEL_TEMPLATE = \
    '''"""
{model_name_camel} Models
"""
from enum import Enum, IntEnum
from typing import List, Dict, Any, Tuple, Optional, Union, Callable

from pydantic import BaseModel

from core.lib import util, logger
from core.model.base import PCallRet, ExecRet


LOGGER = logger.for_model('{model_name}')


class {model_name_camel}(BaseModel):
    """
    {model_name_camel} Model
    """
    pass
'''


def gen_model(model_name: str):
    """
    generate model
    :param model_name: model name
    :return: None
    """
    model_path = os.path.join('app', 'model', '%s.py' % model_name)
    if os.path.isfile(model_path):
        print('cannot generate model %s! file already exists: %s' %
              (model_name, model_path))
        return
    model_code = MODEL_TEMPLATE.format(
        model_name=model_name,
        model_name_camel=snake_to_camel(model_name)
    )
    with open(model_path, mode='w', encoding=ENCODING) as f:
        f.write(model_code)
        f.close()


# service template
SERVICE_TEMPLATE = \
    '''"""
{service_name_camel} Service
"""
from typing import List, Dict, Any, Tuple, Optional, Union, Callable

from core.model.base import PCallRet, ExecRet
from core.lib import util, logger, cfg
from core.service import trans as trans_service


LOGGER = logger.for_service('{service_name}')


def get_{service_name}s() -> None:
    """
    get {service_name}s
    """
    pass


def get_{service_name}({service_name}_id: int) -> None:
    """
    get {service_name}
    :param {service_name}_id: {service_name} ID
    """
    pass


def create_{service_name}() -> None:
    """
    create {service_name} instance
    fill the params with your own model
    """
    pass


def update_{service_name}() -> None:
    """
    update {service_name} instance
    fill the params with your own model
    """
    pass


def delete_{service_name}() -> None:
    """
    delete {service_name} instance
    fill the params with your own model
    """
    pass
'''


def gen_service(service_name: str):
    """
    generate service
    :param service_name: service name
    :return: None
    """
    service_path = os.path.join('app', 'service', '%s.py' % service_name)
    if os.path.isfile(service_path):
        print('cannot generate service %s! file already exists: %s' %
              (service_name, service_path))
        return
    service_code = SERVICE_TEMPLATE.format(
        service_name=service_name,
        service_name_camel=snake_to_camel(service_name)
    )
    with open(service_path, mode='w', encoding=ENCODING) as f:
        f.write(service_code)
        f.close()


# ============= CONFIGS, SET NAMES AS SNAKE CASE ===============
IS_GEN_HANDLER = False
HANDLER_NAMES = [
    'item'
]

IS_GEN_MODEL = False
MODEL_NAMES = [
    'item'
]

IS_GEN_SERVICE = False
SERVICE_NAMES = [
    'item'
]

if __name__ == '__main__':
    # RUN THIS SCRIPT WITH WORKING DIRECTORY AS PROJECT ROOT DIRECTORY!
    if IS_GEN_HANDLER:
        for name in HANDLER_NAMES:
            name = name.strip()
            if name:
                print('Generate Handler: %s' % name)
                gen_handler(name)
    else:
        print('IS_GEN_HANDLER: False')
    if IS_GEN_MODEL:
        for name in MODEL_NAMES:
            name = name.strip()
            if name:
                print('Generate Model: %s' % name)
                gen_model(name)
    else:
        print('IS_GEN_MODEL: False')
    if IS_GEN_SERVICE:
        for name in SERVICE_NAMES:
            name = name.strip()
            if name:
                print('Generate Service: %s' % name)
                gen_service(name)
    else:
        print('IS_GEN_SERVICE: False')
