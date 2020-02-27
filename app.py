from fastapi import FastAPI
from application import router
import os

# init app
app = FastAPI()
router.register_controllers(app)
router.register_middlewares(app)

print('Launching application: %s' % os.getenv('APP_NAME'))
