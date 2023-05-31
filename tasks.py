from app_instance import create_app
from database import db
from models.apolices import Endereco, Inquilino, Beneficiario, Item, Produto


app = create_app()


def validate_house_payload(payload):
    with app.app_context():
        item = payload.pop("item")
        endereco = Endereco(**item.get("endereco"))
        db.session.add(endereco)
        inquilino = Inquilino(**item.get("inquilino"))
        db.session.add(inquilino)
        beneficiario = Beneficiario(**item.get("beneficiario"))
        db.session.add(beneficiario)
        item_obj = Item(
            endereco=endereco,
            inquilino=inquilino,
            beneficiario=beneficiario,
        )

        db.session.add(item_obj)
        db.session.commit()

        produto = Produto(item=item_obj, **payload)
        db.session.add(produto)
        db.session.commit()
        produtos = Produto.query.all()
        print(produtos)

        print(app.config.get("SQLALCHEMY_DATABASE_URI"))


def validate_car_payload(payload):
    with app.app_context():
        item = payload.pop("item")
        item_obj = Item(**item)

        db.session.add(item_obj)
        db.session.commit()

        produto = Produto(item=item_obj, **payload)
        db.session.add(produto)
        db.session.commit()
