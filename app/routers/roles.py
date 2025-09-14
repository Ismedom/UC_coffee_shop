from fastapi import Form, Request, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Role

@router.post("/roles/create")
async def create_role(request: Request, name: str = Form(...), description: str = Form(""), db: Session = Depends(get_db)):
    role_name = name.replace(" ", "")
    
    new_role = Role(name=role_name, description=description)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    
    return RedirectResponse(url="/roles", status_code=303)
