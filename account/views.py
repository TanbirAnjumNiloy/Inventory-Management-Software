from django.shortcuts import (
    render,
    redirect,
    HttpResponseRedirect,
    reverse,
    HttpResponse,
)
from django.db.models import Subquery, OuterRef
from django.utils import timezone
from django.db.models import Max
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.db.models import F
from django.contrib import messages
from django.shortcuts import render
from django.db.models import OuterRef, Subquery, Sum, Max
from .models import Supplier, Brand, Product, Doprice, Sellprice, Dsr, Sales
from django.urls import reverse
from django.shortcuts import get_object_or_404
from decimal import Decimal
from decimal import Decimal, InvalidOperation
from django.db import transaction
from .models import *
from setup.models import *
from .models import Bank, BankTransaction
from decimal import Decimal
from decimal import Decimal
from django.db.models import Q


# account  views Start.---------------------------------------------------------------------


@login_required
def account(request):
    return render(request, "account/account.html")


# lifting  views Start.---------------------------------------------------------------------


@login_required
def lifting(request):
    suppliers = Supplier.objects.all()
    brands = Brand.objects.all()
    products = Product.objects.all().order_by("name")

    latest_price_subquery = (
        Doprice.objects.filter(product_id=OuterRef("id"))
        .order_by("-added_on")
        .values("price")[:1]
    )
    products = products.annotate(current_price=Subquery(latest_price_subquery))

    if request.method == "POST":
        supplier_id = request.POST.get("supplier")
        brand_id = request.POST.get("brand")
        challan_number = request.POST.get("challan_number")

        if "save_price" in request.POST:
            selected_products = []
            date = request.POST.get("date")
            invoicing = request.POST.get("invoicing")

            for product in products:
                if str(product.id) in request.POST.getlist("product_ids[]"):
                    qty = request.POST.get(f"{product.id}_qty")
                    total = request.POST.get(f"{product.id}_total")
                    if qty and total:
                        selected_products.append(
                            {
                                "product_id": product.id,
                                "qty": qty,
                                "price": product.current_price,
                                "total": total,
                            }
                        )

            request.session["selected_products"] = selected_products
            request.session["lifting_date"] = date
            request.session["lifting_invoicing"] = invoicing

            return redirect("liftingcart")

        if challan_number:
            lifting_obj = get_object_or_404(Lifting, challan_number=challan_number)
            products = lifting_obj.products.all()

        elif supplier_id and brand_id:
            products = products.filter(supplier_id=supplier_id, brand_id=brand_id)

        if "save_price" in request.POST:
            name = request.POST.getlist("product_ids[]")
            qty_list = []
            total_list = []
            for product in products:
                qty = request.POST.get(f"{product.id}_qty")
                total = request.POST.get(f"{product.id}_total")
                if qty and total:
                    qty_list.append(qty)
                    total_list.append(total)
                    product.current_price = Decimal(
                        request.POST.get(f"{product.id}_price")
                    )
                    product.save()

                    existing_lifting = Lifting.objects.filter(
                        Q(product=product) & Q(date=request.POST.get("date"))
                    ).first()
                    if existing_lifting:
                        existing_qty = existing_lifting.quantity
                        existing_total = existing_lifting.total_amount
                        existing_lifting.quantity = existing_qty + int(qty)
                        existing_lifting.total_amount = existing_total + Decimal(total)
                        existing_lifting.save()

                        product.qty += int(qty)
                        product.save()
                    else:
                        lifting = Lifting.objects.create(
                            product=product,
                            quantity=qty,
                            Doprice=product.current_price,
                            total_amount=total,
                            invoicing=request.POST.get("invoicing"),
                            date=request.POST.get("date"),
                        )

                        product.qty += int(qty)
                        product.save()

            return redirect("lifting")

    return render(
        request,
        "account/lifting.html",
        {"suppliers": suppliers, "brands": brands, "products": products},
    )


@login_required
def display_lifting_cart(request):
    selected_products = request.session.get("selected_products", [])
    products = []
    total_sum = Decimal("0")
    date = request.session.get("lifting_date", None)
    invoicing = request.session.get("lifting_invoicing", None)

    for selected_product in selected_products:
        product = Product.objects.get(id=selected_product["product_id"])
        lifting = Lifting.objects.filter(product=product).order_by("-date").first()

        product_data = {
            "id": product.id,
            "name": product.name,
            "size": product.size,
            "qty": selected_product["qty"],
            "price": selected_product["price"],
            "total": selected_product["total"],
            "date": date,
            "invoicing": invoicing,
        }
        total_sum += Decimal(selected_product["total"])
        products.append(product_data)

    return render(
        request,
        "account/liftingcart.html",
        {"products": products, "total_sum": total_sum},
    )


