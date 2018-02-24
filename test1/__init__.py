from flask import Flask
import pymysql
pymysql.install_as_MySQLdb()

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('test1.setting')     #模块下的setting文件名，不用加py后缀

db = SQLAlchemy(app)

from test1.model.models import User, Category
from test1.controller import blog_message