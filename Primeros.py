def primeros(gramatica):
    primeros = {nt: set() for nt in gramatica}

    # Paso 1: Inicializar los primeros de los símbolos terminales
    for nt, producciones in gramatica.items():
        for produccion in producciones:
            if isinstance(produccion, tuple) and len(produccion) > 0 and produccion[0] not in gramatica:
                primeros[nt].add(produccion[0])
            elif isinstance(produccion, str):
                primeros[nt].add(produccion)

    for _ in range(len(gramatica)):
        cambios = False
        for nt, producciones in gramatica.items():
            for produccion in producciones:
                if isinstance(produccion, tuple):
                    for simbolo in produccion:
                        if simbolo in gramatica:
                            nuevos_primeros = primeros[simbolo] - {'ε'}
                            if len(nuevos_primeros) > 0:
                                cambios |= nuevos_primeros - primeros[nt] != set()
                                primeros[nt] |= nuevos_primeros
                            if 'ε' not in primeros[simbolo]:
                                break
                        else:
                            cambios |= simbolo not in primeros[nt]
                            primeros[nt].add(simbolo)
                            break
                    else:
                        cambios |= 'ε' not in primeros[nt]
                        primeros[nt].add('ε')
                else:
                    simbolo = produccion
                    if simbolo in gramatica:
                        nuevos_primeros = primeros[simbolo] - {'ε'}
                        if len(nuevos_primeros) > 0:
                            cambios |= nuevos_primeros - primeros[nt] != set()
                            primeros[nt] |= nuevos_primeros
                        if 'ε' not in primeros[simbolo]:
                            continue
                    cambios |= simbolo not in primeros[nt]
                    primeros[nt].add(simbolo)

        if not cambios:
            break
    for no_terminal, conjunto_primeros in primeros.items():
        print(f'PRIMERO({no_terminal}): {conjunto_primeros}')
        
    return primeros