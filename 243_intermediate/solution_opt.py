import sys

TOTAL_MONEY = 500

fruit_combos = set()

fruit_combos.add( (0, ) )

fruit_menu = []

for line in sys.stdin:
    fruit_name, fruit_price = line.strip().split()
    fruit_menu.append( (int(fruit_price), fruit_name ))

fruit_menu.sort()

for fruit_price, fruit_name in fruit_menu:
    new_combos = set()
    for cost, *purchases in fruit_combos:
        max_buy = (TOTAL_MONEY - cost) // fruit_price

        for amount_buy in range(1, max_buy+1):  
            new_cost = cost + fruit_price * amount_buy
            purchase_string = "{count} {name}{plural}".format(
                count=amount_buy,
                name=fruit_name,
                plural="s" if amount_buy > 1 else ""
            )
            new_purchases = tuple(purchases) + (purchase_string ,)

            if new_cost == TOTAL_MONEY: # Solution!
                print(', '.join(new_purchases))
            if new_cost >= TOTAL_MONEY:
                break
            
            new_combos.add( (new_cost,) + new_purchases )
    fruit_combos.update(new_combos)
    
