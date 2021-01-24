import csv
from datetime import date, datetime, timedelta
import sys
import os
from get_highest_number import get_new_id


def get_items_to_be_sold():
    # Doel : haal de lijst te verkopen items op. Deze staat in de file sold.csv
    items_to_be_sold = []
    try:
        with open('./bought.csv', newline='') as csvfile:
            bought_item = csv.reader(csvfile, delimiter=';', quotechar='|')
            for row in bought_item:
                if row[0].isdigit():  # Referentie aan aankoop is altijd een integer
                    price = float(row[3].replace(",", "."))
                    # Opslag in excel veroorzaakt dat nul van datum wordt afgekapt
                    if len(row[2]) == 7:
                        row[2] = "0"+row[2]
                    if len(row[4]) == 7:
                        row[4] = "0"+row[4]
                    items_to_be_sold.append({"id": int(row[0]),
                                             "product_name": row[1],
                                             "buy_date": datetime.strptime(row[2], '%d%m%Y'),
                                             "buy_price": price,
                                             "expiration_date": datetime.strptime(row[4], '%d%m%Y'),
                                             "sold": row[5]})
        csvfile.close()
    except:
        None
    return items_to_be_sold


def get_oldest_sellable_item(items_to_be_sold, args, dates):
    # normaliter zal dit ook het oudste verkochte item zijn. Als een ouder produkt eerder is bedorven dan is dat natuurlijk niet zo.
    item_found = "N"
    bought_id = 0
    index = -1
    index_found = -1
    bought_price = 0
    # zoek match tussen verkoopopdracht en aanwezige inventaris die nog niet is bedorven. Het oudste product wordt het eerst verkocht
    for item in items_to_be_sold:
        index = index+1
        if (item["product_name"] == args.product_name and item["expiration_date"] >= dates.today and item["sold"] == "N" and item_found == "N"):
            index_found = index
            item_found = "Y"
            bought_id = item["id"]
            bought_price = item["buy_price"]
    return bought_id, bought_price, index_found


def rewrite_bought_file(items_to_be_sold):
    # omdat je van tevoren niet weet welk item opnieuw is gewijzigd, moet de aankoopfile worden herschreven
    # je wilt de aankoopfile bij een verkoop wijzigen omdat dat makkelijker is voor b.v. de voorraad- en winstberekening
    with open('./bought.csv', 'w', newline='') as csvfile:
        bought_items = csv.writer(csvfile, delimiter=';',
                                  quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for item in items_to_be_sold:
            bought_items.writerow(
                [str(item["id"])]+[item["product_name"]]+[item["buy_date"].strftime("%d%m%Y")]+[str(item["buy_price"]).replace(".", ",")] +
                [item["expiration_date"].strftime("%d%m%Y")]+[item["sold"]])
    csvfile.close()


def add_sold_item_to_list(max_id, bought_id, args, dates, bought_price):
    # Op hoofdniveau van het script vindt rapportage plaats van het succesvol verlopen van de verkoop.
    # Daarom wordt hier de variabele succes hier toegepast.
    success = False
    with open('./sold.csv', 'a', newline='') as csvfile:
        sold_items = csv.writer(csvfile, delimiter=';',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        sold_items.writerow(
            [str(max_id)]+[str(bought_id)]+[args.product_name]+[dates.today_str]+[]+[str(args.price).replace(".", ",")] +
            [str(bought_price).replace(".", ",")])
        success = True
    csvfile.close()
    return success


def process_sell_instruction(args, dates):
    items_to_be_sold = []
    args.product_name = args.product_name.lower()
    # verzamel inventaris (kan hier nog bedorven zijn)
    items_to_be_sold = get_items_to_be_sold()
    bought_id, bought_price, index_found = get_oldest_sellable_item(
        items_to_be_sold, args, dates)
    # zet betrokken product in aankoopfile op verkocht door verkoopdatum in te vullen. Vergemakkelijkt de volgende keer
    # dat deze functie wordt gedraaid en andere rapportage.
    if index_found != -1:
        items_to_be_sold[index_found]["sold"] = dates.today_str
    rewrite_bought_file(items_to_be_sold)

    if bought_id == 0:
        success = False  # variabele voor succesvol verlopen van de verkoop
    else:
        max_id = get_new_id("sold.csv")
        success = add_sold_item_to_list(
            max_id, bought_id, args, dates, bought_price)
    return success
