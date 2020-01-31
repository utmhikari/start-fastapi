from fastapi import FastAPI
from controller import base, item

app = FastAPI()

# router -> controller callback
app.get('/')(base.get_root)
app.get('/items/{item_id}')(item.get_item)
app.put('/items/{item_id}')(item.save_item)
