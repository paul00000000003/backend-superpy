# Imports
from process_stats_function import process_stats
from make_report_function import make_report_profit, make_report_inventory, make_report_revenue
from sold_function import process_sell_instruction
from get_highest_number import get_new_id
# omdat de verkochte lijst vanuit een aparte file wordt bijgewerkt en de inkooplijst in de hoofdfile en deze functie in beide
# gevallen gelijk is, heb ik er voor gekozen de functie get_new_id in een aparte file te zetten.
from print_helplist import print_helplist
import argparse
import csv
from datetime import date, datetime, timedelta
import sys
import os
from types import SimpleNamespace as Namespace

# Do not change these lines.
__winc_id__ = 'a2bc36ea784242e4989deb157d527ba0'
__human_name__ = 'superpy'

# Your code below this line.


class setDates:
    def __init__(self, day):
        self.today = day
        self.yesterday = self.today+timedelta(days=-1)
        self.fortnight_day = self.today+timedelta(days=2)
        self.tomorrow = self.today+timedelta(days=1)
        self.today_str = self.today.strftime("%d%m%Y")
        self.yesterday_str = self.yesterday.strftime("%d%m%Y")
        self.tomorrow_str = self.tomorrow.strftime("%d%m%Y")
        self.fortnight_day_str = self.fortnight_day.strftime('%d%m%Y')


def parser_():
    parser = argparse.ArgumentParser(add_help=False)
    subparser = parser.add_subparsers(dest='command')
    buy = subparser.add_parser('buy')
    buy.add_argument("--product-name", type=str)
    buy.add_argument("--price", type=float)
    buy.add_argument("--expiration-date", type=str)
    sell = subparser.add_parser('sell')
    sell.add_argument("--product-name", type=str)
    sell.add_argument("--price", type=float)
    report = subparser.add_parser("report")
    subparser_subdivided = report.add_subparsers(dest="command")
    inventory = subparser_subdivided.add_parser("inventory")
    inventory.add_argument("--now", action="store_true")
    inventory.add_argument("--yesterday", action="store_true")
    inventory.add_argument("--date", type=str)
    revenue = subparser_subdivided.add_parser("revenue")
    revenue.add_argument("--yesterday", action="store_true")
    revenue.add_argument("--today", action="store_true")
    revenue.add_argument("--date", type=str)
    profit = subparser_subdivided.add_parser("profit")
    profit.add_argument("--yesterday", action="store_true")
    profit.add_argument("--today", action="store_true")
    profit.add_argument("--date", type=str)
    parser.add_argument("--advance-time", type=int)
    parser.add_argument("--reset-date", action="store_true")
    parser.add_argument("-h", action="store_true")
    parser.add_argument("--help", action="store_true")
    stats = subparser.add_parser("stats")
    stats.add_argument("--product-name", type=str)
    stats.add_argument("--start-date", type=str)
    stats.add_argument("--end-date", type=str)
    stats.add_argument("--number", action="store_true")
    stats.add_argument("--buy-price", action="store_true")
    stats.add_argument("--sell-price", action="store_true")
    stats.add_argument("--profit", action="store_true")
    stats.add_argument("--revenue", action="store_true")
    return parser.parse_args()


def get_referred_date(shift_number_of_days=0, reset="N"):
    # Met deze functie kan de datum een dag worden verzet. Hiervoor wordt een file gebruikt omdat
    # we nog geen link met sql hebben. Het wegschrijfformaat is hetzelfde als hetgeen wordt ingelezen.
    # de eerste parameter dient om de referentiedatum een aantal dagen te verzetten. De tweede om de
    # referentiedatum aan de systeemdatum gelijk te stellen.
    f_get_date = None
    date_validated = "N"
    try:
        f = open('./referred-date.txt', 'r')
        date_line = f.readline().lstrip()[0:10]
        f_get_date = datetime.strptime(date_line, '%d%m%Y')
        f.close()
    except:
        this_moment = datetime.now()
        this_moment_str = this_moment.strftime("%d%m%Y")
        f_get_date = datetime.strptime(this_moment_str, "%d%m%Y")
    if shift_number_of_days != 0:
        f_get_date = f_get_date+timedelta(shift_number_of_days)
    elif reset == "Y":
        f_get_date = datetime.strptime(
            datetime.now().strftime("%d%m%Y"), "%d%m%Y")
    f = open('./referred-date.txt', 'w')
    f.write(f_get_date.strftime("%d%m%Y"))
    f.close()
    date_validated = "Y"
    return f_get_date, date_validated


