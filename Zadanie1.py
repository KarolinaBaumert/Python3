from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, create_engine, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import bcrypt
import jwt
from datetime import datetime, timedelta

app = FastAPI()

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    email = Column(String, unique=True)
    roles = Column(ARRAY(String))


class LoginSchema(BaseModel):
    username: str
    password: str


class UserCreateSchema(BaseModel):
    username: str
    password: str
    email: str = None
    roles: list = ["ROLE_USER"]


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token wygasł")
    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Błędny token")


def get_current_user(token: str = Depends(verify_token)) -> dict:
    return token


def has_role_admin(roles: list):
    if "ROLE_ADMIN" not in roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Brak uprawnień do wykonania tej akcji")


@app.post("/login", status_code=200)
def login(data: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nie znaleziono użytkownika o podanym loginie",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nieprawidłowe hasło",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username, "roles": user.roles})

    return {
        "message": "Zalogowano pomyślnie",
        "access_token": access_token,
        "token_type": "bearer",
        "user_email": user.email
    }


@app.post("/register", status_code=201)
def register(data: UserCreateSchema, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == data.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Użytkownik już istnieje")

    hashed_password = hash_password(data.password)

    new_user = User(username=data.username, password=hashed_password, email=data.email, roles=data.roles)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Użytkownik zarejestrowany pomyślnie",
        "username": new_user.username,
        "email": new_user.email,
        "roles": new_user.roles
    }


@app.post("/users", status_code=201)
def create_user(user_data: UserCreateSchema, db: Session = Depends(get_db),
                current_user: dict = Depends(get_current_user)):
    has_role_admin(current_user["roles"])

    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Użytkownik o tym username już istnieje")

    hashed_password = hash_password(user_data.password)

    new_user = User(username=user_data.username, password=hashed_password, email=user_data.email, roles=user_data.roles)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Użytkownik został dodany pomyślnie",
        "username": new_user.username,
        "email": new_user.email,
        "roles": new_user.roles
    }


@app.get("/users/me")
def read_users_me(current_user: dict = Depends(get_current_user)):
    return {"username": current_user["sub"], "roles": current_user["roles"]}


@app.get("/user_details")
def user_details(current_user: dict = Depends(get_current_user)):
    return {
        "username": current_user["sub"],
        "roles": current_user["roles"]
    }


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)

    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
