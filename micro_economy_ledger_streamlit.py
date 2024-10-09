from dataclasses import dataclass, field
from typing import List, Dict, Generator
from decimal import Decimal
import datetime

# ----------------------------------------------------------------------
@dataclass
class Entry:
    description: str
    amount: Decimal

@dataclass
class Transaction:
    date: str
    description: str
    entries: List[Entry] = field(default_factory=list)

@dataclass
class Ledger:
    transactions: List[Transaction] = field(default_factory=list)

    def entries(self) -> Generator[Entry, None, None]:
        return (
            entry 
            for transaction in self.transactions 
            for entry       in transaction.entries)
    
    def display_balance(self):
        for entry in self.entries():
            print(f"{entry.description}: {entry.amount}")
# ----------------------------------------------------------------------
# actions
# ----------------------------------------------------------------------
def get_substrings(input_str: str) -> List[str]:
    result = []
    parts = input_str.split(':')
    for i in range(len(parts), 0, -1):
        result.append(':'.join(parts[:i]))
    return result

def dig_for_gold(ledger: Ledger, date: str, name: str, amount: Decimal):
    ledger.transactions.append(Transaction(
        date=date,
        description=f"dig for gold: {name}",
        entries=[
            Entry(description=f"{name}:assets:gold", amount=amount),
            # Entry(description=f"{name}:equity", amount=-amount)
            Entry(description=f"{name}:equity:mining", amount=-amount)
        ]
    ))

def grow_apples(ledger: Ledger, date: str, name: str, amount: Decimal):
    ledger.transactions.append(Transaction(
        date=date,
        description=f"grow_apples: {name}",
        entries=[
            Entry(description=f"{name}:assets:apples", amount=amount),
            # Entry(description=f"{name}:equity", amount=-amount)
            Entry(description=f"{name}:equity:farming", amount=-amount)
        ]
    ))

def buy_treasury_securities(ledger: Ledger, date: str, name: str, amount: Decimal):
    ledger.transactions.append(Transaction(
        date=date,
        description=f"buy_treasury_securities: {name}",
        entries=[
            # Entry(description=f"{name}:assets:treasury_securities", amount=amount),
            Entry(f'{name}:assets:gold',              -amount),
            Entry(f'fed:liabilities:tga:assets:gold',  amount),

            Entry(f'{name}:assets:securities',                    amount),
            Entry(f'fed:liabilities:tga:liabilities:securities', -amount)
            
        ]
    ))

def barter(ledger: Ledger, date: str, name_a: str, name_b: str, asset_a: str, asset_b: str, amount: Decimal, check=True):

    if check:

        asset_a_available = sum(
            entry.amount 
            for entry in ledger.entries() 
            if entry.description == f"{name_a}:assets:{asset_a}")

        asset_b_available = sum(
            entry.amount
            for entry in ledger.entries()
            if entry.description == f"{name_b}:assets:{asset_b}")

        if asset_a_available < amount:
            st.info(f"Insufficient {asset_a}")
            return
        
        if asset_b_available < amount:
            st.info(f"Insufficient {asset_b}")
            return

    ledger.transactions.append(Transaction(
        date=date,
        description=f"barter: {name_a} {asset_a} <-> {name_b} {asset_b}",
        entries=[
            Entry(description=f"{name_a}:assets:{asset_a}", amount=-amount),
            Entry(description=f"{name_b}:assets:{asset_a}", amount=amount),
            Entry(description=f"{name_a}:assets:{asset_b}", amount=amount),
            Entry(description=f"{name_b}:assets:{asset_b}", amount=-amount)
        ]
    ))

def deposit_gold(ledger: Ledger, date: str, person: str, bank: str, amount: Decimal):
    
    gold = sum(
        entry.amount
        for entry in ledger.entries()
        if entry.description == f"{person}:assets:gold"
    )
    
    if amount > gold:
        print("Insufficient gold")
        return

    ledger.transactions.append(Transaction(
        date=date,
        description=f"deposit_gold: {person} -> {bank}",
        entries=[
            Entry(description=f"{person}:assets:gold", amount=-amount),
            Entry(description=f"{person}:assets:deposits:{bank}", amount=amount),
            Entry(description=f"{bank}:assets:reserves:gold", amount=amount),
            Entry(description=f"{bank}:liabilities:deposits:{person}", amount=-amount)
        ]
    ))