def process_buy_instruction(args, dates):
    success = False
    max_id = get_new_id("bought.csv")  # algemene functie voor ophalen nieuw id
    # bij de onderstaande opening van de file voegen we een regel toe en daarom gebruiken we de a voor append
    args.product_name = args.product_name.lower()
    with open('./bought.csv', 'a', newline='') as csvfile:
        bought_item = csv.writer(csvfile, delimiter=';',
                                 quotechar='|', quoting=csv.QUOTE_MINIMAL)
        expiration_date = datetime.strptime(args.expiration_date, "%Y-%m-%d")
        if max_id != 0:
            bought_item.writerow([str(max_id)]+[args.product_name]+[dates.today_str] +
                                 [str(args.price).replace('.', ',')] + [expiration_date.strftime("%d%m%Y")]+["N"])
            success = True
    csvfile.close()
    return success


def get_sell_data(start_date, end_date):
    sold_items = []
    total_amount_sold = 0
    try:
        with open('./sold.csv', newline='') as csvfile:
            sold_items_source = csv.reader(
                csvfile, delimiter=';', quotechar='|')
            for row in sold_items_source:
                if row[0].isdigit():
                    if len(row[3]) == 7:  # in excel wordt bij opslag voorloopnul afgekapt
                        row[3] = "0"+row[3]
                    sell_date = datetime.strptime(row[3], "%d%m%Y")
                    if (sell_date >= start_date and sell_date <= end_date):
                        total_amount_sold = total_amount_sold + \
                            float(row[4].replace(",", "."))
                        sold_items.append({"id": row[0],
                                           "buy_id": row[1],
                                           "product_name": row[2],
                                           "sell_price": float(row[4].replace(',', '.')),
                                           "sell_date": sell_date,
                                           "buy_price": float(row[5].replace(',', '.'))})
        csvfile.close()
    except:
        None
    return sold_items, total_amount_sold


def get_bought_data(start_date, end_date):
   # Ophalen van gekochte en bedorven produkten in de periode waarover de winst wordt berekend.
    try:
        purchased_items = []
        total_amount_bought = 0
        with open('./bought.csv', newline='') as csvfile:
            bought_item = csv.reader(csvfile, delimiter=';', quotechar='|')
            for row in bought_item:
                if row[0].isdigit():
                    # bij opslag in excel wordt voorloopnul afgekapt
                    if len(row[2]) == 7:
                        row[2] = "0"+row[2]
                    if len(row[4]) == 7:
                        row[4] = "0"+row[4]
                    buy_date = datetime.strptime(row[2], "%d%m%Y")
                    # check of produkt binnen gecontroleerde periode wordt verkocht
                    if (buy_date >= start_date and buy_date <= end_date):
                        purchased_items.append({"id": row[0],
                                                "product_name": row[1],
                                                "price": float(row[3].replace(",", ".")),
                                                "buy_date": buy_date,
                                                "expiration_date": datetime.strptime(row[4], '%d%m%Y'),
                                                "sold ": row[5]})
                        total_amount_bought = total_amount_bought + \
                            float(row[3].replace(",", "."))
        csvfile.close()
    except:
        None
    return purchased_items, total_amount_bought


def raise_inventory_data(product_name, price_str, expiry_date_str, inventoryData):
    # deze functie werkt de tabel inventoryData bij met een item in het aantal
    # Feitelijk hoeft alleen de geneste value bij te worden gewerkt {product_name:{expiry_date:{price:x}}} waarbij x het aantal items is
    if product_name in inventoryData:
        if expiry_date_str in inventoryData[product_name]:
            if price_str.replace(',', '.') in inventoryData[product_name][expiry_date_str]:
                inventoryData[product_name][expiry_date_str][price_str.replace(",", ".")
                                                             ] = inventoryData[product_name][expiry_date_str][price_str.replace(",", ".")]+1
            else:
                inventoryData[product_name
                              ][expiry_date_str][price_str.replace(",", ".")] = 1
        else:
            inventoryData[product_name][expiry_date_str] = {}
            inventoryData[product_name][expiry_date_str
                                        ][price_str.replace(",", ".")] = 1
    else:
        inventoryData[product_name] = {}
        inventoryData[product_name][expiry_date_str] = {}
        inventoryData[product_name][expiry_date_str
                                    ][price_str.replace(",", ".")] = 1
    return inventoryData


