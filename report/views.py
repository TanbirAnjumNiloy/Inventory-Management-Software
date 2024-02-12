from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from django.db.models import Sum
from django.db.models import Subquery, OuterRef
from django.db.models import OuterRef, Subquery, Sum
from decimal import Decimal, DivisionUndefined
from itertools import groupby
from operator import attrgetter
from django.db.models import Sum, F
from django.db.models import F
from itertools import groupby
from .models import *
from setup.models import *
from account.models import *
from django.db.models import Sum, F
from django.db.models import Sum
from account.models import Lifting
from decimal import Decimal
from django.db.models import Q
from operator import attrgetter
from itertools import chain
from itertools import groupby
from django.contrib.auth.decorators import login_required
from django.db.models import (
    F,
    ExpressionWrapper,
    FloatField,
    Subquery,
    OuterRef,
    Case,
    When,
)
from django.db.models.functions import Cast
from django.shortcuts import render
from django.db.models import Sum, OuterRef, Subquery, Q
from datetime import datetime
from django.db.models import (
    F,
    ExpressionWrapper,
    FloatField,
    Subquery,
    OuterRef,
    Case,
    When,
)
from django.db.models import (
    Sum,
    Avg,
    F,
    FloatField,
    Case,
    When,
    Subquery,
    OuterRef,
    ExpressionWrapper,
)
from django.db.models import Sum, Q
from datetime import timedelta


# Create your views here.


# report  views Start.---------------------------------------------------------------------
@login_required
def report(request):
    return render(request, "report/report.html")


# stockreport  views Start.---------------------------------------------------------------------


