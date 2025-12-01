# Diccionarios completos para el proyecto final - MIPS32 EXACTO

INSTRUCCIONES_R = {
    'ADD': {'tipo': 'R', 'opcode': 0b000000, 'funct': 0b100000},  # 0x20
    'SUB': {'tipo': 'R', 'opcode': 0b000000, 'funct': 0b100010},  # 0x22
    'AND': {'tipo': 'R', 'opcode': 0b000000, 'funct': 0b100100},  # 0x24
    'OR':  {'tipo': 'R', 'opcode': 0b000000, 'funct': 0b100101},  # 0x25
    'SLT': {'tipo': 'R', 'opcode': 0b000000, 'funct': 0b101010},  # 0x2A
}

INSTRUCCIONES_I = {
    'ADDI': {'tipo': 'I', 'opcode': 0b001000},  # 0x08
    'ANDI': {'tipo': 'I', 'opcode': 0b001100},  # 0x0C
    'ORI':  {'tipo': 'I', 'opcode': 0b001101},  # 0x0D
    'XORI': {'tipo': 'I', 'opcode': 0b001110},  # 0x0E
    'SLTI': {'tipo': 'I', 'opcode': 0b001010},  # 0x0A
    'LW':   {'tipo': 'I', 'opcode': 0b100011},  # 0x23
    'SW':   {'tipo': 'I', 'opcode': 0b101011},  # 0x2B
    'BEQ':  {'tipo': 'I', 'opcode': 0b000100},  # 0x04
}

INSTRUCCIONES_J = {
    'J':    {'tipo': 'J', 'opcode': 0b000010},  # 0x02
}

# Diccionario combinado para búsqueda rápida
TODAS_INSTRUCCIONES = {**INSTRUCCIONES_R, **INSTRUCCIONES_I, **INSTRUCCIONES_J}

def limpiar_linea(linea):
    """
    Limpia la línea: quita comentarios, espacios extras y convierte a mayúsculas
    """
    if '#' in linea:
        linea = linea.split('#')[0]  # Quita todo después del #
    return linea.strip().upper()

def validar_registro(registro_str):
    """
    Valida y convierte un registro a número
    Ejemplo: '$10' -> 10, '$t0' -> 8
    """
    if not registro_str.startswith('$'):
        raise ValueError(f"Registro debe empezar con $: {registro_str}")
    
    registro = registro_str[1:]  # Quita el $
    
    # Registros numéricos (0-31)
    if registro.isdigit():
        num = int(registro)
        if 0 <= num <= 31:
            return num
        else:
            raise ValueError(f"Registro fuera de rango (0-31): ${registro}")
    
    # Registros con nombre
    registros_nombrados = {
        'ZERO': 0, 'AT': 1, 'V0': 2, 'V1': 3, 'A0': 4, 'A1': 5, 'A2': 6, 'A3': 7,
        'T0': 8, 'T1': 9, 'T2': 10, 'T3': 11, 'T4': 12, 'T5': 13, 'T6': 14, 'T7': 15,
        'S0': 16, 'S1': 17, 'S2': 18, 'S3': 19, 'S4': 20, 'S5': 21, 'S6': 22, 'S7': 23,
        'T8': 24, 'T9': 25, 'K0': 26, 'K1': 27, 'GP': 28, 'SP': 29, 'FP': 30, 'RA': 31
    }
    
    if registro in registros_nombrados:
        return registros_nombrados[registro]
    
    raise ValueError(f"Registro no válido: {registro_str}")

def parsear_valor_inmediato(valor_str):
    """
    Parsea un valor inmediato (decimal o hexadecimal)
    Ejemplo: '100' -> 100, '0xFF' -> 255, '-10' -> -10 (en complemento a 2)
    """
    valor_str = valor_str.strip()
    
    # Hexadecimal
    if valor_str.startswith('0X'):
        valor = int(valor_str, 16)
        if valor > 0xFFFF:
            raise ValueError(f"Valor hexadecimal demasiado grande: {valor_str}")
        return valor
    # Decimal (positivo o negativo)
    elif valor_str.replace('-', '').isdigit():
        valor = int(valor_str)
        # Verificar rango para 16 bits con signo
        if valor < -32768 or valor > 65535:
            raise ValueError(f"Valor inmediato fuera de rango: {valor}")
        # Convertir negativo a complemento a 2 de 16 bits
        if valor < 0:
            valor = (1 << 16) + valor
        return valor & 0xFFFF  # Mantener solo 16 bits
    else:
        raise ValueError(f"Valor inmediato no válido: {valor_str}")

