import sqlite3 as sql

from sys import platform


def _display_options(all_options, title, type):
    option_num = 1
    option_list = []
    print("\n", title, "\n")
    for option in all_options:
        code = option[0]
        desc = option[1]
        print("{0}.\t{1}".format(option_num, desc))
        option_num = option_num + 1
        option_list.append(code)
    selected_option = 0
    while selected_option > len(option_list) or selected_option == 0:
        prompt = "Enter the number against the " + type + " you want to choose: "
        selected_option = int(input(prompt))
    return option_list[selected_option - 1]


def login(db_, shopper_id_):
    cursor = db_.cursor()
    sql_query = "SELECT * FROM shoppers WHERE shopper_id=" + str(shopper_id_)
    cursor.execute(sql_query)
    shopper = cursor.fetchone()

    if shopper:
        shopper_name_ = shopper[2]
        return shopper_name_
    else:
        return None


def print_menu():
    print("------------------------------------")
    print("ORINOCO – SHOPPER MAIN MENU")
    print("------------------------------------")
    print("1.\tDisplay your order history")
    print("2.\tAdd an item to your basket")
    print("3.\tView your basket")
    print("4.\tCheckout")
    print("5.\tExit")
    print("------------------------------------")


def display_your_order_history(db_, shopper_id_):
    cursor = db_.cursor()
    sql_query = """SELECT SO.order_id AS 'Order ID',
       SO.order_date AS 'Order Date',
       products.product_description AS 'Product Description',
       sellers.seller_name AS 'Seller',
       PRINTF("£%.2f",ordered_products.price) AS 'Price',
       ordered_products.quantity AS 'Qty',
       ordered_products.ordered_product_status AS 'Status'
      FROM shopper_orders SO
           INNER JOIN
           ordered_products ON SO.order_id = ordered_products.order_id
           INNER JOIN
           products ON products.product_id = ordered_products.product_id
           INNER JOIN
           sellers ON sellers.seller_id = ordered_products.seller_id
           
     WHERE SO.shopper_id = """ + str(shopper_id_) + """
     ORDER BY SO.order_date DESC """

    cursor.execute(sql_query)
    order_history_list = cursor.fetchall()
    print(order_history_list)
    print("Order ID\tOrder Date\tProduct Description Seller\t\t\t\tPrice\t\tQuantity Status")

    if len(order_history_list) > 0:
        for order_history in order_history_list:
            output_string = str(order_history[0]) + "\t\t" + str(order_history[1]) + "\t" + str(order_history[2])[
                                                                                            0:15] + "\t\t" + str(
                order_history[3]) + "\t\t" + str(order_history[4]) + "\t\t\t" + str(order_history[5]) + "\t" + str(
                order_history[6])
            print(output_string)
    else:
        print("No orders placed by this customer")


def db_connect():
    if platform == "linux" or platform == "linux2":
        # Linux...
        db_local = sql.connect(r'/home/anoopp/SQLiteStudio/SafeedaAssignment.db')
        return db_local
    else:
        # Windows...
        db_local = sql.connect(r'C:\Users\user\Desktop\Assignment.db')
        return db_local


def get_all_product_categories(db_):
    sql_query = "select * from categories"
    cursor = db_.cursor()
    result = cursor.execute(sql_query)
    categories = result.fetchall()
    return categories


# def print_category_menu(categories_list):
#     if len(categories_list) > 0:
#         i = 1
#         print("\nProduct Categories :\n")
#         for category in categories_list:
#             output = str(i) + ".\t" + str(category[2])
#             print(output)
#             i = i + 1


# def print_product_menu(products_list):
#     if len(products_list) > 0:
#         i = 1
#         print("\n\tProducts \n")
#         for product in products_list:
#             output = str(i) + ".\t" + str(product[3])
#             print(output)
#             i = i + 1
#

def get_all_category_products(db_, category_id):
    sql_query = "select * from products where category_id=" + str(category_id)
    cursor = db_.cursor()
    result = cursor.execute(sql_query)
    product_list = result.fetchall()
    return product_list


def get_all_sellers_for_product(db_, product_id_):
    sql_query = "select * from product_sellers where product_id=" + str(product_id_)
    cursor = db_.cursor()
    result = cursor.execute(sql_query)
    sellers_for_product_list = result.fetchall()
    return sellers_for_product_list


def get_seller_details(db_, seller_id_):
    sql_query = "select * from sellers where seller_id=" + str(seller_id_)
    cursor = db_.cursor()
    result = cursor.execute(sql_query)
    seller = result.fetchone()
    return seller


