# Blog Management API

A simple **Blog Management API** built using **FastAPI, SQLite, SQLAlchemy ORM, JWT Authentication, Image Uploads, Pagination, Search, Email Notifications, Subscription-Based Access Control, Billing, and Invoice Generation**.

---

# 🚀 Project Overview

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
* Subscribe to Basic, Premium, or Pro plans
* Access features according to their subscription limits
* Upgrade their subscription
* Generate subscription invoices
* View billing history

The API also provides **Swagger documentation** for easy API testing.

---

# 🆕 Latest Features Added

## 1. Image Upload

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

---

## 2. Pagination

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

---

## 3. Search

Posts can be searched using a keyword.

Search is performed against:

* Post title
* Post content

Example:

```http
GET /posts/?search=fastapi
```

The search is case-insensitive.

---

## 4. Search + Pagination

Search and pagination can be used together.

Example:

```http
GET /posts/?page=1&limit=10&search=fastapi
```

---

# 💳 5. Subscription-Based Access Control

The API provides three subscription plans:

* Basic
* Premium
* Pro

Each subscription plan has different limits for posts, comments, and likes.

## Subscription Plans

| Feature  | Basic | Premium |       Pro |
| -------- | ----: | ------: | --------: |
| Price    |    ₹0 |    ₹499 |      ₹999 |
| Posts    |     1 |       2 | Unlimited |
| Images   |     1 |       2 | Unlimited |
| Comments |    10 |      50 | Unlimited |
| Likes    |    10 |      50 | Unlimited |

`NULL` limits are used for the Pro plan to represent unlimited access.

---

## Subscription Flow

```text
User
  ↓
Select Subscription Plan
  ↓
Upgrade API
  ↓
Check selected plan
  ↓
Create transaction ID
  ↓
Generate invoice PDF
  ↓
Create billing history
  ↓
Update user's subscription plan
  ↓
Return subscription details
```

---

# 🔐 Subscription Access Control

The user's subscription plan controls access to certain actions.

## Post Limit

Before creating a post, the API checks the number of posts already created by the user.

Example:

```text
Basic Plan
Maximum posts = 1

Existing posts = 1
        ↓
Limit reached
        ↓
New post rejected
```

The API returns:

```text
403 Forbidden
```

with:

```text
You've reached your plan limit. Kindly upgrade your plan to continue.
```

---

## Comment Limit

Before creating a comment, the API counts the comments created by the current user.

Example:

```text
Basic Plan
Maximum comments = 10

Existing comments = 10
        ↓
Limit reached
        ↓
New comment rejected
```

Premium users can create up to 50 comments.

Pro users have unlimited comments.

---

## Like Limit

Before creating a new like, the API counts the likes created by the current user.

Example:

```text
Basic Plan
Maximum likes = 10

Existing likes = 10
        ↓
Limit reached
        ↓
New like rejected
```

Premium users can create up to 50 likes.

Pro users have unlimited likes.

---

## Duplicate Like Validation

The subscription limit and duplicate-like validation are separate checks.

A user cannot like the same post twice.

Example:

```text
User 1
   ↓
Likes Post 1
   ↓
Like created

User 1
   ↓
Likes Post 1 again
   ↓
Rejected
```

Response:

```text
You already liked this post
```

---

# 📋 Subscription APIs

## Get Subscription Plans

```http
GET /subscriptions/plans
```

Returns all active subscription plans.

Example:

```json
[
  {
    "id": 1,
    "name": "Basic",
    "price": 0,
    "max_posts": 1,
    "max_images": 1,
    "max_comments": 10,
    "max_likes": 10,
    "is_active": true
  },
  {
    "id": 2,
    "name": "Premium",
    "price": 499,
    "max_posts": 2,
    "max_images": 2,
    "max_comments": 50,
    "max_likes": 50,
    "is_active": true
  },
  {
    "id": 3,
    "name": "Pro",
    "price": 999,
    "max_posts": null,
    "max_images": null,
    "max_comments": null,
    "max_likes": null,
    "is_active": true
  }
]
```

---

## Upgrade Subscription

```http
POST /subscriptions/upgrade/{plan_id}
```