@login_required
def finalize_lifting_cart(request):
    if request.method == "POST":
        selected_products = request.session.get("selected_products", [])

        for selected_product in selected_products:
            product = Product.objects.get(id=selected_product["product_id"])

            lifting = Lifting.objects.create(
                product=product,
                quantity=selected_product["qty"],
                Doprice=selected_product["price"],
                total_amount=selected_product["total"],
                invoicing=request.POST.get("invoicing"),
                date=request.POST.get("date"),
            )

            product.qty += int(selected_product["qty"])
            product.save()

        del request.session["selected_products"]

    return redirect("lifting")


@login_required
def liftingcart(request):
    return render(request, "account/liftingcart.html")


@login_required
def remove_from_cart(request, product_id):
    selected_products = request.session.get("selected_products", [])

    for selected_product in selected_products:
        if selected_product["product_id"] == int(product_id):
            selected_products.remove(selected_product)
            break

    request.session["selected_products"] = selected_products
    return redirect("liftingcart")


# sales  views Start.---------------------------------------------------------------------


@login_required
def sales(request):
    suppliers = Supplier.objects.all()
    brands = Brand.objects.all()
    products = Product.objects.all().order_by("name")
    selected_product_ids = []

    latest_price_subquery = (
        Sellprice.objects.filter(product_id=OuterRef("id"))
        .order_by("-added_on")
        .values("price")[:1]
    )
    products = products.annotate(current_pricee=Subquery(latest_price_subquery))

    latest_price_subquery = (
        Doprice.objects.filter(product_id=OuterRef("id"))
        .order_by("-added_on")
        .values("price")[:1]
    )
    products = products.annotate(current_price=Subquery(latest_price_subquery))

    next_mem_number = Sales.objects.all().aggregate(Max("mem_number"))[
        "mem_number__max"
    ]
    if next_mem_number:
        next_mem_number += 1
    else:
        next_mem_number = 1

    if request.method == "POST":
        supplier_id = request.POST.get("supplier")
        brand_id = request.POST.get("brand")
        if supplier_id and brand_id:
            products = products.filter(supplier_id=supplier_id, brand_id=brand_id)

        if "save_price" in request.POST or "update_price" in request.POST:
            selected_product_ids = request.POST.getlist("product_ids[]")
            cart = {}
            request.session["sales_date"] = request.POST.get("date")
            request.session["sales_mem_number"] = request.POST.get("invoicing")
            insufficient_stock = False
            for product_id in selected_product_ids:

                product = get_object_or_404(Product, id=product_id)
                qty_str = request.POST.get(f"price_{product_id}")
                qty = int(qty_str) if qty_str.strip() else 0
                if qty > product.qty:
                    insufficient_stock = True
                    break
                product_data = {
                    "id": product_id,
                    "qty": qty,
                    "price": products.get(id=product_id).current_pricee,
                }
                cart[product_id] = product_data

            if insufficient_stock:
                messages.warning(request, "You do not have enough products in stock")
            else:
                request.session["cart"] = cart
                return redirect("salescart")

    return render(
        request,
        "account/sales.html",
        {
            "suppliers": suppliers,
            "brands": brands,
            "products": products,
            "next_mem_number": next_mem_number,
        },
    )


@login_required
def salescart(request):
    cart = request.session.get("cart", {})
    products = []
    dsrs = Dsr.objects.all()
    markets = Market.objects.all()

    sales_date = request.session.get("sales_date", "")
    sales_mem_number = request.session.get("sales_mem_number", "")

    for product_id, product_data in cart.items():
        product = Product.objects.filter(id=product_id).first()
        if not product:
            messages.warning(request, f"Product with ID {product_id} not found")
            continue
        product_data["product"] = product
        product_data["total_amount"] = float(product_data["qty"]) * float(
            product_data["price"]
        )
        product_data["total_commission"] = float(product_data["qty"]) * float(
            product.commission
        )
        product_data["current_pricee"] = product_data["price"]
        products.append(product_data)

    if request.method == "POST":
        selected_products = []

        for product in products:
            total_amount = request.POST.get(f"{product_id}_total_amount")
            total_commission = request.POST.get(f"{product_id}_total_commission")
            if total_amount and total_commission:
                selected_products.append(
                    {
                        "product_id": product_id,
                        "qty": product_data["qty"],
                        "price": product_data["price"],
                        "total_amount": total_amount,
                        "total_commission": total_commission,
                    }
                )

        request.session["selected_products"] = selected_products

        return redirect("salescart")

    return render(
        request,
        "account/salescart.html",
        {
            "products": products,
            "dsrs": dsrs,
            "markets": markets,
            "sales_date": sales_date,
            "sales_mem_number": sales_mem_number,
        },
    )