def print_seller_menu(db_, sellers_for_product_list_):
    if len(sellers_for_product_list_) > 0:
        print("\n\tSellers who sell this products \n")
        i = 1
        for seller_product in sellers_for_product_list_:
            if len(seller_product) > 2:
                seller = get_seller_details(db_, seller_product[1])
                output = str(i) + ".\t" + str(seller[2]) + "\t(£" + str(seller_product[2]) + ")"
                print(output)
                i = i + 1


def add_to_basket(db_, details):
    cursor = db_.cursor()
    if len(details) > 4:
        sql_query1 = "INSERT INTO shopper_baskets (shopper_id,basket_created_date_time) VALUES (" + str(
            details[0]) + ",DateTime('now')" + ")"
        cursor.execute(sql_query1)
        last_ins_id1 = cursor.lastrowid
        if last_ins_id1 > 0:
            sql_query2 = "INSERT INTO basket_contents (basket_id,product_id,seller_id,price,quantity) VALUES (" + str(
                last_ins_id1) + "," + str(details[1]) + "," + str(details[2]) + "," + str(details[3]) + "," + str(
                details[4]) + ")"
            cursor.execute(sql_query2)
            last_ins_id2 = cursor.lastrowid
            if last_ins_id2 > 0:
                return True
    return False


def add_item_to_basket(db_, shopper_id_):
    categories_list = get_all_product_categories(db_)
    options1 = []
    if len(categories_list) > 0:
        for category in categories_list:
            x1 = [category[0], category[2]]
            options1.append(x1)

    table_category_id = _display_options(options1, "Product Category", "product category")

    if table_category_id > 0:
        product_list = get_all_category_products(db_, table_category_id)
        if len(product_list) > 0:
            options2 = []
            for product in product_list:
                x2 = [product[0], product[3]]
                options2.append(x2)

            product_id = _display_options(options2, "Products", "products")
            table_product = None
            for p in product_list:
                if p[0] == product_id:
                    table_product = p
                    break
            if table_product:
                sellers_for_product_list = get_all_sellers_for_product(db_, table_product[0])
                print_seller_menu(db_, sellers_for_product_list)
                seller_id = int(input("Enter the number against the seller you want to choose : "))
                table_seller_product = None
                for i in range(len(sellers_for_product_list)):
                    if i + 1 == seller_id:
                        table_seller_product = sellers_for_product_list[i]
                        break
                if table_seller_product:
                    quantity = int(input("Enter the quantity of the selected product you want to buy : "))
                    price = float(table_seller_product[2])
                    selected_product_id = table_seller_product[0]
                    selected_seller_id = table_seller_product[1]
                    details = [shopper_id_, selected_product_id, selected_seller_id, price, quantity]
                    if add_to_basket(db_, details):
                        print("\nItem added to your basket !")
                        db_.commit()
                    else:
                        print("\nSomething went wrong ! Please try again later !")
                        db_.rollback()


def delete_shopper_basket(db_, basket_id):
    cursor = db_.cursor()
    sql_query = "DELETE FROM shopper_baskets WHERE basket_id=" + str(basket_id)
    cursor.execute(sql_query)


def delete_basket_contents(db_, basket_id, product_id_):
    cursor = db_.cursor()
    sql_query = "DELETE FROM basket_contents WHERE basket_id=" + str(basket_id) + " AND product_id = " + str(
        product_id_)
    cursor.execute(sql_query)


def delete_all_basket_entries_for_shopper(db_, basket):
    for element in basket:
        delete_shopper_basket(db_, element[0])
        delete_basket_contents(db_, element[0], element[1])


def get_basket(db_, shopper_id_):
    sql_query1 = "select basket_id from shopper_baskets where shopper_id=" + str(shopper_id_)
    sql_query2 = "select * from basket_contents where basket_id in (" + sql_query1 + ")"
    cursor = db_.cursor()
    result = cursor.execute(sql_query2)
    basket = result.fetchall()
    return basket


def get_product_description(db_, product_id_):
    sql_query2 = "select product_description from products where product_id =" + str(product_id_)
    cursor = db_.cursor()
    result = cursor.execute(sql_query2)
    product_description = result.fetchone()
    return product_description


