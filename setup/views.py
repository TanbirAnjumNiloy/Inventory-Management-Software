from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Subquery, OuterRef
from .models import *
from django.utils import timezone
from account.models import SupplierPayment
from django.contrib.auth.decorators import login_required


# Create your views here.


# setup----------------------------------------------------------------
@login_required
def setup(request):
    return render(request, "setup/setup.html")


# End setup----------------------------------------------------------------


# Supplier  views here.-----------------------------------------------------------
@login_required
def suppliers_setup(request):
    if request.method == "POST":
        sname = request.POST.get("sname")
        saddress = request.POST.get("saddress")
        smobile = request.POST.get("smobile")
        sbalance = request.POST.get("sbalance")

        data = Supplier(
            sname=sname,
            saddress=saddress,
            smobile=smobile,
            sbalance=sbalance,
        )
        data.save()

    return render(request, "setup/suppliers_setup.html")


# End Supplier  views here.--------------------------------------------------------------


# Brand  views here.---------------------------------------------------------------------
@login_required
def brand_setup(request):
    if request.method == "POST":
        supplier_id = request.POST.get("supplier")
        brand_name = request.POST.get("brand_name")

        supplier_obj = Supplier.objects.get(pk=supplier_id)
        brand = Brand(supplier=supplier_obj, name=brand_name)
        brand.save()

        return redirect("brand_setup")

    suppliers = Supplier.objects.all()
    return render(request, "setup/brand_setup.html", {"suppliers": suppliers})


# End Brand  views here.--------------------------------------------------------------


# Group  views here.--------------------------------------------------------------------
@login_required
def group_name(request):
    return render(request, "setup/group_name.html")


# End Brand  views here.----------------------------------------------------------------


# Product  views here.----------------------------------------------------------------------
@login_required
def product_name(request):
    brands = Brand.objects.all()
    suppliers = Supplier.objects.all()

    if request.method == "POST":
        # Get the form data from the request
        name = request.POST.get("name")
        size = request.POST.get("size")
        commission = request.POST.get("commission")
        brand_id = request.POST.get("brand")
        supplier_id = request.POST.get("supplier")

        # Create a new Product object and save it to the database
        product = Product(
            name=name,
            size=size,
            commission=commission,
            brand_id=brand_id,
            supplier_id=supplier_id,
        )
        product.save()

        # Redirect the user to a success page
        return redirect("product_name")

    # If the request method is not POST, just render the product form template
    return render(
        request, "setup/product_name.html", {"brands": brands, "suppliers": suppliers}
    )


# End Product  views here.------------------------------------------------------


# Market  views here.----------------------------------------------------------
@login_required
def market_setup(request):
    if request.method == "POST":
        area = request.POST.get("area")
        address = request.POST.get("address")
        number = request.POST.get("number")
        market = Market(
            area=area,
            address=address,
            number=number,
        )
        market.save()
    return render(request, "setup/market_setup.html")


# End Market  views here.-----------------------------------------------------


# Bank  views here.-----------------------------------------------------------
@login_required
def bank_setup(request):
    if request.method == "POST":
        bank_name = request.POST.get("bank_name")
        account_no = request.POST.get("account_no")
        branch = request.POST.get("branch")
        account_type = request.POST.get("account_type")

        Bank.objects.create(
            bank_name=bank_name,
            account_no=account_no,
            branch=branch,
            account_type=account_type,
        )

        return HttpResponseRedirect(reverse("bank_setup"))
    return render(request, "setup/bank_setup.html")


# End bank   views here.-------------------------------------------------------


