import os

import requests


def crawler():
    file = open("links.txt")
    links = file.readlines()
    file.close()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
    }

    i = 1
    if not os.path.isdir("results"):
        os.mkdir("results")
    with open("index.txt", 'w') as index_file:
        for link in links:

            try:
                r = requests.get(link.strip(), headers)
            except Exception as e:
                print("Error on request " + link)
                continue

            print("Successfully download " + link)
            index_file.write("выкачка-" + str(i) + ".txt" + " " + link.strip() + "\n")

            with open('results/выкачка-' + str(i) + '.txt', 'w') as output_file:
                output_file.write(r.text)
            i += 1


if __name__ == '__main__':
    crawler()
