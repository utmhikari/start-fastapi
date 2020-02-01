from application.controller import success


def get_root():
    return success({'Hello': 'World'})
