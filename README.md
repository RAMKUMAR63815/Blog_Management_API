# Blog Management API

A simple **Blog Management API** built using **FastAPI, SQLite, SQLAlchemy ORM, JWT Authentication, Image Uploads, Pagination, Search, and Email Notifications**.

---

## 🚀 Project Overview

This project is a mini blogging system where authenticated users can:

* Register and login
* Create blog posts
* Upload images with blog posts
* View blog posts
* Search blog posts
* Paginate blog posts
* Update their own posts
* Update post images
* Delete their own posts
* Add comments to posts
* View comments
* Like and unlike posts
* Receive email notifications for new comments and likes

The API also provides **Swagger documentation** for easy API testing.

---

## 🆕 Latest Features Added

The following features were added as part of the latest enhancement:

### 1. Image Upload

Users can upload an image while creating or updating a post.

Uploaded images are stored in:

```text
media/posts/
```

The database stores the image path instead of storing the actual image binary data.

Example:

```text
/media/posts/6d33702627e6455aabb19bfffe5731df_images.jpg
```

The image can be accessed through:

```text
http://127.0.0.1:8000/media/posts/6d33702627e6455aabb19bfffe5731df_images.jpg
```

### 2. Pagination

The posts API supports pagination using:

```text
page
limit
```

Example:

```http
GET /posts/?page=1&limit=10
```

Response includes:

* Current page
* Records per page
* Total number of matching posts
* Total number of pages
* Posts for the current page

### 3. Search

Posts can be searched using a keyword.

Search is performed against:

* Post title
* Post content

Example:

```http
GET /posts/?search=fastapi
```

### 4. Search + Pagination

Search and pagination can be used together.

Example:

```http
GET /posts/?page=1&limit=10&search=fastapi
```

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
* UploadFile
* StaticFiles

---

# 📁 Project Structure

```text
Blog_Management_API/

│
├── .env
├── .gitignore
├── blog.db
├── requirements.txt
├── README.md
│
├── media/
│   └── posts/
│       └── uploaded images
│
├── Screenshots/
│
└── app/
    │
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
        ├── post.py
        ├── comment.py
        └── like.py
```

---

# 🗄️ Database

The project uses **SQLite** with **SQLAlchemy ORM**.

Database file:

```text
blog.db
```

## Database Tables

The following tables are used:

1. `users`
2. `posts`
3. `comments`
4. `likes`

---

## Users Table

Stores registered users.

```text
id
username
email
password
```

Passwords are stored in **hashed form**, not as plain text.

---

## Posts Table

Stores blog posts.

```text
id
title
content
image
author_id
created_at
```

### Image Column

The `image` column stores the path of the uploaded image.

Example:

```text
/media/posts/unique_filename.jpg
```

The actual image is stored inside:

```text
media/posts/
```

---

## Comments Table

Stores comments made on blog posts.

```text
id
post_id
user_id
text
created_at
```

---

## Likes Table

Stores likes given to posts.

```text
id
post_id
user_id
```

A user can like a particular post only once.

---

# 🔐 Authentication

The API uses **JWT (JSON Web Token)** authentication.

---

## Register

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

---

## Login

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

The token is used to access protected APIs.

---

# 📝 Post APIs

## Create Post

```http
POST /posts/
```

Authentication required.

The create-post API uses:

```text
multipart/form-data
```

because it supports both text fields and an image file.

### Form Fields

```text
title
content
image
```

Example:

```text
title: My First Blog
content: This is my first blog post using FastAPI.
image: images.jpg
```

The image field is optional.

---

## Image Upload Flow

```text
User selects image
        ↓
UploadFile receives image
        ↓
Image is saved to media/posts/
        ↓
Unique filename is generated
        ↓
Image path is stored in database
        ↓
API returns image path
        ↓
StaticFiles serves the image
```

Example database value:

```text
/media/posts/6d33702627e6455aabb19bfffe5731df_images.jpg
```

Example browser URL:

```text
http://127.0.0.1:8000/media/posts/6d33702627e6455aabb19bfffe5731df_images.jpg
```

---

# 📄 View All Posts

```http
GET /posts/
```

This endpoint is publicly accessible.

By default:

```text
page = 1
limit = 10
```

Example:

```http
GET /posts/?page=1&limit=10
```

Example response:

```json
{
  "page": 1,
  "limit": 10,
  "total_count": 3,
  "total_pages": 1,
  "posts": [
    {
      "id": 1,
      "title": "My First Blog Post",
      "content": "This is my first blog post created using FastAPI and SQLite.",
      "author_id": 1,
      "image": null,
      "created_at": "2026-09-10T17:18:31.546105"
    }
  ]
}
```

---

# 🔎 Search Posts

Posts can be searched using the `search` query parameter.

Search checks both:

```text
Post title
Post content
```

Example:

