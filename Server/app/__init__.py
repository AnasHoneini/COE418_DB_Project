#file to tell python that this is a package

from flask import Flask

app = Flask(__name__)  


#import any file from the package
from app import views 
from app import admin_views