@login_required
def stockreport(request):
    suppliers = Supplier.objects.all()
    brands = Brand.objects.all()
    products = Product.objects.all()

    latest_do_price_subquery = (
        Doprice.objects.filter(product_id=OuterRef("id"))
        .order_by("-id")
        .values("price")[:1]
    )
    products = products.annotate(do_price=Subquery(latest_do_price_subquery))

    latest_sell_price_subquery = (
        Sellprice.objects.filter(product_id=OuterRef("id"))
        .order_by("-id")
        .values("price")[:1]
    )
    products = products.annotate(sell_price=Subquery(latest_sell_price_subquery))

    if request.method == "POST":
        supplier_id = request.POST.get("supplier")
        brand_id = request.POST.get("brand")
        date = request.POST.get("from-date")
        another_date = request.POST.get("from-date2")

        if supplier_id and brand_id:
            products = products.filter(supplier_id=supplier_id, brand_id=brand_id)

        if date:
            date_obj = datetime.strptime(date, "%Y-%m-%d").date()
            ten_days_before = date_obj - timedelta(days=10)

            for product in products:
                sales_in_last_10_days = Sales.objects.filter(
                    product=product, date__range=[ten_days_before, date_obj]
                ).exists()
                product.not_sold_in_last_10_days = not sales_in_last_10_days

            for product in products:
                today_sales = Sales.objects.filter(
                    product=product, date=date_obj
                ).aggregate(today_sales=Sum("quantity"))["today_sales"]
                product.today_sales = today_sales if today_sales is not None else 0

            total_purchases = (
                Lifting.objects.filter(Q(date__lte=date_obj) & Q(product__in=products))
                .values("product")
                .annotate(total_purchase_qty=Sum("quantity"))
            )
            total_sales = (
                Sales.objects.filter(Q(date__lte=date_obj) & Q(product__in=products))
                .values("product")
                .annotate(total_sales_qty=Sum("quantity"))
            )

            product_stats = {}
            for purchase in total_purchases:
                product_id = purchase["product"]
                product_stats[product_id] = {
                    "total_purchase_qty": purchase["total_purchase_qty"],
                    "total_sales_qty": 0,
                }

            for sale in total_sales:
                product_id = sale["product"]
                if product_id in product_stats:
                    product_stats[product_id]["total_sales_qty"] = sale[
                        "total_sales_qty"
                    ]
                else:
                    product_stats[product_id] = {
                        "total_purchase_qty": 0,
                        "total_sales_qty": sale["total_sales_qty"],
                    }

            for product in products:
                if product.id in product_stats:
                    product.total_purchase_qty = product_stats[product.id][
                        "total_purchase_qty"
                    ]
                    product.total_sales_qty = product_stats[product.id][
                        "total_sales_qty"
                    ]
                    product.stock_on_date = (
                        product.total_purchase_qty - product.total_sales_qty
                    )
                else:
                    product.total_purchase_qty = 0
                    product.total_sales_qty = 0
                    product.stock_on_date = 0

            for product in products:
                product.stock_value_do_price = (
                    product.stock_on_date * product.do_price if product.do_price else 0
                )
                product.stock_value_sell_price = (
                    product.stock_on_date * product.sell_price
                    if product.sell_price
                    else 0
                )

        if another_date:
            another_date_obj = datetime.strptime(another_date, "%Y-%m-%d").date()

            another_total_purchases = (
                Lifting.objects.filter(
                    Q(date__lte=another_date_obj) & Q(product__in=products)
                )
                .values("product")
                .annotate(total_purchase_qty=Sum("quantity"))
            )
            another_total_sales = (
                Sales.objects.filter(
                    Q(date__lte=another_date_obj) & Q(product__in=products)
                )
                .values("product")
                .annotate(total_sales_qty=Sum("quantity"))
            )

            another_product_stats = {}
            for purchase in another_total_purchases:
                product_id = purchase["product"]
                another_product_stats[product_id] = {
                    "total_purchase_qty": purchase["total_purchase_qty"],
                    "total_sales_qty": 0,
                }

            for sale in another_total_sales:
                product_id = sale["product"]
                if product_id in another_product_stats:
                    another_product_stats[product_id]["total_sales_qty"] = sale[
                        "total_sales_qty"
                    ]
                else:
                    another_product_stats[product_id] = {
                        "total_purchase_qty": 0,
                        "total_sales_qty": sale["total_sales_qty"],
                    }

            for product in products:
                if product.id in another_product_stats:
                    product.total_purchase_qty_another_date = another_product_stats[
                        product.id
                    ]["total_purchase_qty"]
                    product.total_sales_qty_another_date = another_product_stats[
                        product.id
                    ]["total_sales_qty"]
                    product.stock_on_another_date = (
                        product.total_purchase_qty_another_date
                        - product.total_sales_qty_another_date
                    )
                else:
                    product.total_purchase_qty_another_date = 0
                    product.total_sales_qty_another_date = 0
                    product.stock_on_another_date = 0

            for product in products:
                product.stock_value_do_price_another_date = (
                    product.stock_on_another_date * product.do_price
                    if product.do_price
                    else 0
                )
                product.stock_value_sell_price_another_date = (
                    product.stock_on_another_date * product.sell_price
                    if product.sell_price
                    else 0
                )

    selected_date = request.POST.get("from-date")

    context = {
        "suppliers": suppliers,
        "brands": brands,
        "products": products,
        "selected_date": selected_date,
    }

    return render(request, "report/stockreport.html", context)


# liftingreport  views Start.---------------------------------------------------------------------


@login_required
def liftingreport(request):
    suppliers = Supplier.objects.all()
    brands = Brand.objects.all()
    liftings = Lifting.objects.all()
    search_clicked = False

    if request.method == "GET":
        supplier_id = request.GET.get("supplier")
        brand_id = request.GET.get("brand")
        from_date = request.GET.get("from-date")
        to_date = request.GET.get("to-date")
        search_clicked = request.GET.get("search") is not None

        if supplier_id:
            liftings = liftings.filter(product__supplier_id=supplier_id)
        if brand_id:
            liftings = liftings.filter(product__brand_id=brand_id)
        if from_date and to_date:
            liftings = liftings.filter(date__range=[from_date, to_date])

        liftings = liftings.order_by("invoicing")

    total_product_value = liftings.aggregate(total=Sum("total_amount"))["total"] or 0

    if search_clicked:
        liftings = liftings.order_by("invoicing", "product__name")
        grouped_liftings = {
            k: list(v) for k, v in groupby(liftings, key=lambda x: x.invoicing)
        }
        return render(
            request,
            "report/liftingreportresult.html",
            {
                "suppliers": suppliers,
                "brands": brands,
                "grouped_liftings": grouped_liftings,
                "total_product_value": total_product_value,
            },
        )
    else:
        return render(
            request,
            "report/liftingreport.html",
            {"suppliers": suppliers, "brands": brands},
        )


