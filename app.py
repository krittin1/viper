# requests are objects that flask handle
from flask import Flask, render_template, request
# import os

# APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)


@app.route('/', defaults={'snake': ''}, methods=['GET', 'POST'])

def homepage(snake):
    return render_template('snake.html')

if __name__=='__main__':
    app.debug = True;

    app.run();






if __name__ == "__main__":
    app.run(port=4555, debug=True)
