module Mem_Datos(
     input clk,
    input [31:0] address,
    input [31:0] write_data,
    input mem_read,
    input mem_write,
    output reg [31:0] read_data
);
    reg [31:0] mem [0:255];
    
    integer i;
    initial begin
        for (i = 0; i < 256; i = i + 1) begin
            mem[i] = 32'b0;
        end
        
        mem[1] = 32'h0000000A;  // address 0x04
        mem[2] = 32'h0000000B;  // address 0x08  
        mem[3] = 32'h0000000C;  // address 0x0C
        mem[4] = 32'h0000000D;  // address 0x10
        mem[5] = 32'h0000000E;  // address 0x14
        
        $display(" Memoria de datos inicializada:");
        $display("   MEM[1]=%h, MEM[2]=%h, MEM[3]=%h", mem[1], mem[2], mem[3]);
    end
    
    always @* begin
        if (mem_read) begin
            read_data = mem[address >> 2];
            $display(" %0t: MEM_READ[%0d] = %h", $time, address >> 2, read_data);
        end else begin
            read_data = 32'b0;
        end
    end
    
    always @(posedge clk) begin
        if (mem_write) begin
            mem[address >> 2] <= write_data;
            $display("%0t: MEM_WRITE[%0d] <= %h", $time, address >> 2, write_data);
        end
    end
endmodule