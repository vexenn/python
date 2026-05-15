function processTransaction(balance, amount, transactionType) {

    // Validation
    if (balance < 0 || amount <= 0) {
        return "Invalid Input";
    }

    // Deposit
    if (transactionType === "deposit") {
        return balance + amount;
    }

    // Withdraw
    if (transactionType === "withdraw") {

        if (amount > balance) {
            return "Insufficient Balance";
        }

        return balance - amount;
    }

    return "Invalid Transaction Type";
}

module.exports = processTransaction;