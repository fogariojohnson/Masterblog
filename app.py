from flask import Flask, render_template
import json

app = Flask(__name__)


@app.route('/')
def index():
    # add code here to fetch the job posts from a file
    with open("user.json", "r") as file_obj:
        blog_posts = json.loads(file_obj.read())
    return render_template('index.html', posts=blog_posts)


if __name__ == '__main__':
    app.run()
