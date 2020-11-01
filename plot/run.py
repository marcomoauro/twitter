import plot.plotter as plotter

date = '2020-10-31'

if __name__ == '__main__':
    plotter.tweets('account', date)
    #plotter.tweets('hashtag_ticker', date)
    plotter.tweets('hashtag_company', date)
