from http.server import HTTPServer
from bin.http_server import Rod
from bin.get_config import Config
import argparse, re

def args():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', metavar="url", help='URL du site à copié')
    parser.add_argument('-s', '--server', metavar="localhost:8080")
    parser.add_argument('-u', '--user-agent', metavar="user-agent")
    parser.add_argument('--ssl', nargs=2, metavar="cert key", help='Active le SSL')
    parser.add_argument('-v', '--version', action="store_true" ,help='Voir la version')
    args = parser.parse_args()

    url_regex = re.match("^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$", args.url)

    if args.version:
        Config().App()['version']

    if args.server:
        server = args.server
    else:
        server = f"{Config().Settings()['host']}:{Config().Settings()['port']}"

    if args.user_agent:
        user_agent = args.user_agent
    else:
        user_agent = None
    
    if args.ssl:
        print(f"Cert {args.ssl[0]} / Key {args.ssl[1]}")

    if url_regex:
        rod = Rod(args.url, user_agent, Config().Settings()['output-filename'] )
        webServer = HTTPServer((server.split(':')[0], int(server.split(":")[1])), rod)
        print(f"Server http://{server.split(':')[0]}:{server.split(':')[1]} / Target {args.url}")

        try:
            webServer.serve_forever()
        except KeyboardInterrupt:
            pass

        webServer.server_close()
        print("Server stopped.")
    else:
        print("Adresse du site invalide")
