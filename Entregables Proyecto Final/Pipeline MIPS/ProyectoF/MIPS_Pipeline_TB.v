`timescale 1ns/1ns

module MIPS_Pipeline_TB;

    reg clk;
    reg reset;
    wire [31:0] pc_out;
    wire [31:0] instruction_out;
    wire [31:0] alu_result_out;
    wire [31:0] mem_data_out;
    wire [31:0] wb_data_out;

    MIPS_Pipeline dut(
        .clk(clk),
        .reset(reset),
        .pc_out(pc_out),
        .instruction_out(instruction_out),
        .alu_result_out(alu_result_out),
        .mem_data_out(mem_data_out),
        .wb_data_out(wb_data_out)
    );

    // Generación de reloj
    always #10 clk = ~clk;

    initial begin
        // Configurar archivo de waveforms
        $dumpfile("mips_pipeline.vcd");
        $dumpvars(0, MIPS_Pipeline_TB);
        
        // Inicializar
        clk = 0;
        reset = 1;
        
        // Reset
        #20;
        reset = 0;
        
        $display("Iniciando simulación del Pipeline MIPS");
        $display("Time\tPC\tInstruction\tALU_Result\tMem_Data\tWB_Data");
        $display("----------------------------------------------------------------");
        
        // Ejecutar por 500ns
        #500;
        
        $display("----------------------------------------------------------------");
        $display("Simulación completada");
        $finish;
    end
    
    // Monitoreo cada ciclo de reloj
    always @(posedge clk) begin
        if (!reset) begin
            $display("%0t\t%h\t%h\t%h\t%h\t%h",
                     $time, pc_out, instruction_out, alu_result_out, mem_data_out, wb_data_out);
        end
    end

endmodule
