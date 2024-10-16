import streamlit as st

from micro_economy_ledger_streamlit import *

import dill as pickle
import base64

import micro_economy_ledger_streamlit

micro_economy_ledger_streamlit.reserve_ratio = st.sidebar.number_input(
    "Reserve Ratio", min_value=0.0, max_value=1.0, value=0.1, step=0.01)

reserve_ratio = micro_economy_ledger_streamlit.reserve_ratio

st.sidebar.markdown(f'Max money multiplier: {1 / reserve_ratio:.2f}')

# if 'ledger' not in st.session_state:

#     if 'ledger' in st.query_params:

#         encoded_ledger = st.query_params.ledger

#         serialized_ledger = base64.urlsafe_b64decode(encoded_ledger)

#         # ledger = pickle.loads(serialized_ledger)

#         st.session_state.ledger = pickle.loads(serialized_ledger)

#     else:

#         st.session_state.ledger = Ledger()

# if 'ledger' not in st.session_state:

#     if 'ledger' in st.query_params:

#         encoded_ledger = st.query_params.ledger

#         serialized_ledger = base64.urlsafe_b64decode(encoded_ledger)

#         # ledger = pickle.loads(serialized_ledger)

#         st.session_state.ledger = pickle.loads(serialized_ledger)

#     else:

#         st.session_state.ledger = Ledger()

# ledger = Ledger()

if 'ledger' not in st.session_state:

    st.session_state.ledger = Ledger()

ledger = st.session_state.ledger


# st.sidebar.markdown(f'Monetary base: {monetary_base(ledger):.2f}')

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
    amount = st.number_input("Amount", value=100)    

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
    check = st.checkbox(label='Check available assets', value=True)
        
    if st.button("go  "):
        barter(ledger, date, person_a, person_b, asset_a, asset_b, amount, check)

with st.sidebar.expander("deposit gold", expanded=False):

    date = st.text_input("Date  ", "2020-01-01")
    person = st.text_input("Person  ", "person_a")
    bank = st.text_input("Bank", "bank_a")
    amount = st.number_input("Amount  ", value=100)

    if st.button("Deposit gold"):    
        deposit_gold(ledger, date, person, bank, amount)

with st.sidebar.expander('get loan', expanded=False):

    date   = st.text_input("Date ", "2020-01-01", key=' ')
    person = st.text_input("Person     ", "person_a")
    bank   = st.text_input("Bank", "bank_a", key='')
    amount = st.number_input("Amount ", value=100)

    if st.button("Get loan"):
        get_loan(ledger, date, person, bank, amount)


def fed_money_printer(ledger: Ledger, date: str, amount: Decimal):
    
    ledger.transactions.append(
        Transaction(
            date=date,
            description=f'Fed fires up money printer',
            entries=[
                Entry('fed:assets:reserves', amount),
                Entry('fed:liabilities:money_printer', -amount)
            ]
        ))

with st.sidebar.expander('Fed money printer', expanded=False):
    
    date = st.text_input("Date    ", "2020-01-01")
    amount = st.number_input("Amount ", value=1)

    if st.button("Fire up money printer"):
        fed_money_printer(ledger, date, amount)


with st.sidebar.expander("Buy securities from U.S. Treasury", expanded=False):

    date = st.text_input("Date     ", "2020-01-01")
    entity = st.text_input("Entity ", "person_a")
    amount = st.number_input("Amount   ", value=1)    

    if st.button("go   "):
        buy_treasury_securities(ledger, date, entity, amount)




# ----------------------------------------------------------------------

st.sidebar.markdown('# Presets')

if st.sidebar.button("Dig for gold"):

    # st.session_state.ledger = Ledger()    

    st.markdown("### Code:")

    with st.echo():
        dig_for_gold(ledger, "2020-01-01", "person_a", 100)
        
if st.sidebar.button("Barter"):

    st.session_state.ledger = Ledger()    

    st.markdown("### Code:")

    with st.echo():
        dig_for_gold(ledger, "2020-01-01", "person_a", 100)
        grow_apples( ledger, "2020-01-01", "person_b", 100)        
        barter(ledger, "2020-01-01", "person_a", "person_b", "gold", "apples", 50)