@login_required
def final(request):
    if request.method == "POST":
        dsr_id = request.POST.get("dsr_id")
        market_id = request.POST.get("market_id")

        date = request.session.get("sales_date", "")
        memo_number = request.session.get("sales_mem_number", "")

        if date:
            date_object = datetime.strptime(date, "%Y-%m-%d").date()
        else:
            date_object = None

        product_ids = [
            int(p.split("_")[1])
            for p in request.POST
            if p.startswith("product_") and p.endswith("_qty")
        ]

        with transaction.atomic():
            for product_id in product_ids:
                product = Product.objects.get(id=product_id)
                sell_price = Sellprice.objects.get(product_id=product_id)
                dsr = Dsr.objects.get(id=dsr_id)
                market = Market.objects.get(id=market_id)
                quantity = int(request.POST[f"product_{product_id}_qty"])
                price = float(request.POST[f"product_{product_id}_price"])
                total_amount = float(request.POST[f"product_{product_id}_total_amount"])
                total_commission = float(
                    request.POST[f"product_{product_id}_total_commission"]
                )

                sales = Sales(
                    mem_number=memo_number,
                    product=product,
                    sell_price=sell_price,
                    dsr=dsr,
                    market=market,
                    quantity=quantity,
                    total_product_price=price * quantity,
                    total_sum=total_amount,
                    total_commission=total_commission,
                    date=date_object,
                )
                sales.save()

                product.qty = F("qty") - quantity
                product.save()

        if "cart" in request.session:
            del request.session["cart"]

        return redirect("sales")

    return redirect("salescart")


# damage  views Start.---------------------------------------------------------------------


@login_required
def damage(request):
    suppliers = Supplier.objects.all()
    brands = Brand.objects.all()
    products = Product.objects.all()
    selected_product_ids = []

    latest_price_subquery = (
        Sellprice.objects.filter(product_id=OuterRef("id"))
        .order_by("-added_on")
        .values("price")[:1]
    )
    products = products.annotate(current_pricee=Subquery(latest_price_subquery))

    latest_price_subquery = (
        Doprice.objects.filter(product_id=OuterRef("id"))
        .order_by("-added_on")
        .values("price")[:1]
    )
    products = products.annotate(current_price=Subquery(latest_price_subquery))

    next_mem_number = Damage.objects.all().aggregate(Max("mem_number"))[
        "mem_number__max"
    ]
    if next_mem_number:
        next_mem_number += 1
    else:
        next_mem_number = 1

    products = products.annotate(total_qty=Sum("qty"))

    items = Damage.objects.select_related(
        "product", "Purchase_Price", "sales_Price", "dsr", "market"
    ).all()

    if request.method == "POST":
        supplier_id = request.POST.get("supplier")
        brand_id = request.POST.get("brand")
        if supplier_id and brand_id:
            products = products.filter(supplier_id=supplier_id, brand_id=brand_id)

    return render(
        request,
        "account/damage.html",
        {
            "suppliers": suppliers,
            "brands": brands,
            "products": products,
            "next_mem_number": next_mem_number,
            "items": items,
        },
    )


@login_required
def add_to_damage(request):
    if request.method == "POST":
        selected_product_ids = request.POST.getlist("product_ids[]")
        mem_number = request.POST.get("mem_number")

        max_mem_number = Damage.objects.all().aggregate(Max("mem_number"))[
            "mem_number__max"
        ]
        new_mem_number = max_mem_number + 1 if max_mem_number else 1

        for product_id in selected_product_ids:
            product = Product.objects.get(id=product_id)
            latest_doprice_instance = product.doprice_set.order_by("-added_on").first()
            latest_sellprice_instance = product.sellprice_set.order_by(
                "-added_on"
            ).first()
            damage = Damage.objects.create(
                product=product,
                Purchase_Price=latest_doprice_instance,
                sales_Price=latest_sellprice_instance,
                date=request.POST.get("date"),
                mem_number=new_mem_number,
                qty=float(request.POST.get(f"price_{product_id}")),
            )

            damage.save()

        items = Damage.objects.select_related(
            "product", "Purchase_Price", "sales_Price"
        ).filter(product_id__in=selected_product_ids, mem_number=new_mem_number)
        total_sales_amount = sum(item.sales_amount for item in items)
        total_purchase_amount = sum(item.purchase_amount for item in items)
        return render(
            request,
            "account/damagecart.html",
            {
                "items": items,
                "total_sales_amount": total_sales_amount,
                "total_purchase_amount": total_purchase_amount,
            },
        )


