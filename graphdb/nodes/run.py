import graphdb.nodes.tweets as tweets
import graphdb.nodes.com_stampa as com_stampa
import datetime


def save_timestamp():
    with open('/home/marco/Scrivania/tirocinio-unicredit/graphdb/timestamp.txt', 'w') as file:
        file.write(datetime.datetime.now().strftime("%Y-%m-%d"))


if __name__ == '__main__':
    tweets.nodes_file()
    #com_stampa.nodes_file()
    save_timestamp()
