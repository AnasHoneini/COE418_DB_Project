from flask import Flask, render_template

app= Flask(__name__, template_folder="templates", static_folder="static")

@app.route('/')
def hello_world():
    return render_template('index.html') 

@app.route('/home')
def home():
      return 'hello world'

@app.route('/login')
def login():
    return render_template('login.html') 

@app.route('/login/signup')
def signup():
    return render_template('signup.html')         

if __name__=="__main__":
        app.run()