if st.sidebar.button("Loan"):

    st.markdown("### Code:")

    with st.echo():
        dig_for_gold(ledger, "2020-01-01", "person_a",           100)
        deposit_gold(ledger, "2020-01-01", "person_a", "bank_a", 100)
        get_loan(    ledger, "2020-01-01", "person_b", "bank_a", 90)
        grow_apples( ledger, "2020-01-01", "person_c",           100)
        barter(      ledger, "2020-01-01", "person_b", "person_c", "gold", "apples", 90)
        deposit_gold(ledger, "2020-01-01", "person_c", "bank_b", 90)
        
    # dig_for_gold(ledger, "2020-01-01", "person_a", 1000)
    # deposit_gold(ledger, "2020-01-01", "person_a", "bank_a", 1000)


if st.sidebar.button("Deposit max"):

    st.markdown("### Code:")

    with st.echo():
        
        deposit_amount = sum(entry.amount for entry in ledger.entries() if entry.description == "person_a:assets:gold")

        deposit_gold(ledger, "2020-01-01", "person_a", "bank_a", deposit_amount)

if st.sidebar.button("Loan max"):
        
        st.markdown("### Code:")
    
        with st.echo():
            
            loan_amount = amount_available_for_loan_at_bank(ledger, "bank_a")
       
            get_loan(ledger, "2020-01-01", "person_a", "bank_a", loan_amount)

if st.sidebar.button("Iterate loan"):

    st.markdown("### Code:")

    with st.echo():
        
        deposit_amount = sum(entry.amount for entry in ledger.entries() if entry.description == "person_a:assets:gold")

        deposit_gold(ledger, "2020-01-01", "person_a", "bank_a", deposit_amount)

        loan_amount = amount_available_for_loan_at_bank(ledger, "bank_a")
       
        get_loan(ledger, "2020-01-01", "person_a", "bank_a", loan_amount)

# if st.sidebar.button('Daisy chain loans'):

#     st.markdown("### Code:")

#     with st.echo():

#         dig_for_gold(ledger, "2020-01-01", "person_0", 100)

#         deposit_gold(ledger, "2020-01-01", "person_0", "bank_0", 100)

        
#         max_loan = amount_available_for_loan_at_bank(ledger, "bank_0")

#         get_loan(ledger, "2020-01-01", "person_1", "bank_0", max_loan)

#         deposit_gold(ledger, "2020-01-01", "person_1", "bank_1", max_loan)


#         max_loan = amount_available_for_loan_at_bank(ledger, "bank_1")

#         get_loan(ledger, "2020-01-01", "person_2", "bank_1", max_loan)

#         deposit_gold(ledger, "2020-01-01", "person_2", "bank_2", max_loan)

#         max_loan = amount_available_for_loan_at_bank(ledger, "bank_2")

#         get_loan(ledger, "2020-01-01", "person_3", "bank_2", max_loan)

#         deposit_gold(ledger, "2020-01-01", "person_3", "bank_3", max_loan)

#         max_loan = amount_available_for_loan_at_bank(ledger, "bank_3")

#         get_loan(ledger, "2020-01-01", "person_4", "bank_3", max_loan)

#         deposit_gold(ledger, "2020-01-01", "person_4", "bank_4", max_loan)

#         max_loan = amount_available_for_loan_at_bank(ledger, "bank_4")

#         get_loan(ledger, "2020-01-01", "person_5", "bank_4", max_loan)

#         deposit_gold(ledger, "2020-01-01", "person_5", "bank_5", max_loan)

#         max_loan = amount_available_for_loan_at_bank(ledger, "bank_5")

#         get_loan(ledger, "2020-01-01", "person_6", "bank_5", max_loan)


# with st.sidebar.expander("Daisy chain loans", expanded=False):

#     n = st.number_input("Number of iterations", value=10)

#     if st.button("go    "):

#         dig_for_gold(ledger, "2020-01-01", "person_0", 100)

#         deposit_gold(ledger, "2020-01-01", "person_0", "bank_0", 100)
        
#         for i in range(1, n):
        
#             max_loan = amount_available_for_loan_at_bank(ledger, f"bank_{i-1}")

#             get_loan(ledger, "2020-01-01", f"person_{i}", f"bank_{i-1}", max_loan)

#             deposit_gold(ledger, "2020-01-01", f"person_{i}", f"bank_{i}", max_loan)
        


