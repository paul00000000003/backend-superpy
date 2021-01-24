I didn't confine myself to mentioning just 3 technical details which I found worthwhile mentioning. I'll stick to the most important ones though which are :
- parsing
- manipulation of strings 
- manipulation of dates 

- parsing. The topic of parsing CLI commands seems to be well elaborated in python. Also for this case parsing 
  should be discussed by a number of subtopics. I'll confine myself to :
  - subparsing. Subparsing creates the possibility of handling various positional arguments. With respect to 
    parsing python differentiates between positional (without preceding hyphens) and optional arguments (with 
    preceding hyphens). If several possibilities exist within an argument a subparser needs to be created for 
    each positional argument (eg sell,buy,report). If a cli contains more than one consecutive positional 
    arguments subparsers need to be created on several levels e.g. report inventory. The last argument in a cli 
    always needs to be an optional argument.     
  - arguments with no values. Arguments can be defined by means of a type such as int,float,str. An argument can 
    have none, one and multiple values. If the number is one only the type should be specified and no other \
    action needs to be taken. If more than one value is needed/given the keyword nargs should be used. If no 
    value is given this should be solvied by defining action="store_true". The latter implies that if the 
    argument is present the value True will be stored in the namespace for the cli. If it's absent the value 
    False will be stored. Hence its value can be interpreted as a boolean and specific actions can be taken on 
    the basis of its value
  - add-help. Python sets this variable to the default action true. When the program will then be run with the 
    argument -h or --help it will return the first positional and optional values for the arguments. However in 
    our case more options and branches with several cli commands need to be elaborated. Hence this value needs to 
    be set to False in the declaration of the parser. Doing this makes it possible to return a better text upon 
    using the help function. 

-   manipulation of strings. There's much to with respect to this topic so I'll mention just a few highlights. 
    1. Fractional numbers. Any computational language uses the . for decimals. However most of our customers will 
       probably not come from any other country than the Netherlands. The representation of a number in a report
       is by default string (actually funny if you think about this when you're writing a number in a report. Why
       does that also work for none strings). I chose to make the decimal . into a ,. This has large implications
       for the program because every time a value is written or read translation needs to take place.
    2. Since we're in Holland all dates in reporting are represented by dd-mm-yyyy to make it easy to read. Excel
       tends to cut off preceding 0 in the dates. While testing it's ok to save the content in the files sold.csv 
       and bought.csv. The length of the string to be converted to a date is checked and preceded by 0 in the 
       case of 0 (Dutch people call this hufterproef)
    3. Unlike SQL javascript and python don't use a superficial key value for a table. After all we're using OOP 
       and not a relational database. This is a bit of a bold statement and can easily be discussed. However 
       there is a work around when you're using nesting. Take e.g. the solution I used to increase the count when 
       assembling the data for the inventory. When using nesting the python value is actually the python key for 
       the next level. Hence I'm using {product_name:{expiration_date:{buy_price:number}}}. 
-   manipulation of dates. Strings containing dates are converted into values (datetime.striptime) and vice 
    versa (value.strftime("%d-%m-%Y)). This is a very nice but well known feature. The value for the last day 
    of the month is a bit more complicated. It's used in this program in order to convert a month value to 
    a date value. The first day is easily computed since you just have to add 01 to it. The last date is 
    computed as follows. Every month has always got a day 28 in it. To get the last date of the month just add 
    4 days to it using timedelta and then subtract the day value of the date you got as an answer. 

Apologies for using more than 300 words to describe fun technical issues. 