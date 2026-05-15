import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Personal Expense Tracker", layout="wide")

if "transactions" not in st.session_state:
    st.session_state.transactions = []

st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go To",
    ["Home", "Add Transaction", "View Transactions", "Summary"]
)

if page == "Home":

    st.title("Personal Expense Tracker")

    st.write("""
    This application helps users:

    - Track income and expenses
    - View transaction history
    - Calculate balance
    - Analyze spending categories
    """)

elif page == "Add Transaction":

    st.title("Add Transaction")

    transaction_type = st.selectbox(
        "Transaction Type",
        ["Income", "Expense"]
    )

    if transaction_type == "Income":
        category = st.text_input("Income Source")
    else:
        category = st.selectbox(
            "Expense Category",
            [
                "Food",
                "Travel",
                "Shopping",
                "Bills",
                "Education",
                "Medical",
                "Others"
            ]
        )

    amount = st.number_input(
        "Amount",
        min_value=0.0,
        format="%.2f"
    )

    date = st.date_input("Date", date.today())

    if st.button("Add Transaction"):
        transaction = {
            "Type": transaction_type,
            "Category": category,
            "Amount": amount,
            "Date": str(date)
        }

        st.session_state.transactions.append(transaction)

        st.success("Transaction Added Successfully!")

elif page == "View Transactions":
    st.title("📋 Transaction History")

    if st.session_state.transactions:
        df = pd.DataFrame(st.session_state.transactions)

        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No transactions available.")

elif page == "Summary":
    st.title("📊 Financial Summary")

    if st.session_state.transactions:
        df = pd.DataFrame(st.session_state.transactions)

        total_income = df[df['Type'] == 'Income']['Amount'].sum()
        total_expense = df[df['Type'] == 'Expense']['Amount'].sum()
        balance = total_income - total_expense

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Income", f"₹ {total_income:.2f}")
        col2.metric("Total Expenses", f"₹ {total_expense:.2f}")
        col3.metric("Balance", f"₹ {balance:.2f}")

        st.subheader("Category-wise Expense Summary")
        expense_df = df[df['Type'] == 'Expense']

        if not expense_df.empty:
            category_summary = expense_df.groupby('Category')['Amount'].sum()
            st.bar_chart(category_summary)
            st.dataframe(category_summary)
        else:
            st.info("No expense data available.")
    else:
        st.warning("No transactions available.")