import logging
from fastapi import APIRouter, Depends, HTTPException
from app.models import UserModel, FollowModel, RecommendationModel
from sqlalchemy.orm import Session
from app import crud, schemas, database
from app.services import llm_service
from typing import List

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.get("/all-users", response_model=List[schemas.UserWithRecommendations])
def get_all_users(db: Session = Depends(database.get_db)):
    users = crud.get_all_users(db)

    for user in users:
        # Populate the user's recommendations
        user_recommendations = (
            db.query(RecommendationModel)
            .filter(RecommendationModel.user_id == user.id)
            .all()
        )

        # Populate the users they are following
        followed_users = (
            db.query(UserModel)
            .join(FollowModel, FollowModel.to_user_id == UserModel.id)
            .filter(FollowModel.from_user_id == user.id)
            .all()
        )

        # Set follows to an empty list if there are no followed users
        user.follows = (
            [followed_user.name for followed_user in followed_users]
            if followed_users
            else []
        )
        user.recommendations = user_recommendations

    return users


@router.post("/generate-email/{user_id}", response_model=schemas.EmailContent)
def generate_email(
    user_id: int,
    email_type_request: schemas.EmailTypeRequest,
    db: Session = Depends(database.get_db),
):
    try:
        user_with_recommendations = crud.get_user_with_recommendations(db, user_id)
        if user_with_recommendations is None:
            raise HTTPException(status_code=404, detail="User not found")

        email_content = llm_service.generate_email_content(
            user_with_recommendations, email_type_request.type
        )
        logger.info(
            f"Generated {email_type_request.type} email for user {user_id}: {email_content}"
        )
        return email_content
    except Exception as e:
        logger.error(
            f"Error generating {email_type_request.type} email for user {user_id}: {str(e)}"
        )
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
