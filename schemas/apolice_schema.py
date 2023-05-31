from marshmallow import Schema, fields, pre_load, ValidationError


class EnderecoSchema(Schema):
    rua = fields.String(required=True)
    numero = fields.Integer(required=True)


class InquilinoSchema(Schema):
    nome = fields.String(required=True)
    CPF = fields.Integer(required=True)


class BeneficiarioSchema(Schema):
    nome = fields.String(required=True)
    CNPJ = fields.Integer(required=True)


class ItemPayload1Schema(Schema):
    endereco = fields.Nested(
        EnderecoSchema, required=True, data_key="endereço"
    )
    inquilino = fields.Nested(InquilinoSchema, required=True)
    beneficiario = fields.Nested(BeneficiarioSchema, required=True)


class ItemPayload2Schema(Schema):
    placa = fields.String(required=True)
    chassis = fields.Integer(required=True)
    modelo = fields.String(required=True)


class Payload1Schema(Schema):
    produto = fields.Integer(required=True)
    item = fields.Nested(ItemPayload1Schema, required=True)
    preco_total = fields.Float(required=True)
    parcelas = fields.Integer(required=True)

    @pre_load
    def map_keys(self, data, **kwargs):
        valores = data.pop("valores", None)
        if valores:
            data["preco_total"] = valores.get("precoTotal")
            data["parcelas"] = valores.get("parcelas")
            return data
        raise ValidationError(
            "valores é um campo obrigatório", "valores", data=data
        )


class Payload2Schema(Schema):
    produto = fields.Integer(required=True)
    item = fields.Nested(ItemPayload2Schema, required=True)
    preco_total = fields.Float(required=True)
    parcelas = fields.Integer(required=True)

    @pre_load
    def map_keys(self, data, **kwargs):
        valores = data.pop("valores", None)
        if valores:
            data["preco_total"] = valores.get("precoTotal")
            data["parcelas"] = valores.get("parcelas")
            return data
        raise ValidationError(
            "valores é um campo obrigatório", "valores", data=data
        )
