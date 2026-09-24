import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


def load_posts():
    with open("blog_posts.json", "r") as file:
        return json.load(file)

def save_posts(posts):
    with open("blog_posts.json", "w") as file:
        json.dump(posts, file, indent=4)

def fetch_post_by_id(post_id):
    blog_posts = load_posts()

    for post in blog_posts:
        if post["id"] == post_id:
            return post

    return None

@app.route("/")
def index():
    blog_posts = load_posts()

    return render_template("index.html", posts=blog_posts)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        author = request.form.get("author")
        title = request.form.get("title")
        content = request.form.get("content")

        blog_posts = load_posts()

        if blog_posts:
            new_id = max(post["id"] for post in blog_posts) + 1
        else:
            new_id = 1

        new_post = {
            "id": new_id,
            "author": author,
            "title": title,
            "content": content,
            "likes": 0
        }

        blog_posts.append(new_post)
        save_posts(blog_posts)

        return redirect(url_for("index"))

    return render_template("add.html")

@app.route("/update/<int:post_id>", methods=["GET", "POST"])
def update(post_id):
    post = fetch_post_by_id(post_id)

    if post is None:
        return "Post not found", 404

    if request.method == "POST":
        blog_posts = load_posts()

        for blog_post in blog_posts:
            if blog_post["id"] == post_id:
                blog_post["author"] = request.form.get("author")
                blog_post["title"] = request.form.get("title")
                blog_post["content"] = request.form.get("content")
                break

        save_posts(blog_posts)

        return redirect(url_for("index"))

    return render_template("update.html", post=post)

@app.route("/delete/<int:post_id>")
def delete(post_id):
    blog_posts = load_posts()

    for post in blog_posts:
        if post["id"] == post_id:
            blog_posts.remove(post)
            break

    save_posts(blog_posts)

    return redirect(url_for("index"))

@app.route("/like/<int:post_id>")
def like(post_id):
    blog_posts = load_posts()

    for post in blog_posts:
        if post["id"] == post_id:
            post["likes"] += 1
            break

    save_posts(blog_posts)

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