with st.sidebar.expander("Daisy chain loans", expanded=False):

    # n = st.number_input("Number of iterations", value=10)

    if st.button('initialize'):

        dig_for_gold(ledger, "2020-01-01", "person_0", 100)

        deposit_gold(ledger, "2020-01-01", "person_0", "bank_0", 100)        

        st.session_state.i = 1

    if st.button('iterate'):

        i = st.session_state.i

        max_loan = amount_available_for_loan_at_bank(ledger, f"bank_{i-1}")

        get_loan(ledger, "2020-01-01", f"person_{i}", f"bank_{i-1}", max_loan)

        deposit_gold(ledger, "2020-01-01", f"person_{i}", f"bank_{i}", max_loan)

        st.session_state.i += 1        


def abc():
    st.markdown("### Code:")

    with st.echo():

        # Commercial bank sells treasuries to Fed

        # ledger.transactions.append(
        #     Transaction(
        #         date='2020-01-01',
        #         description=f'Fed fires up money printer',
        #         entries=[
        #             Entry('fed:assets:reserves', 1),
        #             Entry('fed:liabilities:money_printer', -1)
        #         ]
        #     ))

        # fed_money_printer(ledger, "2020-01-01", 1)

        barter(ledger, "2020-01-01", "fed", "bank", "reserves", "securities", 1, check=False)
        
        # ledger.transactions.append(
        #     Transaction(
        #         date='2020-01-01',
        #         description=f'Bank sends securities to Fed',
        #         entries=[
        #             Entry('bank:assets:securities', -1),
        #             Entry('fed:assets:securities',   1)
        #         ]
        #     ))
        
        # ledger.transactions.append(
        #     Transaction(
        #         date='2020-01-01',
        #         description=f'Bank gets reserves',
        #         entries=[
        #             Entry('bank:assets:reserves',   1),
        #             Entry('fed:assets:reserves', -1)
        #         ]
        #     ))

def cb101_1():
    st.markdown("### Code:")

    with st.echo():

        # Commercial bank sells treasuries to Fed

        dig_for_gold(ledger, "2020-01-01", "bank", 1)
        buy_treasury_securities(ledger, "2020-01-01", "bank", 1)
        fed_money_printer(ledger, "2020-01-01", 1)
        barter(ledger, "2020-01-01", "fed", "bank", "reserves", "securities", 1)

# ----------------------------------------------------------------------
# CB101 : chapter 1 : example 2
# corporation sells treasuries to Fed
# ----------------------------------------------------------------------

def cb101_ch1_ex2_simple():

    st.markdown("### Code:")

    st.markdown("Note: in this case, the Fed balance sheet isn't displayed")

    with st.echo():

        ledger.transactions.append(
            Transaction(
                date='2020-01-01',
                description=f'corporation hands over securities for bank deposits',
                entries=[
                    Entry('corp:assets:securities',    -1),
                    Entry('corp:assets:deposits:bank',  1)
                ]
            ))
        
        ledger.transactions.append(
            Transaction(
                date='2020-01-01',
                description=f'bank',
                entries=[
                    Entry('bank:assets:reserves',            1),
                    Entry('bank:liabilities:deposits:corp', -1)
                ]
            ))        

        # ledger.transactions.append(
        #     Transaction(
        #         date='2020-01-01',
        #         description=f'corporation hands over securities for bank deposits',
        #         entries=[
        #             Entry('corp:assets:securities',    -1),
        #             Entry('corp:assets:deposits:bank',  1)
        #         ]
        #     ))
        
        # ledger.transactions.append(
        #     Transaction(
        #         date='2020-01-01',
        #         description=f'bank',
        #         entries=[
        #             Entry('bank:assets:reserves',            1),
        #             Entry('corp:liabilities:deposits:corp', -1)
        #         ]
        #     ))        

