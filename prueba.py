import json
def main():
    lista = b'["1","2","3"]'
    listastr = json.dumps(lista)
    print(listastr)
    lista2 = json.loads(listastr)
    lista2.pop()
    print(lista2)

main()