# salesreport  views Start.---------------------------------------------------------------------


@login_required
def salesreport(request):
    suppliers = Supplier.objects.all()
    brands = Brand.objects.all()
    return render(
        request, "report/salesreport.html", {"suppliers": suppliers, "brands": brands}
    )


@login_required
def sales_report_result(request):
    if request.method == "GET":
        supplier_id = request.GET.get("supplier")
        brand_id = request.GET.get("brand")
        from_date = request.GET.get("from-date")
        to_date = request.GET.get("to-date")

        sales_data = (
            Sales.objects.filter(
                product__supplier_id=supplier_id,
                product__brand_id=brand_id,
                date__range=(from_date, to_date),
            )
            .values("product__name", "product__size")
            .annotate(total_qty=Sum("quantity"), total_value=Sum("total_product_price"))
        )

        for sale in sales_data:
            total_qty = float(sale["total_qty"])
            total_value = float(sale["total_value"])
            if total_qty != 0:
                sale["sales_rate"] = total_value / total_qty
            else:
                sale["sales_rate"] = 0.0

        total_sum = sales_data.aggregate(total_sum=Sum("total_value"))["total_sum"]

        return render(
            request,
            "report/salesreportresult.html",
            {"sales_data": sales_data, "total_sum": total_sum},
        )
    else:
        return redirect("salesreport")


@login_required
def salesreport(request):
    suppliers = Supplier.objects.all()
    brands = Brand.objects.all()
    dsr = Dsr.objects.all()
    sales_data = Sales.objects.all()
    return render(
        request,
        "report/salesreport.html",
        {
            "suppliers": suppliers,
            "brands": brands,
            "dsrs": dsr,
            "sales_data": sales_data,
        },
    )


@login_required
def dsrsalesreport(request):
    suppliers = Supplier.objects.all()
    brands = Brand.objects.all()
    dsrs = Dsr.objects.all()
    sales_data = Sales.objects.all()

    if request.method == "GET":
        supplier_id = request.GET.get("supplier")
        brand_id = request.GET.get("brand")
        dsr_id = request.GET.get("dsr")
        from_date = request.GET.get("from-date")
        to_date = request.GET.get("to-date")

        if supplier_id:
            sales_data = sales_data.filter(product__supplier_id=supplier_id)
        if brand_id:
            sales_data = sales_data.filter(product__brand_id=brand_id)
        if dsr_id:
            sales_data = sales_data.filter(dsr_id=dsr_id)
        if from_date and to_date:
            sales_data = sales_data.filter(date__range=(from_date, to_date))

        sales_data = sales_data.values(
            "product__name", "product__size", "sell_price__price"
        ).annotate(
            total_qty=Sum("quantity"),
            total_product_price=Sum(F("quantity") * F("sell_price__price")),
        )

    total_sum = sales_data.aggregate(total_sum=Sum("total_product_price"))["total_sum"]

    return render(
        request,
        "report/dsrsalesreport.html",
        {
            "suppliers": suppliers,
            "brands": brands,
            "dsrs": dsrs,
            "sales_data": sales_data,
            "total_sum": total_sum,
        },
    )


@login_required
def salesreport(request):
    suppliers = Supplier.objects.all()
    brands = Brand.objects.all()
    dsr = Dsr.objects.all()
    market = Market.objects.all()
    sales_data = Sales.objects.all()
    return render(
        request,
        "report/salesreport.html",
        {
            "suppliers": suppliers,
            "brands": brands,
            "dsrs": dsr,
            "markets": market,
            "sales_data": sales_data,
        },
    )


