from sqlalchemy import create_engine, MetaData, text

# Connect to the [Relational Dataset Repository](https://relational.fit.cvut.cz/)
engine = create_engine("mysql+mysqldb://guest:relational@relational.fit.cvut.cz:3306")

print(engine)

metadata = MetaData()
metadata.reflect(bind=engine, schema='financial')

for table in metadata.tables:
    print(table)

with engine.connect() as connection:
    result = connection.execute(text('SELECT * FROM financial.account'))
    for row in result:
        print(row)
