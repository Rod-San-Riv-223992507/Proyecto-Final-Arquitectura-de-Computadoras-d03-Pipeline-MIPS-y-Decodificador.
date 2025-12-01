module ID_EX(
    input clk,
    input reset,
    // Señales de control
    input reg_write_in, mem_to_reg_in, mem_read_in, mem_write_in,
    input alu_src_in, reg_dst_in, 
    input [1:0] alu_op_in,
    // Datos
    input [31:0] pc_plus_4_in,
    input [31:0] read_data1_in, read_data2_in,
    input [31:0] sign_extend_in,
    input [4:0] rt_in, rd_in,
    input [5:0] funct_in,
    
    output reg reg_write_out, mem_to_reg_out, mem_read_out, mem_write_out,
    output reg alu_src_out, reg_dst_out,
    output reg [1:0] alu_op_out,
    output reg [31:0] pc_plus_4_out,
    output reg [31:0] read_data1_out, read_data2_out,
    output reg [31:0] sign_extend_out,
    output reg [4:0] rt_out, rd_out,
    output reg [5:0] funct_out
);
    always @(posedge clk or posedge reset) begin
        if (reset) begin
            reg_write_out <= 1'b0; mem_to_reg_out <= 1'b0;
            mem_read_out <= 1'b0; mem_write_out <= 1'b0;
            alu_src_out <= 1'b0; reg_dst_out <= 1'b0;
            alu_op_out <= 2'b00;
            pc_plus_4_out <= 32'b0;
            read_data1_out <= 32'b0; read_data2_out <= 32'b0;
            sign_extend_out <= 32'b0;
            rt_out <= 5'b0; rd_out <= 5'b0;
            funct_out <= 6'b0;
        end else begin
            reg_write_out <= reg_write_in; mem_to_reg_out <= mem_to_reg_in;
            mem_read_out <= mem_read_in; mem_write_out <= mem_write_in;
            alu_src_out <= alu_src_in; reg_dst_out <= reg_dst_in;
            alu_op_out <= alu_op_in;
            pc_plus_4_out <= pc_plus_4_in;
            read_data1_out <= read_data1_in; read_data2_out <= read_data2_in;
            sign_extend_out <= sign_extend_in;
            rt_out <= rt_in; rd_out <= rd_in;
            funct_out <= funct_in;
        end
    end
endmodule
