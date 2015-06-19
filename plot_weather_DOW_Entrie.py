from pandas import *
from ggplot import *
import numpy as np
import pandas as pd


def plot_weather_DOW_Entrie(turnstile_weather):
    
    '''
    You are passed in a dataframe called turnstile_weather.
    Use turnstile_weather along with ggplot to make a data visualization
    focused on the MTA and weather data we used in assignment #3.
    You should feel free to implement something that we discussed in class
    (e.g., scatterplots, line plots, or histograms) or attempt to implement
    something more advanced if you'd like.

    Here are some suggestions for things to investigate and illustrate:
     * Ridership by time of day or day of week
     * How ridership varies based on Subway station
     * Which stations have more exits or entries at different times of day

    If you'd like to learn more about ggplot and its capabilities, take
    a look at the documentation at:
    https://pypi.python.org/pypi/ggplot/

    You can check out:
    https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv

    To see all the columns and data points included in the turnstile_weather
    dataframe.

    However, due to the limitation of our Amazon EC2 server, we are giving you
    about 1/3 of the actual data in the turnstile_weather dataframe
    '''

    dataframe = pandas.read_csv('turnstile_data_master_with_weather.csv')
    # dataframe =pd.DataFrame(turnstile_weather)

    dataframe.fillna(0)
    # Select Features (try different features!)
    print len(pd.DataFrame(dataframe[dataframe.rain == 1]))
    print len(pd.DataFrame(dataframe[dataframe.rain == 0]))

    # Add day of the week

    dataframe['Dow1'] = dataframe['DATEn'].apply(lambda x:
        datetime.strftime(datetime.strptime(x, "%Y-%m-%d"), "%w"))
    Dyl_avgw1 = dataframe.groupby(['Dow1', 'rain'],
        as_index=False)['ENTRIESn_hourly'].agg([np.mean])

    Dyl_avgwr = (Dyl_avgw1[Dyl_avgw1.index.labels[1] == 1]).reset_index()
    Dyl_avgwn = (Dyl_avgw1[Dyl_avgw1.index.labels[1] == 0]).reset_index()
    Dyl_avgwr['rain1'] = 2*(Dyl_avgwr['ENTRIESn_hourly'] -
        Dyl_avgwn['ENTRIESn_hourly']) / (Dyl_avgwr['ENTRIESn_hourly'] +
        Dyl_avgwn['ENTRIESn_hourly'])

    # Ridership by  day of the week

    plot = ggplot(Dyl_avgwr, aes(x=Dyl_avgwr['Dow1'], y='rain1')) +\
        geom_bar(aes(x=Dyl_avgwr['Dow1'],
                     weight='rain1',
                     width=.8,
                     fill='blue'), stat="identity") +\
        scale_x_continuous(name="Day of the week", breaks=(range(24))) +\
        scale_y_continuous(name="mean ENTRIES") +\
        ggtitle("differance betwee Avg Enteries during rainy and non rainy by hour") +\
        xlim(0, 7) +\
        ylim(-0.25, 0.25)

    return plot
