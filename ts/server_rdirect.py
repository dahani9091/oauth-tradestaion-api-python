from http.server import BaseHTTPRequestHandler
from client import TradeStationClient
import re
import threading

class Pages:
    @staticmethod
    def getRoot(access_url):
        root = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>API Test</title>
            </head>
            <body>
                <script type="application/javascript">
                    window.location.href= "{access_url}"
                </script>
            </body>
            </html>
                    """.encode('utf-8')
        return root            

    @staticmethod
    def getDone():
        done = """<!DOCTYPE html><html><body><pre>
            Closing localhost server and launching application.

            This page may now be closed.
            </pre></html>""".encode(
                    "utf-8")
        return done            

    @staticmethod
    def getUnknown():
        unknown = "<!DOCTYPE html><html><body><pre>404 - Page not found.</pre></html>".encode(
            "utf-8")
        return unknown


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        # Serve root page with sign in link
        if self.path == '/':

            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(Pages.getRoot(TradeStationClient.getAccessUrl()))

            return

        # Check if query path contains case insensitive "code="
        code_match = re.search(r'code=(.+)', self.path, re.I)

        if code_match:

            user_auth_code = code_match[1]
            with open("temp/code.txt", "w") as f:
                f.write(user_auth_code)
            #global token_access
            #token_access = Context.convertAuthCode(user_auth_code)
            #Context.TOKENS.from_dic(token_access)
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(Pages.getDone())

            # User has logged in - terminate localhost server
            thread = threading.Thread(target=TradeStationClient.HTTPD.shutdown, daemon=True)
            thread.start()

            return

        # Send 404 error if path is none of the above
        self.send_response(404)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(Pages.getUnknown())

        return