document.addEventListener('DOMContentLoaded', () => {
    const expenseForm = document.getElementById('expense-form');
    const expenseTableBody = document.getElementById('expense-table-body');
    const budgetInput = document.getElementById('budget-input');
    const setBudgetBtn = document.getElementById('set-budget-btn');
    const budgetStatus = document.getElementById('budget-status');

    // Load expenses initially
    loadExpenses();
    trackBudget();

    // Add Expense Form submission
    expenseForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const expense = {
            date: document.getElementById('date').value,
            category: document.getElementById('category').value,
            amount: document.getElementById('amount').value,
            description: document.getElementById('description').value
        };
        await fetch('/add_expense', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(expense)
        });
        expenseForm.reset();
        loadExpenses();
        trackBudget();
    });

    // Set Budget
    setBudgetBtn.addEventListener('click', async () => {
        const budget = budgetInput.value;
        await fetch('/set_budget', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({budget})
        });
        trackBudget();
    });

    // Load expenses function
    async function loadExpenses() {
        const response = await fetch('/expenses');
        const data = await response.json();
        expenseTableBody.innerHTML = '';
        data.forEach(exp => {
            expenseTableBody.innerHTML += `
                <tr>
                    <td>${exp.date}</td>
                    <td>${exp.category}</td>
                    <td>${exp.amount.toFixed(2)}</td>
                    <td>${exp.description}</td>
                </tr>
            `;
        });
    }

    // Track budget function
    async function trackBudget() {
        const response = await fetch('/track_budget');
        const data = await response.json();
        budgetStatus.textContent = `Budget: ${data.budget.toFixed(2)}, Spent: ${data.total_expenses.toFixed(2)}, Remaining: ${data.remaining.toFixed(2)}`;
        budgetStatus.className = data.status === 'over_budget' ? 'text-danger' : 'text-success';
    }
});