def parsear_desplazamiento_memoria(operando_str):
    """
    Parsea operandos de memoria: '4($s0)' -> (4, 16)
    """
    if '(' not in operando_str or ')' not in operando_str:
        raise ValueError(f"Formato de memoria inválido: {operando_str}")
    
    # Separar desplazamiento y registro
    partes = operando_str.split('(')
    if len(partes) != 2:
        raise ValueError(f"Formato de memoria inválido: {operando_str}")
    
    desplazamiento_str = partes[0].strip()
    registro_str = partes[1].replace(')', '').strip()
    
    desplazamiento = parsear_valor_inmediato(desplazamiento_str) if desplazamiento_str else 0
    registro = validar_registro(registro_str)
    
    return desplazamiento, registro

def parsear_operandos_r(operandos_str):
    """
    Parsea operandos para instrucciones tipo R: rd, rs, rt
    Ejemplo: '$10, $3, $4' -> (10, 3, 4)
    """
    operandos = [op.strip().replace(',', '') for op in operandos_str.split()]
    
    if len(operandos) != 3:
        raise ValueError(f"Se esperaban 3 operandos, se encontraron {len(operandos)}: {operandos_str}")
    
    rd = validar_registro(operandos[0])
    rs = validar_registro(operandos[1]) 
    rt = validar_registro(operandos[2])
    
    return rd, rs, rt

def parsear_operandos_i(operandos_str, instruccion):
    """
    Parsea operandos para instrucciones tipo I
    Diferentes formatos según la instrucción
    """
    operandos = [op.strip().replace(',', '') for op in operandos_str.split()]
    
    if instruccion in ['LW', 'SW']:
        # Formato: rt, offset(rs)
        if len(operandos) != 2:
            raise ValueError(f"LW/SW necesitan 2 operandos: rt, offset(rs)")
        
        rt = validar_registro(operandos[0])
        desplazamiento, rs = parsear_desplazamiento_memoria(operandos[1])
        return rs, rt, desplazamiento
    
    elif instruccion in ['BEQ', 'BNE']:
        # Formato: rs, rt, label (simulamos label como inmediato)
        if len(operandos) != 3:
            raise ValueError(f"BEQ/BNE necesitan 3 operandos: rs, rt, label")
        
        rs = validar_registro(operandos[0])
        rt = validar_registro(operandos[1])
        # Simulamos label como valor inmediato (en realidad sería dirección)
        inmediato = parsear_valor_inmediato(operandos[2])
        return rs, rt, inmediato
    
    else:
        # Formato: rt, rs, inmediato (ADDI, ANDI, ORI, XORI, SLTI)
        if len(operandos) != 3:
            raise ValueError(f"Se esperaban 3 operandos, se encontraron {len(operandos)}: {operandos_str}")
        
        rt = validar_registro(operandos[0])
        rs = validar_registro(operandos[1])
        inmediato = parsear_valor_inmediato(operandos[2])
        return rs, rt, inmediato

def parsear_operandos_j(operandos_str):
    """
    Parsea operandos para instrucciones tipo J: address
    """
    operandos = [op.strip().replace(',', '') for op in operandos_str.split()]
    
    if len(operandos) != 1:
        raise ValueError(f"Instrucción J-type necesita 1 operando: address")
    
    # Simulamos address como valor (en realidad sería dirección de memoria)
    address = parsear_valor_inmediato(operandos[0])
    return address

def decodificar_instruccion(linea):
    """
    Decodifica una instrucción MIPS (R-type, I-type, J-type)
    Retorna el código binario de 32 bits o None si es línea vacía/comentario
    """
    linea_limpia = limpiar_linea(linea)
    if not linea_limpia or linea_limpia.startswith('#'):
        return None
    
    # Dividir en mnemónico y operandos
    partes = linea_limpia.split(maxsplit=1)
    if len(partes) < 2:
        raise ValueError(f"Instrucción incompleta: {linea}")
    
    mnemonic = partes[0]
    operandos_str = partes[1]
    
    # Verificar tipo de instrucción
    if mnemonic in TODAS_INSTRUCCIONES:
        tipo = TODAS_INSTRUCCIONES[mnemonic]['tipo']
        
        if tipo == 'R':
            return decodificar_instruccion_r(mnemonic, operandos_str)
        elif tipo == 'I':
            return decodificar_instruccion_i(mnemonic, operandos_str)
        elif tipo == 'J':
            return decodificar_instruccion_j(mnemonic, operandos_str)
    else:
        raise ValueError(f"Instrucción no soportada: {mnemonic}")