@login_required
def remove_from_damage(request, damage_id):
    damage_item = Damage.objects.get(id=damage_id)
    mem_number = damage_item.mem_number
    damage_item.delete()

    return HttpResponseRedirect(reverse("damagecart", args=(mem_number,)))


@login_required
def damagecart(request, mem_number):
    items = Damage.objects.select_related(
        "product", "Purchase_Price", "sales_Price", "dsr", "market"
    ).filter(mem_number=mem_number)
    total_sales_amount = sum(item.sales_amount for item in items)
    total_purchase_amount = sum(item.purchase_amount for item in items)
    return render(
        request,
        "account/damagecart.html",
        {
            "items": items,
            "total_sales_amount": total_sales_amount,
            "total_purchase_amount": total_purchase_amount,
        },
    )


# bank_manage  views Start.---------------------------------------------------------------------


@login_required
def bank_manage(request):
    if request.method == "POST":
        bank_id = request.POST.get("bank")
        if not bank_id:
            return HttpResponse("Please select a valid bank branch.")

        try:
            amount = Decimal(request.POST.get("amount") or 0)
        except InvalidOperation:
            return HttpResponse("Invalid amount. Please enter valid numbers.")

        try:
            bank = Bank.objects.get(id=bank_id)
        except Bank.DoesNotExist:
            return HttpResponse("Bank not found. Please select a valid bank branch.")

        BankTransaction.objects.create(bank=bank, amount=amount)

        return HttpResponseRedirect(reverse("bank_manage") + f"?bank={bank_id}")

    banks = Bank.objects.all()

    for bank in banks:
        total_amount = (
            BankTransaction.objects.filter(bank=bank).aggregate(Sum("amount"))[
                "amount__sum"
            ]
            or 0
        )
        bank.current_balance = total_amount

    current_balance = None
    bank_id = request.GET.get("bank")
    if bank_id:
        total_amount = (
            BankTransaction.objects.filter(bank__id=bank_id).aggregate(Sum("amount"))[
                "amount__sum"
            ]
            or 0
        )
        current_balance = total_amount

    return render(
        request,
        "account/bank_manage.html",
        {"banks": banks, "current_balance": current_balance},
    )


# supplierspayment  views Start.---------------------------------------------------------------------


@login_required
def supplierspayment(request):
    suppliers = Supplier.objects.all()
    banks = Bank.objects.all()
    error_message = None

    if request.method == "POST":
        supplier_id = request.POST.get("supplier")
        bank_id = request.POST.get("bank")
        amount = float(request.POST.get("amount"))
        date = request.POST.get("date")

        supplier = Supplier.objects.get(id=supplier_id)
        bank = Bank.objects.get(id=bank_id)

        total_amount = (
            BankTransaction.objects.filter(bank=bank).aggregate(Sum("amount"))[
                "amount__sum"
            ]
            or 0
        )

        if total_amount >= amount:

            SupplierPayment.objects.create(
                supplier=supplier, bank=bank, amount=amount, date=date
            )

            BankTransaction.objects.create(bank=bank, amount=-amount)

            return HttpResponseRedirect(reverse("supplierspayment"))
        else:
            error_message = "Insufficient balance, please deposit to your bank account."

    for bank in banks:
        total_amount = (
            BankTransaction.objects.filter(bank=bank).aggregate(Sum("amount"))[
                "amount__sum"
            ]
            or 0
        )
        bank.current_balance = total_amount

    return render(
        request,
        "account/supplierspayment.html",
        {"suppliers": suppliers, "banks": banks, "error_message": error_message},
    )


# Discount  views Start.---------------------------------------------------------------------


@login_required
def acdiccount(request):
    suppliers = Supplier.objects.all()
    brands = Brand.objects.all()
    discount_setups = Discountsetup.objects.all()
    sr = Salesmanager.objects.all()

    if request.method == "POST":
        supplier_id = request.POST.get("supplier")
        brand_id = request.POST.get("brand")
        sr_id = request.POST.get("sr")
        discount_id = request.POST.get("discount")
        date = request.POST.get("date")
        amount = request.POST.get("amount")

        supplier = Supplier.objects.get(id=supplier_id)
        brand = Brand.objects.get(id=brand_id)
        salesmanager = Salesmanager.objects.get(id=sr_id)
        discount = Discountsetup.objects.get(id=discount_id)

        data = Acdiccount(
            supplier=supplier,
            brand=brand,
            sr=salesmanager,
            discount=discount,
            date=date,
            amount=amount,
        )
        data.save()

    if sr:
        return render(
            request,
            "account/acdiccount.html",
            {
                "suppliers": suppliers,
                "brands": brands,
                "sr": sr,
                "discount_setups": discount_setups,
            },
        )
    else:
        return render(
            request,
            "account/acdiccount.html",
            {
                "suppliers": suppliers,
                "brands": brands,
                "discount_setups": discount_setups,
            },
        )