def deposit_cash(ledger: Ledger, date: str, person: str, bank: str, amount: Decimal):
    
    cash = sum(
        entry.amount
        for entry in ledger.entries()
        if entry.description == f"{person}:assets:cash"
    )
    
    if amount > cash:
        print("Insufficient cash")
        return

    ledger.transactions.append(Transaction(
        date=date,
        description=f"deposit_cash: {person} -> {bank}   ${amount}",
        entries=[
            Entry(description=f"{person}:assets:cash", amount=-amount),
            Entry(description=f"{person}:assets:deposits:{bank}", amount=amount),
            Entry(description=f"{bank}:assets:reserves:cash", amount=amount),
            Entry(description=f"{bank}:liabilities:deposits:{person}", amount=-amount)
        ]
    ))

# Standalone variable (previously field in Utils)
reserve_ratio: Decimal = Decimal('0.1')

# get_loan : cash version

# def get_loan(ledger: Ledger, date: str, person: str, bank: str, amount: Decimal):
    
#     reserves = sum(entry.amount for entry in ledger.entries() if entry.description.startswith(f"{bank}:assets:reserves"))
#     deposits = sum(entry.amount for entry in ledger.entries() if entry.description.startswith(f"{bank}:liabilities:deposits"))
    
#     minimum_reserves = deposits * reserve_ratio
#     proposed_reserves = reserves - amount

#     # available_for_loan = reserves - minimum_reserves

#     # print(f"minimum_reserves: {minimum_reserves}")
#     # print(f"proposed_reserves: {proposed_reserves}")
    
#     if proposed_reserves < minimum_reserves:
#         print("Insufficient reserves")
#         return

#     ledger.transactions.append(Transaction(
#         date=date,
#         description=f"get_loan: {person} <- {bank}",
#         entries=[
#             Entry(description=f"{person}:assets:cash", amount=amount),
#             Entry(description=f"{person}:liabilities:loans:{bank}", amount=-amount),
#             Entry(description=f"{bank}:assets:reserves", amount=-amount),
#             Entry(description=f"{bank}:assets:loans", amount=amount)
#         ]
#     ))

def get_loan(ledger: Ledger, date: str, person: str, bank: str, amount: Decimal):
    
    reserves = sum(entry.amount for entry in ledger.entries() if entry.description.startswith(f"{bank}:assets:reserves"))
    deposits = sum(entry.amount for entry in ledger.entries() if entry.description.startswith(f"{bank}:liabilities:deposits"))
    
    minimum_reserves = deposits * reserve_ratio
    proposed_reserves = reserves - amount

    # available_for_loan = reserves - minimum_reserves

    # print(f"minimum_reserves: {minimum_reserves}")
    # print(f"proposed_reserves: {proposed_reserves}")
    
    if proposed_reserves < minimum_reserves:
        print("Insufficient reserves")
        return

    ledger.transactions.append(Transaction(
        date=date,
        description=f"get_loan: {person} <- {bank}",
        entries=[
            Entry(description=f"{person}:assets:gold", amount=amount),
            Entry(description=f"{person}:liabilities:loans:{bank}", amount=-amount),
            Entry(description=f"{bank}:assets:reserves:gold", amount=-amount),
            Entry(description=f"{bank}:assets:loans", amount=amount)
        ]
    ))




# ----------------------------------------------------------------------
# display
# ----------------------------------------------------------------------
def deep_clone_ledger(ledger: Ledger) -> Ledger:
    return Ledger(transactions=[
        Transaction(
            date=transaction.date,
            description=transaction.description,
            entries=[Entry(description=entry.description, amount=entry.amount) for entry in transaction.entries]
        ) for transaction in ledger.transactions
    ])

def display_balances(ledger: Ledger):
        
    entries = ledger.entries()

    categories = sorted(set(substring for entry in entries for substring in get_substrings(entry.description)))
    
    for category in categories:
        total = sum(entry.amount for entry in entries if entry.description.startswith(category))
        print(f"{category}: {total}")

def transform_description(description: str) -> str:
    parts = description.split(':')
    category = parts[-2] if parts[-1] == '' else parts[-1]
    indent_level = len(parts) - 2 if parts[-1] == '' else len(parts) - 1
    # indent = '    ' * indent_level
    indent = '  ' * indent_level
    # indent = '____' * indent_level
    return f"{indent}{category}"

# transform_description("person_a:")

# Example usage:
# print(transform_description("person_a:assets:"))  # "    assets:"
# print(transform_description("person_a:assets:gold:"))  # "        gold:"
# print(transform_description("bank_a:assets:reserves:gold:"))  # "            gold:"        

