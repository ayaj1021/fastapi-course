from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import models, schema, utils
from sqlalchemy.orm import Session
from .. import database, schema, models, utils, oauth2


router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model= schema.Token)
async def login(
    #  user_credentials:schema.UserLogin, db: Session = Depends(database.get_db)
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):
    # user = (
    #     db.query(models.User)
    #     .filter(models.User.email == user_credentials.email)
    #     .first()
    # )

    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials"
        )

    if not utils.verifyPassword(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials"
        )

    # We can still add other things to this data dictionary maybe user role and sort
    access_token = oauth2.create_access_token(data={"user_id": str(user.id)})

    # create token
    # return token
    return {"access_token": access_token, "token_type": "Bearer"}
