import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from decodificador import decodificar_archivo, obtener_instrucciones_soportadas, verificar_formato_verilog

class DecodificadorMIPSApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Decodificador MIPS - Proyecto Final Pipeline")
        self.root.geometry("1000x750")
        
        # Variables para almacenar datos
        self.lineas_originales = []
        self.instrucciones_bin = []
        self.bytes_salida = []
        self.archivo_cargado = None
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Título principal
        titulo = tk.Label(self.root, text="🚀 DECODIFICADOR MIPS - PROYECTO FINAL PIPELINE", 
                         font=("Arial", 14, "bold"), fg="darkblue")
        titulo.pack(pady=10)
        
        # Frame para instrucciones soportadas
        frame_info = tk.Frame(self.root, relief=tk.GROOVE, bd=2, bg="#F0F8FF")
        frame_info.pack(fill=tk.X, padx=10, pady=5)
        
        # Mostrar instrucciones por tipo
        info_text = tk.Text(frame_info, height=4, width=100, font=("Consolas", 9), bg="#F0F8FF")
        info_text.pack(padx=5, pady=5)
        info_text.insert(tk.END, obtener_instrucciones_soportadas())
        info_text.config(state=tk.DISABLED)
        
        # Frame para las 3 pantallas
        frame_pantallas = tk.Frame(self.root)
        frame_pantallas.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # PANEL 1: Código Assembly Original (.asm)
        frame_asm = tk.LabelFrame(frame_pantallas, text="1. ENTRADA: Código Assembly Original", 
                                 font=("Arial", 10, "bold"), bg="#E8F4FD")
        frame_asm.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # Botones de entrada
        frame_entrada = tk.Frame(frame_asm, bg="#E8F4FD")
        frame_entrada.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Button(frame_entrada, text="📁 Cargar Archivo .asm", 
                 command=self.cargar_archivo, bg="#4CAF50", fg="white", font=("Arial", 9)).pack(side=tk.LEFT, padx=2)
        tk.Button(frame_entrada, text="⭐ Ejemplo Proyecto", 
                 command=self.cargar_ejemplo_proyecto, bg="#2196F3", fg="white", font=("Arial", 9)).pack(side=tk.LEFT, padx=2)
        tk.Button(frame_entrada, text="🧹 Limpiar Entrada", 
                 command=self.limpiar_entrada, bg="#FF9800", fg="white", font=("Arial", 9)).pack(side=tk.LEFT, padx=2)
        
        self.texto_asm = scrolledtext.ScrolledText(frame_asm, height=15, width=30, font=("Consolas", 10))
        self.texto_asm.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Texto de ayuda
        texto_ayuda = """EJEMPLOS RÁPIDOS:
ADD $10, $3, $4      # R-type
ADDI $8, $9, 100     # I-type  
LW $10, 4($8)        # Memoria
BEQ $8, $9, label    # Salto
J 0x00400000         # J-type
# Comentarios con # son ignorados"""
        tk.Label(frame_asm, text=texto_ayuda, fg="gray", justify=tk.LEFT, 
                font=("Arial", 8), bg="#E8F4FD").pack()
        
        # PANEL 2: Instrucciones Limpias
        frame_limpias = tk.LabelFrame(frame_pantallas, text="2. PROCESAMIENTO: Instrucciones Validadas", 
                                     font=("Arial", 10, "bold"), bg="#F0F8FF")
        frame_limpias.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.texto_limpias = scrolledtext.ScrolledText(frame_limpias, height=15, width=25, 
                                                     font=("Consolas", 9), bg="#F0F8FF")
        self.texto_limpias.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        tk.Label(frame_limpias, text="✅ = Válida, ❌ = Error", 
                fg="blue", font=("Arial", 9), bg="#F0F8FF").pack()
        
        # PANEL 3: Código Binario
        frame_binario = tk.LabelFrame(frame_pantallas, text="3. SALIDA: Código Máquina MIPS32", 
                                     font=("Arial", 10, "bold"), bg="#FFF0F5")
        frame_binario.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.texto_binario = scrolledtext.ScrolledText(frame_binario, height=15, width=35, 
                                                     font=("Consolas", 9), bg="#FFF0F5")
        self.texto_binario.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        tk.Label(frame_binario, text="SOLO BINARIO: 32 bits Big Endian", 
                fg="darkred", font=("Arial", 9), bg="#FFF0F5").pack()
        
        # Frame para los botones principales
        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=10)
        
        # BOTÓN 2: Decodificar
        btn_decodificar = tk.Button(frame_botones, text="⚡ DECODIFICAR Instrucciones", 
                                   command=self.decodificar, width=22, height=2,
                                   bg="#4CAF50", fg="white", font=("Arial", 11, "bold"))
        btn_decodificar.pack(side=tk.LEFT, padx=5)
        
        # BOTÓN 4: Guardar Resultado
        btn_guardar = tk.Button(frame_botones, text="💾 GUARDAR Para Verilog", 
                               command=self.guardar_resultado, width=20, height=2,
                               bg="#2196F3", fg="white", font=("Arial", 11, "bold"))
        btn_guardar.pack(side=tk.LEFT, padx=5)
        
        # BOTÓN 3: Limpiar Todo
        btn_limpiar = tk.Button(frame_botones, text="🧹 LIMPIAR Todo", 
                               command=self.limpiar_todo, width=15, height=2,
                               bg="#FF9800", fg="white", font=("Arial", 11, "bold"))
        btn_limpiar.pack(side=tk.LEFT, padx=5)
        
        # BOTÓN 5: Verificar Verilog
        btn_verilog = tk.Button(frame_botones, text="🔧 Verificar Verilog", 
                               command=self.verificar_verilog, width=15, height=2,
                               bg="#9C27B0", fg="white", font=("Arial", 11))
        btn_verilog.pack(side=tk.LEFT, padx=5)
        
        # Área de estado
        self.estado = tk.Label(self.root, text="🎯 LISTO - Escribe código MIPS o carga archivo .asm", 
                              relief=tk.SUNKEN, anchor=tk.W, bg="#E8F5E8", fg="darkgreen",
                              font=("Arial", 10, "bold"))
        self.estado.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=2)
    
    def cargar_archivo(self):
        """Carga archivo .asm o .txt"""
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo MIPS",
            filetypes=[("Archivos assembly", "*.asm"), ("Archivos texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        
        if archivo:
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                
                self.texto_asm.delete(1.0, tk.END)
                self.texto_asm.insert(1.0, contenido)
                self.archivo_cargado = archivo
                self.estado.config(text=f"✅ Archivo cargado: {archivo}")
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{e}")
    
    def cargar_ejemplo_proyecto(self):
        """Carga ejemplo del proyecto final"""
        ejemplo = """# PROYECTO FINAL - Programa no trivial para Pipeline MIPS
# Calcula la suma de los primeros N números y maneja arrays

# Inicialización
    ADDI $sp, $zero, 0x1000  # Inicializar stack pointer
    ADDI $s0, $zero, 10      # N = 10 (calcular suma de 1 a 10)
    ADD $s1, $zero, $zero    # suma = 0
    ADD $s2, $zero, $zero    # i = 0

# Loop principal - suma los primeros N números
LOOP:
    SLT $t0, $s2, $s0        # $t0 = 1 si i < N
    BEQ $t0, $zero, FIN_LOOP # Si i >= N, termina loop
    
    # Calcular dirección en "array" (simulado en stack)
    SLL $t1, $s2, 2          # $t1 = i * 4 (desplazamiento)
    ADD $t1, $t1, $sp        # $t1 = dirección en stack
    
    # Guardar valor actual en "array"
    ADDI $t2, $s2, 1         # $t2 = i + 1 (valor a guardar)
    SW $t2, 0($t1)           # array[i] = i + 1
    
    # Sumar al acumulador
    ADD $s1, $s1, $t2        # suma += (i + 1)
    
    # Operaciones lógicas de prueba
    ANDI $t3, $s2, 1         # $t3 = i AND 1 (par/impar)
    ORI $t4, $s2, 0xFF00     # $t4 = i OR 0xFF00
    XORI $t5, $s2, 0x00FF    # $t5 = i XOR 0x00FF
    SLTI $t6, $s2, 5         # $t6 = 1 si i < 5
    
    # Incrementar contador
    ADDI $s2, $s2, 1         # i++
    J LOOP                   # Repetir loop

FIN_LOOP:
    # Verificar resultado (suma debería ser 55 para N=10)
    ADDI $t6, $zero, 55      # Resultado esperado
    SLT $t7, $s1, $t6        # $t7 = 1 si suma < 55
    BEQ $t7, $zero, RESULTADO_CORRECTO

RESULTADO_INCORRECTO:
    ADDI $v0, $zero, 0       # Código de error
    J FIN_PROGRAMA

RESULTADO_CORRECTO:
    ADDI $v0, $zero, 1       # Código de éxito
    SW $s1, 0($sp)           # Guardar resultado en memoria

FIN_PROGRAMA:
    # Limpiar y terminar
    ADD $a0, $v0, $zero      # Pasar código de resultado
    J 0x00000000             # Salir (simulación)"""
        
        self.texto_asm.delete(1.0, tk.END)
        self.texto_asm.insert(1.0, ejemplo)
        self.estado.config(text="✅ Ejemplo del Proyecto Final cargado")
    
    def limpiar_entrada(self):
        """Limpia solo el panel de entrada"""
        self.texto_asm.delete(1.0, tk.END)
        self.estado.config(text="✅ Entrada limpiada - Escribe nuevas instrucciones")
    
    def decodificar(self):
        """Decodifica las instrucciones - SOLO BINARIO EN PANEL 3"""
        contenido = self.texto_asm.get(1.0, tk.END).strip()
        if not contenido:
            messagebox.showwarning("Entrada Vacía", "Escribe instrucciones MIPS o carga un archivo.")
            return
        
        try:
            # Usar nuestro decodificador
            self.lineas_originales, self.instrucciones_bin, self.bytes_salida = decodificar_archivo(contenido)
            
            # Mostrar en Panel 2: instrucciones válidas
            self.texto_limpias.delete(1.0, tk.END)
            instrucciones_validas = []
            errores = []
            
            for i, (linea, inst_bin) in enumerate(zip(self.lineas_originales, self.instrucciones_bin)):
                linea_limpia = linea.strip()
                if linea_limpia and not linea_limpia.startswith('#'):
                    if inst_bin is not None:
                        # Detectar tipo de instrucción
                        mnemonic = linea_limpia.split()[0]
                        tipo = "R" if mnemonic in ['ADD','SUB','AND','OR','SLT'] else \
                               "I" if mnemonic in ['ADDI','ANDI','ORI','XORI','SLTI','LW','SW','BEQ'] else "J"
                        instrucciones_validas.append(f"✅ [{tipo}] Línea {i+1}: {linea_limpia}")
                    else:
                        instrucciones_validas.append(f"❌ Línea {i+1}: {linea_limpia} [ERROR]")
                        errores.append(f"Línea {i+1}")
            
            self.texto_limpias.insert(1.0, '\n'.join(instrucciones_validas))
            
            # 🎯 PANEL 3: SOLO BINARIO PURO (32 bits por línea)
            self.texto_binario.delete(1.0, tk.END)
            
            instruccion_count = 0
            for i, inst_bin in enumerate(self.instrucciones_bin):
                if inst_bin is not None:
                    instruccion_count += 1
                    bin_str = format(inst_bin, '032b')  # 32 bits puros
                    # 🚫 SOLO ESCRIBIMOS LOS BITS, NADA MÁS
                    self.texto_binario.insert(tk.END, f"{bin_str}\n")
            
            # Actualizar estado
            total_lineas = len([l for l in self.lineas_originales if l.strip() and not l.strip().startswith('#')])
            mensaje = f"✅ Decodificación completada: {instruccion_count}/{total_lineas} instrucciones procesadas"
            if errores:
                mensaje += f" - Errores en: {', '.join(errores)}"
            self.estado.config(text=mensaje)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en decodificación:\n{e}")
            self.estado.config(text="❌ Error en decodificación")
    
    def limpiar_todo(self):
        """Limpia todas las pantallas"""
        self.texto_asm.delete(1.0, tk.END)
        self.texto_limpias.delete(1.0, tk.END)
        self.texto_binario.delete(1.0, tk.END)
        
        self.lineas_originales = []
        self.instrucciones_bin = []
        self.bytes_salida = []
        self.archivo_cargado = None
        
        self.estado.config(text="✅ Todo limpiado - Listo para nuevo código")
    
    def guardar_resultado(self):
        """Guarda el resultado en instrucciones.txt - SOLO BINARIO"""
        if not self.bytes_salida:
            messagebox.showwarning("Sin Datos", "No hay datos para guardar. Decodifica primero.")
            return
        
        try:
            archivo_salida = filedialog.asksaveasfilename(
                title="Guardar para Verilog",
                defaultextension=".txt",
                filetypes=[("Archivo texto", "*.txt"), ("Todos los archivos", "*.*")],
                initialfile="instrucciones.txt"
            )
            
            if archivo_salida:
                with open(archivo_salida, 'w', encoding='utf-8') as f:
                    # 🎯 SOLO ESCRIBIMOS BINARIO, SIN TEXTO
                    for i in range(0, len(self.bytes_salida), 4):
                        instruccion_bytes = self.bytes_salida[i:i+4]
                        instruccion_32bits = 0
                        for j, byte in enumerate(instruccion_bytes):
                            instruccion_32bits |= (byte << (24 - j * 8))
                        # 🚫 SOLO LOS 32 BITS, NADA MÁS
                        f.write(f"{instruccion_32bits:032b}\n")
                
                self.estado.config(text=f"✅ Archivo guardado: {archivo_salida}")
                messagebox.showinfo("Éxito", 
                    f"✅ Archivo guardado exitosamente!\n\n"
                    f"📁 Archivo: {archivo_salida}\n"
                    f"🔢 Instrucciones: {len(self.bytes_salida) // 4}\n"
                    f"🎯 Formato: 32 bits Big Endian\n"
                    f"💾 Listo para Verilog: $readmemb(\"instrucciones.txt\", mem);")
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")
    
    def verificar_verilog(self):
        """Verifica el formato para Verilog"""
        if not self.bytes_salida:
            messagebox.showwarning("Sin Datos", "No hay datos para verificar. Decodifica primero.")
            return
        
        # Crear ventana de verificación
        ventana_verilog = tk.Toplevel(self.root)
        ventana_verilog.title("Verificación Formato Verilog")
        ventana_verilog.geometry("600x400")
        
        texto_verilog = scrolledtext.ScrolledText(ventana_verilog, font=("Consolas", 9))
        texto_verilog.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Redirigir print a la ventana
        import io
        from contextlib import redirect_stdout
        
        f = io.StringIO()
        with redirect_stdout(f):
            verificar_formato_verilog(self.bytes_salida)
        
        texto_verilog.insert(tk.END, f.getvalue())
        texto_verilog.config(state=tk.DISABLED)
        
        btn_cerrar = tk.Button(ventana_verilog, text="Cerrar", command=ventana_verilog.destroy,
                              bg="#4CAF50", fg="white", font=("Arial", 10))
        btn_cerrar.pack(pady=5)
    
    def mostrar_info(self):
        """Muestra información del programa"""
        info_texto = f"""
DECODIFICADOR MIPS - PROYECTO FINAL PIPELINE

{obtener_instrucciones_soportadas()}

🎯 CARACTERÍSTICAS:
• Decodificador completo para Pipeline MIPS de 5 etapas
• Formato MIPS32 exacto (Big Endian)
• Preparado para precarga en memoria Verilog
• Validación completa de sintaxis
• Interfaz gráfica intuitiva

📋 INSTRUCCIONES REQUERIDAS:
• R-type: Operaciones entre registros
• I-type: Operaciones con inmediato/memoria/saltos  
• J-type: Saltos incondicionales

💾 USO EN VERILOG:
module instruction_memory (
    input [31:0] address,
    output reg [31:0] instruction
);
    reg [31:0] mem [0:255];
    initial begin
        $readmemb("instrucciones.txt", mem);
    end
    // ... resto del código
endmodule

🛠️ DESARROLLADO PARA: Proyecto Final - Arquitectura de Computadoras
        """
        messagebox.showinfo("🎓 Decodificador MIPS - Proyecto Final", info_texto)

if __name__ == "__main__":
    app = DecodificadorMIPSApp()
    app.root.mainloop()