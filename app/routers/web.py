from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.database import get_db
from typing import List, Optional
from app.services.roles_service import AuthService
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import Role, Permission, User
from app.models.product import Product
from sqlalchemy import select
from fastapi.responses import RedirectResponse
from app.schemas import PurchaseOrderCreate
from app.models.order import PurchaseOrder
import os

router = APIRouter()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        "welcome.html",
        {"request": request, "status": "healthy", "version": "1.0.0"}
    )

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    print(templates)
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@router.get("/products", response_class=HTMLResponse)
async def list_products(request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product))
    products = result.scalars().all()
    return templates.TemplateResponse("products/list.html", {"request": request, "products": products})

@router.get("/products/create", response_class=HTMLResponse)
async def create_product_page(request: Request):
    return templates.TemplateResponse("products/create.html", {"request": request})

@router.post("/products/create")
async def create_product(
    name: str = Form(...),
    description: str = Form(""),
    price: float = Form(...),
    image_url: str = Form(None),
    db: AsyncSession = Depends(get_db)
):
    product = Product(name=name, description=description, price=price, image_url=image_url)
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return RedirectResponse("/products", status_code=303)

@router.get("/products/edit/{product_id}", response_class=HTMLResponse)
async def edit_product_page(product_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return templates.TemplateResponse("products/edit.html", {"request": request, "product": product})

@router.post("/products/edit/{product_id}")
async def edit_product(
    product_id: int,
    name: str = Form(...),
    description: str = Form(""),
    price: float = Form(...),
    image_url: str = Form(None),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product.name = name
    product.description = description
    product.price = price
    product.image_url = image_url
    
    db.add(product)
    await db.commit()
    await db.refresh(product)
    
    return RedirectResponse("/products", status_code=303)

@router.post("/products/delete/{product_id}")
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    await db.delete(product)
    await db.commit()
    return RedirectResponse("/products", status_code=303)

@router.get("/users", response_class=HTMLResponse)
async def users_page(request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return templates.TemplateResponse("users/users.html", {"request": request, "users": users})

@router.get("/users/create", response_class=HTMLResponse)
async def create_user_page(request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Role))
    roles = result.scalars().all()
    return templates.TemplateResponse("users/create_user.html", {"request": request, "roles": roles})


@router.get("/users/edit/{user_id}", response_class=HTMLResponse)
async def edit_user_page(user_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        return RedirectResponse("/users", status_code=303)

    result = await db.execute(select(Role))
    roles = result.scalars().all()

    return templates.TemplateResponse("users/edit_user.html", {"request": request, "user": user, "roles": roles})

@router.post("/users/edit/{user_id}")
async def edit_user(
    user_id: int,
    username: str = Form(...),
    password: str = Form(""),
    roles: list[int] = Form([]),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        return RedirectResponse("/users", status_code=303)
    
    user.username = username
    if password:
        user.password = password

    result = await db.execute(select(Role).where(Role.id.in_(roles)))
    selected_roles = result.scalars().all()
    user.roles = selected_roles

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return RedirectResponse("/users", status_code=303)

@router.post("/users/create")
async def create_user(
    username: str = Form(...),
    password: str = Form(...),
    roles: list[int] = Form([]),
    email: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Role).where(Role.id.in_(roles)))
    selected_roles = result.scalars().all()

    new_user = User(
        username=username,
        email=email,
        password=password,
        roles=selected_roles
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return RedirectResponse("/users", status_code=303)

@router.get("/roles", response_class=HTMLResponse)
async def roles_page(request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Role))
    roles = result.scalars().all()
    return templates.TemplateResponse("roles/roles.html", {"request": request, "roles": roles})

@router.get("/roles/edit/{role_id}", response_class=HTMLResponse)
async def edit_role_page(role_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Role).where(Role.id == role_id))
    role = result.scalar_one_or_none()
    if not role:
        return RedirectResponse("/roles", status_code=303)

    result = await db.execute(select(Permission))
    all_permissions = result.scalars().all()

    role_permissions = {p.id for p in role.permissions}

    return templates.TemplateResponse(
        "roles/edit_role.html",
        {
            "request": request,
            "role": role,
            "all_permissions": all_permissions,
            "role_permissions": role_permissions,
        },
    )

@router.post("/roles/create")
async def create_role(request: Request, name: str = Form(...), description: str = Form(""), db: Session = Depends(get_db)):
    return await AuthService.create_role(name, description, db)

@router.post("/roles/edit/{role_id}")
async def edit_role(
    role_id: int,
    name: str = Form(...),
    description: str = Form(""),
    permissions: Optional[List[int]] = Form(None),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Role).where(Role.id == role_id))
    role = result.scalar_one_or_none()

    if not role:
        return RedirectResponse("/roles", status_code=303)

    role.name = name
    role.description = description
    if permissions is not None:
        result = await db.execute(select(Permission).where(Permission.id.in_(permissions)))
        selected_permissions = result.scalars().all()
        role.permissions = selected_permissions

    db.add(role)
    await db.commit()
    await db.refresh(role)

    return RedirectResponse("/roles", status_code=303)

@router.get("/orders", response_class=HTMLResponse)
async def list_orders_page(request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PurchaseOrder))
    orders = result.scalars().all()
    return templates.TemplateResponse("orders/list.html", {
        "request": request,
        "orders": orders
    })

@router.get("/orders/create", response_class=HTMLResponse)
async def create_order_page(request: Request):
    return templates.TemplateResponse("orders/create.html", {"request": request})

@router.post("/orders/create")
async def create_order(
    request: Request,
    user_id: int = Form(...),
    product_id: int = Form(...),
    quantity: int = Form(...),
    unit_price: float = Form(...),
    db: AsyncSession = Depends(get_db)
):
    order_data = PurchaseOrderCreate(
        user_id=user_id,
        details=[{
            "product_id": product_id,
            "quantity": quantity,
            "unit_price": unit_price
        }]
    )
    order = await create_order(db, order_data)

    return RedirectResponse(url="/orders", status_code=303)

@router.get("/orders/{order_id}/complete")
async def complete_order(order_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PurchaseOrder).where(PurchaseOrder.id == order_id))
    order = result.scalars().first()
    if order:
        order.status = "Completed"
        await db.commit()
    return RedirectResponse(url="/orders", status_code=303)

@router.get("/orders/{order_id}/delete")
async def delete_order(order_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PurchaseOrder).where(PurchaseOrder.id == order_id))
    order = result.scalars().first()
    if order:
        await db.delete(order)
        await db.commit()
    return RedirectResponse(url="/orders", status_code=303)

@router.get("/payments", response_class=HTMLResponse)
async def payments_page(request: Request):
    return templates.TemplateResponse("payments/payments.html", {"request": request})