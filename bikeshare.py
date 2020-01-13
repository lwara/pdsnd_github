import time
import pandas as pd
import numpy as np
import json

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june'] #the required months to filter from

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
    
    
    while True:
        city=input('Now from which city do you want to start viewing ? chicago, new york city OR washington :').lower()
        if city not in ('chicago','new york city','washington'):
            print('sorry your input was wrong, please enter chicago OR new york city OR washington..')
            continue
        else:
            break   
        

    # filter by month , day or Both
    while True:
        # get user input for month (all, january, february, ... , june)
        month= input('How would you like to filter your data ?All,  January..., June  :').lower()
        if month not in ('all','january','february','march','april','may','june'):
            print('wrong input, please enter month OR day Or both...')
            continue
        else:
            break
    while True:
         # get user input for day of week (all, monday, tuesday, ... sunday)
         day= int(input('Now choose a specific day you want to view your data ? please give it as an integer.. :'))
         if day not in (1,2,3,4,5,6,7):
             print ('wrong input, please enter an integer only...')
             continue
         else :
             break
            

    print('*'*40)
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
    #lead data from an external file 
    df = pd.read_csv(CITY_DATA[city])#get the csv file

    # now get the start time and convert it to datetime so that you easily get the month and day
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    #get the day of the week
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    
    #get the hours...this is going to be used to filter the most common start hour
    df['hour'] = df['Start Time'].dt.hour

    #now get the month
    if month != 'all':
       month =  MONTHS.index(month) + 1 # get the correct month
       df = df[ df['month'] == month ]

    #now get the day
    if day != 'all':         
       df = df[ df['day_of_week'] == day]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].value_counts().idxmax()
    print("The most common month found is :", most_common_month)

    # display the most common day of week
    the_most_common_day_of_week = df['day_of_week'].value_counts().idxmax()
    print('The most common day of week is :', the_most_common_day_of_week)


    # display the most common start hour
    the_most_common_start_hour = df['hour'].value_counts().idxmax()
    print("The most common start hour is :", the_most_common_start_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('*'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    the_most_common_start_station = df['Start Station'].value_counts().idxmax()
    print("The most commonly used Start Station is :", the_most_common_start_station)


    # display most commonly used end station
    the_most_common_end_station = df['End Station'].value_counts().idxmax()
    print("The most commonly used End Station is :", the_most_common_end_station)


    # display most frequent combination of start station and end station trip
    the_most_common_start_end_station = (df["Start Station"] + "-"+ df['End Station']).value_counts().idxmax()
    print("The most commonly used start station and end station : {}, ".format(the_most_common_start_end_station))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('*'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    the_total_travel_time=df['Trip Duration'].sum()
    print('\n The most Travel Time is :', the_total_travel_time)


    # display mean travel time
    the_total_mean_travel_time=df['Trip Duration'].mean()
    print('\n The mean Travel Time is  :', the_total_mean_travel_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('*'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    the_number_of_user_types=df['User Type'].value_counts()
    print('\n The number of User Types is :', the_number_of_user_types)


    # Display counts of gender
    if 'Gender' in df.columns:
        counts_of_gender=df['Gender'].value_counts()
        print('\n The number of Gender found is  :', counts_of_gender)


    if 'Birth Year' in df.columns:
        # Display earliest, most recent, and most common year of birth
        birth_year = df['Birth Year']
        # the most common birth year
        the_most_common_year = birth_year.value_counts().idxmax()
        print("The most common birth year:", the_most_common_year)
        # the most recent birth year
        most_recent = birth_year.max()
        print("The most recent birth year:", most_recent)
        # the most earliest birth year
        the_earliest_year = birth_year.min()
        print("The most earliest birth year:", the_earliest_year)
    



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('*'*40)

def display_individual_data(df):
    """Displays Individual bikeshare data."""
    row_length = df.shape[0]

    # iterate from 0 to the number of rows in steps of 3
    for i in range(0, row_length, 3):

        yes = input('\nWould you like to examine the particular user trip data? Type \'yes\' or \'no\'\n> ')
        if yes.lower() != 'yes':
            break

        # retrieve and convert data to json format         
        row_data = df.iloc[i: i + 3].to_json(orient='records', lines=True).split('\n')
        #now retrive the data one by one
        for row in row_data:
            # pretty print each user data
            parsed_row = json.loads(row)
            json_row = json.dumps(parsed_row, indent=2)
            print(json_row)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        
        display_individual_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
