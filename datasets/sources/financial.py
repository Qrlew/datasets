from collections.abc import Collection
from sqlalchemy import Engine, create_engine
from datasets.database import Database

class Financial(Database):
    def engine(self) -> Engine:
        return create_engine("mysql+pymysql://guest:relational@relational.fit.cvut.cz:3306")
    
    def schema(self) -> str:
        return 'financial'
