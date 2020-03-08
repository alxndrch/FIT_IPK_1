
# Projektová dokumentace 
## Alexandr Chalupnik (xchalu15)

---

#### Cíl projektu

Cílem projektu byla implementace serveru, který bude komunikovat protokolem HTTP a bude zajišťovat překlad doménových jmen. Pro překlad jmen bude server používat lokální resolver stanice na které běží.

### Implementace

K vytvoření serveru se využíva modul `socket`(nízko-úrovňové síťové rozhraní), kterým je vytvořeno TCP spojení na lokalní adrese na uživatelem zadaném portu.

```python
...
serverSocket = socket(AF_INET,SOCK_STREAM)
try:
    serverSocket.bind(("",int(PORT)))
except:
    ...
```
Po vytvoření spojení, server čeká na HTTP dotazy od klienta ve specifikovaném formátu, které vyhodnocuje. K vyhodnocování správnosti obdrženého dotazu slouží modul `re`, kterým se kontroluje parametry nebo zadané domény/IP adresy.
K samotnému vyhodnocení domén a IP adrese podle zadaného požadavku,se používaji funkce `gethostbyaddr()` a `gethostbyname()`.
```python
...
try:
    addr = gethostbyaddr(name)
except:
    return ("404 Not Found","")
...
```
Po vyhodnocení dotazu server odesílá klientovi HTTP odpověď, která obsahuje stavový kód a v případě úspěchu i obsah zprávy:
```
HTTP/1.1 200 OK

...obsah...
```
Pro zpřístupnění argumentů a ukončení programu je připojen modul `sys`.

### Spuštění serveru
Server se spouští pomocí souboru Makefile, příkazem:
```console
$ make run PORT=<číslo portu>
```
Pro spuštění serveru musí být zadáno číslo portu, ke kterému se má server přpojit, pokud port nebyl zadán, server upozorňuje uživatele hlaškou `PORT IS MISSING`. V případě, že se server nemůže připojit k zadanému portu, vypisuje se chybová hláška `PORT IS NOT ACCESSIBLE`. V obou případech se běh programu ukončuje.
V případě uspěšného připojení, server běží dokud ho uživatel sám neukončí pomocí `Ctrl + C`.
Další hlašky: Úspěšné připojení `SERVER IS READY`; Ukončení programu `SERVER DISCONNECTED`
