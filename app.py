from fastapi import FastAPI
from application import router

# init app
app = FastAPI()
router.register_controllers(app)
router.register_middlewares(app)
