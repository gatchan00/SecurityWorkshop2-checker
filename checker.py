import requests
import tokenize

inputFile = 'combo.txt'
outputFile = 'output.txt'
tempFile = tokenize.open(inputFile)
fileEncoding = tempFile.encoding
tempFile.close()
with open(inputFile, 'r', encoding=fileEncoding, errors="backslashreplace") as f:
    with open(outputFile, 'w') as out:
        for linea in f:
            (user, password) = linea.replace("\r", "").replace("\n", "").split(":")
            payload = {'user': user,
                       'pass': password}
            respuesta = requests.post('http://localhost:5002/validateLogin', data=payload)
            if respuesta.status_code == 200:
                out.write(linea)
                print(user, password)