def print_basket(db_, shopper_id_):
    basket = get_basket(db_, shopper_id_)
    if len(basket) > 0:
        print("\nBasket Contents")
        print("---------------------\n")
        print("{:<50} {:<18} {:<5} {:<12} {:<15}".format('Product Description', 'Seller Name', 'Qty', 'Price', 'Total'))
        print("")
    else:
        print("\nYour Basket is Empty")
        return

    cart_total = 0
    for element in basket:
        p_id = element[1]
        s_id = element[2]
        qty = int(element[3])
        price = float(element[4])
        total_price = qty * price
        cart_total = cart_total + total_price
        p_desc = get_product_description(db_, p_id)
        seller = get_seller_details(db_, s_id)
        print("{:<50} {:<18} {:<5} £ {:<10} £ {:<12}".format(p_desc[0], str(seller[2]), qty, price, total_price))

    print("\n")
    print("{:<50} {:<18} {:<5}  {:<10}  £ {:<12}".format("", "Basket Total", "", "", cart_total))

    print("\n")


def get_shopper_delivery_addresses(db_, shopper_id_):
    sql_query1 = "select delivery_address_id from shopper_orders where shopper_id=" + str(shopper_id_)
    sql_query2 = "select * from shopper_delivery_addresses where delivery_address_id in (" + sql_query1 + ")"
    cursor = db_.cursor()
    result = cursor.execute(sql_query2)
    shopper_delivery_addresses = result.fetchall()
    return shopper_delivery_addresses


def get_payment_cards(db_, shopper_id_):
    sql_query1 = "select payment_card_id from shopper_orders where shopper_id=" + str(shopper_id_) + " ORDER BY " \
                                                                                                     " order_date DESC "
    sql_query2 = "select * from shopper_payment_cards where payment_card_id in (" + sql_query1 + ")"
    cursor = db_.cursor()
    result = cursor.execute(sql_query2)
    payment_cards = result.fetchall()
    return payment_cards


def get_delivery_addresses_options(shopper_delivery_addresses):
    delivery_addresses_options = []
    for address in shopper_delivery_addresses:
        temp_address = [str(x) for x in address[1:]]
        st = ' , '.join(temp_address)
        temp = [address[0], st]
        delivery_addresses_options.append(temp)
    return delivery_addresses_options


def get_new_delivery_address():
    print("As you have not placed any order, you will need to enter your delivery address\n")
    while True:
        address_1 = input("Enter the delivery address line 1 :")
        address_2 = input("Enter the delivery address line 2 :")
        address_3 = input("Enter the delivery address line 3 (optional) :")
        country = input("Enter the delivery country :")
        post_code = input("Enter the delivery post code :")

        if address_1 == "" or address_2 == "" or country == "" or post_code == "":
            print("Only address line 3 is Optional!")
            continue
        new_delivery_address = [address_1, address_2, address_3, country, post_code]
        return new_delivery_address


def add_shopper_order(db_, row):
    cursor = db_.cursor()
    if len(row) > 2:
        sql_query1 = "INSERT INTO shopper_orders (shopper_id,delivery_address_id,payment_card_id,order_date,order_status) " \
                     "VALUES(" + str(row[0]) + "," + str(row[1]) + "," + str(
            row[2]) + "," + " DateTime('now'), 'Placed') "
        cursor.execute(sql_query1)
        last_ins_id1 = cursor.lastrowid
        return last_ins_id1

    return 0


def add_ordered_products(db_, order_id, basket_):
    cursor = db_.cursor()
    if len(basket_) > 0:
        for basket_row in basket_:
            sql_query1 = "INSERT INTO ordered_products (order_id,product_id,seller_id,quantity,price," \
                         "ordered_product_status) " \
                         "VALUES(" + str(order_id) + "," + str(basket_row[1]) + "," + str(basket_row[2]) + "," + str(
                basket_row[3]) + "," + str(basket_row[4]) + ",'Placed') "
            cursor.execute(sql_query1)


def get_card_options(cards):
    cards_options = []
    for card in cards:
        st = str(card[1]) + " ending in " + str(card[2])
        temp = [card[0], st]
        cards_options.append(temp)
    return cards_options


def get_new_card():
    print("As you have not placed any order, you will need to enter your payment card details\n")
    while True:
        card_type = input("Enter the card type (Visa, Mastercard or AMFX ) :")
        card_num = input("Enter the 16-digit card number :")
        if card_type == "" or card_num == "":
            print("Please give all data")
            continue
        new_card = [card_type, card_num]
        return new_card


def add_payment_card(db_, new_card):
    cursor = db_.cursor()
    sql_query = "INSERT INTO shopper_payment_cards(card_type,card_number) VALUES ('" + str(new_card[0]) + "','" + str(
        new_card[1]) + "')"
    cursor.execute(sql_query)
    last_ins_id = cursor.lastrowid
    return last_ins_id


