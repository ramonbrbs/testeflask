from marshmallow import Schema, fields, ValidationError, post_load
from validate_docbr import CPF, CNPJ
from .entities import Transaction, Store
import re


def validate_cpf(data):
    cpf = CPF()
    valid = cpf.validate(data)
    if not data or not valid:
        raise ValidationError("Cpf is not valid")


def validate_cnpj(data):
    cnpj = CNPJ()
    valid = cnpj.validate(data)
    if not data or not valid:
        raise ValidationError("CNPJ is not valid")


class CnpjField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        return '{}.{}.{}/{}-{}'.format(value[:2], value[2:5], value[5:8], value[8:12], value[12:])

    def _deserialize(self, value, attr, data, **kwargs):
        import re
        return re.sub('[^0-9]', '', value)


class StoreSchema(Schema):
    name = fields.String(data_key="nome")
    cnpj = CnpjField(data_key="cnpj")
    owner = fields.String(data_key="dono")
    phone = fields.String(data_key="telefone")


class TransactionSchema(Schema):
    store = CnpjField(data_key="estabelecimento", validate=validate_cnpj)
    client = fields.String(data_key="cliente", validate=validate_cpf)
    price = fields.Decimal(data_key="valor", required=True)
    description = fields.String(data_key="descricao", required=True)

    @post_load
    def make_user(self, data, **kwargs):
        cnpj = data['store']
        del data['store']
        transaction = Transaction(**data)
        transaction.store = Store(cnpj=cnpj)
        return transaction


class TransactionsPerStore(Schema):
    store = fields.Nested(StoreSchema, data_key="estabelecimento")
    transactions = fields.Nested(TransactionSchema(only=('client', 'price', 'description')),
                                 data_key="transacoes", many=True)
    total_received = fields.Decimal(data_key='total_recebido')