Authentication required.

Example:

```http
POST /subscriptions/upgrade/2
```

Here:

```text
2 = Premium plan
```

The API:

1. Finds the selected plan
2. Checks whether the plan is active
3. Prevents upgrading to the same plan
4. Creates subscription dates
5. Generates a fake transaction ID
6. Generates an invoice PDF
7. Creates a billing history record
8. Updates the user's subscription plan

Example response:

```json
{
  "message": "Successfully upgraded to Premium plan.",
  "plan": "Premium",
  "amount": 499,
  "transaction_id": "TXN_8A3D5F107E9B",
  "invoice": "/media/invoices/invoice_TXN_8A3D5F107E9B.pdf",
  "start_date": "2026-09-18T10:00:00",
  "end_date": "2026-10-18T10:00:00"
}
```

---

# 🧾 Invoice Generation

A fake subscription invoice is generated using **ReportLab**.

Invoice files are stored in:

```text
media/invoices/
```

Example:

```text
media/invoices/invoice_TXN_8A3D5F107E9B.pdf
```

The invoice contains:

* User ID
* Plan name
* Amount
* Transaction ID
* Start date
* End date

The database stores the invoice path.

---

# 💰 Billing History

Billing records are stored in the:

```text
billing_history
```

table.

The billing history contains:

```text
id
user_id
plan_id
amount
transaction_id
invoice_path
start_date
end_date
created_at
```

---

## Get Billing History

```http
GET /subscriptions/billing
```

Authentication required.

The endpoint returns billing records belonging to the currently authenticated user.

---

# 📊 Subscription Database Tables

The project uses the following tables:

1. `users`
2. `posts`
3. `comments`
4. `likes`
5. `subscription_plans`
6. `billing_history`

---

# 🗄️ Database

The project uses **SQLite** with **SQLAlchemy ORM**.

Database file:

```text
blog.db
```

---

## Users Table

Stores registered users.

```text
id
username
email
password
subscription_plan_id
```

Passwords are stored in **hashed form**, not as plain text.

`subscription_plan_id` connects the user with their current subscription plan.

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

## Subscription Plans Table

Stores subscription plan configuration.

```text
id
name
price
max_posts
max_images
max_comments
max_likes
is_active
```

---

## Billing History Table

Stores subscription billing information.

```text
id
user_id
plan_id
amount
transaction_id
invoice_path
start_date
end_date
created_at
```

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

The image field is optional.

Before creating the post, the API checks the user's subscription post limit.

---

# 🖼️ Image Upload Flow

```text
User selects image
        ↓
UploadFile receives image
        ↓
Unique filename is generated
        ↓
Image is saved to media/posts/
        ↓
Image path is stored in database
        ↓
API returns image path
        ↓
StaticFiles serves the image
```

Example:

```python
filename = f"{uuid4().hex}_{image.filename}"
```

The UUID helps prevent filename conflicts.

---

# 📄 View All Posts

```http
GET /posts/
```

This endpoint is publicly accessible.

Default values:

```text
page = 1
limit = 10
```

Example:

```http
GET /posts/?page=1&limit=10
```

---

# 🔎 Search Posts

Search using:

```text
search
```

Example:

```http
GET /posts/?search=thor
```

Search checks:

```text
Post title
Post content
```

The search is case-insensitive.

---

# 📑 Pagination

The API supports:

```text
page
limit
```

Example:

```http
GET /posts/?page=2&limit=10
```

Pagination uses:

```python
skip = (page - 1) * limit
```

Example:

```text
Page 1 → skip 0
Page 2 → skip 10
Page 3 → skip 20
```

The API returns:

```text
page
limit
total_count
total_pages
posts
```

---

# 🔎📑 Search + Pagination

Search and pagination can be combined.

Example:

```http
GET /posts/?page=1&limit=10&search=thor
```

---

# 👤 View My Posts

```http
GET /posts/mine
```

Authentication required.

Returns posts created by the currently authenticated user.

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

If a new image is uploaded, a unique filename is generated and the post's image path is updated.

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

Before creating the comment, the API checks the user's subscription comment limit.

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

The API checks:

