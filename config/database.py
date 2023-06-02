import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# nombre de la base de datos
sqlite_filename='../database.sqlite'
base_dir = os.path.dirname(os.path.realpath(__file__))

# se crea en la ruta de este archivo
database_url = f"sqlite:///{os.path.join(base_dir,sqlite_filename)}"

engine = create_engine(database_url, echo=True)
#conexión a la BBDD
session = sessionmaker(bind=engine)

# modo de intección, es propio de Alchemy
Base = declarative_base()