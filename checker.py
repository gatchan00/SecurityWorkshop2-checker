import requests


with open('combo.txt', 'r') as f:
    with open('output.txt', 'w') as out:
        for linea in f:
            (user, password) = linea.replace("\r", "").replace("\n", "").split(":")
            payload = {'user': user,
                       'pass': password}
            respuesta = requests.post('http://localhost:5002/validateLogin', data=payload)
            if respuesta.status_code == 200:
                out.write(linea)
                print(user, password)
