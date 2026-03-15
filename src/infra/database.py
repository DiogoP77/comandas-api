from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from settings import STR_DATABASE

# cria o engine do banco
engine = create_engine(STR_DATABASE, echo=True)

# sessão
Session = sessionmaker(bind=engine, autocommit=False, autoflush=True)

# base das tabelas
Base = declarative_base()

# cria as tabelas
async def cria_tabelas():
    Base.metadata.create_all(engine)

# dependência para rotas
def get_db():
    db_session = Session()
    try:
        yield db_session
    finally:
        db_session.close()