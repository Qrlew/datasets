from sqlalchemy import create_engine, MetaData, text
from datasets import postgresql

# # Connect to the [Relational Dataset Repository](https://relational.fit.cvut.cz/)
# input_engine = create_engine("mysql+pymysql://guest:relational@relational.fit.cvut.cz:3306")
# metadata = MetaData()
# metadata.reflect(bind=input_engine, schema='financial')

# for table in metadata.tables:
#     print(table)

# with input_engine.connect() as connection:
#     result = connection.execute(text('SELECT * FROM financial.account'))
#     for row in result:
#         print(row)

output_engine = postgresql.create_engine(port=5433)

print(output_engine)