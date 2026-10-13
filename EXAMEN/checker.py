from sys import path

import requests

SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


def build_url(host):
    """Returnează o adresă completă, de exemplu https://example.com/login."""
    response = requests.get(host + path)
    pass


def is_https(url : ):
    """Returnează True dacă adresa începe cu https://, altfel False."""
    if url.startswith("https://"):
        return True
    else:
        return False

pass

def show_response("https://example.com"):
    """Trimite un GET la url și afișează statusul și Content-Type."""
    response = requests.get(url)
    print("Statutul: {response.status_code}")
    print("Content Type: {response.headers['Content-Type']}")
    pass


def check_site(url):
    """Returnează un dicționar cu: status, content_type, length, server."""
    response = requests.get(url)
    return (response.headers["content-type"],
            response.headers["content-length"],
            response.headers["server"],
            response.headers["status"])
pass



def scan_sites():
    """Verifică toate site-urile din SITES, afișează-le pe cele care merg și un rezumat."""
    for s in SITES:
        response = requests.get(s)
        if response.status_code == 200:
            print("Site: {s}".format(s=s))
    pass


def check_headers(url):
    """Returnează un dicționar cu: present, missing, score."""
    response = requests.get(url)
    return ((response.headers["present"],  response.headers["missing"],
            response.headers["score"])

    pass
    )

def retry_check(url,atttempts: int=3):
    """Încearcă de cel mult `attempts` ori; returnează un dicționar cu: status, attempts."""
    for s in range(attempts):
        response = requests.get(url)
        return (response.headers["status"], response.headers["attempts"])

    pass
