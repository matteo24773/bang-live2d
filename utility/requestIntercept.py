from playwright.sync_api import sync_playwright as pls
from urllib.parse import urlparse
from bs4 import BeautifulSoup as bs

json_data = {}
class request():

    def __init__(self, link):
        self.link = link

    def page(self):
        self.pls = pls().start()
        self.browser = self.pls.chromium.launch(executable_path="C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe")
        self.pag = self.browser.new_context().new_page()
    def goto(self):
        self.pag.goto(self.link)
        self.pag.wait_for_load_state("networkidle")
    
    def close(self):
        self.pls.stop()
        
def response(response):
    try:
        request = response.request
        # prova a stampare il corpo della risposta come testo
        # print(f"Response for POST to {request.url}:")
        if ".json" in request.url:
            json_data[urlparse(request.url).path.strip("/").replace("/","_")] = response.json()

    except:
        print("No response body available")



