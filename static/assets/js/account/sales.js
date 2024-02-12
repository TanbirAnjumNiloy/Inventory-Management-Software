
function updateQty(productId) {
    var acceptInput = document.getElementById("accept_" + productId);
    var returnInput = document.getElementById("return_" + productId);
    var qtyInput = document.getElementById("qty_" + productId);
    var stockInput = document.getElementById("total_qty_" + productId);
    var sellPriceInput = document.getElementById("sell_price_" + productId);
    var amountInput = document.getElementById("amount_" + productId);
    var totalCommissionInput = document.getElementById("total_commission_" + productId);
    var currentStockInput = document.getElementById("current_stock_" + productId);

    var acceptValue = parseFloat(acceptInput.value) || 0;
    var returnValue = parseFloat(returnInput.value) || 0;
    var stockValue = parseFloat(stockInput.value) || 0;
    var sellPrice = parseFloat(sellPriceInput.value) || 0;
  

    var qty = acceptValue - returnValue;
  

    qty = qty < 0 ? 0 : qty;
  

    qtyInput.value = qty;
  
   
    var amount = qty * sellPrice;
    amountInput.value = amount.toFixed(2);
  

    var commissionInput = document.getElementById("commission_" + productId);
    var commission = parseFloat(commissionInput.value) || 0;
    var totalCommission = qty * commission;
    totalCommissionInput.value = totalCommission.toFixed(2);
  
 
    var currentStock = stockValue - qty;
    currentStockInput.value = currentStock.toFixed(2);
  
  
    if (qty > stockValue) {
      acceptInput.value = ""; 
      acceptInput.disabled = true;
    } else {
      acceptInput.disabled = false;
    }
  }
  
 
  function checkCheckbox(productId) {
    var acceptValue = parseFloat(document.getElementById("accept_" + productId).value) || 0;
    var checkbox = document.getElementById("checkbox_" + productId);
  

    checkbox.checked = acceptValue > 0;
  }
  

  {% for product in products %}
  document.getElementById("accept_{{ product.id }}").addEventListener("input", function () {
    updateQty({{ product.id }});
    checkCheckbox({{ product.id }});
  });
  
  document.getElementById("return_{{ product.id }}").addEventListener("input", function () {
    updateQty({{ product.id }});
  });
  
  {% endfor %}