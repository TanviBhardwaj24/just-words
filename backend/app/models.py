from sqlalchemy import Column, Integer, String, ForeignKey, ARRAY
from sqlalchemy.orm import relationship
from app.database import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    location = Column(String)
    interests = Column(ARRAY(String))
    facebook = Column(String)
    instagram = Column(String)
    linkedin = Column(String)
    github = Column(String)
    recommendations = relationship(
        "RecommendationModel", back_populates="user", cascade="all, delete-orphan"
    )
    description = Column(String)


class RecommendationModel(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    type = Column(String)
    title = Column(String)
    description = Column(String)
    user = relationship("UserModel", back_populates="recommendations")


class FollowModel(Base):
    __tablename__ = "follows"

    id = Column(Integer, primary_key=True, index=True)
    from_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    to_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    from_user = relationship(
        "UserModel", foreign_keys=[from_user_id], backref="following"
    )
    to_user = relationship("UserModel", foreign_keys=[to_user_id], backref="followers")
