#file to tell python that this is a package
import db
from flask import Flask


app = Flask(__name__)
app.secret_key ='anasistheadmin'

#import any file from the package
from app import views 
