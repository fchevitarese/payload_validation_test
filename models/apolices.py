from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

from database import db


class Endereco(db.Model):
    __tablename__ = "endereco"
    id = Column(Integer, primary_key=True, autoincrement=True)
    rua = Column(String)
    numero = Column(Integer)


class Inquilino(db.Model):
    __tablename__ = "inquilino"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    CPF = Column(Integer)


class Beneficiario(db.Model):
    __tablename__ = "beneficiario"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    CNPJ = Column(Integer)


class Item(db.Model):
    __tablename__ = "item"
    id = Column(Integer, primary_key=True, autoincrement=True)
    endereco_id = Column(Integer, ForeignKey("endereco.id"), nullable=True)
    inquilino_id = Column(Integer, ForeignKey("inquilino.id"), nullable=True)
    beneficiario_id = Column(
        Integer, ForeignKey("beneficiario.id"), nullable=True
    )
    endereco = relationship("Endereco")
    inquilino = relationship("Inquilino")
    beneficiario = relationship("Beneficiario")
    placa = Column(String, nullable=True)
    chassis = Column(Integer, nullable=True)
    modelo = Column(String, nullable=True)


class Produto(db.Model):
    __tablename__ = "produto"
    id = Column(Integer, primary_key=True, autoincrement=True)
    produto = Column(Integer)
    item_id = Column(Integer, ForeignKey("item.id"))
    item = relationship("Item")
    preco_total = Column(Float)
    parcelas = Column(Integer)
