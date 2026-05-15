const calculateDiscount = require('./discount');

test('Premium Customer gets 20% discount', () => {
    expect(calculateDiscount(1000, 'premium')).toBe(800);
});

test('Regular Customer gets 10% discount', () => {
    expect(calculateDiscount(1000, 'regular')).toBe(900);
});

test('Guest Customer gets no discount', () => {
    expect(calculateDiscount(1000, 'guest')).toBe(1000);
});

test('negative price return error message', () => {
    expect(calculateDiscount(-1000, 'regular')).toBe("Invalid Price");
});