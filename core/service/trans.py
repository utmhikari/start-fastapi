"""
Service: Trans
"""
from core.model.trans import TransManager


MANAGER: TransManager = TransManager()


def get_manager() -> TransManager:
    """
    get transaction manager instance
    :return: trans manager
    """
    global MANAGER
    if not isinstance(MANAGER, TransManager):
        MANAGER = TransManager()
    return MANAGER
