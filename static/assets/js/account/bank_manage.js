function updateBankNameAndAccountNumber() {
    const branchSelect = document.getElementById('branch');
    const bankNameSelect = document.getElementById('bank_name');
    const accountNumberSelect = document.getElementById('account_number');
    const currentBalanceInput = document.getElementById('current_balance');

    const selectedBank = branchSelect.options[branchSelect.selectedIndex];
    const bankName = selectedBank.getAttribute('data-bank-name');
    const accountNumber = selectedBank.getAttribute('data-account-no');
    const currentBalance = selectedBank.getAttribute('data-current-balance');

    bankNameSelect.value = bankName;
    accountNumberSelect.value = accountNumber;
    currentBalanceInput.value = currentBalance;
}