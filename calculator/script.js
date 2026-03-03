class Calculator {
    constructor(previousOperandElement, currentOperandElement) {
        this.previousOperandElement = previousOperandElement;
        this.currentOperandElement = currentOperandElement;
        this.clear();
    }

    clear() {
        this.currentOperand = '0';
        this.previousOperand = '';
        this.operation = undefined;
    }

    delete() {
        if (this.currentOperand === '0') return;
        this.currentOperand = this.currentOperand.toString().slice(0, -1) || '0';
    }

    appendNumber(number) {
        if (number === '.' && this.currentOperand.includes('.')) return;
        if (this.currentOperand === '0' && number !== '.') {
            this.currentOperand = number.toString();
        } else {
            this.currentOperand = this.currentOperand.toString() + number.toString();
        }
    }

    chooseOperation(operation) {
        if (this.currentOperand === '') return;
        if (this.previousOperand !== '') this.compute();
        this.operation = operation;
        this.previousOperand = this.currentOperand;
        this.currentOperand = '';
    }

    compute() {
        let computation;
        const prev = parseFloat(this.previousOperand);
        const current = parseFloat(this.currentOperand);
        if (isNaN(prev) || isNaN(current)) return;

        switch (this.operation) {
            case '+': computation = prev + current; break;
            case '-': computation = prev - current; break;
            case '*': computation = prev * current; break;
            case '÷': 
                computation = current === 0 ? 'Error' : prev / current; 
                break;
            default: return;
        }
        this.currentOperand = computation;
        this.operation = undefined;
        this.previousOperand = '';
    }

    updateDisplay() {
        this.currentOperandElement.innerText = this.currentOperand;
        this.previousOperandElement.innerText = this.operation 
            ? `${this.previousOperand} ${this.operation}` 
            : '';
    }
}

// --- Initialization & Event Delegation ---
const calculator = new Calculator(
    document.querySelector('[data-previous-operand]'),
    document.querySelector('[data-current-operand]')
);

document.getElementById('calculator').addEventListener('click', e => {
    const btn = e.target;
    if (btn.hasAttribute('data-number')) {
        calculator.appendNumber(btn.innerText);
    } else if (btn.hasAttribute('data-operation')) {
        calculator.chooseOperation(btn.innerText);
    } else if (btn.hasAttribute('data-equals')) {
        calculator.compute();
    } else if (btn.hasAttribute('data-all-clear')) {
        calculator.clear();
    } else if (btn.hasAttribute('data-delete')) {
        calculator.delete();
    }
    calculator.updateDisplay();
});

// Keyboard Support
window.addEventListener('keydown', e => {
    if ((e.key >= 0 && e.key <= 9) || e.key === '.') calculator.appendNumber(e.key);
    if (e.key === '=' || e.key === 'Enter') calculator.compute();
    if (e.key === 'Backspace') calculator.delete();
    if (e.key === 'Escape') calculator.clear();
    if (['+', '-', '*', '/'].includes(e.key)) {
        const op = e.key === '/' ? '÷' : e.key;
        calculator.chooseOperation(op);
    }
    calculator.updateDisplay();
});