```http
GET /posts/?search=thor
```

For example, searching:

```text
thor
```

can find a post with:

```text
Title: Thor
```

or content containing:

```text
Thor
```

The search is case-insensitive.

---

# 📑 Pagination

Pagination prevents the API from returning a large number of posts at once.

The API supports:

```text
page
limit
```

Example:

```http
GET /posts/?page=1&limit=10
```

For page 2:

```http
GET /posts/?page=2&limit=10
```

For page 3:

```http
GET /posts/?page=3&limit=10
```

### Pagination Formula

The API calculates the number of records to skip using:

```python
skip = (page - 1) * limit
```

Example:

```text
Page 1 → skip 0
Page 2 → skip 10
Page 3 → skip 20
```

The API also returns:

```text
total_count
total_pages
```

---

# 🔎📑 Search + Pagination

Search and pagination can be used together.

Example:

```http
GET /posts/?page=1&limit=10&search=thor
```

Example response:

```json
{
  "page": 1,
  "limit": 10,
  "total_count": 1,
  "total_pages": 1,
  "posts": [
    {
      "id": 3,
      "title": "Thor",
      "content": "Thunder Strom",
      "author_id": 3,
      "image": "/media/posts/5d49371ae12244758dc02e8e238a08db_images.jpg",
      "created_at": "2026-09-16T08:05:26.548122"
    }
  ]
}
```

---

# 📌 Post API Query Parameters

The `/posts/` endpoint supports:

| Parameter | Type    | Default | Description              |
| --------- | ------- | ------: | ------------------------ |
| `page`    | integer |       1 | Page number              |
| `limit`   | integer |      10 | Number of posts per page |
| `search`  | string  |    None | Search title/content     |

Examples:

```http
GET /posts/
```

```http
GET /posts/?page=2
```

```http
GET /posts/?limit=5
```

```http
GET /posts/?search=fastapi
```

```http
GET /posts/?page=2&limit=5&search=fastapi
```

---

# 👤 View My Posts

```http
GET /posts/mine
```

Authentication required.

This endpoint returns posts created by the currently authenticated user.

---

# 🔍 View One Post

```http
GET /posts/{post_id}
```

Example:

```http
GET /posts/1
```

---

# ✏️ Update Post

```http
PUT /posts/{post_id}
```

Authentication required.

Only the post owner can update the post.

The update API supports:

```text
title
content
image
```

The request uses:

```text
multipart/form-data
```

Example:

```text
title: Updated Blog Title
content: Updated blog content.
image: new_image.jpg
```

The image is optional.

If a new image is uploaded, a new unique filename is generated and the post's image path is updated.

---

# 🗑️ Delete Post

```http
DELETE /posts/{post_id}
```

Authentication required.

Only the post owner can delete the post.

---

# 💬 Comment APIs

## Add Comment

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

---

## View Comments

```http
GET /comments/posts/{post_id}
```

Comments can be viewed publicly.

---

# ❤️ Like APIs

## Like Post

```http
POST /likes/posts/{post_id}
```

Authentication required.

---

## Unlike Post

```http
DELETE /likes/posts/{post_id}
```

Authentication required.

---

## Get Like Count

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

# 📧 Email Notifications

The application sends email notifications when:

## New Comment

When another user comments on a post, the post owner receives an email notification.

## New Like

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

# ✅ Validation

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

# 🔒 Ownership Protection

Users can update or delete **only their own posts**.

Example:

```text
User 1 → Post 1
User 2 → Post 2
```

User 1 can:

```text
Update Post 1
Delete Post 1
```

User 1 cannot:

```text
Update Post 2
Delete Post 2
```

The API returns:

```text
403 Forbidden
```

when a user attempts to modify another user's post.

---

# 🖼️ Image Storage

Uploaded images are stored in:

```text
media/posts/
```

Example:

```text
media/
└── posts/
    ├── 6d33702627e6455aabb19bfffe5731df_images.jpg
    ├── 5d49371ae12244758dc02e8e238a08db_images.jpg
    └── another_image.jpg
```

A unique UUID is added to the filename to prevent filename conflicts.

Example:

```python
filename = f"{uuid4().hex}_{image.filename}"
```

The database stores only the URL/path:

```text
/media/posts/unique_filename.jpg
```

---

# ▶️ Installation

## 1. Clone or Download the Project

Open the project folder in VS Code.

---

## 2. Create Virtual Environment

Open PowerShell in the project folder:

```powershell
python -m venv venv
```

---

## 3. Activate Virtual Environment

```powershell
.\venv\Scripts\Activate.ps1
```

---

## 4. Install Dependencies

```powershell
pip install -r requirements.txt
```

---

## 5. Configure Environment Variables

Create a `.env` file in the project root.

Example:

