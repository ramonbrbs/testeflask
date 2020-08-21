class Store:

    def __init__(self, cnpj, name=None, owner=None, phone=None):
        self.name = name
        self.cnpj = cnpj
        self.owner = owner
        self.phone = phone


class Transaction:

    def __init__(self, store: Store=None, client=None, price=None, description=None):
        self.store = store
        self.client = client
        self.price = price
        self.description = description
