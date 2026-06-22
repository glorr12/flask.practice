from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello Oleg!'


@app.route('/user/<name>')
def user_name(name: str) -> str:
    return f"Hello, {name}!"


if __name__ == '__main__':
    app.run(debug=True)
