import streamlit as st

from micro_economy_ledger_streamlit import *

if 'ledger' not in st.session_state:
    st.session_state.ledger = Ledger()

# ledger = Ledger()

ledger = st.session_state.ledger

with st.sidebar.expander("dig for gold", expanded=False):

    date = st.text_input("Date", "2020-01-01")
    person = st.text_input("Person", "person_a")
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

history_of_balances(ledger)


if st.sidebar.button("Clear ledger"):
    st.session_state.ledger = Ledger()