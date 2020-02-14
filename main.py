from fastapi import FastAPI
from application import router, config
import uvicorn
import sys
import getopt

app = FastAPI()
router.register_controllers(app)
router.register_middlewares(app)


def main():
    # get application config
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'e:', ['env='])  # no error handling here
    except getopt.GetoptError as e:
        raise e
    for o, a in opts:
        if o == '-e':
            if a == 'prod':
                print('Application running in production mode...')
                config.load_cfg('prod')
    if not config.get_instance():
        print('Application running in development mode...')
        config.load_cfg('dev')
        cfg = config.get_instance()
        if not cfg:
            raise Exception('Failed to load config!')
    # run application
    uvicorn.run('main:app', **config.get_app_cfg())


if __name__ == '__main__':
    main()
