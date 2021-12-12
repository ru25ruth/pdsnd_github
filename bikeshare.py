import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Enter one of these city names (chicago, new york city, washington): ').lower()
        if city in CITY_DATA:
            break
    # Get user input for month (all, january, february, ... , june)
    MONTH_NAME = { 'january','february','march','april','may','june','all' }
    while True:
        month = input('Enter a month of the year(january-june) or "all" for no filtering: ').lower()
        if month in MONTH_NAME:
            break
    # Get user input for day of week (all, monday, tuesday, ... sunday)
    DAY_NAME = {'monday','tuesday','wednesday','thursday','friday','saturday','sunday','all'}
    while True:
        day = input('Enter a day of week(monday-sunday) or "all" for no filtering: ').lower()
        if day in DAY_NAME:
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
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.strftime('%B')
    df['day'] = df['Start Time'].dt.strftime('%A')
    df['hour'] = df['Start Time'].dt.hour

    # filter by months
    if month != 'all':
        month = month.title()
        df = df[df['month'] == month]
    if day != 'all':
        day_of_week = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
        day = day.title()
        df = df[df['day'] == day]
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    print("The most common month: ", df['month'].mode()[0])
    # Display the most common day of week
    print("The most common day of week: ", df['day'].mode()[0])
    # Display the most common start hour
    print("The most common start hour:",df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    print('The most commonly used start station: ', df['Start Station'].mode()[0])
    # Display most commonly used end station
    print('The most commonly used end station: ', df['End Station'].mode()[0])
    # Display most frequent combination of start station and end station trip
    df['conbination'] = df['Start Station'] +' and '+ df['End Station']
    print('The most popular station conbination : ', df['conbination'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_time = df['Trip Duration'].sum()
    print('Total travel time: {}h {}m {}s'.format(int(total_time//3600), int(total_time%3600//60), int(round((total_time%3600)%60))))
    # Display mean travel time
    avarage_time = df['Trip Duration'].mean()
    print('Avarage travel time: {}h {}m {}s'.format(int(avarage_time//3600), int(avarage_time%3600//60), int(round((avarage_time%3600)%60))))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("user_types:")
    print(user_types)
    # Display counts of gender
    # Keyerror handling
    try:
        gender = df['Gender'].value_counts()
        print("\ngender:")
        print(gender)
    except KeyError:
        print("\nThere is no gender data.")
    # Display earliest, most recent, and most common year of birth
    # Keyerror handling
    try:
        earliest_year = int(df['Birth Year'].min())
        most_recent_year = int(df['Birth Year'].max())
        most_common_year = int(df['Birth Year'].mode())
        print('\nThe earliest year of birth: '+ str(earliest_year))
        print('The most recent year of birth: '+ str(most_recent_year))
        print('The most common year of birth: '+ str(most_common_year))
    except KeyError:
        print("\nThere is no Birth Year data.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def view_data(df):
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
    start_loc = 0
    last_loc = df['Start Time'].count()
    print(last_loc)
    while (start_loc<=last_loc):
        print(df.iloc[start_loc:start_loc+4])
        start_loc += 5
        view_data = input("Do you wish to continue?: ").lower()
        if view_data != "yes":
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        view_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
