#!/usr/bin/env python3

import csv
import json
import urllib.request
import urllib.parse
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get speed results for desktop and mobile versions of websites.')

    parser.add_argument(
        'urls_fils',
        metavar='urls',
        help='File containing list of newline-separated URLs'
    )

    parser.add_argument(
        'out_file',
        metavar='out',
        help='Filepath to write results to'
    )

    args = parser.parse_args();

    with open('results.csv', 'w') as resultsFile:
        csvwriter = csv.writer(resultsFile, delimiter=',')
        csvwriter.writerow([
            'Url',
            'Desktop Speed',
            'Mobile Speed'
        ])

        with open('urls.txt', 'r') as urlsFile:
            for url in urlsFile:
                url = url.strip()
                print("Running for url: {url}".format(url=url))
                res = urllib.request.urlopen(
                    "https://www.googleapis.com/pagespeedonline/v2/runPagespeed?url={url}&key=AIzaSyDT1P6RRZmTJAoACGr5_82s8D1Z0xRpVYE".format(
                        url=urllib.parse.quote_plus(url)
                    )
                ).read()
                desktop_result = json.loads(res)

                res = urllib.request.urlopen(
                    "https://www.googleapis.com/pagespeedonline/v2/runPagespeed?url={url}&strategy=mobile&key=AIzaSyDT1P6RRZmTJAoACGr5_82s8D1Z0xRpVYE".format(
                        url=urllib.parse.quote_plus(url)
                    )
                ).read()
                mobile_result = json.loads(res)

                csvwriter.writerow([
                    url,
                    desktop_result['ruleGroups']['SPEED']['score'],
                    mobile_result['ruleGroups']['SPEED']['score']
                ])