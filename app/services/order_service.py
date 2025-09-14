from sqlalchemy.orm import Session
from app.models import PurchaseOrder, PurchaseOrderDetail, User
from app.schemas import PurchaseOrderCreate, PurchaseOrderRead, PurchaseOrderDetailRead, CurrentUser
from app.helper.auth import get_current_user

class OrderService:

    @staticmethod
    async def create_order(db: Session, order_data: PurchaseOrderCreate, current_user: CurrentUser) -> PurchaseOrderRead:
        order = PurchaseOrder(user_id=current_user.user_id)
        db.add(order)
        db.flush()

        total = 0
        details_list = []

        for item in order_data.details:
            subtotal = item.quantity * item.unit_price
            detail = PurchaseOrderDetail(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=item.unit_price,
                subtotal=subtotal,
            )
            total += subtotal
            db.add(detail)
            details_list.append(detail)

        order.total_amount = total
        await db.commit()
        await db.refresh(order)
        for d in details_list:
            await db.refresh(d)

        return PurchaseOrderRead(
            id=order.id,
            user_id=order.user_id,
            total_amount=float(order.total_amount),
            created_at=order.created_at,
            details=[
                PurchaseOrderDetailRead(
                    id=d.id,
                    product_id=d.product_id,
                    quantity=d.quantity,
                    unit_price=d.unit_price,
                    subtotal=d.subtotal
                ) for d in details_list
            ]
        )

    @staticmethod
    def list_orders(db: Session):
        return db.query(PurchaseOrder).all()

    @staticmethod
    def get_order(db: Session, order_id: int):
        return db.query(PurchaseOrder).filter(PurchaseOrder.id == order_id).first()

    @staticmethod
    def delete_order(db: Session, order_id: int):
        order = db.query(PurchaseOrder).filter(PurchaseOrder.id == order_id).first()
        if order:
            db.delete(order)
            db.commit()
        return order
