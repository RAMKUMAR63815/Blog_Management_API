# Blog Management API

A simple **Blog Management API** built using **FastAPI, SQLite, SQLAlchemy ORM, JWT Authentication, and Email Notifications**.

## 🚀 Project Overview

This project is a mini blogging system where authenticated users can:

* Register and login
* Create blog posts
* View blog posts
* Update their own posts
* Delete their own posts
* Add comments to posts
* View comments
* Like and unlike posts
* Receive email notifications for new comments and likes

The API also provides Swagger documentation for easy API testing.

---

## 🛠️ Technologies Used

* Python
* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* JWT Authentication
* Passlib
* Bcrypt
* SMTP / Gmail
* Uvicorn
* Swagger UI

---

## 📁 Project Structure

```text
Blog_Management_API/
│
├── .env
├── blog.db
├── requirements.txt
├── README.md
│
└── app/
    ├── __init__.py
    ├── main.py
    ├── database.py
    ├── models.py
    ├── schemas.py
    ├── auth.py
    ├── dependencies.py
    │
    ├── utils/
    │   ├── __init__.py
    │   └── email.py
    │
    └── routers/
        ├── __init__.py
        ├── auth.py
        ├── posts.py
        ├── comments.py
        └── likes.py
```

---

## 🗄️ Database

The project uses **SQLite** with **SQLAlchemy ORM**.

Database file:

```text
blog.db
```

### Database Tables

The following tables are created automatically:

1. `users`
2. `posts`
3. `comments`
4. `likes`

### Users Table

Stores registered users.

```text
id
username
email
password
```

Passwords are stored in **hashed form**, not as plain text.

### Posts Table

Stores blog posts.

```text
id
title
content
author_id
created_at
```

### Comments Table

Stores comments made on blog posts.

```text
id
post_id
user_id
text
created_at
```

### Likes Table

Stores likes given to posts.

```text
id
post_id
user_id
```

A user can like a particular post only once.

---

## 🔐 Authentication

The API uses **JWT (JSON Web Token)** authentication.

### Register

```http
POST /auth/register
```

Example request:

```json
{
  "username": "ramkumar",
  "email": "ramkumar@example.com",
  "password": "password123"
}
```

### Login

```http
POST /auth/login
```

Example request:

```json
{
  "email": "ramkumar@example.com",
  "password": "password123"
}
```

The login API returns an access token.

Use the token to access protected APIs.

---

## 📝 Post APIs

### Create Post

```http
POST /posts/
```

Authentication required.

Example:

```json
{
  "title": "My First Blog",
  "content": "This is my first blog post using FastAPI."
}
```

### View All Posts

```http
GET /posts/
```

This endpoint is publicly accessible.

### View One Post

```http
GET /posts/{post_id}
```

### View My Posts

```http
GET /posts/mine
```

Authentication required.

### Update Post

```http
PUT /posts/{post_id}
```

Only the post owner can update the post.

Example:

```json
{
  "title": "Updated Blog Title",
  "content": "Updated blog content."
}
```

### Delete Post

```http
DELETE /posts/{post_id}
```

Only the post owner can delete the post.

---

## 💬 Comment APIs

### Add Comment

```http
POST /comments/posts/{post_id}
```

Authentication required.

Example:

```json
{
  "text": "Great blog post!"
}
```

### View Comments

```http
GET /comments/posts/{post_id}
```

Comments can be viewed publicly.

---

## ❤️ Like APIs

### Like Post

```http
POST /likes/posts/{post_id}
```

Authentication required.

### Unlike Post

```http
DELETE /likes/posts/{post_id}
```

Authentication required.

### Get Like Count

```http
GET /likes/posts/{post_id}/count
```

Example response:

```json
{
  "post_id": 1,
  "like_count": 5
}
```

If a user tries to like the same post twice, the API returns an error.

---

## 📧 Email Notifications

The application sends email notifications when:

### New Comment

