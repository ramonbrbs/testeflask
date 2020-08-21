from .context import AppContext
from .transaction.entities import Store, Transaction


def generate_store_padrao():
    store = Store("45283163000167","Nosso Restaurante de Todo Dia LTDA","Fabio I.", "11909000300")
    context = AppContext()
    context.StoreRepository.add(store)

def register(app):
    @app.cli.command('add-store')
    def add_store():
        generate_store_padrao()

