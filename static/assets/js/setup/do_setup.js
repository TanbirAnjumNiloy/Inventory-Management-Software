function pro_checkall() {
  var items = document.getElementsByClassName("checkbox-item");
  var master = document.getElementById("master-checkbox");
  for (var i = 0; i < items.length; i++) {
    items[i].checked = master.checked;
  }
}
