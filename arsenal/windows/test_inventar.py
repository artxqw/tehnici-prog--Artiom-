from arsenal.windows.inventar import Proces, Eveniment


def test_proces_din_temp_e_suspect():
    p = Proces(1, "x.exe", "ana", "C:\\Users\\ana\\AppData\\Local\\Temp\\x.exe")
    assert p.e_suspect() is True


def test_proces_din_roaming_e_suspect():
    p = Proces(3, "svch0st.exe", "ana", "C:\\Users\\ana\\AppData\\Roaming\\svch0st.exe")
    assert p.e_suspect() is True


def test_proces_din_windows_nu_e_suspect():
    p = Proces(2, "svchost.exe", "SYSTEM", "C:\\Windows\\System32\\svchost.exe")
    assert p.e_suspect() is False


def test_cale_suspecta_cu_litere_mici():
    p = Proces(4, "x.exe", "ana", "c:\\users\\ana\\appdata\\local\\temp\\x.exe")
    assert p.e_suspect() is True


def test_dataclass_eq_compara_dupa_campuri():
    a = Proces(1, "x.exe", "ana", "C:\\Temp\\x.exe")
    b = Proces(1, "x.exe", "ana", "C:\\Temp\\x.exe")
    assert a == b


def test_eveniment_cu_id_suspect():
    e = Eveniment(4625, "warning", "Security", "administrator", "failed logon")
    assert e.e_suspect() is True


def test_eveniment_critical_e_suspect():
    e = Eveniment(9999, "critical", "System", "SYSTEM", "ceva grav")
    assert e.e_suspect() is True


def test_eveniment_normal_nu_e_suspect():
    e = Eveniment(4624, "info", "Security", "ana", "logon ok")
    assert e.e_suspect() is False