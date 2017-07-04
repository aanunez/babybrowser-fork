import requests

def network_get(url):
    return requests.get(url).text

def network_get_image(url):
    return requests.get(url).content

