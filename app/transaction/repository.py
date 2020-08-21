from .. import mongo
from mongoengine import (StringField, DecimalField, ReferenceField)
from .entities import Transaction, Store
import re


class StoreMongoModel(mongo.Document):
    owner = StringField(required=True)
    cnpj = StringField(required=True, unique=True)
    phone = StringField(required=True)
    name = StringField(required=True)

    def from_entity(self, entity: Store):
        self.owner = entity.owner
        self.cnpj = entity.cnpj
        self.phone = entity.phone
        self.name = entity.name

    def to_entity(self):
        entity = Store(cnpj=self.cnpj, name=self.name,owner=self.owner,phone=self.phone)
        return entity


class TransactionMongoModel(mongo.Document):
    client = StringField(required=True)
    price = DecimalField(required=True)
    description = StringField(required=True)
    store = ReferenceField(StoreMongoModel)

    def from_entity(self, entity: Transaction):
        self.client = entity.client
        self.price = entity.price
        self.description = entity.description
        self.store = StoreMongoModel.objects(cnpj=re.sub('[^0-9]', '', entity.store.cnpj)).first()

    def to_entity(self):
        entity = Transaction(self.store, self.client, self.price,
                             self.description)
        return entity


class TransactionMongoRepository:
    def __init__(self):
        self.transaction = TransactionMongoModel()


    def add(self, entity):
        self.transaction.from_entity(entity)
        self.transaction.save()

    def get(self, page=1, per_page=20):
        TransactionMongoModel.objects.paginate(page=page, per_page=per_page)

    def delete_all(self):
        TransactionMongoModel.objects().delete()


class StoreMongoRepository:
    def __init__(self):
        self.store = StoreMongoModel()

    def add(self, entity):
        self.store.from_entity(entity)
        self.store.save()

    def get_transactions_per_store(self, store_cnpj, page=1, per_page=10):
        store_cnpj = re.sub('[^0-9]', '', store_cnpj)
        store : StoreMongoModel = StoreMongoModel.objects(cnpj=store_cnpj).first()
        if not store:
            return None
        store_entity = store.to_entity()
        transactions = TransactionMongoModel.objects(store=store.id).all()
        transactions_entities = [t.to_entity() for t in transactions]
        total_received = sum([t.price for t in transactions_entities])
        return {'store': store_entity, 'transactions':transactions_entities, 'total_received': total_received}

    def delete_all(self):
        StoreMongoModel.objects().delete()

    def get(self, cnpj):
        return StoreMongoModel.objects(cnpj=cnpj)
