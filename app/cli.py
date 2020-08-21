from .context import AppContext
import click
from .transaction.entities import Store, Transaction


def _add_standard_store():
    store = Store("45283163000167","Nosso Restaurante de Todo Dia LTDA","Fabio I.", "11909000300")
    context = AppContext()
    context.StoreRepository.add(store)


def _add_store(cnpj, name, owner, phone):
    store = Store(cnpj, name, owner, phone)
    context = AppContext()
    context.StoreRepository.add(store)


def register(app):

    @app.cli.command('add-store')
    @click.argument("cnpj")
    @click.argument("name")
    @click.argument("owner")
    @click.argument("phone")
    def add_store(cnpj,name,owner,phone):
        _add_store(cnpj)

    @app.cli.command('seed')
    def seed():
        _add_standard_store()

