from sqlalchemy import Column, Integer, VARCHAR, CHAR
from src.infra.database import Base


class ClienteDB(Base):

    __tablename__ = "tb_cliente"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nome = Column(VARCHAR(100), nullable=False)
    cpf = Column(CHAR(11), unique=True, nullable=False, index=True)
    telefone = Column(CHAR(11), nullable=False)