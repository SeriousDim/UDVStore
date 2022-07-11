from decimal import Decimal
from typing import Iterable, List, Optional

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import IntegrityError
from django.db.models import F, QuerySet
from django.db.transaction import atomic

from api.internal.models.product import Product
from api.internal.models.storage_cell import StorageCell
from api.internal.models.transaction import Transaction, TransactionTypes


def get_requests_from_users() -> QuerySet[Transaction]:
    return Transaction.objects.filter(type=TransactionTypes.REQUEST, response=None).order_by("created_at")


def try_accrue(transactions: List[Transaction]) -> bool:
    try:
        with atomic():
            for transaction in transactions:
                destination = transaction.destination
                destination.balance = F("balance") + transaction.accrual

                destination.save(update_fields=("balance",))
                transaction.save()

                destination.refresh_from_db(fields=("balance",))

        return True
    except IntegrityError:
        return False


def try_connect_transactions(old_transaction: Transaction, response: Transaction) -> bool:
    try:
        with atomic():
            old_transaction.response = response
            response.save()
            old_transaction.save()

        return True
    except IntegrityError:
        return False


def try_create_product(
    name: str, photo: InMemoryUploadedFile, description: str, price: Decimal, cells: List[dict]
) -> Optional[Product]:
    try:
        with atomic():
            product = Product.objects.create(name=name, photo=photo, description=description, price=price)

            StorageCell.objects.bulk_create(
                StorageCell(product=product, size=cell["size"], amount=cell["amount"]) for cell in cells
            )

            return product
    except IntegrityError:
        return None


def toggle_product_visible(product_id: int) -> bool:
    product = Product.objects.filter(id=product_id).first()
    if not product:
        raise ValueError(f"Unknown product {product_id}")

    product.is_visible = not product.is_visible
    product.save(update_fields=["is_visible"])

    return product.is_visible