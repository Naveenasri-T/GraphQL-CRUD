import strawberry
from typing import List, Optional
from sqlalchemy.orm import Session
from .database import get_db, engine, SessionLocal
from .models import Base, User

Base.metadata.create_all(bind=engine)

@strawberry.type
class UserType:
    id: int
    name: str
    email: str
    age: Optional[int]
    country: Optional[str]
    city: Optional[str]
    phone: Optional[str]

def get_database_session() -> Session:
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

@strawberry.type
class Query:
    @strawberry.field
    def get_users(self) -> List[UserType]:
        db = SessionLocal()
        try:
            users = db.query(User).all()
            return [UserType(
                id=user.id,
                name=user.name,
                email=user.email,
                age=user.age,
                country=user.country,
                city=user.city,
                phone=user.phone
            ) for user in users]
        finally:
            db.close()
    
    @strawberry.field
    def get_user_by_id(self, id: int) -> Optional[UserType]:
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.id == id).first()
            if user:
                return UserType(
                    id=user.id,
                    name=user.name,
                    email=user.email,
                    age=user.age,
                    country=user.country,
                    city=user.city,
                    phone=user.phone
                )
            return None
        finally:
            db.close() 
    
# Mutation
@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_user(self, name: str, email: str, age: Optional[int] = None, country: Optional[str] = None, city: Optional[str] = None, phone: Optional[str] = None) -> UserType:
        db = SessionLocal()
        try:
            new_user = User(name=name, email=email, age=age, country=country, city=city, phone=phone)
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return UserType(
                id=new_user.id,
                name=new_user.name,
                email=new_user.email,
                age=new_user.age,
                country=new_user.country,
                city=new_user.city,
                phone=new_user.phone
            )
        finally:
            db.close()
    
    @strawberry.mutation
    def update_user(self, id: int, name: Optional[str] = None, email: Optional[str] = None, age: Optional[int] = None, country: Optional[str] = None, city: Optional[str] = None, phone: Optional[str] = None) -> Optional[UserType]:
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.id == id).first()
            if user:
                if name is not None:
                    user.name = name
                if email is not None:
                    user.email = email
                if age is not None:
                    user.age = age
                if country is not None:
                    user.country = country
                if city is not None:
                    user.city = city
                if phone is not None:
                    user.phone = phone
                db.commit()
                db.refresh(user)
                return UserType(
                    id=user.id,
                    name=user.name,
                    email=user.email,
                    age=user.age,
                    country=user.country,
                    city=user.city,
                    phone=user.phone
                )
            return None
        finally:
            db.close()
    
    @strawberry.mutation
    def delete_user(self, id: int) -> bool:
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.id == id).first()
            if user:
                db.delete(user)
                db.commit()
                return True
            return False
        finally:
            db.close()
    
schema = strawberry.Schema(query=Query, mutation=Mutation)
     