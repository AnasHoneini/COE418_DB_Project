from flask import Flask, render_template

app= Flask(__name__)

@app.route('/')
def hello_world():
    return 'hello world'

@app.route('/home')
def home():
    return render_template('index1.html')   


if __name__=="__main__":
        app.run(debug=True)
