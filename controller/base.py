from application.controller import success
from fastapi import APIRouter

router = APIRouter()


@router.get('/')
def get_root():
    return success({'Hello': 'World'})
