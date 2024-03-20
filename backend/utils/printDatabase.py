from sqlalchemy import create_engine, MetaData, Table

# 设置你的数据库URI
DATABASE_URI = 'postgresql://zekai:liuzekai@localhost/generatedpaints'
engine = create_engine(DATABASE_URI)

# 反射数据库中的所有表
metadata = MetaData()
metadata.reflect(bind=engine)

for table_name in metadata.tables:
    print(f"Table: {table_name}")
    # 使用 Table 对象来访问每个表
    table = Table(table_name, metadata, autoload_with=engine)
    # 打印表的内容
    with engine.connect() as connection:
        results = connection.execute(table.select()).fetchall()
        for row in results:
            print(row)
    print("\n")
