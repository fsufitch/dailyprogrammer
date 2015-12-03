import sys

TOTAL_MONEY = 500

fruit_combos = []

# A combo includes a total cost and a list of amount/name strings (eg. "3 apples")
# We start with an empty combo
fruit_combos.append( {
    "cost": 0,
    "purchases": [],
})

for line in sys.stdin:
    # Parse the input
    fruit_name, fruit_price = line.strip().split()
    fruit_price = int(fruit_price)

    # We are going to try to add some amount of fruit to all the current combos
    new_combos = []
    for combo in fruit_combos:
        money_left = TOTAL_MONEY - combo["cost"]
        max_buy = money_left // fruit_price

        # Try to add every possible amount of the current fruit
        for amount_buy in range(1, max_buy+1):  
            purchase_cost = fruit_price * amount_buy
            purchase_string = "{count} {name}{plural}".format(
                count=amount_buy,
                name=fruit_name,
                plural="s" if amount_buy > 1 else ""
            )
            
            # Put the new combo together and record it.
            new_combo = {
                "cost": combo["cost"] + purchase_cost,
                "purchases": combo["purchases"] + [purchase_string],
            }

            new_combos.append(new_combo)

    # Now we have a bunch of new combos, let's check for solutions and invalid combos
    for combo in new_combos:
        if combo["cost"] == TOTAL_MONEY: # This is a solution!
            solution_string = ', '.join(combo["purchases"])
            print(solution_string)
        
        if combo["cost"] >= TOTAL_MONEY: 
            # No way to increase this combo further and keep it valid, so remove it
            new_combos.remove(combo)

    # Add the remaining combos to the current combo list
    fruit_combos += new_combos

# That's it. By the time we go through all the fruit inputs, we will have generated all 
# possible combos and printed out the ones that sum up to 500.
    
