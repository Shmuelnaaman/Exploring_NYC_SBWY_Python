from pandas import *
from ggplot import *
import numpy as np


def normalize_features(array):
    #   Normalize the features in the data set.

    array_normalized = (array-array.mean())/array.std()
    mu = array.mean()
    sigma = array.std()

    return array_normalized, mu, sigma


def plot_weather_temp_time(turnstile_weather):

    '''
    plot_weather_data is passed a dataframe called turnstile_weather.
    Use turnstile_weather along with ggplot to make another data visualization
    focused on the MTA and weather data we used in Project 3.

    Make a type of visualization different than what you did in the previous
    exercise. Try to use the data in a different way (e.g., if you made a
    lineplot concerning ridership and time of day in exercise #1, maybe look at
    weather and try to make a histogram in this exercise). Or try to use
    multiple encodings in your graph if you didn't in the previous exercise.

    You should feel free to implement something that we discussed in class
    (e.g., scatterplots, line plots, or histograms) or attempt to implement
    something more advanced if you'd like.

    Here are some suggestions for things to investigate and illustrate:
     * Ridership by time-of-day or day-of-week
     * How ridership varies by subway station
     * Which stations have more exits or entries at different times of day

    If you'd like to learn more about ggplot and its capabilities, take
    a look at the documentation at:
    https://pypi.python.org/pypi/ggplot/

    You can check out the link
    https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv
    to see all the columns and data points included in the turnstile_weather
    dataframe.

    However, due to the limitation of our Amazon EC2 server, we will give you 
    only about 1/3 of the actual data in the turnstile_weather dataframe.
    '''

    dataframe = pandas.read_csv('turnstile_data_master_with_weather.csv')

    param = 'meantempi'

    min_par = int(min(dataframe[param]))
    max_par = int(max(dataframe[param]))
    dif_par = abs((min_par - max_par) / 8)
    dif_par = 3

    # fill NA values
    dataframe.fillna(1)

    # aggregaate data acording to hour and temp
    dataframe['mntmp'] = (np.digitize(dataframe[param],
                          range(min_par, max_par, dif_par)) *
                          dif_par) + (min_par-2)
    dataframe['mnHr'] = (np.digitize(dataframe['Hour'],
                         range(0, 23, 3)) * 3) - 1

    # average entries acording to  Houer and temp
    Dyl_avg = dataframe.groupby(['mnHr', 'mntmp'],
                                as_index=False)['ENTRIESn_hourly'].agg([np.mean])

    # normalize entries for each hour
    UN_MX = Dyl_avg.groupby(level=['mnHr'],
                            as_index=False).apply(lambda t : (t.ENTRIESn_hourly['mean'] -
                            t.ENTRIESn_hourly['mean'].mean()) / t.ENTRIESn_hourly['mean'].std()).reset_index()
    # normalize entries for each temp

    # UN_MX=  Dyl_avg.groupby(level=['mntmp'],
    #    as_index=False).apply(lambda t: (t.ENTRIESn_hourly['mean']-
    # t.ENTRIESn_hourly['mean'].mean())/t.ENTRIESn_hourly['mean'].std()).reset_index()

    # print UN_MX
    qsec = abs(UN_MX['mean'])

    trsh = 1
    UN_MX1 = UN_MX
    UN_MX1.loc[UN_MX['mean'] >= trsh, 'mean'] = trsh
    UN_MX1.loc[abs(UN_MX['mean']) < trsh, 'mean'] = 0
    UN_MX1.loc[UN_MX['mean'] <= -trsh, 'mean'] = -trsh

    # alpha= qsec
    # geom_point(aes(colour='blue',size=qsec*500+100,alpha= qsec/max(qsec))) +\
    # scale_color_brewer(type = 'diverging', palette = 3) +\
    # scale_colour_gradient(low="blue", mid="#22FF00", high="red")+\

    plot = ggplot(UN_MX1, aes(x='mnHr', y='mntmp', color='mean')) +\
    geom_point(aes(size=qsec*700)) + \
    scale_x_continuous(name="Time [H]", breaks=range(0, 24, 2), size=30) +\
    scale_y_continuous(name=param, breaks=range(min_par, max_par, dif_par), size=30) +\
    ggtitle("Hourly ENTRIES as function of Temp normalize by the hourly variation") +\
    xlim(0, 24) +\
    ylim(min_par, max_par)

    return plot
