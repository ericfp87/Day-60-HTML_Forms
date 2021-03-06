from flask import Flask, render_template, request
import requests
import smtplib

MY_USER = "teste@teste.com"
MY_PASSWORD = "abc@123"

posts = requests.get("https://api.npoint.io/43644ec4f0013682fc0d").json()

app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        send_mail(data['username'], data['email'], data['phone'], data['message'])
        return render_template("contact.html", msg_sent=True)
    else:
        return render_template("contact.html", msg_sent=False)

def send_mail(username, email, phone, message):
    email_message = f"Subject:Nova Mensagem\n\nName: {username}\nEmail: {email}\nTelefone: {phone}\nMensagem: {message}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_USER, password=MY_PASSWORD)
        connection.sendmail(from_addr=MY_USER, to_addrs=MY_USER, msg=email_message)


if __name__ == "__main__":
    app.run(debug=True)