When another user comments on a post, the post owner receives an email notification.

### New Like

When another user likes a post, the post owner receives an email notification.

Email configuration is stored in the `.env` file.

Example:

```env
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

**Never commit your real email password or App Password to GitHub.**

---

## ✅ Validation

Pydantic is used for request validation.

Examples:

* Username must contain at least 3 characters
* Password must contain at least 6 characters
* Email must be valid
* Post title must contain at least 3 characters
* Post content must contain at least 10 characters
* Comment text cannot be empty

Invalid data is rejected by the API.

---

## 🔒 Ownership Protection

Users can update or delete **only their own posts**.

For example:

```text
User 1 → Post 1
User 2 → Post 2
```

User 1 can update/delete Post 1.

User 1 cannot update/delete Post 2.

The API returns:

```text
403 Forbidden
```

when a user attempts to modify another user's post.

---

## ▶️ Installation

### 1. Clone or download the project

Open the project folder in VS Code.

### 2. Create virtual environment

Open PowerShell in the project folder:

```powershell
python -m venv venv
```

### 3. Activate virtual environment

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the project root and add your email configuration.

### 6. Run the FastAPI server

```powershell
uvicorn app.main:app --reload
```

The application will run at:

```text
http://127.0.0.1:8000
```

---

## 📚 Swagger Documentation

FastAPI automatically provides interactive API documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

Swagger can be used to test:

* Authentication
* Posts
* Comments
* Likes
* Validation
* Authorization

---

## 🧪 API Testing Flow

Recommended testing order:

### Step 1

Register a user.

```text
POST /auth/register
```

### Step 2

Login.

```text
POST /auth/login
```

Copy the returned access token.

### Step 3

Authorize in Swagger.

Click **Authorize** and enter:

```text
Bearer YOUR_ACCESS_TOKEN
```

### Step 4

Create a post.

```text
POST /posts/
```

### Step 5

View posts.

```text
GET /posts/
```

### Step 6

Add a comment.

```text
POST /comments/posts/{post_id}
```

### Step 7

Like the post.

```text
POST /likes/posts/{post_id}
```

### Step 8

Check like count.

```text
GET /likes/posts/{post_id}/count
```

### Step 9

Unlike the post.

```text
DELETE /likes/posts/{post_id}
```

### Step 10

Update and delete your own post.

---

## 🗃️ SQLite Verification

The SQLite database can be opened using **DB Browser for SQLite**.

Open:

```text
blog.db
```

The following tables can be checked:

```text
users
posts
comments
likes
```

SQL queries:

```sql
SELECT * FROM users;
```

```sql
SELECT * FROM posts;
```

```sql
SELECT * FROM comments;
```

```sql
SELECT * FROM likes;
```

---

## 📸 Project Deliverables

The following screenshots can be included for submission:

* Swagger `/docs`
* User registration
* User login
* Create post
* View posts
* Update post
* Delete post
* Add comment
* Like post
* Unlike post
* Email notification
* SQLite `users` table
* SQLite `posts` table
* SQLite `comments` table
* SQLite `likes` table

---

## 🎯 Features Completed

* [x] FastAPI application
* [x] SQLite database
* [x] SQLAlchemy ORM
* [x] User registration
* [x] Password hashing
* [x] JWT authentication
* [x] User login
* [x] Post creation
* [x] Post viewing
* [x] Post update
* [x] Post deletion
* [x] Post ownership validation
* [x] Comments
* [x] Likes
* [x] Unlike functionality
* [x] Duplicate like validation
* [x] Pydantic validation
* [x] Email notifications
* [x] Swagger documentation
* [x] SQLite table verification

---

## 👨‍💻 Author

**Ramkumar S**

B.Tech Computer Science and Engineering

---

## 📌 Conclusion

The Blog Management API provides a complete backend blogging system using FastAPI. It includes secure authentication, database management, post CRUD operations, comments, likes, ownership authorization, validation, and email notifications.
