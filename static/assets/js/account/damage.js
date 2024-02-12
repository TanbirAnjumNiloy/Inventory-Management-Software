function pro_checkall() {
    var items = document.getElementsByClassName("checkbox-item");
    var master = document.getElementById("master-checkbox");
    for (var i = 0; i < items.length; i++) {
      items[i].checked = master.checked;
    }
  }
  
  // Add this script inside your <script> tag
  document.addEventListener("DOMContentLoaded", function () {
    const products = Array.from(document.querySelectorAll("[id^='qty_']"));
    products.forEach((product) => {
      product.addEventListener("input", function (event) {
        const id = event.target.id.split("_")[1];
        const qty = parseFloat(event.target.value);
        const sellPriceInput = document.getElementById(`sell_price_${id}`);
        const purchasePriceInput = document.getElementById(`${id}_price`);
        const salesAmountInput = document.getElementById(`sales_amount_${id}`);
        const purchaseAmountInput = document.getElementById(`purchase_amount_${id}`);

        
        if (!isNaN(qty)) {
          const sellPrice = parseFloat(sellPriceInput.value);
          const purchasePrice = parseFloat(purchasePriceInput.value);
          const salesAmount = qty * sellPrice;
          const purchaseAmount = qty * purchasePrice;
          
          salesAmountInput.value = salesAmount.toFixed(2);
          purchaseAmountInput.value = purchaseAmount.toFixed(2);
        } else {
          salesAmountInput.value = "";
          purchaseAmountInput.value = "";
        }
      });
    });
  });
  
  function pro_checkall() {
  var items = document.getElementsByClassName("checkbox-item");
  var master = document.getElementById("master-checkbox");
  for (var i = 0; i < items.length; i++) {
    items[i].checked = master.checked;
  }
}

// Add this script inside your <script> tag
document.addEventListener("DOMContentLoaded", function () {
  const products = Array.from(document.querySelectorAll("[id^='qty_']"));
  products.forEach((product) => {
    product.addEventListener("input", function (event) {
      const id = event.target.id.split("_")[1];
      const qty = parseFloat(event.target.value);
      const sellPriceInput = document.getElementById(`sell_price_${id}`);
      const purchasePriceInput = document.getElementById(`${id}_price`);
      const salesAmountInput = document.getElementById(`sales_amount_${id}`);
      const purchaseAmountInput = document.getElementById(`purchase_amount_${id}`);
      const checkbox = document.querySelector(`[name="product_ids[]"][value="${id}"]`);

      if (!isNaN(qty)) {
        const sellPrice = parseFloat(sellPriceInput.value);
        const purchasePrice = parseFloat(purchasePriceInput.value);
        const salesAmount = qty * sellPrice;
        const purchaseAmount = qty * purchasePrice;

        salesAmountInput.value = salesAmount.toFixed(2);
        purchaseAmountInput.value = purchaseAmount.toFixed(2);
        
        if (qty > 0) {
          checkbox.checked = true;
        } else {
          checkbox.checked = false;
        }
      } else {
        salesAmountInput.value = "";
        purchaseAmountInput.value = "";
        checkbox.checked = false;
      }
    });
  });
});