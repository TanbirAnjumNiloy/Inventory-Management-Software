from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.db.models import Subquery, OuterRef
from django.contrib import messages
from .models import *
from account.models import *
from setup.models import Supplier, Brand, Market, Dsr, Bank, Product
import json
from django.db.models import OuterRef, Subquery, Sum, Max
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import F
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.
@login_required
def control(request):
    return render(request, "control/control.html")


@login_required
def supplieredit(request):

    data = Supplier.objects.all()
    contex = {
        "data": data,
    }

    return render(request, "control/supplieredit.html", contex)


@login_required
def brandedit(request):
    brand = Brand.objects.all()
    contex = {
        "item": brand,
    }
    return render(request, "control/brandedit.html", contex)


@login_required
def marketedit(request, market_id):
    market = get_object_or_404(Market, pk=market_id)

    if request.method == "POST":
        area = request.POST.get("area")
        address = request.POST.get("address")
        number = request.POST.get("number")

        market.area = area
        market.address = address
        market.number = number
        market.save()

        return redirect("marketedit", market_id=market.id)

    return render(request, "control/marketedit.html", {"market": market})


@login_required
def market_list(request):
    market = Market.objects.all()
    contex = {
        "market": market,
    }
    return render(request, "control/market_list.html", contex)


# -----------------DSR Edit Function---------------------------------------------#
@login_required
def dsredit(request, dsr_id):
    dsr = get_object_or_404(Dsr, pk=dsr_id)

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        address = request.POST.get("address")

        dsr.name = name
        dsr.phone = phone
        dsr.email = email
        dsr.address = address
        dsr.save()

        return redirect("dsredit", dsr_id=dsr.id)

    return render(request, "control/dsredit.html", {"dsr": dsr})


@login_required
def dsr_list(request):
    dsr = Dsr.objects.all()
    context = {
        "dsr": dsr,
    }
    return render(request, "control/dsr_list.html", context)


# -----------------DSR Edit Function End ---------------------------------------------#


@login_required
def bankedit(request):
    bank = Bank.objects.all()
    contex = {
        "data": bank,
    }
    return render(request, "control/bankedit.html", contex)


