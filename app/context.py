from .transaction.repository import TransactionMongoRepository
from .transaction.repository import StoreMongoRepository


class AppContext:

    def __init__(self):
        self.TransactionRepository = TransactionMongoRepository()
        self.StoreRepository = StoreMongoRepository()