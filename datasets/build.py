from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.schema import CreateSchema
from datasets.sources.financial import Financial
from datasets.databases.postgresql import PostgreSQL

# Get a source db
input = Financial()
for table in input.tables():
    print(table)

# Copy to Postgresql
output = PostgreSQL(port=5432)
output.add_schema(input.schema())
for table in input.tables():
    print(table)
    table.create(output)
