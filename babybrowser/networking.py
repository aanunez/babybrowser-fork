import requests

def network_get(self, url):
    return requests.get(url).text

def network_get_image(url):
    return requests.get(url).content

