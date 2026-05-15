const processTransaction = require('./transaction_buggy'); // or './transaction_buggy'

describe('processTransaction Logic', () => {
    
    // --- Happy Path Tests ---
    test('should successfully add a deposit to the balance', () => {
        expect(processTransaction(1000, 500, 'deposit')).toBe(1500);
    });

    test('should successfully subtract a withdrawl from the balance', () => {
        expect(processTransaction(1000, 400, 'withdraw')).toBe(600);
    });

    //  --- Validation & Edge Cases ---
    test('Should return "Invalid Input" if amount is zero or negative', () => {
        expect(processTransaction(1000, 0, 'deposit')).toBe("Invalid Input");
        expect(processTransaction(1000, -50, 'deposit')).toBe("Invalid Input");
    });
    
    test('should return "Invalid Input" if initial balance is negative', () => {
        expect(processTransaction(-100, 50, 'deposit')).toBe("Invalid Input");
    });

    //  --- Business Logic Constraints ---
    test('should return "Insufficient Balance" if withdrawal exceeds balance', () => {
        expect(processTransaction(100, 500, 'withdraw')).toBe("Insufficient Balance");
    });

    test('Should return "Invalid Transaction Type" for unknown types', () => {
        expect(processTransaction(1000, 100, 'crypto')).toBe("Invalid Transaction Type");
    });

});