1. Whether the post exists
2. Whether the user already liked the post
3. Whether the user's subscription like limit has been reached

---

## Unlike Post

```http
DELETE /likes/posts/{post_id}
```

Authentication required.

Unlike does not consume a new like limit.

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

---

# 🧾 Invoice Storage

Subscription invoices are stored in:

```text
media/invoices/
```

Example:

```text
media/
├── posts/
│   └── uploaded images
└── invoices/
    └── invoice_TXN_ABC123.pdf
```

---

# 🛠️ Technologies Used

* Python
* FastAPI
* SQLite
* SQLAlchemy ORM
* Pydantic
* JWT Authentication
* Passlib
* Bcrypt
* SMTP / Gmail
* Uvicorn
* Swagger UI
* UploadFile
* StaticFiles
* ReportLab
* Django Admin

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
├── seed_plans.py
├── assign_basic_plan.py
│
├── media/
│   ├── posts/
│   │   └── uploaded images
│   │
│   └── invoices/
│       └── generated invoices
│
├── Screenshots/
│
├── app/
│   │
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   ├── dependencies.py
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── email.py
│   │   └── subscription.py
│   │
│   └── routers/
│       ├── __init__.py
│       ├── auth.py
│       ├── post.py
│       ├── comment.py
│       ├── like.py
│       └── subscription.py
│
└── django_admin/
    │
    ├── manage.py
    │
    ├── django_admin/
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── urls.py
    │   ├── asgi.py
    │   └── wsgi.py
    │
    └── subscriptions/
        ├── __init__.py
        ├── admin.py
        ├── apps.py
        ├── models.py
        ├── migrations/
        ├── tests.py
        └── views.py
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

If ReportLab is not installed:

