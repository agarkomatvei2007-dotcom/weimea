"""
Auth Service - User Authentication and Authorization
Provides JWT-based authentication with email verification and OAuth support
"""
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime, timedelta
from typing import Optional
import sys
import os
import hashlib
import secrets
import jwt
import re

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from shared.database import get_db, Base, engine, SessionLocal

app = FastAPI(title="Authentication Service", version="1.0.0")

# JWT Configuration
JWT_SECRET = os.getenv("JWT_SECRET", "your-super-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24

security = HTTPBearer(auto_error=False)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# User Model
class User(Base):
    """User table"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    email_verified = Column(Boolean, default=False)
    verification_token = Column(String, nullable=True)
    verification_token_expires = Column(DateTime, nullable=True)
    reset_token = Column(String, nullable=True)
    reset_token_expires = Column(DateTime, nullable=True)
    oauth_provider = Column(String, nullable=True)  # google, github
    oauth_id = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    language = Column(String, default="en")  # en, ru, kk


# Create tables
Base.metadata.create_all(bind=engine)


# Helper functions
def hash_password(password: str) -> str:
    """Hash password with salt"""
    salt = os.getenv("PASSWORD_SALT", "default-salt")
    return hashlib.sha256(f"{password}{salt}".encode()).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    return hash_password(password) == hashed


def create_jwt_token(user_id: int, email: str) -> str:
    """Create JWT access token"""
    payload = {
        "user_id": user_id,
        "email": email,
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_jwt_token(token: str) -> Optional[dict]:
    """Decode and validate JWT token"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def generate_verification_token() -> str:
    """Generate random verification token"""
    return secrets.token_urlsafe(32)


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password: str) -> tuple[bool, str]:
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit"
    return True, "Password is valid"


# Dependency for protected routes
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """Get current user from JWT token"""
    if not credentials:
        return None

    payload = decode_jwt_token(credentials.credentials)
    if not payload:
        return None

    user = db.query(User).filter(User.id == payload.get("user_id")).first()
    return user


