from fastapi import (APIRouter,Depends, HTTPException, status,Form,File,UploadFile)
import os
import shutil #helps us copy/move the uploaded file to our storage folder
from uuid import uuid4  # gives each uploaded image a unique filename and prevents overwritingfrom sqlalchemy.orm import Session
from ..database import get_db
from ..models import Post , User
from ..utils.subscription import check_post_limit
from ..schemas import (  PostResponse)
from ..dependencies import get_current_user
from sqlalchemy import or_ #Search the keyword in title OR content.


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

UPLOAD_DIR = "media/posts" #where upload/save the image

os.makedirs(UPLOAD_DIR, exist_ok=True) # make file ist doent "If the folder already exists, that's okay Continue


# =========================================================
# CREATE POST
# =========================================================

@router.post(
    "/",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED
)
def create_post(

    title : str = Form(...),
    content : str = Form(...),  #form we are sending a file + text fields together become http request multipart/form-data  Multipart = request is divided into multiple parts.Form-data = those parts contain form values/data.
    image : UploadFile | None = File(None), 
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)

):
    # ===================================================== #
    #  SUBSCRIPTION PLAN LIMIT CHECK #
    #  =====================================================
    current_post_count = db.query(Post).filter( Post.author_id == current_user.id ).count() 
    check_post_limit( db=db, user=current_user, current_post_count=current_post_count )

    image_path = None

    if image:
        filename = f"{uuid4().hex}_{image.filename}"
        file_path = f"{UPLOAD_DIR}/{filename}"

        with open(file_path, "wb") as file:
             shutil.copyfileobj(image.file, file) # copy sourece to destination ,save permentle in new folder in media

        image_path = f"/media/posts/{filename}"
    new_post = Post(
        title=title,
        content=content,
        image=image_path,
        author_id=current_user.id
       
    )

    db.add(new_post)

    db.commit()

    db.refresh(new_post)

    return new_post


# =========================================================
# GET ALL POSTS
# PUBLIC &PAGINATION
# =========================================================
#query parameter is extra information sent in the URL after a ?
#Pagination means splitting a large amount of data into smaller pages instead of sending everything at once.without it get largr no of data in one page
@router.get(
    "/")
def get_posts(
    page: int = 1,
    limit :int = 10,
    search : str | None = None, #serach or This creates an optional query parameter.
    db: Session = Depends(get_db)
):
    skip = (page-1) * limit #first 10 rows 11-20

    query=db.query(Post) #can talk to SQLite.

    if search :
        search_pattern =f"%{search}%"
        query= query.filter(
            or_(
                Post.title.ilike(search_pattern),
                Post.content.ilike(search_pattern)
            )
        )

    posts = query.offset(skip).limit( # offset Ignore first 10 rows
        limit).all()# Take only limited records executes
    #.all() the query and returns all matching records as a Python list 
    
    total_count= query.count()
    total_pages = (total_count + limit -1) // limit #(25 + 10 -1)//10=  34//10=3.4 ==3 floor remove decimal give only whole no

    return {
        "page": page,
        "limit": limit,
        "total_count": total_count,
        "total_pages": total_pages,
        "posts": posts
    }


# =========================================================
# GET MY POSTS
# AUTHENTICATED
# =========================================================

@router.get(
    "/mine",
    response_model=list[PostResponse]
)
def get_my_posts(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    posts = db.query(Post).filter(
        Post.author_id == current_user.id
    ).order_by(
        Post.created_at.desc()
    ).all()

    return posts


# =========================================================
# GET SINGLE POST
# PUBLIC
# =========================================================

@router.get(
    "/{post_id}",
    response_model=PostResponse
)
def get_post(
    post_id: int,
    db: Session = Depends(get_db)
):

    post = db.query(Post).filter(
        Post.id == post_id
    ).first()

    if post is None:

        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

   
   # =====================================================
    # POST VIEW TRACKING
    # =====================================================

    # Someone opened this post.
    # So increase view count by 1.
    post.views += 1


    # Save updated views value into database.
    db.commit()


    # Refresh object with latest database value.
    db.refresh(post)


    return post


# =========================================================
# UPDATE POST
# OWNER ONLY
# =========================================================

@router.put(
    "/{post_id}",
    response_model=PostResponse
)
def update_post(
    post_id: int,
    title: str | None = Form(None),
    content: str | None = Form(None),
    image: UploadFile | None = File(None),                    # post_data: PostUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    post = db.query(Post).filter(
        Post.id == post_id
    ).first()

    if post is None:

        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    # Ownership check
    if post.author_id != current_user.id:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can update only your own posts"
        )

    if title is not None:

        post.title = title

    if content is not None:

        post.content = content
    if image:

        filename = f"{uuid4().hex}_{image.filename}"
        file_path = f"{UPLOAD_DIR}/{filename}"

        with open(file_path, "wb") as file:
            shutil.copyfileobj(image.file, file)
        post.image = f"/media/posts/{filename}"


    db.commit()

    db.refresh(post)

    return post


# =========================================================
# DELETE POST
# OWNER ONLY
# =========================================================

@router.delete(
    "/{post_id}"
)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    post = db.query(Post).filter(
        Post.id == post_id
    ).first()

    if post is None:

        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    # Ownership check
    if post.author_id != current_user.id:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can delete only your own posts"
        )

    db.delete(post)

    db.commit()

    return {
        "message": "Post deleted successfully"
    }