from pydantic import BaseModel, HttpUrl

class WebsiteCreate(BaseModel):
    url: HttpUrl
    check_interval: int = 60

class WebsiteResponse(BaseModel):
    id: int
    url: str
    check_interval: int
    is_active: bool

    class Config:
        from_attributes = True
