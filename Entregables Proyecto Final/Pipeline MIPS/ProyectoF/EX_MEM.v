module EX_MEM(
    input clk,
    input reset,
    // Señales de control
    input reg_write_in, mem_to_reg_in, mem_read_in, mem_write_in,
    input branch_in,
    input [31:0] branch_target_in,
    input zero_in,
    // Datos
    input [31:0] alu_result_in,
    input [31:0] read_data2_in,
    input [4:0] write_reg_in,
    
    output reg reg_write_out, mem_to_reg_out, mem_read_out, mem_write_out,
    output reg branch_out,
    output reg [31:0] branch_target_out,
    output reg zero_out,
    output reg [31:0] alu_result_out,
    output reg [31:0] read_data2_out,
    output reg [4:0] write_reg_out
);
    always @(posedge clk or posedge reset) begin
        if (reset) begin
            reg_write_out <= 1'b0; mem_to_reg_out <= 1'b0;
            mem_read_out <= 1'b0; mem_write_out <= 1'b0;
            branch_out <= 1'b0;
            branch_target_out <= 32'b0;
            zero_out <= 1'b0;
            alu_result_out <= 32'b0;
            read_data2_out <= 32'b0;
            write_reg_out <= 5'b0;
        end else begin
            reg_write_out <= reg_write_in; mem_to_reg_out <= mem_to_reg_in;
            mem_read_out <= mem_read_in; mem_write_out <= mem_write_in;
            branch_out <= branch_in;
            branch_target_out <= branch_target_in;
            zero_out <= zero_in;
            alu_result_out <= alu_result_in;
            read_data2_out <= read_data2_in;
            write_reg_out <= write_reg_in;
        end
    end
endmodule
