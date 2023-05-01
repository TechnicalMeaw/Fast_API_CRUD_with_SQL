from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils, oauth2
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix= "/vote",
    tags=["Vote"]
)

@router.post("/", status_code= status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    product = db.query(models.Product).filter(models.Product.id == vote.product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id: {vote.product_id} does not exist")

    vote_query = db.query(models.Vote).filter(models.Vote.product_id == vote.product_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first() 
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on product {vote.product_id}")
        new_vote = models.Vote(product_id = vote.product_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"messege": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"messege": "successfully deleted vote"}