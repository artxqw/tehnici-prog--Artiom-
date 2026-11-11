from dataclasses import dataclass, asdict
import json

CAI_SUSPECTE = ("\\Temp\\", "\\Roaming\\")

@dataclass
class Proces:
    pid: int
    nume: str
    user: str
    cale: str

    def e_suspect(self):
        cale = self.cale.lower()
        return any(c.lower() in cale for c in CAI_SUSPECTE)

p = Proces(3120, "update.exe", "ana", r"C:\Users\ana\AppData\Local\Temp\update.exe")
print(p.pid, p.nume)
print(p)


print(p.e_suspect())  # True (update.exe din Temp)

SUSPECTE_ID = {4625, 1102, 7045}


@dataclass
class Eveniment:
    id: int;
    nivel: str;
    sursa: str;
    cont: str;
    mesaj: str

    def e_suspect(self):
        return self.id in SUSPECTE_ID or self.nivel == "critical"

def evenimente_din_json(cale):
    with open(cale, encoding="utf-8") as f:
        return [Eveniment(**d) for d in json.load(f)]


@dataclass
class Inventar:
    procese: list

    @classmethod
    def din_json(cls, cale):
        with open(cale, encoding="utf-8") as f:
            # TODO: return cls([Proces(**d) for d in json.load(f)])
            return cls([Proces(**d) for d in json.load(f)])

    def __len__(self):
        return len(self.procese)


    def suspecte(self):
        # TODO: lista proceselor cu p.e_suspect()
        return [p for p in self.procese if p.e_suspect()]


    def pe_user(self):
        # TODO: dict user -> lista de nume (foloseste setdefault)
        rezultat = {}
        for p in self.procese:
            rezultat.setdefault(p.user, []).append(p.nume)
        return rezultat


inv = Inventar.din_json("arsenal/windows/start/procese.json")
print("procese:", len(inv))

for p in inv.suspecte():
    print(f"  [{p.pid}] {p.nume}  {p.cale}")
print(inv.pe_user())

from dataclasses import asdict


def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("capturi")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    inv = Inventar.din_json(a.capturi + "/procese.json")
    ev = evenimente_din_json(a.capturi + "/evenimente.json")
    alarma = [e for e in ev if e.e_suspect()]
    # TODO: cu --json, json.dumps cu asdict pe suspecte si alarma;
    suspecte = inv.suspecte()

    if a.json:
        print(json.dumps(
            {
                "suspecte": [asdict(p) for p in suspecte],
                "alarma": [asdict(e) for e in alarma],
            },
            indent=2,
            ensure_ascii=False,
        ))
        return

    print(f"Procese: {len(inv)} ({len(suspecte)} suspecte)")
    for p in suspecte:
        print(f"  [{p.pid}] {p.nume} ({p.user})  {p.cale}")
    print(f"Evenimente: {len(ev)} ({len(alarma)} in alarma)")
    for e in alarma:
        print(f"  [{e.id}] {e.nivel} {e.sursa} cont={e.cont}: {e.mesaj}")

if __name__ == "__main__":
    main()

from arsenal.windows.inventar import Proces


def test_proces_din_temp_e_suspect():
    p = Proces(1, "x.exe", "ana", "C:\\Users\\ana\\AppData\\Local\\Temp\\x.exe")
    assert p.e_suspect() is True


def test_proces_din_windows_nu_e_suspect():
    p = Proces(2, "svchost.exe", "SYSTEM", "C:\\Windows\\System32\\svchost.exe")
    assert p.e_suspect() is False

