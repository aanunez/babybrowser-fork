import requests

class Network:

    def __init__(self):
        self.request = None

    def get(self, url):
        self.request = requests.get(url)
        return self.request.text

    def get_image(url):
        img_request = requests.get(url)
        return img_request.content

