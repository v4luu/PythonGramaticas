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
        nueva_produccion = list(produccion)

        # Manejo de la recursividad
        for i, simbolo in enumerate(produccion):
            if simbolo == nt:
                for produccion_recursiva in gramatica[nt]:
                    if produccion_recursiva != produccion:
                        nueva_produccion.pop(i)
                        nueva_produccion[i:i] = produccion_recursiva
                        break  # Añadido para limitar la recursión a una sola vez
                break  # Añadido para evitar procesar múltiples ocurrencias del mismo NT en una producción

        # Cálculo de los primeros y siguientes
        for simbolo in nueva_produccion:
            if simbolo in primeros:
                pred |= primeros[simbolo]
                pred.discard('ε')
            elif simbolo != 'ε':
                pred.add(simbolo)
                break
            else:
                pred |= siguientes[nt]

        predicciones[tuple(nueva_produccion)] = pred

    return predicciones

for nt in gramatica:
    pred = calcular_prediccion(gramatica.copy(), nt, conjunto_primeros, conjunto_siguientes)
    print("PRED(", nt, "):", pred)
