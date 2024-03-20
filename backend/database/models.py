# database/models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from . import Base  # import the Base object

class Prompt(Base):
    __tablename__ = 'prompts'

    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    translated_text = Column(String)
    real_prompt = Column(String, nullable=False)

    images = relationship('Image', back_populates='prompt')


class Image(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True)
    file_path = Column(String, nullable=False)
    prompt_id = Column(Integer, ForeignKey('prompts.id'), nullable=False)
    creation_time = Column(DateTime, nullable=False)
    selected = Column(Boolean, default=False)

    prompt = relationship('Prompt', back_populates='images')


class ModelVersion(Base):
    __tablename__ = 'model_versions'

    id = Column(Integer, primary_key=True)
    version_name = Column(String(100), nullable=False)
    description = Column(String)

# from flask_sqlalchemy import SQLAlchemy
#
# db = SQLAlchemy()
#
#
# class Image(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     file_path = db.Column(db.String(200), nullable=False)
#     prompt_id = db.Column(db.Integer, db.ForeignKey('prompt.id'), nullable=False)
#     creation_time = db.Column(db.DateTime, nullable=False)
#     selected = db.Column(db.Boolean, default=False)
#
#     prompt = db.relationship('Prompt', backref=db.backref('images', lazy='dynamic'))
#
#
# class Prompt(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     text = db.Column(db.Text, nullable=False)
#     translated_text = db.Column(db.Text)
#     real_prompt = db.Column(db.Text, nullable=False)
#
#
# class ModelVersion(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     version_name = db.Column(db.String(100), nullable=False)
#     description = db.Column(db.Text)
