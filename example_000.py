# import * from micro_economy_ledger

from micro_economy_ledger import *

ledger = Ledger()

dig_for_gold(ledger, "2020-01-01", "person_a", 100)

deposit_gold(ledger, "2020-01-02", "person_a", "bank_a", 100)

get_loan(ledger, "2020-01-03", "person_b", "bank_a", 90)

grow_apples(ledger, "2020-01-04", "person_c", 100)

barter(ledger, "2020-01-05", "person_b", "person_c", "cash", "apples", 90)

deposit_cash(ledger, "2020-01-06", "person_c", "bank_b", 90)

get_loan(ledger, "2020-01-07", "person_d", "bank_b", 81)

history_of_balances(ledger)

# display_money_supply(ledger)