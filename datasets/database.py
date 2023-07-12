
from collections.abc import Collection
from sqlalchemy import Engine, MetaData, Table, Column
from sqlalchemy.schema import CreateSchema

class Database:
    def engine(self) -> Engine:
        """Return the SQL engine"""
        raise NotImplementedError()

    def schema(self) -> str:
        """Select a schema"""
        return None

    def metadata(self) -> MetaData:
        """Return Metadata"""
        if not hasattr(self, '_metadata'):
            self._metadata = MetaData()
            self._metadata.reflect(bind=self.engine(), schema=self.schema())
        return self._metadata

    def tables(self) -> Collection[Table]:
        """Return all the tables"""
        return self.metadata().sorted_tables
    
class MutableDatabase(Database):
    def schema(self) -> str:
        if not hasattr(self, '_schema'):
            self._schema = None
        return self._schema

    def add_schema(self, schema: str):
        with self.engine().connection() as connection:
            connection.execute(CreateSchema(schema))
    
    def set_schema(self, schema: str):
        self._schema = schema
        

        