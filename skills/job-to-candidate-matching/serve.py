import os
import sys
import webbrowser
import http.server
import socketserver

# Force UTF-8 output encoding for Windows stdout
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

PORT = 8080
DASHBOARD_DIR = os.path.dirname(os.path.abspath(__file__))

class QuietHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DASHBOARD_DIR, **kwargs)

def main():
    os.chdir(DASHBOARD_DIR)
    url = f"http://localhost:{PORT}/index.html"
    print("==================================================")
    print("LLM Wiki Jobs Match & Recommendation Dashboard")
    print("==================================================")
    print(f"Dashboard URL: {url}")
    print("Press Ctrl+C to stop the server.")
    
    # Open browser
    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"Could not automatically open browser: {e}")

    with socketserver.TCPServer(("", PORT), QuietHTTPRequestHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

if __name__ == "__main__":
    main()