# Dailycost  views Start.---------------------------------------------------------------------


@login_required
def dailycost(request):
    dsrs = Dsr.objects.all()

    if request.method == "POST":
        dsr_id = request.POST.get("dsr")
        car_cost = request.POST.get("car_cost")
        dsr_bill = request.POST.get("dsr_bill")
        toll = request.POST.get("toll")
        other_cost = request.POST.get("other_cost")
        date = request.POST.get("date")

        dsr_instance = Dsr.objects.get(id=dsr_id)

        data = Dailycost(
            dsr=dsr_instance,
            carcost=car_cost,
            dsrbill=dsr_bill,
            toll=toll,
            othercost=other_cost,
            date=date,
        )
        data.save()

    return render(request, "account/dailycost.html", {"dsrs": dsrs})


# Chack  views Start.---------------------------------------------------------------------


@login_required
def chack(request):
    if request.method == "POST":
        supplier_id = request.POST.get("supplier")
        brand_id = request.POST.get("brand")

        products = Product.objects.filter(
            supplier_id=supplier_id, brand_id=brand_id
        ).order_by("name")

        for product in products:
            try:
                price = Sellprice.objects.filter(product=product).latest("added_on")
                product.current_price = price.price
            except Sellprice.DoesNotExist:
                product.current_price = None
    else:
        products = None

    suppliers = Supplier.objects.all()
    brands = Brand.objects.all()

    return render(
        request,
        "account/chack.html",
        {"suppliers": suppliers, "brands": brands, "products": products},
    )


# Collection  views Start.---------------------------------------------------------------------


@login_required
def collection(request):
    current_amount = Decimal("0.00")

    if request.method == "POST":
        collection_man_id = request.POST.get("collection-man")
        date = request.POST.get("date")
        transaction_type = request.POST.get("transaction-type")
        amount = Decimal(request.POST.get("amount"))

        collection_man = get_object_or_404(Collectionsetup, id=collection_man_id)
        latest_transaction = CollectionTransaction.objects.filter(
            collection_man=collection_man
        ).last()

        if latest_transaction:
            current_amount = latest_transaction.current_amount

        if transaction_type == "deposit":
            current_amount += amount
        else:
            current_amount -= amount

        transaction = CollectionTransaction(
            collection_man=collection_man,
            date=date,
            transaction_type=transaction_type,
            amount=amount,
            current_amount=current_amount,
        )
        transaction.save()

    collection_men = Collectionsetup.objects.all()

    return render(
        request,
        "account/collection.html",
        {"collection_men": collection_men, "current_amount": current_amount},
    )


# Assets  views Start.---------------------------------------------------------------------


@login_required
def assets(request):
    if request.method == "POST":

        date = request.POST.get("date")
        shop_due = request.POST.get("shop_due")
        rashed_due = request.POST.get("rashed")
        bazar_due = request.POST.get("bazar")
        tso = request.POST.get("tso")
        milon = request.POST.get("milon")
        bank_check = request.POST.get("check")
        mehdi_sr = request.POST.get("mehdisr")
        card = request.POST.get("card")
        damage = request.POST.get("damage")
        naitrogen_damage = request.POST.get("nitrogen")
        robiul_sr = request.POST.get("robiul")
        pubali_bank = request.POST.get("pubalibank")
        robiul_dsr = request.POST.get("robiuldsr")
        stock = request.POST.get("stock")
        other = request.POST.get("other")

        asset = Assets(
            date=date,
            shop_due=shop_due,
            rashed_due=rashed_due,
            bazar_due=bazar_due,
            tso=tso,
            milon=milon,
            bank_check=bank_check,
            mehdi_sr=mehdi_sr,
            card=card,
            damage=damage,
            naitrogen_damage=naitrogen_damage,
            robiul_sr=robiul_sr,
            pubali_bank=pubali_bank,
            robiul_dsr=robiul_dsr,
            stock=stock,
            other=other,
        )
        asset.save()

        return redirect("success_page")

    return render(request, "account/assets.html")


# Success  views Start.---------------------------------------------------------------------


@login_required
def success_page_view(request):
    return render(request, "account/success_page.html")
