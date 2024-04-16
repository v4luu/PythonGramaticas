from Primeros import primeros as calcular_primeros
def procesar_producciones(gramatica, primeros, siguientes):
    cambios = True
    while cambios:
        cambios = False
        for nt, producciones in gramatica.items():
            for produccion in producciones:
                for i, simbolo in enumerate(produccion):
                    if simbolo in gramatica:
                        siguiente = produccion[i + 1:i + 2]  # Obtener el siguiente símbolo
                        if siguiente and siguiente[0] in gramatica.keys():
                            primeros_beta = primeros[siguiente[0]]
                            siguientes_a = siguientes[nt]
                            if 'ε'  in primeros_beta or siguiente == ('ε',):
                                nuevos_siguientes = siguientes_a | siguientes[simbolo]
                                if nuevos_siguientes != siguientes[simbolo]:
                                    cambios = True
                                    siguientes[simbolo] = nuevos_siguientes
                                    
                            nuevos_siguientes = siguientes[simbolo].copy()
                            for primero in primeros_beta - {'ε'}:
                                if primero not in nuevos_siguientes:
                                    cambios = True
                                    nuevos_siguientes.add(primero)
                            if nuevos_siguientes != siguientes[simbolo]:
                                cambios = True
                                siguientes[simbolo] = nuevos_siguientes
                        elif siguiente:
                            nuevos_siguientes = siguientes[simbolo] | {siguiente[0]}
                            if nuevos_siguientes != siguientes[simbolo]:
                                cambios = True
                                siguientes[simbolo] = nuevos_siguientes
                        else:
                            nuevos_siguientes = siguientes[simbolo] | siguientes[nt]
                            if nuevos_siguientes != siguientes[simbolo]:
                                cambios = True
                                siguientes[simbolo] = nuevos_siguientes
def siguientes(gramatica, primeros):
    siguientes = {nt: set() for nt in gramatica}
    siguientes[list(gramatica.keys())[0]].add('$')
    procesar_producciones(gramatica, primeros, siguientes)
    return siguientes
gramatica = {
    'S': [('A', 'uno', 'B', 'C'), ('S', 'dos')],
    'A': [('B', 'C', 'D'), ('A', 'tres'), ('ε',)],
    'B': [('D', 'cuatro', 'C', 'tres'), ('ε',)],
    'C': [('cinco', 'D', 'B'), ('ε',)],
    'D': [('seis',), ('ε',)]
}


conjunto_primeros = calcular_primeros(gramatica)

conjunto_siguientes = siguientes(gramatica, conjunto_primeros)


print("Conjunto de Siguientes:")
for nt, s in conjunto_siguientes.items():
    print(nt, ":", s)


def calcular_prediccion(gramatica, nt, primeros, siguientes):
    predicciones = {}
    for produccion in gramatica[nt]:
        pred = set()
        primeros_prod = primeros_alfa(produccion, primeros)
        if 'ε' in primeros_prod:
            primeros_prod.remove('ε')
            pred |= siguientes[nt]
        pred |= primeros_prod
        predicciones[produccion] = pred
    return predicciones

def primeros_alfa(alfa, primeros):
    primeros_alfa = set()
    for simbolo in alfa:
        if simbolo in primeros:
            primeros_alfa |= primeros[simbolo]
            if 'ε' not in primeros[simbolo]:
                break
        else:
            primeros_alfa.add(simbolo)
            break
    return primeros_alfa

for nt in gramatica:
    pred = calcular_prediccion(gramatica, nt, conjunto_primeros, conjunto_siguientes)
    print("PRED(", nt, "):", pred)