@login_required
def market_salesreport(request):
    suppliers = Supplier.objects.all()
    brands = Brand.objects.all()
    market = Market.objects.all()
    sales_data = Sales.objects.all()

    if request.method == "GET":
        supplier_id = request.GET.get("supplier")
        brand_id = request.GET.get("brand")
        market_id = request.GET.get("market")
        from_date = request.GET.get("from-date")
        to_date = request.GET.get("to-date")

        if supplier_id:
            sales_data = sales_data.filter(product__supplier_id=supplier_id)
        if brand_id:
            sales_data = sales_data.filter(product__brand_id=brand_id)
        if market_id:
            sales_data = sales_data.filter(market_id=market_id)
        if from_date and to_date:
            sales_data = sales_data.filter(date__range=(from_date, to_date))

        sales_data = sales_data.values(
            "product__name", "product__size", "sell_price__price"
        ).annotate(
            total_qty=Sum("quantity"),
            total_product_price=Sum(F("quantity") * F("sell_price__price")),
        )

    total_sum = sales_data.aggregate(total_sum=Sum("total_product_price"))["total_sum"]

    return render(
        request,
        "report/market_salesreport.html",
        {
            "suppliers": suppliers,
            "brands": brands,
            "market": market,
            "sales_data": sales_data,
            "total_sum": total_sum,
        },
    )


from django.db.models import Count


# damagereport  views Start.---------------------------------------------------------------------


@login_required
def damagereport(request):
    suppliers = Supplier.objects.all()
    brands = Brand.objects.all()
    if request.method == "POST":
        supplier_id = request.POST.get("supplier")
        brand_id = request.POST.get("brand")
        from_date = request.POST.get("from-date")
        to_date = request.POST.get("to-date")

        damage_data = (
            Damage.objects.filter(
                product__supplier_id=supplier_id,
                product__brand_id=brand_id,
                date__range=(from_date, to_date),
            )
            .values("date", "mem_number")
            .annotate(count=Count("id"))
        )

        serialized_damage_data = []
        for record in damage_data:
            serialized_record = {
                "date": str(record["date"]),
                "mem_number": record["mem_number"],
                "count": record["count"],
            }
            serialized_damage_data.append(serialized_record)

        request.session["filtered_damage_data"] = serialized_damage_data

        return redirect("damagereportwithinvoivce")

    return render(
        request, "report/damagereport.html", {"suppliers": suppliers, "brands": brands}
    )


@login_required
def damagereportwithinvoivce(request):
    damage_data = request.session.get("filtered_damage_data", [])
    return render(
        request, "report/damagereportwithinvoivce.html", {"damage_data": damage_data}
    )


@login_required
def damagewithtable(request, mem_number):
    damage_data_for_table = Damage.objects.filter(mem_number=mem_number)
    return render(
        request,
        "report/damagewithtable.html",
        {"damage_data_for_table": damage_data_for_table},
    )


@login_required
def damage_report_result(request):
    if request.method == "GET":
        supplier_id = request.GET.get("supplier")
        brand_id = request.GET.get("brand")
        from_date = request.GET.get("from-date")
        to_date = request.GET.get("to-date")

        damage_data = (
            Damage.objects.filter(
                product__supplier_id=supplier_id,
                product__brand_id=brand_id,
                date__range=(from_date, to_date),
            )
            .values("product__name", "product__size")
            .annotate(total_qty=Sum("qty"), total_value=Sum("purchase_amount"))
        )

        for damage in damage_data:
            try:
                damage["sales_rate"] = damage["total_value"] / damage["total_qty"]
            except (ValueError, ZeroDivisionError):
                damage["sales_rate"] = 0

        total_sum = damage_data.aggregate(total_sum=Sum("total_value"))["total_sum"]

        return render(
            request,
            "report/damagereportresult.html",
            {"damage_data": damage_data, "total_sum": total_sum},
        )
    else:
        return redirect("damagereport")


# supplier_ledger_report  views Start.---------------------------------------------------------------------


