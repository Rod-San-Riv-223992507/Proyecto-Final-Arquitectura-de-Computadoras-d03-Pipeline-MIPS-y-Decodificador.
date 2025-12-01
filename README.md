# Proyecto-Final-Arquitectura-de-Computadoras-d03
Proyecto final de la materia de Arquitectura de Computadoras. Consiste en un Pipeline MIPS de 5 etapas en Verilog (usando el programa de ModelSim) y de un decodificador en Python que decodifica instrucciones MIPS (assembly) a binario (Big Endian).
# Pipeline MIPS de 5 Etapas con Decodificador en Python


## Características

### Decodificador Python (GUI)
- Interfaz gráfica intuitiva con tkinter
- Conversión de assembly MIPS a binario MIPS32
- Validación de sintaxis en tiempo real
- Generación de archivos para Verilog (Big Endian)
- Manejo robusto de errores

### Pipeline MIPS (Verilog)
- Pipeline de 5 etapas: IF, ID, EX, MEM, WB
- Soporte completo para instrucciones R-type, I-type, J-type
- Buffers interetapas sincronizados
- Testbench completo con verificación automática
- Logging detallado para debugging

## Instalación y Uso

### Prerrequisitos
```bash
# Python 3.8+
python --version

# ModelSim o simulador Verilog compatible
# tkinter (generalmente incluido con Python)
# Compilar todos los módulos
vlog *.v

# Ejecutar testbench
vsim MIPS_Pipeline_TB

# Agregar señales al wave
add wave *

# Ejecutar simulación
run 300ns (Para ver el proceso completo sino ir de 25ns a 25ns para ver cada intrucción trabajar)
mips-pipeline/
├── 📁 python/                 # Decodificador en Python
│   ├── main.py               # Interfaz gráfica principal
│   ├── decodificador.py      # Motor de decodificación
├── 📁 verilog/               # Pipeline MIPS en Verilog
│   ├── MIPS_Pipeline.v       # Módulo principal
│   ├── PC.v                  # Contador de programa
│   ├── InsMem.v              # Memoria de instrucciones
│   ├── Reg_File.v            # Banco de registros
│   ├── ALU.v                 # Unidad aritmético-lógica
│   ├── UniCon.v              # Unidad de control
│   ├── Mem_Datos.v           # Memoria de datos
│   ├── Buffers/              # Buffers de pipeline
│   │   ├── IF_ID.v
│   │   ├── ID_EX.v
│   │   ├── EX_MEM.v
│   │   └── MEM_WB.v
│   └── Testbench/
│       └── MIPS_Pipeline_TB.v
│   ├── Reporte_Proyecto.pdf
└── README.md
