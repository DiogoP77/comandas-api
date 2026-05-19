from sqlalchemy import Column, VARCHAR, DECIMAL, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.infra.database import Base


class ComandaDB(Base):
    __tablename__ = "tb_comanda"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    comanda = Column(VARCHAR(100), nullable=False)
    data_hora = Column(DateTime, nullable=False)

    # 0 = aberta, 1 = fechada, 2 = cancelada
    status = Column(Integer, nullable=False, default=0)

    cliente_id = Column(
        Integer,
        ForeignKey("tb_cliente.id", ondelete="RESTRICT"),
        nullable=True
    )

    funcionario_id = Column(
        Integer,
        ForeignKey("tb_funcionario.id", ondelete="RESTRICT"),
        nullable=False
    )

    # 🔥 RELACIONAMENTOS
    cliente = relationship("ClienteDB", backref="comandas")
    funcionario = relationship("FuncionarioDB", backref="comandas")
    produtos = relationship(
        "ComandaProdutoDB",
        back_populates="comanda",
        cascade="all, delete-orphan"
    )


class ComandaProdutoDB(Base):
    __tablename__ = "tb_comanda_produto"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    comanda_id = Column(
        Integer,
        ForeignKey("tb_comanda.id", ondelete="RESTRICT"),
        nullable=False
    )

    produto_id = Column(
        Integer,
        ForeignKey("tb_produto.id", ondelete="RESTRICT"),
        nullable=False
    )

    funcionario_id = Column(
        Integer,
        ForeignKey("tb_funcionario.id", ondelete="RESTRICT"),
        nullable=False
    )

    quantidade = Column(Integer, nullable=False)
    valor_unitario = Column(DECIMAL(10, 2), nullable=False)

    # 🔥 RELACIONAMENTOS
    comanda = relationship("ComandaDB", back_populates="produtos")
    produto = relationship("ProdutoDB")
    funcionario = relationship("FuncionarioDB")