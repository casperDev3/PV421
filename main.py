from flask import Flask, render_template, request
from datetime import datetime
from db.posts import POSTS

app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.route('/')
def root():
    return render_template("index.html", current_time=datetime.now(), title="Home Page - 012")


@app.route('/about')
def about():
    return render_template("about.html", current_time=datetime.now(), title="About Page - 012", is_show=False)


# Endpoints for posts
@app.route('/api/posts/', methods=['POST'])
def create_post():
    payload = request.get_json()
    new_post = {
        "id": len(POSTS) + 1,
        "title": payload.get("title"),
        "content": payload.get("content"),
        "author": payload.get("author"),
        "date_posted": datetime.now().strftime("%Y-%m-%d")
    }
    POSTS.append(new_post)
    return {
        "status": 201,
        "success": True,
        "message": "Post created successfully",
        "data": new_post,
        "meta": {
            "timestamp": datetime.now().isoformat(),
            "version": "0.0.1",
            "total_posts": len(POSTS)
        }
    }, 201


@app.route('/api/posts/', methods=['GET'])
def get_posts():
    return {
        "status": 200,
        "success": True,
        "message": "Posts retrieved successfully",
        "data": POSTS,
        "meta": {
            "timestamp": datetime.now().isoformat(),
            "version": "0.0.1",
            "total_posts": len(POSTS)
        }
    }, 200

@app.route('/api/posts/<int:post_id>/', methods=['GET'])
def get_post(post_id):
    post = next((post for post in POSTS if post["id"] == post_id), None)
    if post:
        return {
            "status": 200,
            "success": True,
            "message": "Post retrieved successfully",
            "data": post,
            "meta": {
                "timestamp": datetime.now().isoformat(),
                "version": "0.0.1"
            }
        }, 200
    else:
        return {
            "status": 404,
            "success": False,
            "message": "Post not found",
            "data": None,
            "meta": {
                "timestamp": datetime.now().isoformat(),
                "version": "0.0.1"
            }
        }, 404

@app.route('/api/posts/<int:post_id>/',  methods=['DELETE'])
def delete_post(post_id):
    global POSTS
    post = next((post for post in POSTS if post["id"] == post_id), None)
    if post:
        POSTS = [p for p in POSTS if p["id"] != post_id]
        return {
            "status": 200,
            "success": True,
            "message": "Post deleted successfully",
            "data": None,
            "meta": {
                "timestamp": datetime.now().isoformat(),
                "version": "0.0.1"
            }
        }, 200
    else:
        return {
            "status": 404,
            "success": False,
            "message": "Post not found",
            "data": None,
            "meta": {
                "timestamp": datetime.now().isoformat(),
                "version": "0.0.1"
            }
        }, 404

@app.route('/api/posts/<int:post_id>/', methods=['PUT'])
def update_post(post_id):
    payload = request.get_json()
    post = next((post for post in POSTS if post["id"] == post_id), None)
    if post:
        post.update({
            "title": payload.get("title", post["title"]),
            "content": payload.get("content", post["content"]),
            "author": payload.get("author", post["author"]),
            "date_posted": datetime.now().strftime("%Y-%m-%d")
        })
        return {
            "status": 200,
            "success": True,
            "message": "Post updated successfully",
            "data": post,
            "meta": {
                "timestamp": datetime.now().isoformat(),
                "version": "0.0.1"
            }
        }, 200
    else:
        return {
            "status": 404,
            "success": False,
            "message": "Post not found",
            "data": None,
            "meta": {
                "timestamp": datetime.now().isoformat(),
                "version": "0.0.1"
            }
        }, 404


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", current_time=datetime.now(), title="404 Not Found - 012"), 404


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
