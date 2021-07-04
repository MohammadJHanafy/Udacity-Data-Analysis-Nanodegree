import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Please specify a city(chicago, new york city, washington): ")
    while True:
        if(city.lower() not in CITY_DATA.keys()):
            city = input(
                "Please specify a city(chicago, new york city, washington): ")
        else:
            break

    # get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    filter_month = input("Would you like to filter the data by month(y/n): ")
    while True:
        if(filter_month.lower() == 'y'):
            month = input(
                "Please specify a month(january, february, ... , june): ")
            while True:
                if(month.lower() not in months):
                    month = input(
                        "Please enter a valid month(january, february, ... , june): ")
                else:
                    break
        elif(filter_month.lower() == 'n'):
            month = "all"
            break
        else:
            filter_month = input(
                "Would you like to filter the data by month(y/n): ")
        break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'saturday', 'sunday']
    filter_day = input("Would you like to filter the data by day(y/n): ")
    while True:
        if(filter_day.lower() == 'y'):
            day = input(
                "Please specify a day(monday, tuesday, ... , sunday): ")
            while True:
                if(day.lower() not in days):
                    day = input(
                        "Please enter a valid day(monday, tuesday, ... , sunday): ")
                else:
                    break
        elif(filter_day.lower() == 'n'):
            day = "all"
            break
        else:
            filter_day = input(
                "Would you like to filter the data by day(y/n): ")
        break

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city.lower()])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        days = ['monday', 'tuesday', 'wednesday',
                'thursday', 'friday', 'saturday', 'sunday']
        day = days.index(day.lower())
        df = df.loc[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = (df['month'].mode()[0]) - 1
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    print("Most common travelling month: {}".format(months[most_common_month].title()))

    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    if(most_common_day == 0):
        most_common_day = "Monday"
    elif(most_common_day == 1):
        most_common_day = "Tuesday"
    elif(most_common_day == 1):
        most_common_day = "Wednesday"
    elif(most_common_day == 1):
        most_common_day = "Thursday"
    elif(most_common_day == 1):
        most_common_day = "Saturday"
    elif(most_common_day == 1):
        most_common_day = "Tuesday"
    else:
        most_common_day = "Sunday"
    print("Most common  travelling day: {}".format(most_common_day))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    if(most_common_hour > 12):
        ampm = "PM"
        hour = most_common_hour - 12
    else:
        ampm = "AM"
        hour = most_common_hour
    print("Most common travelling hour: {} = {} {}".format(most_common_hour, hour, ampm))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_ss = df['Start Station'].mode()[0]
    print("Most Common Start Station: {}".format(most_common_ss))

    # display most commonly used end station
    most_common_es = df['End Station'].mode()[0]
    print("Most Common End Station: {}".format(most_common_es))

    # display most frequent combination of start station and end station trip
    df["Start/End Stations"] = df["Start Station"] + "  ==>  " + df["End Station"]
    most_common_comb = df['Start/End Stations'].mode()[0]
    print("Most Common Trip: {}".format(most_common_comb))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum()
    print("The total Duration: {} Sec = {} Hrs = {} Days".format(
        total_duration, (total_duration/3600), (total_duration/86400)))

    # display mean travel time
    average_duration = df['Trip Duration'].mean()
    print("The average Duration: {} Sec = {} Hrs = {} Days".format(
        average_duration, (total_duration/3600), (total_duration/86400)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Count of user types: \n{}".format(user_types))

    # Display counts of gender
    if('Gender' not in df.columns):
        print('There are no gender data available for this city.')
    else:
        genders = df['Gender'].value_counts()
        print("Count of Genders: \n{}".format(genders))

    # Display earliest, most recent, and most common year of birth
    if('Birth Year' not in df.columns):
        print('There are no birth year data available for this city.')
    else:
        most_common_birthyear = int(df['Birth Year'].mode()[0])
        earliest_birthyear = int(df['Birth Year'].min())
        mostrecent_birthyear = int(df['Birth Year'].max())
        print("Most common birth year: {}, while the most recent is: {} and the earliest is: {}".format(
            most_common_birthyear, mostrecent_birthyear, earliest_birthyear))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def data_display(df):
    """Displays the raw data 5 rows at a time upon request by the user"""

    display_data = input(
        "Would you like to see the first 5 rows of the raw data about the city(y/n): ")
    counter = 0
    while True:
        if(display_data.lower() == 'n'):
            break
        elif(display_data.lower() == 'y'):
            print(df[counter:(counter+5)])
            counter += 5
            display_data = input(
                "Would you like to see the next 5 rows of the raw data about the city(y/n): ")
        else:
            display_data = input(
                "Would you like to see the first 5 rows of the raw data about the city(y/n): ")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        data_display(df)

        restart = input('\nWould you like to restart? (y/n).\n')
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
    main()
