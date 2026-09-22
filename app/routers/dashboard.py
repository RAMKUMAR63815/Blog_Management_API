from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..database import get_db #Imports Dependency Injection SQL Functions
from ..dependencies import get_current_user
from ..models import Post, Comment, Like

router = APIRouter(
    prefix="/dashboard", #Swagger la separate Dashboard section varum.
    tags=["Dashboard"]
)

@router.get("/")
def get_dashboard(
    db: Session = Depends(get_db), # dependency injection
    current_user = Depends(get_current_user) #JWT Authentication irundhu current user find pannuvo
):
    total_posts = (
    db.query(Post)
    .filter(
        Post.author_id == current_user.id #Total Posts Count using aggregate function count(). filter()
    )
    .count()
)

    
    total_comments = (
    db.query(Comment)
    .filter(
        Comment.user_id == current_user.id #Total Comments Count
    )
    .count()
)

    
    total_likes_received = (
    db.query(Like)
    .join(
        Post,                         #Total Likes Received
        Like.post_id == Post.id
    )
    .filter(
        Post.author_id == current_user.id
    )
    .count()
)



    likes_per_post = (
    db.query(
        Post.title,
        func.count(Like.id).label("likes") #Likes Per Post Analytics
    )
    .outerjoin(
        Like,
        Like.post_id == Post.id
    )
    .filter(
        Post.author_id == current_user.id
    )
    .group_by(Post.id)
    .all()
)

    #Comments Per Post Analytics

    comments_per_post = (
    db.query(
        Post.title,
        func.count(Comment.id).label("comments")#COUNT(likes.id) AS likes
    )
    .outerjoin(
        Comment,
        Comment.post_id == Post.id
    )
    .filter(
        Post.author_id == current_user.id
    )
    .group_by(Post.id)
    .all()
)
    #total views
    total_views = (
    db.query(func.sum(Post.views))
    .filter(Post.author_id == current_user.id)
    .scalar()
    or 0
)
    #JSON Response Design @ API Development
    return {
    "total_posts": total_posts,
    "total_comments": total_comments, #How many comments did the current user WRITE?
    "total_likes_received": total_likes_received,
     "total_views": total_views,

    "likes_per_post": [#Database rows-ai frontend-friendly JSON format-ku convert panna list comprehension use panninen
        {
            "title": row.title, #List Comprehension & JSON Transformation
            "likes": row.likes
        }  
        for row in likes_per_post
    ],

    "comments_per_post": [
        {
            "title": row.title,
            "comments": row.comments
        }
        for row in comments_per_post
    ]
}
#outer : returns both matching and non-matching rows from two tables

#Analytics Query: Dashboard statistics generate panna aggregation-based analytics queries use panninen

#Likes/comments per post should be shown graphically.

#So first backend-la Chart.js-ku required data prepare pannuvom.

@router.get("/chart-data")
def get_chart_data(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    likes_per_post = (
        db.query(#seleet clasue
            Post.title,
            func.count(Like.id).label("likes")
        )
        .outerjoin( # return matching & unmatching records
            Like,
            Like.post_id == Post.id
        )
        .filter(
            Post.author_id == current_user.id #where clause
        )
        .group_by(Post.id)
        .all()
    )

    comments_per_post = (
        db.query(
            Post.title,
            func.count(Comment.id).label("comments")
        )
        .outerjoin(
            Comment,
            Comment.post_id == Post.id
        )
        .filter(
            Post.author_id == current_user.id
        )
        .group_by(Post.id)
        .all()
    )

    return {
        "likes": [
            {
                "title": row.title,
                "count": row.likes
            }
            for row in likes_per_post
        ],

        "comments": [
            {
                "title": row.title,
                "count": row.comments
            }
            for row in comments_per_post
        ]
    }