# -----------------Product Edit Function---------------------------------------------#
@login_required
def productedit(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == "POST":
        name = request.POST.get("name")
        size = request.POST.get("size")
        commission = request.POST.get("commission")

        product.name = name
        product.size = size
        product.commission = commission
        product.save()

        return redirect("productedit", product_id=product.id)

    return render(request, "control/productedit.html", {"product": product})


@login_required
def product_list(request):
    products = Product.objects.all().order_by("name")
    context = {
        "products": products,
    }
    return render(request, "control/product_list.html", context)


# -----------------Product Edit End Function---------------------------------------------#


@login_required
def lifting_update(request):
    if request.method == "POST":
        invoice_number = request.POST.get("invoice_number")
        lifting_items = Lifting.objects.filter(invoicing=invoice_number)
        if lifting_items.exists():
            product_qty_price_total_list = []

            for lifting in lifting_items:
                product = lifting.product
                qty = lifting.quantity
                price = lifting.Doprice
                total_price = price * qty
                product_qty_price_total_list.append(
                    (product, qty, price, total_price, lifting)
                )
            supplier = lifting_items.first().product.supplier
            brand = lifting_items.first().product.brand

            context = {
                "lifting": lifting_items.first(),
                "product_qty_price_total_list": product_qty_price_total_list,
                "supplier": supplier,
                "brand": brand,
            }
            return render(request, "control/lifting_update.html", context=context)
        else:

            pass
    return render(request, "control/lifting_update.html")


@login_required
@csrf_exempt
def update_lifting(request):
    if request.method == "POST":
        data = json.loads(request.body)
        lifting_id = data.get("lifting_id")
        new_qty = data.get("new_qty")
        new_price = data.get("new_price")

        try:
            lifting = Lifting.objects.get(id=lifting_id)
            old_qty = lifting.quantity
            old_total = lifting.total_amount
            lifting.quantity = new_qty
            lifting.Doprice = new_price
            lifting.total_amount = new_price * new_qty
            lifting.save()

            product = lifting.product
            product.qty = product.qty - old_qty + new_qty
            product.save()

            products = Product.objects.all()
            latest_do_price_subquery = (
                Doprice.objects.filter(product_id=OuterRef("id"))
                .order_by("-added_on")
                .values("price")[:1]
            )
            products = products.annotate(do_price=Subquery(latest_do_price_subquery))
            products = products.annotate(total_qty=Sum("qty"))
            res_list = []
            for product in products:
                res = product.total_qty * product.do_price
                res_list.append(res)

            context = {
                "products": zip(products, res_list),
            }
            return JsonResponse(
                {
                    "status": "success",
                    "html": render("report/stockreport_partial.html", context=context),
                }
            )
        except Lifting.DoesNotExist:
            return JsonResponse({"status": "failure"})
    else:
        return JsonResponse({"status": "failure"})


@login_required
def lifting_backdate(request):
    if request.method == "POST":
        invoice_number = request.POST.get("invoice_number")
        new_date = request.POST.get("date")

        lifting_instances = Lifting.objects.filter(invoicing=invoice_number)

        if lifting_instances.exists():
            lifting_instances.update(date=new_date)
            messages.success(request, "Lifting date updated successfully.")
            return redirect("lifting_backdate")
        else:
            messages.error(request, "Invoice number not found.")
            return redirect("lifting_backdate")

    return render(request, "control/liftingbackdate.html")


@login_required
def sales_backdate(request):
    if request.method == "POST":
        memo_number = request.POST.get("memo_number")
        new_date = request.POST.get("date")

        sales_instances = Sales.objects.filter(mem_number=memo_number)

        if sales_instances.exists():
            print(f"Updating the following instances: {sales_instances}")
            sales_instances.update(date=new_date)
            messages.success(request, "Sales date updated successfully.")
            return redirect("sales_backdate")
        else:
            messages.error(request, "Memo number not found.")
            return redirect("sales_backdate")

    return render(request, "control/salesbackdate.html")


@login_required
def damage_backdate(request):
    if request.method == "POST":
        memo_number = request.POST.get("invoice_number")
        new_date = request.POST.get("date")

        if not memo_number or not new_date:
            messages.error(request, "Both memo number and date are required.")
            return redirect("damage_backdate")

        try:
            memo_number = int(memo_number)
        except ValueError:
            messages.error(request, "Invalid memo number.")
            return redirect("damage_backdate")

        damage_instances = Damage.objects.filter(mem_number=memo_number)

        if damage_instances.exists():
            print(f"Updating the following instances: {damage_instances}")
            damage_instances.update(date=new_date)
            messages.success(request, "Damage date updated successfully.")
            return redirect("damage_backdate")
        else:
            messages.error(request, "Memo number not found.")
            return redirect("damage_backdate")

    return render(request, "control/damagebackdate.html")


@login_required
def lifting_delate(request):
    if request.method == "POST":
        invoice_number = request.POST.get("invoice_number")
        if invoice_number:
            lifting_objects = Lifting.objects.filter(invoicing=invoice_number)

            for lifting in lifting_objects:
                product = lifting.product
                product.qty -= lifting.quantity
                product.save()

            lifting_objects.delete()
            messages.success(
                request,
                f"Deleted all items associated with invoice number {invoice_number}",
            )
        else:
            messages.error(request, "Invoice number is required to delete items")

    return render(request, "control/liftingdelate.html")


@login_required
def sales_delate(request):
    if request.method == "POST":
        memo_number = request.POST.get("invoice_number")
        if memo_number:
            sales_objects = Sales.objects.filter(mem_number=memo_number)

            for sale in sales_objects:
                product = sale.product
                product.qty += sale.quantity
                product.save()

            sales_objects.delete()
            messages.success(
                request, f"Deleted all items associated with memo number {memo_number}"
            )
        else:
            messages.error(request, "Memo number is required to delete items")

    return render(request, "control/salesdelate.html")


@login_required
def damage_delate(request):
    if request.method == "POST":
        mem_number = request.POST.get("mem_number")
        Damage.objects.filter(mem_number=mem_number).delete()

        return HttpResponseRedirect(reverse("damage_delete_success"))

    return render(request, "control/damagedelate.html")


@login_required
def damage_delete_success(request):
    return render(request, "control/damage_delete_success.html")


@login_required
def supplierpaymentupadte(request):
    supplier_payments = SupplierPayment.objects.select_related("supplier", "bank").all()
    return render(
        request,
        "control/supplierpaymentsetup.html",
        {"supplier_payments": supplier_payments},
    )


@login_required
def update_supplier_payment(request):
    if request.method == "POST":
        supplier_payment_id = request.POST.get("supplier_payment_id")
        new_amount = float(request.POST.get("amount"))

        supplier_payment = get_object_or_404(SupplierPayment, id=supplier_payment_id)
        bank = supplier_payment.bank

        amount_difference = new_amount - supplier_payment.amount

        BankTransaction.objects.create(bank=bank, amount=-amount_difference)

        supplier_payment.amount = new_amount
        supplier_payment.save()

    return HttpResponseRedirect(reverse("supplierpaymentupadte"))


@login_required
def damagealldelate(request):
    if request.method == "GET":
        supplier_id = request.GET.get("supplier")
        brand_id = request.GET.get("brand")
        from_date = request.GET.get("from-date")
        to_date = request.GET.get("to-date")

        if from_date and to_date:

            q_filter = Q()
            if supplier_id:
                q_filter &= Q(product__supplier_id=supplier_id)
            if brand_id:
                q_filter &= Q(product__brand_id=brand_id)
            if from_date and to_date:
                q_filter &= Q(date__range=(from_date, to_date))

            Damage.objects.filter(q_filter).delete()

            messages.success(request, "Damage records deleted successfully.")

        suppliers = Supplier.objects.all()
        brands = Brand.objects.all()
        return render(
            request,
            "control/damagealldelate.html",
            {"suppliers": suppliers, "brands": brands},
        )

    return HttpResponseBadRequest("Bad Request")
