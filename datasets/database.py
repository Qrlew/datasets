
from collections.abc import Collection
from io import StringIO
import logging
from sqlalchemy import Engine, MetaData, Table, Column, create_mock_engine, select, insert
from sqlalchemy.schema import CreateSchema, CreateTable

logger = logging.getLogger(__name__)

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

    def dump(self) -> str:
        """Return the CREATE TABLE statement"""
        result = StringIO()
        def dump(sql, *multiparams, **params) -> str:
            return result.write(str(sql.compile(dialect=self.engine().dialect)))
        engine = create_mock_engine('postgresql+psycopg://', dump)
        self.metadata().create_all(engine, checkfirst=True)
        return result.getvalue()
    
class MutableDatabase(Database):
    def schema(self) -> str:
        if not hasattr(self, '_schema'):
            self._schema = None
        return self._schema

    def add_schema(self, schema: str):
        logger.info(f'Add schema {schema}')
        with self.engine().connect() as conn:
            conn.execute(CreateSchema(schema, if_not_exists=True))
            conn.commit()
        self.set_schema(schema)
    
    def set_schema(self, schema: str):
        self._schema = schema
        
    def add(self, source: Database):
        logger.info(f'Add {source}')
        self.add_schema(source.schema())
        with self.engine().connect() as conn:
            for table in source.tables():
                # Remove indexes to avoid name collisions
                table.indexes.clear()
                # TODO maybe we can rename indexes
                table.create(conn, checkfirst=True)
                conn.commit()
            # Push data
            with source.engine().connect() as src_conn:
                for table in source.tables():
                    logger.info(f'Loading data from {table}')
                    rows = src_conn.execute(select(table))
                    for row in rows:
                        logger.info(row)
                        conn.execute(insert(table).values(row))
                    conn.commit()

        