# file to tell python that this is a package
from app import admin_views
from app import views
import db
from flask import Flask


app = Flask(__name__)
app.secret_key = 'anasistheadmin'

# import any file from the package
