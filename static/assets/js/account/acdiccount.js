document.addEventListener('DOMContentLoaded', function () {
    const supplierDropdown = document.getElementById('supplier');
    const brandDropdown = document.getElementById('brand');
    const discountDropdown = document.getElementById('discount');

    function filterDiscounts() {
        const selectedSupplier = supplierDropdown.value;
        const selectedBrand = brandDropdown.value;

        const allOptions = discountDropdown.querySelectorAll('option');
        let visibleOptions = 0;

        allOptions.forEach(option => {
            const optionSupplier = option.getAttribute('data-supplier');
            const optionBrand = option.getAttribute('data-brand');

            if (optionSupplier === selectedSupplier && optionBrand === selectedBrand) {
                option.style.display = 'block';
                visibleOptions++;
            } else {
                option.style.display = 'none';
            }
        });

        if (visibleOptions === 0) {
            discountDropdown.value = "";
            discountDropdown.disabled = true;
        } else {
            discountDropdown.disabled = false;
        }
    }

    supplierDropdown.addEventListener('change', filterDiscounts);
    brandDropdown.addEventListener('change', filterDiscounts);

    filterDiscounts();  // Call once to initialize the filtering
});