```env
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

Do not upload real credentials to GitHub.

---

## 6. Run the FastAPI Server

```powershell
uvicorn app.main:app --reload
```

The application will run at:

```text
http://127.0.0.1:8000
```

---

# 📚 Swagger Documentation

FastAPI automatically provides interactive API documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

Swagger can be used to test:

* Authentication
* Posts
* Image upload
* Image update
* Pagination
* Search
* Search + pagination
* Comments
* Likes
* Validation
* Authorization

---

# 🧪 API Testing Flow

Recommended testing order:

## Step 1 — Register

```http
POST /auth/register
```

Create a user account.

---

## Step 2 — Login

```http
POST /auth/login
```

Copy the returned access token.

---

## Step 3 — Authorize Swagger

Click **Authorize** in Swagger.

Enter:

```text
Bearer YOUR_ACCESS_TOKEN
```

---

## Step 4 — Create Post

```http
POST /posts/
```

Use:

```text
title
content
image
```

Upload an image using the `image` field.

---

## Step 5 — View Posts

```http
GET /posts/
```

Verify:

```text
page
limit
total_count
total_pages
posts
```

---

## Step 6 — Test Pagination

Example:

```http
GET /posts/?page=1&limit=2
```

Then:

```http
GET /posts/?page=2&limit=2
```

Verify that different pages return different records when enough posts exist.

---

## Step 7 — Test Search

Example:

```http
GET /posts/?search=thor
```

Verify that matching title/content is returned.

---

## Step 8 — Test Search + Pagination

Example:

```http
GET /posts/?page=1&limit=10&search=thor
```

Verify:

```text
page
limit
total_count
total_pages
posts
```

---

## Step 9 — Test Image URL

Copy the returned image path.

Example:

```text
/media/posts/unique_image.jpg
```

Open:

```text
http://127.0.0.1:8000/media/posts/unique_image.jpg
```

The uploaded image should be displayed.

---

## Step 10 — Add Comment

```http
POST /comments/posts/{post_id}
```

---

## Step 11 — Like Post

```http
POST /likes/posts/{post_id}
```

---

## Step 12 — Check Like Count

```http
GET /likes/posts/{post_id}/count
```

---

## Step 13 — Unlike Post

```http
DELETE /likes/posts/{post_id}
```

---

## Step 14 — Update Post

```http
PUT /posts/{post_id}
```

Test:

* title update
* content update
* image update

---

## Step 15 — Delete Post

```http
DELETE /posts/{post_id}
```

---

# 🗃️ SQLite Verification

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

---

## Verify Users

```sql
SELECT * FROM users;
```

---

## Verify Posts

```sql
SELECT * FROM posts;
```

The posts table should now contain:

```text
id
title
content
image
author_id
created_at
```

---

## Verify Comments

```sql
SELECT * FROM comments;
```

---

## Verify Likes

```sql
SELECT * FROM likes;
```

---

# 📸 Project Deliverables

The following screenshots can be included for submission:

### Swagger

* Swagger `/docs`
* Register
* Login
* Authorize
* Create Post with Image Upload
* View Posts
* Pagination
* Search
* Search + Pagination
* Update Post with Image
* Delete Post
* Add Comment
* Like Post
* Unlike Post
* Like Count

### Database

* SQLite `users` table
* SQLite `posts` table
* SQLite `comments` table
* SQLite `likes` table

### Image Upload

* Uploaded image inside `media/posts/`
* Browser displaying the image URL

### Email

* Email notification for a new comment
* Email notification for a new like

---

# 🎯 Features Completed

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
* [x] Post image upload
* [x] Post image update
* [x] Image URL/path in API response
* [x] Static image serving
* [x] Posts pagination
* [x] Total post count
* [x] Total page calculation
* [x] Post search
* [x] Search by title
* [x] Search by content
* [x] Search with pagination

---

# 📋 New Assignment Requirements

## Image Upload

* [x] Upload image when creating a post
* [x] Upload image when editing a post
* [x] Add image field to Post model
* [x] Store uploaded images in `media/posts/`
* [x] Use FastAPI `UploadFile`
* [x] Return image path in API response

## Pagination & Search

* [x] `GET /posts/?page=1&limit=10`
* [x] Search using `search` query parameter
* [x] Combine search and pagination
* [x] Return total count
* [x] Return total pages

---

# 👨‍💻 Author

**Ramkumar S**

B.Tech Computer Science and Engineering

---

# 📌 Conclusion

The Blog Management API provides a complete backend blogging system using FastAPI.

It includes:

* Secure authentication
* JWT authorization
* SQLite database management
* SQLAlchemy ORM
* Post CRUD operations
* Image upload and image serving
* Pagination
* Search
* Comments
* Likes
* Ownership authorization
* Pydantic validation
* Email notifications
* Swagger API documentation

The project demonstrates the implementation of a practical REST API with authentication, database operations, file handling, searching, and pagination.
