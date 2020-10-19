import plot.plotter as plotter

date = '2020-10-16'

if __name__ == '__main__':
    plotter.tweets('account', date)
    plotter.tweets('hashtag', date)
