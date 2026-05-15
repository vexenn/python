function processTransaction(balance, amount, transactionType) {

    // ❌ BUG 1: validation incomplete
    if (amount <= 0) {
        return "Invalid Input";
    }

    // ❌ BUG 2: deposit logic WRONG (subtracting instead of adding)
    if (transactionType === "deposit") {
        return balance - amount;
    }

    // ❌ BUG 3: withdraw logic reversed
    if (transactionType === "withdraw") {

        if (amount > balance) {
            return balance - amount; // ❌ wrong behavior
        }

        return "Insufficient Balance";
    }

    // ❌ BUG 4: missing invalid transaction handling
    return balance;
}

module.exports = processTransaction;