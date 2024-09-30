import os

from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template
from flask import flash

from flask_bootstrap import Bootstrap5

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ['FLASK_KEY']
bootstrap = Bootstrap5(app)

@app.route("/", methods=["GET"])
def root():
  name = request.args.get('name')
  if name is None: name = ''
  greeting = f"Привет, {name}!"

  return render_template('index.html', greeting=greeting, name=name)

@app.route("/admin", methods=["POST", "GET"])
def admin():
  if request.method == "POST":
    if len(request.form['username']) > 0 and len(request.form['firstname']) > 0 and \
            len(request.form['lastname'])> 0 and  len(request.form['addres'])> 0 and \
            len(request.form['email'])> 0:
      flash("Успешно", category="success")
    else:
      flash("Ошибка", category="error")
  return render_template("admin.html")

@app.route("/status/")
def status():
  return jsonify({ 'status': 'ok' })

if __name__ == "__main__":
  app.run()
