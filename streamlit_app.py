import streamlit as st

from micro_economy_ledger_streamlit import *

import dill as pickle
import base64

if 'ledger' not in st.session_state:

    if 'ledger' in st.query_params:

        encoded_ledger = st.query_params.ledger

        serialized_ledger = base64.urlsafe_b64decode(encoded_ledger)

        # ledger = pickle.loads(serialized_ledger)

        st.session_state.ledger = pickle.loads(serialized_ledger)

    else:

        st.session_state.ledger = Ledger()

# ledger = Ledger()

ledger = st.session_state.ledger

st.sidebar.markdown('# Transactions')

# with st.sidebar.expander("dig for gold", expanded=False):

#     date = st.text_input("Date", "2020-01-01")
#     person = st.text_input("Person", "person_a")
#     amount = st.number_input("Amount", 100)    

#     if st.button("go"):
#         dig_for_gold(ledger, date, person, amount)





with st.sidebar.expander("dig for gold", expanded=False):


    date = st.text_input("Date", "2020-01-01")

    persons = sorted(list(set(
        entry.description.split(":")[0]
        for entry in ledger.entries()
        if entry.description.startswith("person")
    )))

    if st.checkbox('Manual person entry', value=False):
        person = st.text_input("Person")
    else:
        person = st.selectbox("Person", persons)

    # person = st.text_input("Person", "person_a")
    amount = st.number_input("Amount", 100)    

    if st.button("go"):
        dig_for_gold(ledger, date, person, amount)












with st.sidebar.expander("grow apples", expanded=False):
    
    date = st.text_input("Date ", "2020-01-01")
    person = st.text_input("Person ", "person_a")
    amount = st.number_input("Amount ", 100)    

    if st.button("go "):
        grow_apples(ledger, date, person, amount)

with st.sidebar.expander("barter", expanded=False):
    
    date = st.text_input("Date   ", "2020-01-01")
    person_a = st.text_input("Person A  ", "person_a")
    person_b = st.text_input("Person B  ", "person_b")
    asset_a = st.text_input("Asset A  ", "gold")
    asset_b = st.text_input("Asset B  ", "apples")
    amount = st.number_input("Amount   ", value=100)    

    if st.button("go  "):
        barter(ledger, date, person_a, person_b, asset_a, asset_b, amount)

with st.sidebar.expander("deposit gold", expanded=False):

    date = st.text_input("Date  ", "2020-01-01")
    person = st.text_input("Person  ", "person_a")
    bank = st.text_input("Bank", "bank_a")
    amount = st.number_input("Amount  ", value=100)

    if st.button("Deposit gold"):    
        deposit_gold(ledger, date, person, bank, amount)

import random

with st.sidebar.expander('get loan', expanded=False):

    date   = st.text_input("Date ", "2020-01-01", key=random.random())
    person = st.text_input("Person   ", "person_a", key=random.random())
    bank   = st.text_input("Bank", "bank_a", key=random.random())
    amount = st.number_input("Amount ", value=100)

    if st.button("Get loan"):
        get_loan(ledger, date, person, bank, amount)

st.sidebar.markdown('# Presets')

if st.sidebar.button("Loan"):

    st.markdown("### Code:")

    with st.echo():
        dig_for_gold(ledger, "2020-01-01", "person_a",           100)
        deposit_gold(ledger, "2020-01-01", "person_a", "bank_a", 100)
        get_loan(    ledger, "2020-01-01", "person_b", "bank_a", 90)
        grow_apples( ledger, "2020-01-01", "person_c",           100)
        barter(      ledger, "2020-01-01", "person_b", "person_c", "cash", "apples", 90)
        deposit_gold(ledger, "2020-01-01", "person_c", "bank_b", 90)
        deposit_cash(ledger, "2020-01-01", "person_c", "bank_b", 90)


    # dig_for_gold(ledger, "2020-01-01", "person_a", 1000)
    # deposit_gold(ledger, "2020-01-01", "person_a", "bank_a", 1000)

st.sidebar.divider()

if st.sidebar.button("Clear ledger"):
    st.session_state.ledger = Ledger()    













history_of_balances(ledger)

# display_money_supply(ledger)

# ----------------------------------------------------------------------

# for each bank, display amount available for loan

# bank_descriptions = [
#     entry.description 
#     for entry in ledger.entries()
#     if entry.description.startswith("bank")
# ]

# bank_descriptions

# banks = [desc.split(":")[0] for desc in bank_descriptions]

# get unique banks

# banks = sorted(list(set(banks)))

# banks


# st.selectbox("Bank", ["bank_a", "bank_b"])


# banks = sorted(list(set(
#     entry.description.split(":")[0]
#     for entry in ledger.entries()
#     if entry.description.startswith("bank")
# )))

# if st.checkbox('New bank'):
#     new_bank = st.text_input("Bank")
#     if st.button("Add bank"):
#         banks.append(new_bank)
# else:
#     bank = st.selectbox("Bank", banks)

# import pickle

# serialized_ledger = pickle.dumps(ledger)

# st.write(serialized_ledger)

# st.write(type(ledger))




serialized_ledger = pickle.dumps(ledger)

encoded_ledger = base64.urlsafe_b64encode(serialized_ledger).decode('utf-8')

# st.write(encoded_ledger)

# st.write(type(encoded_ledger))

# st.write(len(encoded_ledger))

# st.write(serialized_ledger)

# st.write(type(serialized_ledger))

# st.query_params.abc = 123
# st.query_params.bcd = 234

st.query_params.ledger = encoded_ledger


# st.write(list(st.query_params.keys()))

# if 'ledger' in st.query_params:
#     10
# else:
#     20


# st.write(type(st.query_params))
