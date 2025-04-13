from flask import Flask, render_template, request, jsonify
from Api import get_answer

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_answer", methods=["POST"])
def get_answer_route():
    data = request.get_json()
    question = data.get("question", "")
    answer = get_answer(question)
    return jsonify({"answer": answer})


@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)
