from fastapi import FastAPI
from config import router
import uvicorn
import json

app = FastAPI()

router.register_controllers(app)
router.register_middlewares(app)

app_cfg = json.loads(open('./config/app.json').read())
logger_cfg = json.loads(open('./config/logger.json').read())

if __name__ == '__main__':
    uvicorn.run('main:app', **dict(app_cfg, **{
        'log_config': logger_cfg,
    }))
