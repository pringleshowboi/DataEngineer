import pandas as pd

visits = pd.read_csv('visits.csv',
                     parse_dates=[1])
cart = pd.read_csv('cart.csv',
                   parse_dates=[1])
checkout = pd.read_csv('checkout.csv',
                       parse_dates=[1])
purchase = pd.read_csv('purchase.csv',
                       parse_dates=[1])

print(visits.head())
print(cart.head())
print(checkout.head())
print(purchase.head())

visits_to_cart = pd.merge(visits, cart, how='left')
#print(visits_to_cart)
unordered = visits_to_cart[visits_to_cart.cart_time.isnull()]
unordered = len(unordered) / float(len(visits_to_cart)) * 100
#print(unordered)

cart_checkout = pd.merge(cart, checkout, how='left')
c_checkout_null = cart_checkout[cart_checkout.checkout_time.isnull()]
c_checkout_null = len(c_checkout_null) / float(len(cart_checkout)) * 100
#print(c_checkout_null)

all_data = pd.merge(
  visits,
  purchase,
  how='left').merge(checkout, how='left').merge(cart, how='left')
print(all_data.head())


all_data['time_to_purchase'] = all_data.purchase_time - all_data.visit_time
print(all_data['time_to_purchase'])

average_time = all_data['time_to_purchase'].mean()
print("Average time to purchase:", average_time)