def decodificar_instruccion_r(mnemonic, operandos_str):
    """
    Decodifica instrucciones tipo R a código binario MIPS32
    Formato: [opcode 6b][rs 5b][rt 5b][rd 5b][shamt 5b][funct 6b]
    """
    rd, rs, rt = parsear_operandos_r(operandos_str)
    inst_data = INSTRUCCIONES_R[mnemonic]
    
    # CONSTRUIR INSTRUCCIÓN DE 32 BITS
    instruccion_bin = 0
    
    # Opcode (bits 31-26)
    instruccion_bin |= (inst_data['opcode'] & 0x3F) << 26
    # rs (bits 25-21)
    instruccion_bin |= (rs & 0x1F) << 21
    # rt (bits 20-16)
    instruccion_bin |= (rt & 0x1F) << 16
    # rd (bits 15-11)
    instruccion_bin |= (rd & 0x1F) << 11
    # shamt (bits 10-6) - siempre 0
    instruccion_bin |= (0 & 0x1F) << 6
    # funct (bits 5-0)
    instruccion_bin |= (inst_data['funct'] & 0x3F)
    
    return instruccion_bin

def decodificar_instruccion_i(mnemonic, operandos_str):
    """
    Decodifica instrucciones tipo I a código binario MIPS32
    Formato: [opcode 6b][rs 5b][rt 5b][inmediato 16b]
    """
    rs, rt, inmediato = parsear_operandos_i(operandos_str, mnemonic)
    inst_data = INSTRUCCIONES_I[mnemonic]
    
    # CONSTRUIR INSTRUCCIÓN DE 32 BITS
    instruccion_bin = 0
    
    # Opcode (bits 31-26)
    instruccion_bin |= (inst_data['opcode'] & 0x3F) << 26
    # rs (bits 25-21)
    instruccion_bin |= (rs & 0x1F) << 21
    # rt (bits 20-16)
    instruccion_bin |= (rt & 0x1F) << 16
    # inmediato (bits 15-0)
    instruccion_bin |= (inmediato & 0xFFFF)
    
    return instruccion_bin

def decodificar_instruccion_j(mnemonic, operandos_str):
    """
    Decodifica instrucciones tipo J a código binario MIPS32
    Formato: [opcode 6b][address 26b]
    """
    address = parsear_operandos_j(operandos_str)
    inst_data = INSTRUCCIONES_J[mnemonic]
    
    # CONSTRUIR INSTRUCCIÓN DE 32 BITS
    instruccion_bin = 0
    
    # Opcode (bits 31-26)
    instruccion_bin |= (inst_data['opcode'] & 0x3F) << 26
    # address (bits 25-0) - en J-type, address va en los 26 bits bajos
    instruccion_bin |= (address & 0x3FFFFFF)
    
    return instruccion_bin

def instruccion_a_bytes_big_endian(instruccion_bin):
    """
    Convierte una instrucción de 32 bits a 4 bytes en orden Big Endian
    Big Endian: Byte más significativo primero
    """
    bytes_resultado = []
    
    # Extraer los 4 bytes en orden Big Endian
    for i in range(4):
        # Desplazamos para obtener cada byte (bits 31-24, 23-16, 15-8, 7-0)
        byte = (instruccion_bin >> (24 - i * 8)) & 0xFF
        bytes_resultado.append(byte)
    
    return bytes_resultado

def decodificar_archivo(contenido):
    """
    Procesa todo el contenido de un archivo con instrucciones MIPS
    Retorna:
    - lineas_originales: Lista de líneas originales
    - instrucciones_bin: Lista de instrucciones en binario (o None si hay error)
    - todos_bytes: Lista de todos los bytes para el archivo de salida
    """
    lineas_originales = []
    instrucciones_bin = []
    todos_bytes = []
    
    lineas = contenido.split('\n')
    
    for num_linea, linea in enumerate(lineas, 1):
        # Guardar línea original
        lineas_originales.append(linea)
        
        try:
            # Intentar decodificar la línea
            instruccion = decodificar_instruccion(linea)
            instrucciones_bin.append(instruccion)
            
            # Si se decodificó correctamente, agregar bytes
            if instruccion is not None:
                bytes_inst = instruccion_a_bytes_big_endian(instruccion)
                todos_bytes.extend(bytes_inst)
                
        except Exception as e:
            # Si hay error, marcar como None y continuar
            instrucciones_bin.append(None)
            print(f"❌ Error en línea {num_linea}: {e}")
    
    return lineas_originales, instrucciones_bin, todos_bytes