def report_inventory_data_and_report(ref_date):
    # de voorraad wordt altijd op een datum weergegeven. De voorraad is gelijk aan hetgeen er op een bepaalde datum is gekocht maar nog niet is verkocht
    # en nog niet is bedorven. Hetgeen is bedorven behoort dus niet tot de voorraad De voorraad wordt bepaald op de aangegeven dag vlak voor dat de winkel open gaat
    # het formaat van inventoryData wordt {produkt (row[1]): {expiratiedatum(row[4]):{prijs[row[3]]:x(aantal dus geheel getal) enz
    # ref_date : de controledatum
    # row[0]: index
    # row[1]: product_name
    # row[2]: inkoopdatum
    # row[3]: prijs
    # row[4]: expiratiedatum
    # row[5]: N als het nog niet is verkocht anders de verkoopdatum
    inventoryData = {}
    try:
        with open('./bought.csv', newline='') as csvfile:
            bought_item = csv.reader(csvfile, delimiter=';', quotechar='|')
            for row in bought_item:
                if row[0].isdigit():           # bevat de index : index is altijd integer
                    if len(row[2]) == 7:       # bij opslag in spreadsheet wordt voorloopnul afgekapt
                        row[2] = "0" + row[2]  # inkoopdatum
                    if len(row[4]) == 7:       # expiratiedatum
                        row[4] = "0"+row[4]
                    # produkt is voor controledatum gekocht
                    if datetime.strptime(row[2], "%d%m%Y") < ref_date:
                        checkSell = 'N'  # om het produkt op een bepaalde datum op voorraad te hebben moet het of niet verkocht zijn dan
                        # wel pas op een later tijdstip dan het controlemoment voor de voorraad ('s ochtends voor openingstijd)
                        # produkt is nog niet verkocht en is voor de controledatum ook nog niet bedorven
                        if row[5] == "N":
                            if datetime.strptime(row[4], "%d%m%Y") < ref_date:
                                None
                            else:
                                checkSell = "Y"
                        else:
                            if len(row[5]) == 7:
                                row[5] = '0'+row[5]
                            if datetime.strptime(row[5], "%d%m%Y") >= ref_date:
                                checkSell = "Y"  # produkt is pas na controledatum verkocht
                        if checkSell == "Y":
                            inventoryData = raise_inventory_data(
                                row[1], row[3], row[4], inventoryData)
        csvfile.close()
    except:
        print("the file bought.csv couldn't be opened")
    make_report_inventory(inventoryData, ref_date)


def report_revenue_data_and_report(start_date, end_date):
    # revenue : totaal bedrag waarvoor spullen voor betrokken periode zijn verkocht
    sellData = []
    sellData, total_amount_sold = get_sell_data(
        start_date, end_date)  # ophalen van de verkoopdata
    make_report_revenue(sellData, total_amount_sold,
                        start_date, end_date)  # aanmaken rapport


def report_profit_data_and_report(start_date, end_date):
    # winst : totale verkoop - totaal gekocht op die dag - hetgeen er die dag is bedorven en nog niet verkocht en niet op diezelfde dag is gekocht
    # en nog niet op diezelfde dag verkocht staat er bij omdat je de winst over een periode in het verleden wilt kunnen berekenen
    purchased_items = []
    expired_items = []
    sold_items = []
    total_amount_sold = 0
    total_amount_bought = 0
    total_amount_perished = 0
    # ophalen verkoopdata berekening bedrag totaal verkocht
    sold_items, total_amount_sold = get_sell_data(start_date, end_date)
    # ophalen data gekocht en in betrokken periode bedorven goederen.
    purchased_items, total_amount_bought = get_bought_data(
        start_date, end_date)
    make_report_profit(sold_items, purchased_items, expired_items,
                       total_amount_sold, total_amount_bought, total_amount_perished, start_date, end_date)


