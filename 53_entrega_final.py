# LAB PROJECT - INTEGRANDO PYTHON COM SQLITE E MONGODB

from pprint import pprint
from datetime import datetime
from sqlalchemy import (create_engine, 
                        inspect, 
                        select, 
                        func, 
                        ForeignKey, 
                        Column, 
                        Integer,
                        String)
from sqlalchemy.orm import (declarative_base, 
                            relationship, 
                            Session)
import pymongo
from pymongo.mongo_client import MongoClient

#SQLITE
Base = declarative_base()


class Cliente(Base):
    __tablename__ = 'cliente'

    id = Column(Integer, primary_key=True)
    nome = Column(String(25), nullable=False)
    cpf = Column(String(11), nullable=False)
    endereco = Column(String(80), nullable=False)

    conta = relationship(
        "Conta", back_populates='cliente', cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'Cliente[id:{self.id}, nome:{self.nome}, cpf:{self.cpf}, endereco:{self.endereco}]'


class Conta(Base):
    __tablename__ = 'conta'

    id = Column(Integer, primary_key=True)
    tipo = Column(String(40), nullable=False)
    agencia = Column(String(40), nullable=False)
    num = Column(Integer, nullable=False)
    cliente_id = Column(Integer, ForeignKey("cliente.id"), nullable=False)

    cliente = relationship(
        "Cliente", back_populates='conta'
    )
    
    def __repr__(self):
        return f'Conta[id:{self.id}, tipo:{self.tipo}, agencia:{self.agencia}, num:{self.num}, cliente_id:{self.cliente_id}]'
    
    
pprint(Cliente.__tablename__)
pprint(Conta.__tablename__)
print('-------------------')


engine = create_engine('sqlite://') #/:memory
Base.metadata.create_all(engine)


inspector_engine = inspect(engine)
pprint(inspector_engine.default_schema_name)
pprint(inspector_engine.get_table_names())
pprint(inspector_engine.has_table('cliente'))
pprint(inspector_engine.has_table('conta'))
print('-------------------')

with Session(engine) as session:
    andre = Cliente(
        nome = 'Andre Myszko',
        cpf = '15968795423',
        endereco = 'rua 232, nro 233, casa, 951456-321, curitiba, PR',
        conta = [Conta(tipo='conta corrente', agencia='1234', num='123')]
    )
    gustavo = Cliente(
        nome = 'Gustavo Myszko',
        cpf = '58556585472',
        endereco = 'rua 432, nro 876, casa, 222222-322, goiania, GO',
        conta = [Conta(tipo='conta deposito', agencia='1234', num='321')]
    )
    patrick = Cliente(
        nome = 'Patrick Estrela',
        cpf = '88899955511',
        endereco = 'rua 765, nro 567, casa, 333333-332, jurassicanduva, AC',
        conta = [Conta(tipo='conta univarsitaria', agencia='4321', num='111')]
    )

    session.add_all([andre, gustavo, patrick])

    session.commit()


stmt_find_usr = select(Cliente).where(Cliente.nome.in_(['Andre','Luiz Gustavo']))
for usr in session.scalars(stmt_find_usr):
    pprint(usr)
print('-------------------')

stmt_find_adrs = select(Conta).where(Conta.cliente_id.in_([1]))
for adrs in session.scalars(stmt_find_adrs):
    pprint(adrs)
print('-------------------')

stmt_order_usr = select(Cliente).order_by(Cliente.nome.desc())
for usr in session.scalars(stmt_order_usr):
    pprint(usr)
print('-------------------')

stmt_join_usr_adrs = select(Cliente.nome, Conta.cliente_id, Conta.id, Conta.agencia, Conta.num, Conta.tipo).join_from(Cliente, Conta)
for res in session.scalars(stmt_join_usr_adrs):
    pprint(res)
print('-------------------')


conn = engine.connect()
if conn:
    print('engine connected')
print('-------------------')


results = conn.execute(stmt_join_usr_adrs).fetchall()
for res in results:
    pprint(res)
print('-------------------')

stmt_count_usr = select(func.count(Cliente.id)).select_from(Cliente)
for res in session.scalars(stmt_count_usr):
    pprint(res)
print('-------------------')


session.close()


#PYMONGO
usr = '<user>'
pwd = '<password>' 
cluster_db = '<cluster>'

uri = f"mongodb+srv://{usr}:{pwd}@{cluster_db}.foeehjb.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client.test
bank = db.bank
collections = db.list_collection_names()


new_bank = [
    {
        'nome': 'Andre Myszko',
        'cpf': '12365478915',
        'endereco': 'rua 232, nro 233, casa, 951456-321, curitiba, PR',
        'conta': ["tipo':'conta corrente', 'agencia':'1234', 'num':123"],
        'date': datetime.utcnow(),
    },
    {
        'nome': 'Gustavo Myszko',
        'cpf': '58556585472',
        'endereco': 'rua 432, nro 876, casa, 222222-322, goiania, GO',
        'conta': ["tipo':'conta poupanca', 'agencia':'1234', 'num':321"],
        'date': datetime.utcnow(),
    },
    {
        'nome': 'Patrick Estrela',
        'cpf': '88899955511',
        'endereco': 'rua 765, nro 567, casa, 333333-332, jurassicanduva, AC',
        'conta': ["tipo':'conta univarsitaria', 'agencia':'4321', 'num':111"],
        'date': datetime.utcnow(),
    }

]

result = bank.insert_many(new_bank)
pprint(result.inserted_ids)
pprint(db.bank.find_one({'nome':'Andre Myszko'}))