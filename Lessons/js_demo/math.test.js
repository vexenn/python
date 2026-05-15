const sum = require('./math');

test('adds 2 + 3 to equal 5', () => {
    expect(sum(2, 3)).toBe(5);
});

test('positive numbers', () => {
    expect(sum(2, 3)).toBe(5);
});

test('negative numbers', () => {
    expect(sum(-2, -3)).toBe(-5);
});

test('zero values', () => {
    expect(sum(0, 0)).toBe(0);
});