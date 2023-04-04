Návod k instalaci a spuštění serveru slovníkových překladů
Tento program slouží jako server pro překlady slov z češtiny do angličtiny. Server je navržen jako démon, který běží na pozadí a naslouchá příchozím požadavkům na překlad.

Požadavky
OS Linux, distribuce Debian
Python 3.6 nebo vyšší
Knihovny Python: socket, threading, queue, datetime, yaml

Instalace
Stáhněte si zdrojový kód programu a uložte ho do libovolné složky na vašem počítači.
Otevřete příkazovou řádku a přejděte do složky se staženým zdrojovým kódem.
Nainstalujte potřebné knihovny pomocí následujícího příkazu:   pip install (název knihovny)
Otevřete soubor config.yml a upravte ho podle vašich potřeb.
Spusťte program pomocí následujícího příkazu: python server.py
Server bude spuštěn jako démon a bude naslouchat příchozím požadavkům.

Konfigurace
V souboru config.yml je možné nastavit následující parametry:
host: IP adresa, na které bude server naslouchat.
port: číslo portu, na kterém bude server naslouchat.
start_ip: IP adressa kterou započne scanovat 
end_ip: IP adressa kterou ukončí scanovani
start_port: port kterym započne scanovani
end_port:port kterym ukončí scanovani

Použití

Server naslouchá na zadané IP adrese a portu. Klienti se k serveru mohou připojit pomocí TCP spojení a posílat požadavky na překlad slov. Podporované požadavky jsou:

TRANSLATEPING: server vrátí "TRANSLATEPONG "Nazev programu"".
TRANSLATELOCL "slovo": server přeloží slovo z češtiny do angličtiny pomocí lokálního slovníku.
TRANSLATESCAN "slovo": server přeloží slovo z češtiny do angličtiny pomocí skenování sítě.