```powershell
pip install reportlab
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

# 🌱 Initialize Subscription Plans

Run:

```powershell
python seed_plans.py
```

This creates:

```text
Basic
Premium
Pro
```

Then assign the Basic plan to users who do not currently have a subscription:

```powershell
python assign_basic_plan.py
```

---

# ▶️ Run the FastAPI Server

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
* Comment subscription limits
* Likes
* Like limits
* Unlike
* Validation
* Authorization
* Subscription plans
* Subscription upgrade
* Billing history

---

# 🖥️ Django Admin

The project also contains a Django Admin interface for viewing subscription and billing information.

Run Django from the `django_admin` folder:

```powershell
cd django_admin
python manage.py runserver 8001
```

Open:

```text
http://127.0.0.1:8001/admin/
```

Django Admin provides:

* Subscription Plans
* Billing History
* Plan limit information
* Transaction IDs
* Invoice paths
* Subscription dates
* Billing records

Subscription plans are displayed horizontally:

```text
ID | Name | Price | Max Posts | Max Images | Max Comments | Max Likes | Is Active
```

Billing history is displayed horizontally:

```text
ID | User ID | Plan ID | Amount | Transaction ID | Invoice Path | Start Date | End Date | Created At
```

Subscription plans are ordered:

```text
1 → Basic
2 → Premium
3 → Pro
```

Billing history is ordered with the newest billing record first.

---

# 🧪 API Testing Flow

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

## Step 4 — Check Subscription Plans

```http
GET /subscriptions/plans
```

Verify:

```text
Basic
Premium
Pro
```

---

## Step 5 — Create Post

```http
POST /posts/
```

Use:

```text
title
content
image
```

Test the subscription post limit.

---

## Step 6 — Add Comments

```http
POST /comments/posts/{post_id}
```

Test the comment limit according to the user's plan.

---

## Step 7 — Like Post

```http
POST /likes/posts/{post_id}
```

Test:

* Normal like
* Duplicate like
* Subscription like limit

---

## Step 8 — Unlike Post

```http
DELETE /likes/posts/{post_id}
```

Verify that the like is removed.

---

## Step 9 — Upgrade Subscription

Example:

```http
POST /subscriptions/upgrade/2
```

This upgrades the user to Premium.

---

## Step 10 — Verify Billing

```http
GET /subscriptions/billing
```

Verify:

* Transaction ID
* Amount
* Plan ID
* Invoice path
* Start date
* End date

---

## Step 11 — Verify Invoice

Check:

```text
media/invoices/
```

The generated PDF should be present.

---

## Step 12 — Test Premium Limits

Verify that Premium allows:

```text
2 posts
50 comments
50 likes
```

---

## Step 13 — Test Pro

Upgrade to:

```http
POST /subscriptions/upgrade/3
```

Verify that Pro has unlimited:

```text
Posts
Comments
Likes
```

---

## Step 14 — Test Pagination

```http
GET /posts/?page=1&limit=2
```

Then:

```http
GET /posts/?page=2&limit=2
```

Verify that different pages return different records when enough posts exist.

---

## Step 15 — Test Search

```http
GET /posts/?search=thor
```

Verify that matching title/content is returned.

---

## Step 16 — Test Search + Pagination

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

## Step 17 — Test Image URL

Copy the returned image path:

```text
/media/posts/unique_image.jpg
```

Open:

```text
http://127.0.0.1:8000/media/posts/unique_image.jpg
```

The uploaded image should be displayed.

---

## Step 18 — Update Post

```http
PUT /posts/{post_id}
```

Test:

* Title update
* Content update
* Image update

---

## Step 19 — Delete Post

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
subscription_plans
billing_history
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

## Verify Subscription Plans

```sql
SELECT * FROM subscription_plans;
```

---

## Verify Billing History

```sql
SELECT * FROM billing_history;
```

---

# 📸 Project Deliverables

## Swagger

Screenshots can include:

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
* Comment Limit Validation
* Like Post
* Like Limit Validation
* Unlike Post
* Like Count
* Subscription Plans
* Upgrade Subscription
* Billing History

## Database

Screenshots can include:

* SQLite `users` table
* SQLite `posts` table
* SQLite `comments` table
* SQLite `likes` table
* SQLite `subscription_plans` table
* SQLite `billing_history` table

## Subscription

Screenshots can include:

* Basic plan
* Premium plan
* Pro plan
* Post limit validation
* Comment limit validation
* Like limit validation
* Successful upgrade
* Transaction ID
* Generated invoice

## Django Admin

Screenshots can include:

* Subscription Plans list
* Billing History list
* Plan limits
* Billing details
* Transaction ID
* Invoice path

## Image Upload

Screenshots can include:

* Uploaded image inside `media/posts/`
* Browser displaying the image URL

## Email

Screenshots can include:

* Email notification for a new comment
* Email notification for a new like

---

# 🎯 Features Completed

## Core API

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
* [x] Swagger API documentation

## Image Upload

* [x] Post image upload
* [x] Post image update
* [x] Image URL/path in API response
* [x] Static image serving
* [x] Unique image filenames

## Pagination & Search

* [x] Posts pagination
* [x] Total post count
* [x] Total page calculation
* [x] Post search
* [x] Search by title
* [x] Search by content
* [x] Search with pagination

## Subscription & Billing

* [x] Basic subscription plan
* [x] Premium subscription plan
* [x] Pro subscription plan
* [x] Subscription plan limits
* [x] Post subscription limit
* [x] Comment subscription limit
* [x] Like subscription limit
* [x] Image limit configuration
* [x] Unlimited Pro plan
* [x] Friendly subscription limit message
* [x] Subscription upgrade API
* [x] Plan selection using plan ID
* [x] 30-day subscription period
* [x] Fake transaction ID
* [x] Billing history
* [x] Invoice PDF generation
* [x] ReportLab invoice generation
* [x] Invoice path stored in database
* [x] Current-user billing history API

## Django Admin

* [x] Django Admin setup
* [x] Subscription Plans Admin
* [x] Billing History Admin
* [x] Horizontal plan columns
* [x] Horizontal billing columns
* [x] Plan ordering
* [x] Billing ordering
* [x] Transaction ID links

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
* Subscription-based access control
* Basic, Premium, and Pro plans
* Post, comment, and like limits
* Subscription upgrade functionality
* Billing history
* Fake invoice PDF generation
* Django Admin subscription management

The project demonstrates the implementation of a practical REST API with authentication, database operations, file handling, searching, pagination, subscription access control, billing, invoice generation, and administrative management.
