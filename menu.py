#Define MEnu of cafe or resturant
import string
import os
from datetime import datetime

menu = {
    'pizza' : 1200,
    'burger' : 250,
    'shawarma' : 150,
    'tea' : 80,
    'coffee' : 130,
    'biryani' : 320
}

TAX_RATE = 0.02  # 2% GST tax
DISCOUNT_RATE = 0.01  # Can be modified
orders_history = []

def displayMenu():
    print("\n" + "="*40)
    print("        CAFE MENU")
    print("="*40)
    for key, val in menu.items():
        print(f"{key.capitalize():<20} Rs. {val}")
    print("="*40)
    print("Enter 'C' to Place Order and Checkout\n")

def takeOrder():
    t_price = 0
    s_items = {}
    while(True):
        item = input("Enter name of item you want to Order (or press 'C' to checkout): ").strip()
        
        if(item.lower() == 'c'):
            if len(s_items) == 0:
                print("You have not ordered anything!")
                continue
            else:
                generateBill(s_items, t_price)
                return
        elif(item.lower() not in menu):
            print("Item Not Available. \nSelect Item from Available Menu\n")
            continue
        else:
            try:
                quantity = int(input("Enter Quantity you want to Buy: "))
                if quantity <= 0:
                    print("Please enter a valid quantity!\n")
                    continue
                
                price = int(menu[item.lower()]) * quantity
                
                if item.lower() in s_items:
                    s_items[item.lower()][0] += quantity
                    s_items[item.lower()][1] += price
                else:
                    s_items[item.lower()] = [quantity, price]
                
                t_price += price
                print(f"Added {quantity}x {item} to your cart!\n")
            except ValueError:
                print("Please enter a valid quantity!\n")
                continue

def generateBill(s_items, t_price):
    current_datetime = datetime.now()
    formatted_date = current_datetime.strftime('%d/%m/%Y')  # DD/MM/YYYY format
    formatted_time = current_datetime.strftime('%H:%M:%S')  # HH:MM:SS format
    day_name = current_datetime.strftime('%A')  # Full day name (e.g., Monday)
    
    print("\n" + "="*55)
    print("           CAFE BILL RECEIPT")
    print("="*55)
    print(f"Date: {formatted_date} ({day_name})")
    print(f"Time: {formatted_time}")
    print("="*55)
    print(f"{'Item':<15} {'Quantity':<10} {'Price':<20}")
    print("-"*55)
    
    for item, details in s_items.items():
        quantity = details[0]
        price = details[1]
        print(f"{item.capitalize():<15} {quantity:<10} Rs. {price:<20}")
    
    print("-"*55)
    subtotal = t_price
    
    # Apply discount if available
    discount_amount = 0
    if DISCOUNT_RATE > 0:
        discount_amount = int(subtotal * DISCOUNT_RATE)
        print(f"Subtotal:                        Rs. {subtotal}")
        print(f"Discount ({DISCOUNT_RATE*100}%):                    Rs. -{discount_amount}")
        subtotal -= discount_amount
    else:
        print(f"Subtotal:                        Rs. {subtotal}")
    
    # Apply tax
    tax_amount = int(subtotal * TAX_RATE)
    print(f"Tax (GST {TAX_RATE*100}%):                  Rs. {tax_amount}")
    
    final_total = subtotal + tax_amount
    print("-"*55)
    print(f"{'FINAL TOTAL':<35} Rs. {final_total}")
    print("="*55)
    print("Thank you for your order! Please visit again.\n")
    
    # Store order in history
    order_data = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'items': s_items,
        'subtotal': t_price,
        'discount': discount_amount,
        'tax': tax_amount,
        'total': final_total
    }
    orders_history.append(order_data)
