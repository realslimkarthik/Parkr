import sys
from datetime import datetime
from random import randrange, seed

seed(293)

def get_month():
    return randrange(4, 6)


def get_day(month):
    if month == 4:
        day = randrange(1, 31)
    elif month == 5:
        day = randrange(1, 6)
    return day


def get_hour():
    return randrange(0, 24)


def get_minute_or_second():
    return randrange(0, 60)


def get_microsecond():
    return randrange(0, 1000000)


def get_node():
    return str(randrange(7001, 7041))


def generate_input_line():
    year = 2012
    input_line = ''
    month = get_month()
    day = get_day(month)
    hour = get_hour()
    minute = get_minute_or_second()
    second = get_minute_or_second()
    microsecond = get_microsecond()
    origin = get_node()
    destination = get_node()
    while destination == origin:
        destination = get_node()
    date_time = datetime(year, month, day, hour, minute, second, microsecond)
    date_time_str = date_time.strftime('%Y-%m-%d %H:%M:%S.%f')
    input_line = ','.join([origin, destination, date_time_str]) + '\n'
    return input_line


def main():
    iterations = int(sys.argv[1])
    file_name = sys.argv[2]
    input_data = ['origin,destination,time\n']
    for i in range(iterations):
        line_data = generate_input_line()    
        input_data.append(line_data)

    with open(file_name, 'w') as input_file:
        input_file.writelines(input_data)


if __name__ == '__main__':
    main()