@login_required
def supplier_ledger_report(request):
    suppliers = Supplier.objects.all()
    return render(request, "report/supplierledgerreport.html", {"suppliers": suppliers})


from decimal import Decimal


@login_required
def supplier_ledger_result(request):
    if request.method == "POST":
        supplier_id = request.POST.get("supplier")
        from_date = request.POST.get("from-date")
        to_date = request.POST.get("to-date")

        liftings = Lifting.objects.filter(
            Q(date__range=(from_date, to_date)) & Q(product__supplier_id=supplier_id)
        ).order_by("date", "invoicing")
        supplier_payments = SupplierPayment.objects.filter(
            Q(date__range=(from_date, to_date)) & Q(supplier_id=supplier_id)
        )

        liftings_grouped = {}
        for key, group in groupby(liftings, lambda x: (x.date, x.invoicing)):
            liftings_grouped[key] = list(group)

        for lifting in liftings:
            lifting.invoice_total = sum(
                l.total_amount
                for l in liftings_grouped[(lifting.date, lifting.invoicing)]
            )
            lifting.previous_invoice = None

        prev_invoice = None
        combined_data = []
        for key, value in liftings_grouped.items():
            combined_data += value

        combined_data += supplier_payments
        combined_data.sort(key=attrgetter("date"))

        for item in combined_data:
            if item.item_type == "Lifting":
                item.previous_invoice = prev_invoice
                prev_invoice = item.invoicing

        total_invoice_taka = sum(l.total_amount for l in liftings)
        total_supplies_taka = Decimal(sum(float(p.amount) for p in supplier_payments))
        distance = total_invoice_taka - total_supplies_taka

        return render(
            request,
            "report/supplierledgerresult.html",
            {
                "combined_data": combined_data,
                "total_invoice_taka": total_invoice_taka,
                "total_supplies_taka": total_supplies_taka,
                "distance": distance,
            },
        )
    else:
        return redirect("supplierledgerreport")


@login_required
def profit_loss_report(request):
    suppliers = Supplier.objects.all()
    brands = Brand.objects.all()

    if request.method == "GET":
        supplier_id = request.GET.get("supplier")
        brand_id = request.GET.get("brand")
        from_date = request.GET.get("from-date")
        to_date = request.GET.get("to-date")

        if supplier_id and brand_id and from_date and to_date:
            return HttpResponseRedirect(
                reverse("profitlossreportresult")
                + f"?supplier={supplier_id}&brand={brand_id}&from-date={from_date}&to-date={to_date}"
            )

    return render(
        request,
        "report/profitlossreport.html",
        {"suppliers": suppliers, "brands": brands},
    )


# profit_loss_result  views Start.---------------------------------------------------------------------


@login_required
def profit_loss_result(request):
    supplier_id = request.GET.get("supplier")
    brand_id = request.GET.get("brand")
    from_date = request.GET.get("from-date")
    to_date = request.GET.get("to-date")

    latest_doprice_subquery = (
        Doprice.objects.filter(product_id=OuterRef("product_id"))
        .order_by("-added_on")
        .values("price")[:1]
    )

    sales = (
        Sales.objects.select_related("product")
        .filter(
            product__supplier_id=supplier_id,
            product__brand_id=brand_id,
            date__range=[from_date, to_date],
        )
        .values("product_id", "product__name", "product__size")
        .annotate(
            total_quantity=Sum("quantity"),
            purchase_price=Subquery(latest_doprice_subquery),
            sales_price=Avg("sell_price__price"),
            distance=ExpressionWrapper(
                Avg("sell_price__price") - F("purchase_price"),
                output_field=FloatField(),
            ),
            total_commission=Sum("total_commission"),
        )
        .annotate(
            profit=ExpressionWrapper(
                Case(
                    When(distance__gte=0, then=F("distance") * F("total_quantity")),
                    default=Cast(0, output_field=FloatField()),
                ),
                output_field=FloatField(),
            ),
            loss=ExpressionWrapper(
                Case(
                    When(distance__lt=0, then=F("distance") * F("total_quantity")),
                    default=Cast(0, output_field=FloatField()),
                ),
                output_field=FloatField(),
            ),
        )
    )

    total_profit = sum(sale["profit"] for sale in sales)
    total_loss = sum(sale["loss"] for sale in sales)
    total_commission = sum(sale["total_commission"] for sale in sales)
    net_profit = total_profit - (total_commission + total_loss)

    return render(
        request,
        "report/profitlossreportresult.html",
        {
            "sales": sales,
            "total_profit": total_profit,
            "total_loss": total_loss,
            "total_commission": total_commission,
            "net_profit": net_profit,
        },
    )


