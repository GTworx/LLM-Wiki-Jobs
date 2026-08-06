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
    
    port = PORT
    httpd = None
    for try_port in range(PORT, PORT + 10):
        try:
            httpd = socketserver.TCPServer(("", try_port), QuietHTTPRequestHandler)
            port = try_port
            break
        except OSError:
            continue

    url = f"http://localhost:{port}/index.html"
    print("==================================================")
    print("LLM Wiki Jobs Match & Recommendation Dashboard")
    print("==================================================")
    print(f"Dashboard URL: {url}")
    
    # Open browser
    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"Could not automatically open browser: {e}")

    if httpd:
        print("Press Ctrl+C to stop the server.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
    else:
        print("Using existing running server instance.")

if __name__ == "__main__":
    main()
