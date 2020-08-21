from flask import Blueprint, request
from marshmallow import ValidationError
from .schema import TransactionSchema, TransactionsPerStore
from ..context import AppContext

transaction_blueprint = Blueprint('transaction', __name__, url_prefix='/v1/transacao')


@transaction_blueprint.route('/', methods=['POST'])
def register_payment():
    json_data = request.get_json()
    if not json_data:
        return '',400

    try:
        context = AppContext()
        transactionSchema = TransactionSchema()
        data = transactionSchema.load(json_data)

        if not context.StoreRepository.get(data.store.cnpj):
            return {"aceito": False, "errors": ["Loja inexistente no banco de dados."]},400
        context.TransactionRepository.add(data)

    except ValidationError as err:
        return {"aceito": False, "errors": err.messages}, 422
    return {"aceito": True}, 200


@transaction_blueprint.route('/', methods=['GET'])
def get_payments():
    try:
        context = AppContext()
        schema = TransactionsPerStore()
        store = context.StoreRepository.get_transactions_per_store("45.283.163/0001-67")
        if not store:
            return {"aceito": False},404
        return schema.dump(store)


    except ValidationError as err:
        return {"aceito": False, "errors": err.messages}, 422
