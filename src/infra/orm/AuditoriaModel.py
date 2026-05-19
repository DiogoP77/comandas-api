from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from datetime import datetime

from src.infra.database import Base


class AuditoriaDB(Base):
    """Modelo para registrar auditoria de acessos e ações"""

    __tablename__ = "tb_auditoria"

    # 🔑 ID da auditoria
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    # 👤 Funcionário responsável pela ação
    funcionario_id = Column(
        Integer,
        ForeignKey("tb_funcionario.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    # 🧾 Tipo de ação (LOGIN, LOGOUT, CREATE, UPDATE, DELETE...)
    acao = Column(String(50), nullable=False)

    # 📦 Recurso afetado (comanda, produto, cliente...)
    recurso = Column(String(100), nullable=False)

    # 🔗 ID do recurso afetado
    recurso_id = Column(Integer, nullable=True)

    # 📝 Dados antes da alteração
    dados_antigos = Column(Text, nullable=True)

    # 🆕 Dados depois da alteração
    dados_novos = Column(Text, nullable=True)

    # 🌐 Informações de acesso
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)

    # ⏱ Data e hora da ação
    data_hora = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        index=True
    )