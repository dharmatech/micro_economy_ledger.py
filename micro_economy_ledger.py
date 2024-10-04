from dataclasses import dataclass, field
from typing import List, Dict
from decimal import Decimal
import datetime

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

    def display_balance(self):
        for transaction in self.transactions:
            for entry in transaction.entries:
                print(f"{entry.description}: {entry.amount}")

# Standalone functions (previously methods in Utils)

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
            Entry(description=f"{name}:equity", amount=-amount)
        ]
    ))

def grow_apples(ledger: Ledger, date: str, name: str, amount: Decimal):
    ledger.transactions.append(Transaction(
        date=date,
        description=f"grow_apples: {name}",
        entries=[
            Entry(description=f"{name}:assets:apples", amount=amount),
            Entry(description=f"{name}:equity", amount=-amount)
        ]
    ))

def barter(ledger: Ledger, date: str, name_a: str, name_b: str, asset_a: str, asset_b: str, amount: Decimal):
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
    gold = sum(entry.amount for transaction in ledger.transactions for entry in transaction.entries if entry.description == f"{person}:assets:gold")
    
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
    cash = sum(entry.amount for transaction in ledger.transactions for entry in transaction.entries if entry.description == f"{person}:assets:cash")
    
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

def get_loan(ledger: Ledger, date: str, person: str, bank: str, amount: Decimal):
    # reserves = sum(entry.amount for transaction in ledger.transactions for entry in transaction.entries if entry.description == f"{bank}:assets:reserves")
    # deposits = sum(entry.amount for transaction in ledger.transactions for entry in transaction.entries if entry.description == f"{bank}:liabilities:deposits")

    reserves = sum(entry.amount for transaction in ledger.transactions for entry in transaction.entries if entry.description.startswith(f"{bank}:assets:reserves"))
    deposits = sum(entry.amount for transaction in ledger.transactions for entry in transaction.entries if entry.description.startswith(f"{bank}:liabilities:deposits"))    
    
    minimum_reserves = deposits * reserve_ratio
    proposed_reserves = reserves - amount

    # print(f"minimum_reserves: {minimum_reserves}")
    # print(f"proposed_reserves: {proposed_reserves}")
    
    if proposed_reserves < minimum_reserves:
        print("Insufficient reserves")
        return

    ledger.transactions.append(Transaction(
        date=date,
        description=f"get_loan: {person} <- {bank}",
        entries=[
            Entry(description=f"{person}:assets:cash", amount=amount),
            Entry(description=f"{person}:liabilities:loans:{bank}", amount=-amount),
            Entry(description=f"{bank}:assets:reserves", amount=-amount),
            Entry(description=f"{bank}:assets:loans", amount=amount)
        ]
    ))

def deep_clone_ledger(ledger: Ledger) -> Ledger:
    return Ledger(transactions=[
        Transaction(
            date=transaction.date,
            description=transaction.description,
            entries=[Entry(description=entry.description, amount=entry.amount) for entry in transaction.entries]
        ) for transaction in ledger.transactions
    ])

def display_balances(ledger: Ledger):
    entries = [entry for transaction in ledger.transactions for entry in transaction.entries]
    categories = sorted(set(substring for entry in entries for substring in get_substrings(entry.description)))
    
    for category in categories:
        total = sum(entry.amount for entry in entries if entry.description.startswith(category))
        print(f"{category}: {total}")

def display_balances_with_changes(ledger_a: Ledger, ledger_b: Ledger):
    entries_a = [entry for transaction in ledger_a.transactions for entry in transaction.entries]
    entries_b = [entry for transaction in ledger_b.transactions for entry in transaction.entries]
    
    categories = sorted(set(substring for entries in [entries_a, entries_b] for entry in entries for substring in get_substrings(entry.description)))
    
    for category in categories:
        total_a = sum(entry.amount for entry in entries_a if entry.description.startswith(category))
        total_b = sum(entry.amount for entry in entries_b if entry.description.startswith(category))
        
        if total_a != total_b:
            diff = total_b - total_a
            color = "\033[32m" if diff > 0 else "\033[31m"  # Green for positive, Red for negative
            reset = "\033[0m"  # Reset color
            print(f"{category}: {total_b} {color}{diff:+.2f}{reset}")
        else:
            print(f"{category}: {total_b}")

def history_of_balances(ledger: Ledger):
    tmp_ledger = Ledger()
    
    for transaction in ledger.transactions:
        before = deep_clone_ledger(tmp_ledger)
        tmp_ledger.transactions.append(transaction)
        
        print(f"{transaction.date} {transaction.description}")
        print()
        display_balances_with_changes(before, tmp_ledger)
        print()
        display_money_supply(tmp_ledger)
        print()

def display_money_supply(ledger: Ledger):
    entries = [entry for transaction in ledger.transactions for entry in transaction.entries]
    
    deposits = sum(entry.amount for entry in entries if entry.description.startswith("bank") and "deposits" in entry.description)
    cash = sum(entry.amount for entry in entries if entry.description.startswith("person") and "cash" in entry.description)
    gold = sum(entry.amount for entry in entries if entry.description.startswith("person") and "gold" in entry.description)
    
    print("Money supply:")
    print(f"  Deposits: {-deposits}")
    print(f"  Cash:     {cash}")
    print(f"  Gold:     {gold}")
    print()
    print(f"  Total:    {cash + gold + -deposits}")
    # print(f"  Total:    {cash + -deposits}")

