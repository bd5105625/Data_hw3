import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
# from pmdarima.arima import auto_arima
# from pmdarima.arima import arima
# from pmdarima.arima import ADFTest
from statsmodels.tsa.statespace.sarimax import SARIMAX


# You should not modify this part.
def config():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--consumption", default="./sample_data/consumption.csv", help="input the consumption data path")
    parser.add_argument("--generation", default="./sample_data/generation.csv", help="input the generation data path")
    parser.add_argument("--bidresult", default="./sample_data/bidresult.csv", help="input the bids result path")
    parser.add_argument("--output", default="output.csv", help="output the bids path")

    return parser.parse_args()


def output(path, data):
    import pandas as pd

    df = pd.DataFrame(data, columns=["time", "action", "target_price", "target_volume"])
    df.to_csv(path, index=False)

    return


if __name__ == "__main__":
    args = config()

    # gen = pd.read_csv('training_data/target1.csv')
    gen = pd.read_csv(args.generation)
    generation = gen['generation']

    plt.figure(1)
    plt.plot(generation)

    arima_model = SARIMAX(generation, order=(2,1,0), seasonal_order=(1,1,1,24)).fit(disp=0)
    predict_gen = arima_model.predict(start=169, end=192, dynamic=True)
    for i in range(24):
        if predict_gen.iloc[i] < 0:
            predict_gen.iloc[i] = 0
        else:
            predict_gen.iloc[i] = round(predict_gen.iloc[i],2)
    plt.figure(2)
    dataframe = pd.DataFrame(predict_gen, index=generation[-24:].index)
    dataframe.columns = ['Generation']
    plt.plot(generation[-24:])
    plt.plot(predict_gen, 'red')


    ## for consumption predict
    con = pd.read_csv(args.consumption)
    consumption = con['consumption']
    plt.figure(3)
    plt.plot(consumption)

    arima_model = SARIMAX(consumption, order=(2,1,0), seasonal_order=(1,1,1,24)).fit(disp=0)
    print(consumption)
    predict_con = arima_model.predict(start=169, end=192, dynamic=True)
    for i in range(24):
        if predict_con.iloc[i] < 0:
            predict_con.iloc[i] = 0
        else:
            predict_con.iloc[i] = round(predict_con.iloc[i],2)
    plt.figure(4)
    dataframe = pd.DataFrame(predict_con, index=consumption[-24:].index)
    dataframe.columns = ['Generation']
    plt.plot(consumption[-24:])
    plt.plot(predict_con, 'red')
    data = []
    difference = predict_gen-predict_con
    previous = gen['time'].iloc[-1].split(' ')[0].split('-')[-1] #previous date
    if previous == '31':
        date = '01'
    else:
        date = int(previous)+1
        if date < 10:
            date = '0'+str(date)
    for i in range(24):
        time = gen['time'].iloc[-24+i].split(' ')[1].split(':')[0]
        if difference.iloc[i] < 0:
            data.append(["2018-09-"+date+' '+time+':00:00', "buy", 2.50, abs(difference.iloc[i])])
            data.append(["2018-09-"+date+' '+time+':00:00', "buy", 2.45, abs(difference.iloc[i])])
            data.append(["2018-09-"+date+' '+time+':00:00', "buy", 2.40, abs(difference.iloc[i])])
            data.append(["2018-09-"+date+' '+time+':00:00', "buy", 2.35, abs(difference.iloc[i])])
        elif difference.iloc[i] > 0:
            data.append(["2018-09-"+date+' '+time+':00:00', "sell", 2.50, abs(difference.iloc[i])])
            data.append(["2018-09-"+date+' '+time+':00:00', "sell", 2.45, abs(difference.iloc[i])])
            data.append(["2018-09-"+date+' '+time+':00:00', "sell", 2.40, abs(difference.iloc[i])])
            data.append(["2018-09-"+date+' '+time+':00:00', "sell", 2.35, abs(difference.iloc[i])])
    print(difference)


#2.5 2.45 2.4 2.35 
    # print(predict_gen-predict_con)
    # plt.figure(5)
    # plt.plot(predict_gen,'green')
    # plt.plot(predict_con,'red')
    plt.figure(6)
    plt.plot(predict_gen-predict_con)
    # plt.show()
    # data = [["2018-01-01 00:00:00", "buy", 2.5, 3],
    #         ["2018-01-01 01:00:00", "sell", 3, 5]]
    output(args.output, data)
