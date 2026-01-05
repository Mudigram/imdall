from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.website import WebsiteCreate, WebsiteResponse
from app.models.website import Website
from app.db.deps import get_db


router = APIRouter(prefix="/websites", tags=["Websites"])

@router.post("/", response_model=WebsiteResponse)
def create_website(payload: WebsiteCreate, db: Session = Depends(get_db)):
    website = Website(
        url=str(payload.url),
        check_interval=payload.check_interval
    )
    db.add(website)
    db.commit()
    db.refresh(website)
    return website

@router.get("/", response_model=List[WebsiteResponse])
def list_websites(
    active: bool | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(Website)
    if active is not None:
        query = query.filter(Website.is_active == active)
    return query.all()


@router.patch("/{website_id}", response_model=WebsiteResponse)
def toggle_website(
    website_id: int,
    check_interval: int,
    is_active: bool,
    db: Session = Depends(get_db)
):
    website = db.query(Website).filter(Website.id == website_id).first()

    if not website:
        raise HTTPException(status_code=404, detail="Website not found")

    website.is_active = is_active
    website.check_interval = check_interval
    db.commit()
    db.refresh(website)
    return website