async def require_auth(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Require authentication - raises exception if not authenticated"""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )

    payload = decode_jwt_token(credentials.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    user = db.query(User).filter(User.id == payload.get("user_id")).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled"
        )

    return user


# API Endpoints
@app.get("/")
async def root():
    return {
        "service": "Authentication Service",
        "status": "operational",
        "version": "1.0.0"
    }


@app.post("/register")
async def register(
    email: str,
    password: str,
    full_name: str,
    language: str = "en",
    db: Session = Depends(get_db)
):
    """Register a new user"""
    # Validate email
    if not validate_email(email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )

    # Validate password
    is_valid, message = validate_password(password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )

    # Check if user exists
    existing_user = db.query(User).filter(User.email == email.lower()).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create verification token
    verification_token = generate_verification_token()
    verification_expires = datetime.utcnow() + timedelta(hours=24)

    # Create user
    user = User(
        email=email.lower(),
        password_hash=hash_password(password),
        full_name=full_name,
        verification_token=verification_token,
        verification_token_expires=verification_expires,
        language=language
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    # Create JWT token
    token = create_jwt_token(user.id, user.email)

    return {
        "message": "Registration successful. Please verify your email.",
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "email_verified": user.email_verified,
            "language": user.language
        },
        "token": token,
        "verification_token": verification_token  # In production, send via email
    }


@app.post("/login")
async def login(
    email: str,
    password: str,
    db: Session = Depends(get_db)
):
    """Login with email and password"""
    # Find user
    user = db.query(User).filter(User.email == email.lower()).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Verify password
    if not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Check if active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled"
        )

    # Create JWT token
    token = create_jwt_token(user.id, user.email)

    return {
        "message": "Login successful",
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "email_verified": user.email_verified,
            "language": user.language
        },
        "token": token
    }


@app.post("/oauth/google")
async def google_oauth(
    google_id: str,
    email: str,
    full_name: str,
    db: Session = Depends(get_db)
):
    """Login/Register with Google OAuth"""
    # Check if user exists with this Google ID
    user = db.query(User).filter(User.oauth_id == google_id, User.oauth_provider == "google").first()

    if not user:
        # Check if email exists
        user = db.query(User).filter(User.email == email.lower()).first()

        if user:
            # Link Google to existing account
            user.oauth_provider = "google"
            user.oauth_id = google_id
            user.email_verified = True
        else:
            # Create new user
            user = User(
                email=email.lower(),
                password_hash=hash_password(secrets.token_urlsafe(32)),
                full_name=full_name,
                oauth_provider="google",
                oauth_id=google_id,
                email_verified=True
            )
            db.add(user)

        db.commit()
        db.refresh(user)

    token = create_jwt_token(user.id, user.email)

    return {
        "message": "Google authentication successful",
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "email_verified": user.email_verified,
            "language": user.language
        },
        "token": token
    }


@app.post("/verify-email")
async def verify_email(
    token: str,
    db: Session = Depends(get_db)
):
    """Verify email with token"""
    user = db.query(User).filter(User.verification_token == token).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification token"
        )

    if user.verification_token_expires < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verification token expired"
        )

    user.email_verified = True
    user.verification_token = None
    user.verification_token_expires = None

    db.commit()

    return {"message": "Email verified successfully"}


@app.post("/resend-verification")
async def resend_verification(
    email: str,
    db: Session = Depends(get_db)
):
    """Resend verification email"""
    user = db.query(User).filter(User.email == email.lower()).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if user.email_verified:
        return {"message": "Email already verified"}

    # Generate new token
    verification_token = generate_verification_token()
    user.verification_token = verification_token
    user.verification_token_expires = datetime.utcnow() + timedelta(hours=24)

    db.commit()

    return {
        "message": "Verification email sent",
        "verification_token": verification_token  # In production, send via email
    }


@app.post("/forgot-password")
async def forgot_password(
    email: str,
    db: Session = Depends(get_db)
):
    """Request password reset"""
    user = db.query(User).filter(User.email == email.lower()).first()

    if not user:
        # Don't reveal if user exists
        return {"message": "If the email exists, a reset link has been sent"}

    # Generate reset token
    reset_token = generate_verification_token()
    user.reset_token = reset_token
    user.reset_token_expires = datetime.utcnow() + timedelta(hours=1)

    db.commit()

    return {
        "message": "If the email exists, a reset link has been sent",
        "reset_token": reset_token  # In production, send via email
    }


@app.post("/reset-password")
async def reset_password(
    token: str,
    new_password: str,
    db: Session = Depends(get_db)
):
    """Reset password with token"""
    user = db.query(User).filter(User.reset_token == token).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid reset token"
        )

    if user.reset_token_expires < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reset token expired"
        )

    # Validate new password
    is_valid, message = validate_password(new_password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )

    user.password_hash = hash_password(new_password)
    user.reset_token = None
    user.reset_token_expires = None

    db.commit()

    return {"message": "Password reset successful"}


@app.get("/me")
async def get_me(user: User = Depends(require_auth)):
    """Get current user profile"""
    return {
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "email_verified": user.email_verified,
            "language": user.language,
            "created_at": user.created_at
        }
    }


@app.put("/me")
async def update_me(
    full_name: Optional[str] = None,
    language: Optional[str] = None,
    user: User = Depends(require_auth),
    db: Session = Depends(get_db)
):
    """Update current user profile"""
    if full_name:
        user.full_name = full_name
    if language and language in ["en", "ru", "kk"]:
        user.language = language

    db.commit()
    db.refresh(user)

    return {
        "message": "Profile updated",
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "language": user.language
        }
    }


@app.put("/me/password")
async def change_password(
    current_password: str,
    new_password: str,
    user: User = Depends(require_auth),
    db: Session = Depends(get_db)
):
    """Change password"""
    # Verify current password
    if not verify_password(current_password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )

    # Validate new password
    is_valid, message = validate_password(new_password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )

    user.password_hash = hash_password(new_password)
    db.commit()

    return {"message": "Password changed successfully"}


@app.post("/validate-token")
async def validate_token(
    token: str
):
    """Validate JWT token"""
    payload = decode_jwt_token(token)

    if not payload:
        return {"valid": False}

    return {
        "valid": True,
        "user_id": payload.get("user_id"),
        "email": payload.get("email"),
        "expires": datetime.fromtimestamp(payload.get("exp"))
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