# DSR  views here.--------------------------------------------------------------
@login_required
def dsr_setup(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        address = request.POST.get("address")
        dsr = Dsr(
            name=name,
            phone=phone,
            email=email,
            address=address,
        )
        dsr.save()
    return render(request, "setup/dsr_setup.html")


# End DSR  views here.---------------------------------------------------------------------


# Do setup  views here.---------------------------------------------------------------------
@login_required
def do_setup(request):
    suppliers = Supplier.objects.all()
    brands = Brand.objects.all()
    products = Product.objects.all().order_by("name")  
    selected_product_ids = []

    latest_price_subquery = (
        Doprice.objects.filter(product_id=OuterRef("id"))
        .order_by("-added_on")
        .values("price")[:1]
    )
    products = products.annotate(current_price=Subquery(latest_price_subquery))

    if request.method == "POST":
        supplier_id = request.POST.get("supplier")
        brand_id = request.POST.get("brand")
        if supplier_id and brand_id:
            products = products.filter(supplier_id=supplier_id, brand_id=brand_id)

        if "save_price" in request.POST or "update_price" in request.POST:
            selected_product_ids = request.POST.getlist("product_ids[]")

            prices = {}
            for product in products:
                price_key = f"price_{product.id}"
                price_value = request.POST.get(price_key)
                if price_value:
                    
                    try:
                        price = Doprice.objects.get(product=product)
                        
                        price.price = float(price_value)
                        price.added_on = timezone.now()
                        price.save()
                    except Doprice.DoesNotExist:
                      
                        price = Doprice.objects.create(
                            product=product,
                            price=float(price_value),
                            added_on=timezone.now(),
                        )

                    prices[product.id] = price.id

            request.session["prices"] = prices
            request.session["selected_product_ids"] = selected_product_ids

            return HttpResponseRedirect(reverse("do_setup"))

    return render(
        request,
        "setup/do_setup.html",
        {"suppliers": suppliers, "brands": brands, "products": products},
    )


#  End Do setup  views here.-------------------------------------------------------------


# sell setup  views here.---------------------------------------------------------------------
@login_required
def sell_setup(request):
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

    if request.method == "POST":
        supplier_id = request.POST.get("supplier")
        brand_id = request.POST.get("brand")
        if supplier_id and brand_id:
            products = products.filter(supplier_id=supplier_id, brand_id=brand_id)

        if "save_price" in request.POST or "update_price" in request.POST:
            selected_product_ids = request.POST.getlist("product_ids[]")

            prices = {}
            for product in products:
                price_key = f"price_{product.id}"
                price_value = request.POST.get(price_key)
                if price_value:
                    try:
                        price = Sellprice.objects.get(product=product)
                        price.price = float(price_value)
                        price.added_on = timezone.now()
                        price.save()
                    except Sellprice.DoesNotExist:
                        price = Sellprice.objects.create(
                            product=product,
                            price=float(price_value),
                            added_on=timezone.now(),
                        )

                    prices[product.id] = price.id

            request.session["prices"] = prices
            request.session["selected_product_ids"] = selected_product_ids

            return HttpResponseRedirect(reverse("sell_setup"))

    return render(
        request,
        "setup/sell_setup.html",
        {"suppliers": suppliers, "brands": brands, "products": products},
    )


#  End sell setup  views here.-------------------------------------------------------------

# DSR setup  views here.---------------------------------------------------------------------
@login_required
def salesmanager(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        address = request.POST.get("address")

        sm = Salesmanager(
            name=name,
            phone=phone,
            email=email,
            address=address,
        )

        sm.save()

    return render(request, "setup/salesmanager.html")


# DSR setup  views END.---------------------------------------------------------------------

# Discountsetup setup  views here.---------------------------------------------------------------------


@login_required
def discountsetup(request):
    suppliers = Supplier.objects.all()
    brands = Brand.objects.all()
    if request.method == "POST":
        supplier_id = request.POST.get("supplier")
        brand_id = request.POST.get("brand")
        name = request.POST.get("name")

        Dis = Discountsetup(
            supplier_id=supplier_id,
            brand_id=brand_id,
            name=name,
        )
        Dis.save()

    return render(
        request, "setup/discountsetup.html", {"suppliers": suppliers, "brands": brands}
    )


# discountsetup setup  views end.---------------------------------------------------------------------


# Collectionsetup setup  views here.---------------------------------------------------------------------


@login_required
def collectionsetup(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        address = request.POST.get("address")

        clt = Collectionsetup(
            name=name,
            phone=phone,
            email=email,
            address=address,
        )
        clt.save()
    return render(request, "setup/collectionsetup.html")


# Collectionsetup setup  views end.---------------------------------------------------------------------

# KG setup  views here.---------------------------------------------------------------------
@login_required
def grams(request):
    suppliers = Supplier.objects.all()
    brands = Brand.objects.all()

    if request.method == "POST":

        if "show_products" in request.POST:
            supplier_id = request.POST.get("supplier")
            brand_id = request.POST.get("brand")

            products = Product.objects.filter(
                supplier_id=supplier_id, brand_id=brand_id
            ).order_by("name")
        else:
            product_ids = request.POST.getlist("product_ids[]")
            for product_id in product_ids:
                product = Product.objects.get(id=product_id)

                grams = request.POST.get(f"grams_{product_id}", None)
                current_grams = request.POST.get(f"current_grams_{product_id}", None)

                grams = float(grams) if grams not in [None, ""] else None
                current_grams = (
                    float(current_grams) if current_grams not in [None, ""] else None
                )

                if grams is not None and current_grams is not None:
                    GramSetup.objects.update_or_create(
                        product=product,
                        defaults={"grams": grams, "current_grams": current_grams},
                    )
            return redirect("grams")
    else:

        products = Product.objects.all().order_by("name")

    return render(
        request,
        "setup/grams.html",
        {"suppliers": suppliers, "brands": brands, "products": products},
    )


# KG setup  views end.---------------------------------------------------------------------
