from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


@app.route('/')
def index():
    # add code here to fetch the job posts from a file
    with open("user.json", "r") as file_obj:
        blog_posts = json.loads(file_obj.read())
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    with open("user.json", "r") as file_obj:
        blog_posts = json.loads(file_obj.read())

    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        # Find the maximum ID in the existing posts
        new_id = max([post['id'] for post in blog_posts]) if blog_posts else 0

        # Create a dictionary for the new blog post
        new_post = {
            'id': new_id + 1,
            'author': author,
            'title': title,
            'content': content
        }

        # Append the new post to the existing data
        blog_posts.append(new_post)

        # Write the updated data back to the JSON file
        with open('user.json', 'w') as new_file:
            json.dump(blog_posts, new_file, indent=4)

        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    with open("user.json", "r") as file_obj:
        blog_posts = json.loads(file_obj.read())

    # Find the post with the matching post_id
    post_to_delete = next((post for post in blog_posts if post['id'] == post_id), None)

    if post_to_delete:
        blog_posts.remove(post_to_delete)

        with open("user.json", "w") as new_file:
            json.dump(blog_posts, new_file, indent=4)

    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    # Fetch the blog posts from the JSON file
    with open("user.json", "r") as file_obj:
        blog_posts = json.loads(file_obj.read())

    # Find the post with the matching post_id
    post = next((post for post in blog_posts if post['id'] == post_id), None)

    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        # Update the post details
        post['author'] = request.form.get('author')
        post['title'] = request.form.get('title')
        post['content'] = request.form.get('content')

        # Write the updated data back to the JSON file
        with open('user.json', 'w') as new_file:
            json.dump(blog_posts, new_file, indent=4)

        return redirect(url_for('index'))

    # If it's a GET request, display the update.html page
    return render_template('update.html', post=post)


@app.route('/like/<int:post_id>', methods=['POST'])
def like(post_id):
    # Fetch the blog posts from the JSON file
    with open("user.json", "r") as file_obj:
        blog_posts = json.loads(file_obj.read())

    # Find the post with the matching post_id
    post = next((post for post in blog_posts if post['id'] == post_id), None)

    if post is None:
        # Post not found
        return "Post not found", 404

    # Increment the likes for the post
    post['likes'] = post.get('likes', 0) + 1

    # Write the updated data back to the JSON file
    with open('user.json', 'w') as new_file:
        json.dump(blog_posts, new_file, indent=4)

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
