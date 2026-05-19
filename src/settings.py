from dotenv import load_dotenv, find_dotenv
import os

# ==============================
# 🔥 LOAD ENV
# ==============================

dotenv_file = find_dotenv()
load_dotenv(dotenv_file)


# ==============================
# 🔥 API CONFIG
# ==============================

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
RELOAD = os.getenv("RELOAD", "True").lower() == "true"


# ==============================
# 🔥 DATABASE CONFIG
# ==============================

DB_SGDB = os.getenv("DB_SGDB", "sqlite")
DB_NAME = os.getenv("DB_NAME", "database")

DB_HOST = os.getenv("DB_HOST", "")
DB_USER = os.getenv("DB_USER", "")
DB_PASS = os.getenv("DB_PASS", "")


# ==============================
# 🔥 CONNECTION STRING
# ==============================

if DB_SGDB == "sqlite":
    # SQLite
    STR_DATABASE = f"sqlite:///{DB_NAME}.db"

elif DB_SGDB == "postgres":
    STR_DATABASE = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

elif DB_SGDB == "mysql":
    STR_DATABASE = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

else:
    raise Exception("Banco de dados não suportado")


# ==============================
# 🔥 ASYNC DATABASE
# ==============================

if STR_DATABASE.startswith("sqlite:///"):
    ASYNC_STR_DATABASE = STR_DATABASE.replace(
        "sqlite:///", "sqlite+aiosqlite:///"
    )

elif STR_DATABASE.startswith("postgresql://"):
    ASYNC_STR_DATABASE = STR_DATABASE.replace(
        "postgresql://", "postgresql+asyncpg://"
    )

elif STR_DATABASE.startswith("mysql"):
    ASYNC_STR_DATABASE = STR_DATABASE.replace(
        "mysql+pymysql://", "mysql+aiomysql://"
    )

else:
    ASYNC_STR_DATABASE = STR_DATABASE


# ==============================
# 🔥 JWT CONFIG
# ==============================

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "sua-chave-secreta-super-forte-mudar-em-producao"
)

ALGORITHM = os.getenv("ALGORITHM", "HS256")

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
)

REFRESH_TOKEN_EXPIRE_DAYS = int(
    os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7")
)


# ==============================
# 🔥 CORS
# ==============================

origins_env = os.getenv("CORS_ORIGINS")

if origins_env:
    CORS_ORIGINS = [origin.strip() for origin in origins_env.split(",")]
else:
    CORS_ORIGINS = ["*"]