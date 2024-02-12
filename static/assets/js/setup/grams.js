function pro_checkall() {
    var items = document.getElementsByClassName("checkbox-item");
    var master = document.getElementById("master-checkbox");
    for (var i = 0; i < items.length; i++) {
      items[i].checked = master.checked;
    }
  }

  
  function addClickListenerToGramsInputs() {
    
    var gramsInputs = document.querySelectorAll('input[type="number"].input');
    gramsInputs.forEach(function(input) {
      
      input.addEventListener('click', function() {
      
        var parentRow = this.closest('tr');
        if (parentRow) {
          
          var checkbox = parentRow.querySelector('input[type="checkbox"].checkbox-item');
          if (checkbox) {
            checkbox.checked = true;
          }
        }
      });
    });
  }

  
  document.addEventListener('DOMContentLoaded', addClickListenerToGramsInputs);