@login_required
def calculate_profit_loss_and_commission(sales):
    profit = 0
    loss = 0
    total_commission = 0

    for sale in sales:
        distance = sale.sell_price.price - sale.product.current_price
        amount = distance * sale.quantity
        total_commission += sale.total_commission

        if distance > 0:
            profit += amount
        else:
            loss += -amount

    return profit, loss, total_commission


# discountreport  views Start.---------------------------------------------------------------------


@login_required
def discountreport(request):
    suppliers = Supplier.objects.all()
    brand = Brand.objects.all()
    discount = Discountsetup.objects.all()

    if request.method == "POST":
        supplier_id = request.POST.get("supplier")
        brand_id = request.POST.get("brand")
        discount_id = request.POST.get("discount")
        from_date = request.POST.get("from-date")
        to_date = request.POST.get("to-date")

        filtered_acdiccounts = Acdiccount.objects.filter(
            Q(supplier_id=supplier_id)
            & Q(brand_id=brand_id)
            & Q(discount_id=discount_id)
            & Q(date__range=(from_date, to_date))
        )

        total_amount = filtered_acdiccounts.aggregate(Sum("amount"))["amount__sum"]

        return render(
            request,
            "report/discountreportresult.html",
            {"acdiccounts": filtered_acdiccounts, "total_amount": total_amount},
        )
    else:
        return render(
            request,
            "report/discountreport.html",
            {"suppliers": suppliers, "brands": brand, "discount": discount},
        )


@login_required
def discountreportresult(request):
    return render(request, "report/discountreportresult.html")


# costreport  views Start.---------------------------------------------------------------------


@login_required
def costreport(request):
    dsrs = Dsr.objects.all()

    if request.method == "POST":
        dsr_id = request.POST.get("dsr")
        from_date = request.POST.get("from-date")
        to_date = request.POST.get("to-date")

        filtered_dailycost = Dailycost.objects.filter(
            Q(dsr_id=dsr_id) & Q(date__range=(from_date, to_date))
        )

        total_car_cost = filtered_dailycost.aggregate(Sum("carcost"))["carcost__sum"]
        total_dsr_bill = filtered_dailycost.aggregate(Sum("dsrbill"))["dsrbill__sum"]
        total_toll = filtered_dailycost.aggregate(Sum("toll"))["toll__sum"]
        total_other_cost = filtered_dailycost.aggregate(Sum("othercost"))[
            "othercost__sum"
        ]

        return render(
            request,
            "report/costreportresult.html",
            {
                "dsrs": dsrs,
                "dailycost": filtered_dailycost,
                "total_car_cost": total_car_cost,
                "total_dsr_bill": total_dsr_bill,
                "total_toll": total_toll,
                "total_other_cost": total_other_cost,
            },
        )
    else:
        return render(request, "report/costreport.html", {"dsrs": dsrs})


@login_required
def costreportresult(request):
    return render(request, "report/costreportresult.html")


# dsrsalesreportinvoice  views Start.---------------------------------------------------------------------


@login_required
def dsrsalesreportinvoice(request):
    supplier_id = request.GET.get("supplier")
    brand_id = request.GET.get("brand")
    dsr_id = request.GET.get("dsr")
    from_date = request.GET.get("from-date")
    to_date = request.GET.get("to-date")

    sales_data = Sales.objects.filter(
        Q(product__supplier_id=supplier_id) | Q(product__brand_id=brand_id),
        dsr_id=dsr_id,
        date__range=(from_date, to_date),
    )

    return render(
        request, "report/dsrsalesreportinvoice.html", {"sales_data": sales_data}
    )


