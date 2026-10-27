s = "Salut"
b = s.encode()          # bytes
print(b, b[0])          # b"Salut" 83

# Rezolvare TODO:
hex_representation = b.hex()
print("Hex:", hex_representation)

recovered_bytes = bytes.fromhex(hex_representation)
print("Bytes refăcuți:", recovered_bytes)

# Opțional, poți transforma înapoi în șir de caractere (text):
print("Text refăcut:", recovered_bytes.decode())

import re


def ghici_strat(s):
    # 1. Dacă conține '%' (specific codării URL / percent-encoding)
    if '%' in s:
        return "url"

    # 2. Dacă conține doar caractere hexazecimale (0-9, a-f / A-F) și are lungime pară
    elif all(c in "0123456789abcdefABCDEF" for c in s) and len(s) % 2 == 0:
        return "hex"

    # 3. Dacă conține caractere specifice Base64 (A-Za-z0-9+/=)
    elif re.match(r'^[A-Za-z0-9+/=]+$', s):
        return "base64"

    return "necunoscut"


# Teste:
print(ghici_strat("%2Fetc"))  # url
print(ghici_strat("48656c6c6f"))  # hex

import base64
from urllib.parse import unquote


def desfa(s):
    strat = ghici_strat(s)

    # TODO: pentru fiecare strat, decodeaza
    if strat == "base64":
        rezultat_bytes = base64.b64decode(s)
    elif strat == "hex":
        rezultat_bytes = bytes.fromhex(s)
    elif strat == "url":
        # unquote returnează string, îl convertim la bytes cu .encode()
        rezultat_bytes = unquote(s).encode()
    else:
        rezultat_bytes = s.encode()

    # Întoarce (strat, rezultat_bytes)
    return strat, rezultat_bytes


# Exemplu de utilizare:
print(desfa("48656c6c6f"))  # Returnează: ('hex', b'Hello')
print(desfa("%2Fetc"))  # Returnează: ('url', b'/etc')

date = open("probe/xor.bin", "rb").read()

def citibil(b_data):
    try:
        # Încercăm decodarea în UTF-8
        text = b_data.decode("utf-8")
        # Verificăm dacă toate caracterele sunt printabile sau whitespace uzual
        return all(32 <= ord(c) <= 126 or c in "\n\r\t" for c in text)
    except UnicodeDecodeError:
        return False

for k in range(256):
    clar = bytes(b ^ k for b in date)
    if citibil(clar):
        print("cheie:", k, clar.decode())

import hashlib

tinta = open("probe/hashuri.txt").readline().strip()
print("Lungime hash:", len(tinta))  # 32 md5 / 40 sha1 / 64 sha256[cite: 5]

for cuv in open("probe/wordlist.txt", encoding="latin1"):
    cuv = cuv.strip()

    # Determinarea algoritmului și verificarea hash-ului
    if len(tinta) == 32 and hashlib.md5(cuv.encode()).hexdigest() == tinta:
        print("gasit:", cuv)
        break
    elif len(tinta) == 40 and hashlib.sha1(cuv.encode()).hexdigest() == tinta:
        print("gasit:", cuv)
        break
    elif len(tinta) == 64 and hashlib.sha256(cuv.encode()).hexdigest() == tinta:
        print("gasit:", cuv)
        break

import argparse
import json
from arsenal.forensics.decode import desfa  # Presupunând că funcția desfa este importată corect

p = argparse.ArgumentParser()
p.add_argument("intrare")                  # șir sau cale[cite: 6]
p.add_argument("--fisier", action="store_true")
a = p.parse_args()

# TODO: dacă a.fisier, citește octeții din cale; altfel tratează intrarea ca șir[cite: 6]
if a.fisier:
    with open(a.intrare, "rb") as f:
        continut = f.read().decode("latin1")  # sau procesat ca bytes după caz
else:
    continut = a.intrare

# Aplicăm funcția de decodare realizată anterior
strat, rezultat_bytes = desfa(continut)

# TODO: salvează {strat, rezultat} în arsenal/forensics/fisa.json[cite: 6]
date_iesire = {
    "strat": strat,
    "rezultat": rezultat_bytes.hex()  # Salvăm sub formă hexazecimală pentru a fi serializabil în JSON
}

with open("arsenal/forensics/fisa.json", "w", encoding="utf-8") as f:
    json.dump(date_iesire, f, indent=4)

print(f"Rezultat salvat în fisa.json (strat detectat: {strat})")

# teste/test_decode.py
from arsenal.forensics.decode import desfa
def test_base64():
 strat, b = desfa("U2FsdXQ=")
 assert strat == "base64"
 assert b == b"Salut"