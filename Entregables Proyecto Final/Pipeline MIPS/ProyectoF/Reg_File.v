module Reg_File(
    input clk,
    input [4:0] read_reg1,
    input [4:0] read_reg2,
    input [4:0] write_reg,
    input [31:0] write_data,
    input reg_write,
    output reg [31:0] read_data1,
    output reg [31:0] read_data2
);
    reg [31:0] registers [0:31];
    
    integer i;
    initial begin
        for (i = 0; i < 32; i = i + 1) begin
            registers[i] = 32'b0;
        end
		
        registers[1] = 32'd10;   // $1 
        registers[2] = 32'd20;   // $2   
        registers[3] = 32'd30;   // $3 
        registers[4] = 32'd40;   // $4 
        registers[8] = 32'd200;  // $8  
        registers[9] = 32'd100;  // $9  
        registers[10] = 32'd50;  // $10 
        registers[11] = 32'd60;  // $11 
        
        $display(" Banco de registros inicializado:");
        $display("   $1=%0d, $2=%0d, $3=%0d, $4=%0d", registers[1], registers[2], registers[3], registers[4]);
        $display("   $8=%0d, $9=%0d, $10=%0d, $11=%0d", registers[8], registers[9], registers[10], registers[11]);
    end
    
    // Lectura asíncrona
    always @* begin
        read_data1 = registers[read_reg1];
        read_data2 = registers[read_reg2];
    end
    
    // Escritura síncrona
    always @(posedge clk) begin
        if (reg_write && write_reg != 0) begin
            registers[write_reg] <= write_data;
            $display(" %0t: REG[$%0d] = %h (decimal: %0d)", $time, write_reg, write_data, write_data);
        end
    end
endmodule