# def display_balances_with_changes(ledger_a: Ledger, ledger_b: Ledger):
    
#     entries_a = list(ledger_a.entries())
#     entries_b = list(ledger_b.entries())
        
#     categories = sorted(
#         set(
#             substring 
#             for entries in [entries_a, entries_b] 
#             for entry in entries 
#             for substring in get_substrings(entry.description)
#         )
#     )
    
#     for category in categories:
#         total_a = sum(entry.amount for entry in entries_a if entry.description.startswith(category))
#         total_b = sum(entry.amount for entry in entries_b if entry.description.startswith(category))

#         # category = transform_description(category)
        
#         if total_a != total_b:
#             diff = total_b - total_a
#             color = "green" if diff > 0 else "red"  # Green for positive, Red for negative
#             st.write(f"{category}: {total_b} :{color}-background[{diff:+.2f}]")
#         else:
#             st.write(f"{category}: {total_b}")




# def display_balances_with_changes(ledger_a: Ledger, ledger_b: Ledger):
    
#     entries_a = list(ledger_a.entries())
#     entries_b = list(ledger_b.entries())
        
#     categories = sorted(
#         set(
#             substring 
#             for entries in [entries_a, entries_b] 
#             for entry in entries 
#             for substring in get_substrings(entry.description)
#         )
#     )

#     output = ""

#     max_category_length = max(len(category) for category in categories)
    
#     for category in categories:
#         total_a = sum(entry.amount for entry in entries_a if entry.description.startswith(category))
#         total_b = sum(entry.amount for entry in entries_b if entry.description.startswith(category))

#         # category = transform_description(category)
        
#         if total_a != total_b:
#             diff = total_b - total_a
#             color = "green" if diff > 0 else "red"  # Green for positive, Red for negative
#             # st.write(f"{category}: {total_b} :{color}-background[{diff:+.2f}]")
#             # output += f"{category:<{max_category_length}}: {total_b:>5} ({diff:+.2f})\n"
#             # st.html(f"<span style='color: {color};'>{category:<{max_category_length}}: {total_b:>5} ({diff:+.2f})</span>")
#             st.html(f"<span style='font-family:monospace; white-space:pre; background-color: lightgray;'>{category:<{max_category_length}}: {total_b:>5} <span style='color: {color}'>({diff:+.2f})</span></span>")
#         else:
#             # st.write(f"{category}: {total_b}")
#             output += f"{category:<{max_category_length}}: {total_b:>5}\n"

#     st.code(output)


def display_balances_with_changes(ledger_a: Ledger, ledger_b: Ledger):
    
    entries_a = list(ledger_a.entries())
    entries_b = list(ledger_b.entries())
        
    categories = sorted(
        set(
            substring 
            for entries in [entries_a, entries_b] 
            for entry in entries 
            for substring in get_substrings(entry.description)
        )
    )

    output = ""



    # max_category_length = max(len(category) for category in categories)

    max_category_length = max(len(transform_description(category)) for category in categories)
    
    for category in categories:
        total_a = sum(entry.amount for entry in entries_a if entry.description.startswith(category))
        total_b = sum(entry.amount for entry in entries_b if entry.description.startswith(category))

        category = transform_description(category)

        font_family = '"Source Code Pro", monospace'
        style = f"font-family:{font_family}; font-size: 14px; white-space:pre; background-color: #F8F9FB;"

        if total_a != total_b:
            diff = total_b - total_a
            color = "green" if diff > 0 else "red"  # Green for positive, Red for negative
            # st.write(f"{category}: {total_b} :{color}-background[{diff:+.2f}]")
            # output += f"{category:<{max_category_length}}: {total_b:>5} ({diff:+.2f})\n"
            # st.html(f"<span style='color: {color};'>{category:<{max_category_length}}: {total_b:>5} ({diff:+.2f})</span>")
            # st.html(f"<span style='font-family:monospace; white-space:pre; background-color: lightgray;'>{category:<{max_category_length}}: {total_b:>5} <span style='color: {color}'>({diff:+.2f})</span></span>")
            # output += f"<div style='font-family:monospace; white-space:pre; background-color: lightgray;'>{category:<{max_category_length}}: {total_b:>5} <span style='color: {color}'>({diff:+.2f})</span></div>"
            # output += f"<div style='font-family:monospace; white-space:pre; background-color: #F8F9FB;'>{category:<{max_category_length}}: {total_b:>5} <span style='color: {color}'>({diff:+.2f})</span></div>"
            # output += f"<div style='font-family:{font_family}; font-size: 14px; white-space:pre; background-color: #F8F9FB;'>{category:<{max_category_length}}: {total_b:>5} <span style='color: {color}'>({diff:+.2f})</span></div>"
            output += f"<div style='{style}'>{category:<{max_category_length}}: {total_b:>5} <span style='color: {color}'>({diff:+.2f})</span></div>"
            
        else:
            # st.write(f"{category}: {total_b}")
            # output += f"{category:<{max_category_length}}: {total_b:>5}\n"
            # output += f"<div style='font-family:monospace; white-space:pre; background-color: #F8F9FB;'>{category:<{max_category_length}}: {total_b:>5}</div>"
            
            output += f"<div style='font-family:{font_family}; font-size: 14px; white-space:pre; background-color: #F8F9FB;'>{category:<{max_category_length}}: {total_b:>5}</div>"

    # st.code(output)

    st.html(output)



