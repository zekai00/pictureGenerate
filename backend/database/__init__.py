# database/__init__.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URI = 'postgresql://zekai:liuzekai@localhost/generatedpaints'

# create a standard SQLAlchemy engine
engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create a custom base class for declarative class definitions
Base = declarative_base()


# 使用Base.metadata.create_all(bind=engine)来创建表格
def create_tables():
    Base.metadata.create_all(bind=engine)

# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from flask_sqlalchemy import SQLAlchemy
#
# DATABASE_URI = 'postgresql://zekai:liuzekai@localhost/generatedpaints'
#
# engine = create_engine(DATABASE_URI)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
# Base = declarative_base()
#
# db = SQLAlchemy()
#
# def init_app(app):
#     app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
#     db.init_app(app)
#
# def create_tables():
#     db.create_all()
#
# # from .models import GeneratedPaint
# #
# # def add_generated_paint(user_id, prompt, image_path1, image_path2):
# #     new_paint = GeneratedPaint(user_id=user_id, prompt=prompt, image_path1=image_path1, image_path2=image_path2)
# #     db.session.add(new_paint)
# #     db.session.commit()