def viewOrderHistory():
    if len(orders_history) == 0:
        print("\nNo orders placed yet!\n")
        return
    
    print("\n" + "="*70)
    print("           ORDER HISTORY")
    print("="*70)
    
    for idx, order in enumerate(orders_history, 1):
        print(f"\nOrder #{idx}")
        print(f"Date & Time: {order['timestamp']}")
        print(f"Items: ", end="")
        items_list = [f"{item.capitalize()} x{details[0]}" for item, details in order['items'].items()]
        print(", ".join(items_list))
        print(f"Subtotal: Rs. {order['subtotal']}")
        if order['discount'] > 0:
            print(f"Discount: Rs. -{order['discount']}")
        print(f"Tax: Rs. {order['tax']}")
        print(f"Total: Rs. {order['total']}")
        print("-"*70)
    
    print("\n")

def adminMenu():
    while True:
        print("\n" + "="*50)
        print("     ADMIN MENU")
        print("="*50)
        print("1. View/Modify Menu Items")
        print("2. View Order History")
        print("3. Set Discount Rate")
        print("4. Exit Admin Menu")
        print("="*50)
        
        choice = input("Select Option (1-4): ").strip()
        
        if choice == '1':
            modifyMenu()
        elif choice == '2':
            viewOrderHistory()
        elif choice == '3':
            setDiscount()
        elif choice == '4':
            break
        else:
            print("Invalid choice! Please try again.")

def modifyMenu():
    while True:
        print("\n" + "="*40)
        print("   MENU MANAGEMENT")
        print("="*40)
        print("Current Menu Items:")
        for key, val in menu.items():
            print(f"  {key.capitalize():<15} Rs. {val}")
        print("\n1. Add New Item")
        print("2. Update Price")
        print("3. Remove Item")
        print("4. Back to Admin Menu")
        print("="*40)
        
        choice = input("Select Option (1-4): ").strip()
        
        if choice == '1':
            item_name = input("Enter new item name: ").strip().lower()
            if item_name in menu:
                print("Item already exists!")
                continue
            try:
                item_price = int(input("Enter item price: ").strip())
                if item_price > 0:
                    menu[item_name] = item_price
                    print(f"Item '{item_name}' added successfully!")
                else:
                    print("Price must be positive!")
            except ValueError:
                print("Invalid price!")
        
        elif choice == '2':
            item_name = input("Enter item name to update: ").strip().lower()
            if item_name not in menu:
                print("Item not found!")
                continue
            try:
                new_price = int(input(f"Enter new price for {item_name}: ").strip())
                if new_price > 0:
                    menu[item_name] = new_price
                    print(f"Price updated successfully!")
                else:
                    print("Price must be positive!")
            except ValueError:
                print("Invalid price!")
        
        elif choice == '3':
            item_name = input("Enter item name to remove: ").strip().lower()
            if item_name not in menu:
                print("Item not found!")
                continue
            del menu[item_name]
            print(f"Item '{item_name}' removed successfully!")
        
        elif choice == '4':
            break
        else:
            print("Invalid choice!")

def setDiscount():
    global DISCOUNT_RATE
    try:
        discount_input = float(input("Enter discount rate (0-100%): ").strip())
        if 0 <= discount_input <= 100:
            DISCOUNT_RATE = discount_input / 100
            print(f"Discount rate set to {discount_input}%")
        else:
            print("Please enter a value between 0 and 100")
    except ValueError:
        print("Invalid input!")

def customerMode():
    while True:
        displayMenu()
        takeOrder()
        
        another = input("Do you want to place another order? (Yes/No): ").strip().lower()
        if another != 'yes' and another != 'y':
            print()
            break

def main():
    print("\n" + "="*50)
    print("     WELCOME TO PIZZA CAFE")
    print("="*50)
    
    while True:
        print("\n" + "="*50)
        print("MAIN MENU")
        print("="*50)
        print("1. Customer - Place Order")
        print("2. Admin - Manage Cafe")
        print("3. Exit")
        print("="*50)
        
        choice = input("Select Option (1-3): ").strip()
        
        if choice == '1':
            customerMode()
        elif choice == '2':
            adminMenu()
        elif choice == '3':
            print("\n" + "="*50)
            print("Thank you for visiting Pizza Cafe!")
            print("="*50 + "\n")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()