def call_on_report(args, called_report, dates, ref_today, subparse_version):
    # deze functie dient eigenlijk als doorgeefluik voor de rapportage. De profit en revenue rapporten worden in alle gevallen met een begin-
    # en einddatum aangemaakt. Alleen zijn die voor vandaag en gisteren aan elkaar gelijk en bevatten ze de eerste en laatste dag van de maand
    # voor maandrapportage. De inventory/voorraad heeft altijd maar een controledatum waarvoor de voorraad wordt berekend. Technisch gezien is
    # het argument --now gelijk aan --today
    # zowel de inventory, de revenue als de profit rapportage is bij de optionele parameter --date voor verkeerde invoer robuust gemaakt
    if ref_today == True:
        if subparse_version == "inventory":
            called_report(dates.today)
        else:
            called_report(dates.today, dates.today)
    elif args.yesterday == True:
        if subparse_version == "inventory":
            called_report(dates.yesterday)
        else:
            called_report(dates.yesterday, dates.yesterday)
    else:
        if subparse_version == "inventory":
            date_approved = "Y"
            try:
                date_approved = "N"
                ref_date = datetime.strptime(args.date, "%Y-%m-%d")
                date_approved = "Y"
            except:
                print("Date should have the format yyyy-mm-dd")
            if date_approved == "Y":
                called_report(ref_date)
        else:
            date_range_approved = "N"
            try:
                month = datetime.strptime(args.date, '%Y-%m')
                start_date_str = month.strftime("%Y%m")+'01'
                start_date = datetime.strptime(start_date_str, '%Y%m%d')
                end_date = start_date
                # berekening laatste dag van de maand
                end_date = end_date.replace(day=28)
                end_date = end_date+timedelta(days=4)
                end_date = end_date-timedelta(days=end_date.day)
                date_range_approved = "Y"
            except:
                print("date is not a month in yyyy-mm format")
            # als begin- en einddatum kunnen worden berekend is de variabele data_range_approved gelijk aan Y
            if date_range_approved == "Y":
                called_report(start_date, end_date)


def main():
    args = parser_()
    # Toewijzing van alle argumenten aan de juiste functionaliteit
    if isinstance(args.command, str):
        subparse_version = args.command
    else:
        subparse_version = ""
    if args.advance_time:
        referred_date, date_validated = get_referred_date(args.advance_time)
        if date_validated == "Y":
            print("OK")
        else:
            print("NOK")
    else:
        if args.reset_date:
            # de reset dient ervoor om de referred date naar de systeemdatum om te zetten
            referred_date, date_validated = get_referred_date(0, "Y")
            if date_validated == "Y":
                print("OK")
            else:
                print("NOK")
        else:
            referred_date, date_validated = get_referred_date()
    if args.h == True or args.help == True:
        print_helplist()
    dates = setDates(referred_date)
    if subparse_version == "buy":
        # functie aanroep verwerk koop instructie
        buy = process_buy_instruction(args, dates)
        if buy == True:
            print("OK")
        else:
            print("NOK")
    elif subparse_version == "sell":
        # functieaanroep verwerk sell instructie
        sell = process_sell_instruction(args, dates)
        if sell == True:
            print("Ok")
        else:
            print("ERROR. Product not in stock")
    # functieaanroep call_on_report wordt voor alle rapporten gebruikt. Zowel winst,revenue als inventory
    # merk op dat wat parameters betreft winst en revenue met begin- en einddatum identiek zijn en inventory maar een datum als parameter heeft
    # Verdere overeenkomsten zijn de aanroep met today/now, yesterday. Date voor profit en revenue is een maand in het verleden en inventory is
    # een controledatum
    if subparse_version == "profit":
        call_on_report(args, report_profit_data_and_report,
                       dates, args.today, subparse_version)

    if subparse_version == "revenue":
        call_on_report(args, report_revenue_data_and_report,
                       dates, args.today, subparse_version)

    if subparse_version == "inventory":
        call_on_report(args, report_inventory_data_and_report,
                       dates, args.now, subparse_version)
    # merk op dat process_status diverse verschillende subfuncties heeft, waaronder number, sell_price, buy_price, revenue en profit
    # daarom is er een aparte file voor gebruikt
    if subparse_version == "stats":
        process_stats(args, dates)


if __name__ == '__main__':
    main()
