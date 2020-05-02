import urllib.request
import json

def get_hawker_names(url):
    hawker_names = []

    req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
    fileobj = urllib.request.urlopen(req).read()

    hawker_dict = json.loads(fileobj)
    records = hawker_dict['result']['records']

    for record in records:
        name_of_centre = record['name_of_centre']
        hawker_names.append(name_of_centre)

    return hawker_names