def fixed_width_text(text: str):


    font_family = '"Source Code Pro", monospace'
    style = f"font-family:{font_family}; font-size: 14px; white-space:pre; background-color: #F8F9FB;"

    return f"<div style='{style}'>{text}</div>"



import streamlit as st


def display_money_supply(ledger: Ledger):
    entries = [entry for transaction in ledger.transactions for entry in transaction.entries]

    # entries = ledger.entries()
    
    deposits = sum(entry.amount for entry in entries if entry.description.startswith("bank") and "deposits" in entry.description)
    cash = sum(entry.amount for entry in entries if entry.description.startswith("person") and "cash" in entry.description)
    gold = sum(entry.amount for entry in entries if entry.description.startswith("person") and "gold" in entry.description)
    
    # "Money supply:"    
    # f"  Deposits: {-deposits}"
    # f"  Cash:     {cash}"
    # f"  Gold:     {gold}"
    
    # f"  Total:    {cash + gold + -deposits}"
    
    # st.write("Money supply:")

    # st.write(f"  Deposits: {-deposits}")
    # st.write(f"  Cash:     {cash}")
    # st.write(f"  Gold:     {gold}")
    
    # st.write(f"  Total:    {cash + gold + -deposits}")

    # st.text("Money supply:")
    # st.text(f"  Deposits: {-deposits}")
    # st.text(f"  Cash:     {cash}")
    # st.text(f"  Gold:     {gold}")
    # st.text(f"  Total:    {cash + gold + -deposits}")

    if cash + gold + -deposits != 0:

        st.code(
            f"""    
            Money supply:
                Deposits: {-deposits}
                Cash:     {cash}
                Gold:     {gold}
                Total:    {cash + gold + -deposits}
            """)


# ----------------------------------------------------------------------
def amount_available_for_loan_at_bank(ledger, bank):

    reserves = sum(entry.amount for entry in ledger.entries() if entry.description.startswith(f"{bank}:assets:reserves"))
    deposits = sum(entry.amount for entry in ledger.entries() if entry.description.startswith(f"{bank}:liabilities:deposits"))
    
    minimum_reserves = abs(deposits * reserve_ratio)

    available_for_loan = reserves - minimum_reserves

    return available_for_loan


def display_amounts_available_for_loan(ledger: Ledger):
    banks = sorted(list(set(
        entry.description.split(":")[0]
        for entry in ledger.entries()
        if entry.description.startswith("bank")
    )))

    output = fixed_width_text("Amounts available for loan:")

    for bank in banks:
        amount_available_for_loan = amount_available_for_loan_at_bank(ledger, bank)

        output += fixed_width_text(f"    {bank}: {amount_available_for_loan}")

    st.html(output)

        

# banks = sorted(list(set(
#     entry.description.split(":")[0]
#     for entry in ledger.entries()
#     if entry.description.startswith("bank")
# )))

# # banks


# for bank in banks:
#     amount_available_for_loan = amount_available_for_loan_at_bank(ledger, bank)
#     st.text(f"Amount available for loan at {bank}: {amount_available_for_loan}")





# ----------------------------------------------------------------------
def history_of_balances(ledger: Ledger):
    tmp_ledger = Ledger()
    
    for transaction in ledger.transactions:
        before = deep_clone_ledger(tmp_ledger)
        tmp_ledger.transactions.append(transaction)
        
        st.write(f"**{transaction.date} {transaction.description}**")
        
        display_balances_with_changes(before, tmp_ledger)
        
        display_money_supply(tmp_ledger)
        
        display_amounts_available_for_loan(tmp_ledger)

    

