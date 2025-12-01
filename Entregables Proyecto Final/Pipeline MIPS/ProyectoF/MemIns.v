module MemIns(
    input [31:0] address,
    output reg [31:0] instruction
);
    reg [31:0] mem [0:255];
    integer i;
    initial begin
        
        $readmemb("instrucciones.txt", mem);
        
        
        // Mostrar las primeras 8 instrucciones
        for (i = 0; i < 8; i = i + 1) begin
            if (i < 256) begin
                $display("   MEM[%0d] = %b", i, mem[i]);
            end
        end
    end
    
    always @* begin
        if (address < 1024) begin
            instruction = mem[address >> 2];
        end else begin
            instruction = 32'b0;
        end
    end
endmodule
