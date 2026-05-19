from sqlalchemy import Column, Integer, VARCHAR, Float, LargeBinary
from src.infra.database import Base


class ProdutoDB(Base):

    __tablename__ = "tb_produto"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nome = Column(VARCHAR(100), index=True, nullable=False)
    preco = Column(Float, nullable=False)
    foto = Column(LargeBinary, nullable=True)