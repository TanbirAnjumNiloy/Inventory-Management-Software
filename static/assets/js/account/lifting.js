function pro_checkall() {
    var items = document.getElementsByClassName("checkbox-item");
    var master = document.getElementById("master-checkbox");
    for (var i = 0; i < items.length; i++) {
      items[i].checked = master.checked;
    }
  }
    function calculateTotalAmount(productId) {
      const qtyInput = document.getElementsByName(productId + '_qty')[0];
      const priceInput = document.getElementById(productId + '_price');
      const totalInput = document.getElementById(productId + '_total');
  
      const qty = qtyInput.value;
      const price = priceInput.value;
      const total = qty * price;
  
      totalInput.value = total;
    }

    const checkCheckbox = (event) => {
      const id = event.target.name.split("_")[0];
      const checkbox = document.querySelector(`input[name="product_ids[]"][value="${id}"]`);
      checkbox.checked = true;
    };
  
    document.addEventListener("DOMContentLoaded", function () {
      const quantities = Array.from(document.querySelectorAll("input[type='number'][name$='_qty']"));
  
      quantities.forEach((quantity) => {
        quantity.addEventListener("click", checkCheckbox);
      });
    });