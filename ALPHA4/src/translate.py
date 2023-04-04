import socket

# Slovníček pro lokální překlady
dict_cz_en = {
    "house": "dum",
    "car": "auto",
    "table": "stul",
    "ball": "mic",
    "dog": "pes"
}

def translate_local(word):
    """Provede překlad slova z češtiny do angličtiny z lokálního slovníku"""
    if word in dict_cz_en:
        return "TRANSLATEDSUC" + '"' + dict_cz_en[word] + '"'
    else:
        return "TRANSLATEDERR" + '"nenalezeno ' + word + '"'

def translate_scan(word, start_ip, end_ip, start_port, end_port):
    """Provede překlad slova z češtiny do angličtiny skenováním sítě"""
    start_ip_parts = start_ip.split('.')
    end_ip_parts = end_ip.split('.')
    ips = [f"{start_ip_parts[0]}.{start_ip_parts[1]}.{start_ip_parts[2]}.{i}" for i in range(int(start_ip_parts[3]), int(end_ip_parts[3])+1)]
    ports = range(start_port, end_port+1)
    
    for ip in ips:
        for port in ports:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(5) 
                    sock.connect((ip, port))
                    
                    request = f'TRANSLATELOCL"{word}"\n'
                    
                    sock.sendall(request.encode())
                    response = sock.recv(1024).decode().strip()

                    if response.startswith("TRANSLATEDSUC"):
                        return response, True

            except socket.error:
                pass

    return f'TRANSLATEDERR "nenalezeno {word}"', False
