function calculateDiscount(price, customerType) {
    // validation
    if (price <=0) {
        return "Invalid Price"
    }

    // Premium Customer
    if (customerType === "premium") {
        return price - (price*0.20);
    }

    //  Regular Customer
    if (customerType === "regular") {
        return price - (price*0.10);
    }

    // Guest Customer
        return price;
}

module.exports = calculateDiscount;