def add_delivery_address(db_, new_delivery_address):
    cursor = db_.cursor()
    sql_query = "INSERT INTO shopper_delivery_addresses" \
                "(delivery_address_line_1,delivery_address_line_2,delivery_address_line_3,delivery_county," \
                "delivery_post_code) " \
                "VALUES ('" + str(new_delivery_address[0]) + "','" + str(new_delivery_address[1]) + "','" + str(
        new_delivery_address[2]) + "','" + str(new_delivery_address[3]) + "','" + str(new_delivery_address[4]) + "')"
    cursor.execute(sql_query)
    last_ins_id = cursor.lastrowid
    return last_ins_id


def do_new_checkout(db_, shopper_id_, basket_):
    new_delivery_address = get_new_delivery_address()
    new_card = get_new_card()

    new_delivery_address_id = add_delivery_address(db_, new_delivery_address)
    new_card_id = add_payment_card(db_, new_card)
    if new_card_id > 0 and new_delivery_address_id > 0:
        shopper_order_row = [shopper_id_, new_delivery_address_id, new_card_id]
        order_id = add_shopper_order(db_, shopper_order_row)
        add_ordered_products(db_, order_id, basket_)
        delete_all_basket_entries_for_shopper(db_, basket_)


def do_more_than_one_address_checkout(db_, shopper_id_, shopper_delivery_addresses, basket_):
    delivery_addresses_options = get_delivery_addresses_options(shopper_delivery_addresses)
    delivery_address_id = _display_options(delivery_addresses_options, "Delivery Addresses", "delivery addresses")
    cards = get_payment_cards(db_, shopper_id_)
    if len(cards) == 0:
        return

    if len(cards) > 1:
        card_options = get_card_options(cards)
        card_id = _display_options(card_options, "Payment Cards", "payment card")
        if card_id > 0:
            shopper_order_row = [shopper_id_, delivery_address_id, card_id]
            order_id = add_shopper_order(db_, shopper_order_row)
            add_ordered_products(db_, order_id, basket_)
            delete_all_basket_entries_for_shopper(db_, basket_)
    elif len(cards) == 1:
        print("Card number :", str(cards[0][2]))
        card_id = cards[0][0]
        if card_id > 0:
            shopper_order_row = [shopper_id_, delivery_address_id, card_id]
            order_id = add_shopper_order(db_, shopper_order_row)
            add_ordered_products(db_, order_id, basket_)
            delete_all_basket_entries_for_shopper(db_, basket_)


def do_only_one_address_checkout(db_, shopper_id_, shopper_delivery_addresses, basket_):
    print("Delivery Address :")
    address = shopper_delivery_addresses[0]
    temp_address = [str(x) for x in address[1:]]
    st = ' , '.join(temp_address)
    print(st)
    cards = get_payment_cards(db_, shopper_id_)
    print("Card number :", str(cards[0][2]))
    card_id = cards[0][0]
    if card_id > 0:
        shopper_order_row = [shopper_id_, address[0], card_id]
        order_id = add_shopper_order(db_, shopper_order_row)
        add_ordered_products(db_, order_id, basket_)


def do_checkout(db_, shopper_id_, basket_):
    shopper_delivery_addresses = get_shopper_delivery_addresses(db_, shopper_id_)
    if len(shopper_delivery_addresses) > 1:
        do_more_than_one_address_checkout(db_, shopper_id_, shopper_delivery_addresses, basket_)
    elif len(shopper_delivery_addresses) == 1:
        do_only_one_address_checkout(db_, shopper_id_, shopper_delivery_addresses, basket_)
    else:
        do_new_checkout(db_, shopper_id_, basket_)


def checkout_basket(db_, shopper_id_):
    basket = get_basket(db_, shopper_id_)
    if len(basket) > 0:
        print_basket(db_, shopper_id_)
        try:
            do_checkout(db_, shopper_id, basket)
            db_.commit()
        except:
            db_.rollback()


    else:
        print("Your basket is empty !")
        return


if __name__ == '__main__':
    shopper_id = input("Enter shopper ID : ")
    db = db_connect()
    shopper_name = login(db, shopper_id)
    if shopper_name:
        print("Hi," + str(shopper_name) + " Welcome to ORINOCO")
        while True:
            print_menu()
            try:
                menu_number = int(input("Enter a number from 1 to 5 : "))
            except:
                print("Please enter a number!")
                continue

            if menu_number == 1:
                display_your_order_history(db, shopper_id)
            elif menu_number == 2:
                add_item_to_basket(db, shopper_id)
            elif menu_number == 3:
                print_basket(db, shopper_id)
            elif menu_number == 4:
                checkout_basket(db, shopper_id)
                pass
            elif menu_number == 5:
                break
            else:
                print("Enter a valid number")
    else:
        print("Please enter a valid shopper ID.")

    db.close()