def obtener_instrucciones_soportadas():
    """Retorna string con todas las instrucciones soportadas por tipo"""
    r_inst = ", ".join(INSTRUCCIONES_R.keys())
    i_inst = ", ".join(INSTRUCCIONES_I.keys())
    j_inst = ", ".join(INSTRUCCIONES_J.keys())
    
    return f"R-type: {r_inst}\nI-type: {i_inst}\nJ-type: {j_inst}"

def verificar_formato_verilog(bytes_salida):
    """
    Verifica que el formato de salida sea compatible con Verilog
    para precarga de memoria de instrucciones
    """
    print("🔧 VERIFICANDO FORMATO PARA VERILOG:")
    print("=" * 50)
    
    # Verificar que sean múltiplos de 4 bytes (instrucciones completas)
    if len(bytes_salida) % 4 != 0:
        print("❌ ERROR: Número de bytes no es múltiplo de 4")
        return False
    
    num_instrucciones = len(bytes_salida) // 4
    print(f"✅ {num_instrucciones} instrucciones de 32 bits")
    
    # Mostrar formato de memoria para Verilog
    print("\n📝 FORMATO PARA VERILOG (Big Endian):")
    print("// Memoria de instrucciones - Big Endian")
    print("// Dirección | Byte3 | Byte2 | Byte1 | Byte0")
    print("//           | 31-24 | 23-16 | 15-8  | 7-0")
    
    for i in range(0, min(len(bytes_salida), 16), 4):  # Mostrar primeras 4 instrucciones
        instruccion_bytes = bytes_salida[i:i+4]
        direccion = i // 4
        hex_bytes = [f"{byte:02X}" for byte in instruccion_bytes]
        
        print(f"// 0x{direccion:08X} |   {hex_bytes[0]}  |   {hex_bytes[1]}  |   {hex_bytes[2]}  |   {hex_bytes[3]}")
    
    if len(bytes_salida) > 16:
        print(f"// ... ({num_instrucciones - 4} instrucciones más)")
    
    # Verificar orden Big Endian
    instruccion_test = 0x12345678
    bytes_test = instruccion_a_bytes_big_endian(instruccion_test)
    hex_test = [f"{byte:02X}" for byte in bytes_test]
    
    print(f"\n🧪 TEST BIG ENDIAN (0x12345678):")
    print(f"   Bytes: {hex_test}")
    print(f"   Orden esperado: ['12', '34', '56', '78']")
    
    if hex_test == ['12', '34', '56', '78']:
        print("✅ BIG ENDIAN CORRECTO - Listo para Verilog")
        return True
    else:
        print("❌ ERROR en formato Big Endian")
        return False

# Prueba independiente del decodificador
if __name__ == "__main__":
    print("🔍 PROBANDO DECODIFICADOR COMPLETO - PROYECTO FINAL")
    print("=" * 70)
    
    # Probar todas las instrucciones requeridas
    test_instructions = [
        "# R-type instructions",
        "ADD $10, $3, $4",
        "SUB $8, $8, $9", 
        "AND $5, $6, $7",
        "OR $2, $2, $1",
        "SLT $1, $2, $3",
        "",
        "# I-type arithmetic/logic",
        "ADDI $8, $9, 100",
        "ANDI $10, $11, 255",
        "ORI $12, $13, 0xFF",
        "XORI $14, $15, 0xAA",
        "SLTI $16, $17, 500",
        "",
        "# I-type memory",
        "LW $10, 4($8)",
        "SW $11, 8($9)",
        "",
        "# I-type control flow", 
        "BEQ $8, $9, 0x100",
        "",
        "# J-type",
        "J 0x00400000"
    ]
    
    for inst in test_instructions:
        try:
            resultado = decodificar_instruccion(inst)
            if resultado is not None:
                tipo = "R-type" if inst.split()[0] in INSTRUCCIONES_R else \
                       "I-type" if inst.split()[0] in INSTRUCCIONES_I else "J-type"
                hex_str = format(resultado, '08X')
                print(f"{tipo:8} {inst:30} -> {hex_str}")
            else:
                print(f"{'COMENT':8} {inst:30}")
        except Exception as e:
            print(f"{'ERROR':8} {inst:30} -> {e}")
    
    # Probar formato Verilog
    print("\n" + "=" * 70)
    _, _, bytes_test = decodificar_archivo("\n".join([inst for inst in test_instructions if inst and not inst.startswith('#')]))
    verificar_formato_verilog(bytes_test)