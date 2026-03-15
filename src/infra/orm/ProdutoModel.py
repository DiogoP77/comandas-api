from infra import database
from sqlalchemy import Column, Integer, VARCHAR, Float, LargeBinary

class ProdutoDB(database.Base):

    __tablename__ = "tb_produto"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nome = Column(VARCHAR(100), index=True, nullable=False)
    preco = Column(Float, nullable=False)
    foto = Column(LargeBinary)