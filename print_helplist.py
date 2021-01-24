from rich.console import Console
from rich.table import Table
from rich.style import Style


def print_helplist():
    console = Console()
    console.print("Layout of possible arguments", style="red on white ")
    print("Apart from possibilities to set the date four categories of functional arguments are included in the program")
    print("among which : buy, sell, report, stats. If no illucidation for a part of the argument is given, please copy it literally")
    print("In this explication I use 'referred date'. This is a date which can be set as reference to today")
    print("Every argument should be preceded by the call on the program : py superpy.py")
    print("")
    console.print("Functions to set the date", style="red on white")
    table = Table(show_header=True, header_style="bold", show_lines=True)
    table.add_column("Argument", style="dim", width=85)
    table.add_column("Elucidation", style="dim", width=100)
    table.add_row("--advance-time x",
                  "x should be an integer marking the number of days in which the referred date is forwarded")
    table.add_row("--reset-date",
                  "resets referred date to system date ")
    console.print(table)

    console.print("buy and sell arguments ", style="red on white")
    table = Table(show_header=True, header_style="bold", show_lines=True)
    table.add_column("Argument", style="dim", width=85)
    table.add_column("Elucidation", style="dim", width=100)
    table.add_row("buy --product-name xxx --price xxx.yy --expiration-date yyyy-mm-dd",
                  "xxx: product e.g. orange, bread, milk \nxxx.yy: price as float such as 1.98, 10.76 etc.\nyyyy-mm-dd : date format as year(y),month(m) and d(day)")
    table.add_row("sell --product-name xxxxxx --price xxx.yy",
                  "xxxxx : product e.g. milk,bread,apple\nxxx.yy: price e.g. 10.95,1.45")
    console.print(table)

    console.print("reporting", style="red on white")
    table = Table(show_header=True, header_style="bold", show_lines=True)
    table.add_column("Argument", style="dim", width=85)
    table.add_column("Elucidation", style="dim", width=100)
    table.add_row("report inventory --now",
                  "--now current referred date")
    table.add_row("report inventory --yesterday",
                  "--yesterday : day before the referred date")
    table.add_row("report inventory --date yyyy-mm-dd",
                  "the inventory can only be computed for a certain day.\nDate is flexible and should be report as year(y)-month(m)-d(ay)")
    table.add_row("report profit --today",
                  "today : the referred date")
    table.add_row("report profit --yesterday",
                  "yesterday : day before the referred date")
    table.add_row("report profit --date yyyy-mm",
                  "Profit can also be computed for an entire month\nThe month is written as year(y)-month(m)")
    table.add_row("report report revenue --today",
                  "today : referred date")
    table.add_row("report report revenue --yesterday",
                  "yesterday : day before the referred date")
    table.add_row("report revenue --date yyyy-mm",
                  "The revenue can be reported for an entire month\nThe month is written as year(y)-month(m)")
    console.print(table)

    console.print(
        "statistics (xxxx : product such as apple, orange, banana, tomotoe. yyyy-mm-dd : dateformat (y(year)-m(month)-d(day))", style="red on white")
    table = Table(show_header=True, header_style="bold", show_lines=True)
    table.add_column("Argument", style="dim", width=85)
    table.add_column("Elucidation", style="dim", width=100)
    table.add_row("stats --product-name xxxxx --start-date yyyy-mm-dd --end-date yyyy-mm-dd --number",
                  "fluctuation of sold numbers on different dates")
    table.add_row("stats --product-name xxxxx --start-date yyyy-mm-dd --end-date yyyy-mm-dd --buy-price",
                  "fluctuation of the average daily price for which the goods are bought")
    table.add_row("stats --product-name xxxxx --start-date yyyy-mm-dd --end-date yyyy-mm-dd --sell-price",
                  "fluctuation of the average price for which the goods are sold")
    table.add_row("stats --product-name xxxxx --start-date yyyy-mm-dd --end-date yyyy-mm-dd --revenue",
                  "fluctuation of the daily revenue")
    table.add_row("stats --product-name xxxxx --start-date yyyy-mm-dd --end-date yyyy-mm-dd --profit",
                  "fluctuation of the daily profit")
    console.print(table)

    console.print(
        "For details on functional specifications please read superpy.py.docx ", style="red on white")
    print("dependencies : matploblib 3.3.3")
    print("               rich 9.8,2")
    print("               argparse 1.4.0")
    print("               datetime 4.3")
    print("               python 3.9")
