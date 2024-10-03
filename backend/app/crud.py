import logging
from sqlalchemy.orm import Session
from . import models, schemas

logger = logging.getLogger(__name__)


def get_all_users_with_recommendations(db: Session):
    return db.query(models.UserModel).all()


def get_user_with_recommendations(db: Session, user_id: int):
    try:
        user = db.query(models.UserModel).filter(models.UserModel.id == user_id).first()
        if user:
            user_with_recommendations = schemas.UserWithRecommendations(
                id=user.id,
                name=user.name,
                age=user.age,
                location=user.location,
                interests=user.interests,
                recommendations=[
                    schemas.Recommendation(
                        id=rec.id,
                        type=rec.type,
                        title=rec.title,
                        description=rec.description,
                        user_id=rec.user_id,
                    )
                    for rec in user.recommendations
                ],
            )
            logger.info(
                f"Retrieved user with recommendations: {user_with_recommendations}"
            )
            return user_with_recommendations
        logger.warning(f"User with id {user_id} not found")
        return None
    except Exception as e:
        logger.error(f"Error retrieving user with id {user_id}: {str(e)}")
        raise
