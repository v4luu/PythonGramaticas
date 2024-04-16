def primeros(grammar):
    primeros = {}
    visitados = set()
    
    # Inicializar primeros con conjuntos vacíos para cada no terminal
    for non_terminal in grammar:
        primeros[non_terminal] = set()
    
    # Función auxiliar para verificar si un símbolo es terminal
    def es_terminal(simbolo):
        if isinstance(simbolo, str):
            return simbolo not in grammar
        return False

    
    # Función para calcular primeros recursivamente
    def calcular_primeros(no_terminal):
        if no_terminal in visitados:
            return
        visitados.add(no_terminal)
        for produccion in grammar[no_terminal]:
            produccion_puede_eps = False
            for simbolo in produccion:
                # Caso 1: ε
                if simbolo == 'ε':
                    primeros[no_terminal].add('ε')
                    produccion_puede_eps = True
                    break  # Se agrega esta línea para detener la búsqueda si se encuentra ε en la producción
                elif es_terminal(simbolo):
                    primeros[no_terminal].add(simbolo)
                    produccion_puede_eps = False
                    break  # Se agrega esta línea para detener la búsqueda si se encuentra un terminal
                else:
                    if simbolo != no_terminal:  # Verificar si el símbolo es un no terminal diferente al actual
                        calcular_primeros(simbolo)
                    else :
                        continue
                    primeros[no_terminal]  |= primeros[simbolo]
                    if 'ε' not in primeros[simbolo]:
                        produccion_puede_eps = False
                        break
            if produccion_puede_eps:
                
                primeros[no_terminal].add('ε')

    for no_terminal in grammar:
        calcular_primeros(no_terminal)
        
    for no_terminal in primeros:
        producciones = grammar[no_terminal]
        for produccion in producciones:
            for simbolo in produccion:
                if simbolo != no_terminal and simbolo in primeros:
                    
                    
                    if 'ε' not in primeros[simbolo]:
                        break
                    #primeros[no_terminal].discard('ε')

    for no_terminal, conjunto_primeros in primeros.items():
        print(f'PRIMERO({no_terminal}): {conjunto_primeros}')

    return primeros