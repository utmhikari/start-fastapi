from application.controller import success
from application.logger import get_controller_logger
from fastapi import APIRouter, UploadFile, File

router = APIRouter()

LOGGER = get_controller_logger('BASE')


@router.get('/')
def get_root():
    return success({'Hello': 'World'})


@router.post('/upload')
async def upload_file(file: UploadFile = File(...)):
    filename = file.filename
    content = await file.read()
    LOGGER.info('Received file %s:\n%s' % (
        filename,
        content.decode('utf-8')
    ))
    return success({
        'filename': filename,
        'contentType': file.content_type
    })