def cb101_ch1_ex2_with_fed():
    st.markdown("### Code:")

    st.markdown("Note: Now we see the Fed balance sheet, however, the economy isn't bootstrapped")

    with st.echo():

        ledger.transactions.append(
            Transaction(
                date='2020-01-01',
                description=f'corp sends securities to Fed',
                entries=[
                    Entry('corp:assets:securities', -1),
                    Entry('fed:assets:securities',   1)
                ]
            ))
        
        ledger.transactions.append(
            Transaction(
                date='2020-01-01',
                description=f'Fed sends reserves to bank',
                entries=[
                    Entry('fed:liabilities:reserves', -1),
                    Entry('bank:assets:reserves',      1)
                ]
            ))
        
        ledger.transactions.append(
            Transaction(
                date='2020-01-01',
                description=f'Bank gives deposits to corp',
                entries=[
                    Entry('bank:liabilities:deposits:corp', -1),
                    Entry('corp:assets:deposits:bank',       1)
                ]
            ))

        # barter(ledger, '2020-01-01', 'corp', 'fed', 'securities', 'reserves', 1, check=False)

        # # Commercial bank sells treasuries to Fed

        # dig_for_gold(ledger, "2020-01-01", "bank", 1)
        # buy_treasury_securities(ledger, "2020-01-01", "bank", 1)
        # fed_money_printer(ledger, "2020-01-01", 1)
        # barter(ledger, "2020-01-01", "fed", "bank", "reserves", "securities", 1)

def cb101_ch1_ex2_full():
    st.markdown("### Code:")

    st.markdown("Note: Now we see the Fed balance sheet, and the economy is bootstrapped from nothing")

    with st.echo():

        dig_for_gold(ledger, "2020-01-01", "corp", 1)

        buy_treasury_securities(ledger, "2020-01-01", "corp", 1)

        fed_money_printer(ledger, "2020-01-01", 1)

        ledger.transactions.append(
            Transaction(
                date='2020-01-01',
                description=f'corp sends securities to Fed',
                entries=[
                    Entry('corp:assets:securities', -1),
                    Entry('fed:assets:securities',   1)
                ]
            ))
        
        ledger.transactions.append(
            Transaction(
                date='2020-01-01',
                description=f'Fed sends reserves to bank',
                entries=[
                    # Entry('fed:liabilities:reserves', -1),
                    Entry('fed:assets:reserves', -1),
                    Entry('bank:assets:reserves',      1)
                ]
            ))
        
        ledger.transactions.append(
            Transaction(
                date='2020-01-01',
                description=f'Bank gives deposits to corp',
                entries=[
                    Entry('bank:liabilities:deposits:corp', -1),
                    Entry('corp:assets:deposits:bank',       1)
                ]
            ))

with st.sidebar.expander("Central Banking 101", expanded=False):

    st.markdown('Bank sells treasuries to Fed:')

    # st.button('Bank sells treasuries to Fed (simple)', on_click=abc)
    # st.button('Bank sells treasuries to Fed',          on_click=cb101_1)

    st.button('with Fed ', on_click=abc)
    st.button('full ',          on_click=cb101_1)

    # st.divider()    

    st.markdown('Corporation sells treasuries to Fed:')

    st.button('simple',   on_click=cb101_ch1_ex2_simple)
    st.button('with Fed', on_click=cb101_ch1_ex2_with_fed)
    st.button('full',     on_click=cb101_ch1_ex2_full)


def stock_example_01():

    with st.sidebar.expander('Stock', expanded=False):

        with st.echo():

            ledger.transactions.append(
                Transaction(
                    date='2020-01-01',
                    description=f'corp issues stock',
                    entries=[
                        # Entry('person_a:assets:stock', 0, quantity= 10, unit='CORP', price_per_unit=1),
                        # Entry('corp:equity:stock',     0, quantity=-10, unit='CORP', price_per_unit=1)
                        StockEntry('person_a:assets:stock',  10, 'CORP', 3),
                        StockEntry('corp:equity:stock',     -10, 'CORP', 3)
                    ]
                )
            )

st.sidebar.button('Stock example 01', on_click=stock_example_01)

# ----------------------------------------------------------------------
st.sidebar.divider()

if st.sidebar.button("Clear ledger"):
    st.session_state.ledger = Ledger()    

    ledger = st.session_state.ledger




show_gold = st.sidebar.checkbox('Show gold', value=False)
    
history_of_balances(ledger, display_gold=show_gold)


# ----------------------------------------------------------------------
# serialize
# ----------------------------------------------------------------------

# serialized_ledger = pickle.dumps(ledger)

# encoded_ledger = base64.urlsafe_b64encode(serialized_ledger).decode('utf-8')

# st.query_params.ledger = encoded_ledger


# st.write(
#     [
#         BasicEntry('abc', 10),
#         StockEntry('bcd', 10, 'TSLA', 1)
#     ]
# ) 

# st.write(ledger.entries())