# statement  views Start.---------------------------------------------------------------------


@login_required
def statement(request):
    collection_men = Collectionsetup.objects.all()
    return render(request, "report/statement.html", {"collection_men": collection_men})


from django.shortcuts import render, get_object_or_404


@login_required
def statementreportresult(request):
    if request.method == "POST":
        collection_man_id = request.POST.get("collection-man")
        from_date = request.POST.get("from-date")
        to_date = request.POST.get("to-date")

        collection_man = get_object_or_404(Collectionsetup, id=collection_man_id)
        transactions = CollectionTransaction.objects.filter(
            collection_man=collection_man, date__range=(from_date, to_date)
        )

        return render(
            request, "report/statementreportresult.html", {"transactions": transactions}
        )

    return render(request, "report/statementreportresult.html")


@login_required
def statementreportresultall(request):
    if request.method == "POST":
        from_date = request.POST.get("from-date")
        to_date = request.POST.get("to-date")

        collection_men = Collectionsetup.objects.all()

        collection_balances = {}

        for collection_man in collection_men:
            transactions = CollectionTransaction.objects.filter(
                collection_man=collection_man, date__range=(from_date, to_date)
            )

            balance = Decimal("0.00")
            for transaction in transactions:
                if transaction.transaction_type == "deposit":
                    balance += transaction.amount
                else:
                    balance -= transaction.amount

            collection_balances[collection_man] = balance

        return render(
            request,
            "report/statementreportresultall.html",
            {"collection_balances": collection_balances},
        )

    return render(request, "report/statementreportresultall.html")


# searchkg  views Start.---------------------------------------------------------------------


@login_required
def searchkg(request):
    if request.GET.get("search"):
        request.session["supplier_id"] = request.GET.get("supplier")
        request.session["brand_id"] = request.GET.get("brand")
        request.session["from_date"] = request.GET.get("from-date")
        request.session["to_date"] = request.GET.get("to-date")
        return redirect("findkg")
    suppliers = Supplier.objects.all()
    brands = Brand.objects.all()
    return render(
        request, "report/searchkg.html", {"suppliers": suppliers, "brands": brands}
    )


from django.db.models import Sum


@login_required
def findkg(request):
    supplier_id = request.session.get("supplier_id")
    brand_id = request.session.get("brand_id")
    from_date = request.session.get("from_date")
    to_date = request.session.get("to_date")

    lift_records = Lifting.objects.filter(
        product__supplier_id=supplier_id,
        product__brand_id=brand_id,
        date__range=[from_date, to_date],
    )

    unique_products = lift_records.values("product").distinct()

    product_data = []

    for product in unique_products:
        product_obj = Product.objects.get(id=product["product"])

        total_lifting_qty = (
            lift_records.filter(product=product["product"]).aggregate(Sum("quantity"))[
                "quantity__sum"
            ]
            or 0
        )

        grams = GramSetup.objects.filter(product=product_obj).first()

        if grams:
            set_grams = grams.grams
            total_grams = grams.grams * total_lifting_qty
            total_kg = total_grams / 1000
        else:
            set_grams = 0
            total_grams = 0
            total_kg = 0

        product_data.append(
            {
                "serial_no": ...,
                "product_name": product_obj.name,
                "product_size": product_obj.size,
                "total_lifting_qty": total_lifting_qty,
                "set_grams": set_grams,
                "grams": total_grams,
                "kg": total_kg,
            }
        )

    return render(request, "report/findkg.html", {"product_data": product_data})


# assetview  views Start.---------------------------------------------------------------------


@login_required
def assetview(request):
    return render(request, "report/assetview.html")


@login_required
def assetviewrs(request):
    if request.method == "GET":
        from_date = request.GET.get("from-date")
        to_date = request.GET.get("to-date")

        transactions = Assets.objects.filter(date__range=[from_date, to_date])

        return render(
            request, "report/assetviewrs.html", {"transactions": transactions}
        )

    return render(request, "report/assetviewrs.html")
