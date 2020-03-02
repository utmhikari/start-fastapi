from fastapi import FastAPI
from application import router
import os
import sys
from typing import Dict, Any
import pprint

"""
USE os.getenv() TO GET ENV VARS IN dev.cfg OR prod.cfg
"""

env: str = os.getenv('ENV')
app_name: str = os.getenv('APP_NAME')
description: str = os.getenv('DESCRIPTION')
version: str = os.getenv('VERSION')

fastapi_cfg: Dict[str, Any] = {
    'debug': env != 'prod',
    'title': app_name,
    'description': description,
    'version': version
}

# init app
app = FastAPI(**fastapi_cfg)
router.register_controllers(app)
router.register_middlewares(app)

print('Launching application: %s\n%s' %
      (app_name, pprint.pformat(fastapi_cfg, indent=2, width=50)), file=sys.stderr)
