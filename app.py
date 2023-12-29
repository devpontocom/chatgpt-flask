import os
from flask import Flask, render_template, request, session
from openai import OpenAI


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

app = Flask(__name__)

app.secret_key = "BAD_SECRET_KEY"

client = OpenAI(
    api_key=OPENAI_API_KEY,
)


def chatgpt_send_message(pergunta_do_formulario):
    context = """Voce é um atendente de sac"""
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": pergunta_do_formulario},
        ],
    )
    return {"role": "assistant", "content": completion.choices[0].message.content}


@app.route("/", methods=("GET", "POST"))
def send_messages():
    if request.method == "POST":
        pergunta = request.form["pergunta"]
        user_message = {"role": "user", "content": pergunta}
        historico_chat = session.get("historico_chat", [])
        historico_chat.append(user_message)
        historico_chat.append(chatgpt_send_message(pergunta))
        session["historico_chat"] = historico_chat
        return render_template("index.html", historico_chat=session["historico_chat"])
    return render_template("index.html")


@app.route("/delete-chat", methods=("POST",))
def delete_chat():
    session["historico_chat"] = []
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
