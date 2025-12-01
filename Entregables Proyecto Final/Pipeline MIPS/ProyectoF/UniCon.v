module UniCon(
    input [5:0] opcode,
    output reg reg_write,
    output reg mem_to_reg,
    output reg branch,
    output reg mem_read,
    output reg mem_write,
    output reg alu_src,
    output reg reg_dst,
    output reg jump,
    output reg [1:0] alu_op
);
    always @* begin
        case(opcode)
            // R-type
            6'b000000: begin
                reg_write = 1'b1; mem_to_reg = 1'b0; branch = 1'b0;
                mem_read = 1'b0; mem_write = 1'b0; alu_src = 1'b0;
                reg_dst = 1'b1; jump = 1'b0; alu_op = 2'b10;
            end
            // lw
            6'b100011: begin
                reg_write = 1'b1; mem_to_reg = 1'b1; branch = 1'b0;
                mem_read = 1'b1; mem_write = 1'b0; alu_src = 1'b1;
                reg_dst = 1'b0; jump = 1'b0; alu_op = 2'b00;
            end
            // sw
            6'b101011: begin
                reg_write = 1'b0; mem_to_reg = 1'b0; branch = 1'b0;
                mem_read = 1'b0; mem_write = 1'b1; alu_src = 1'b1;
                reg_dst = 1'b0; jump = 1'b0; alu_op = 2'b00;
            end
            // beq
            6'b000100: begin
                reg_write = 1'b0; mem_to_reg = 1'b0; branch = 1'b1;
                mem_read = 1'b0; mem_write = 1'b0; alu_src = 1'b0;
                reg_dst = 1'b0; jump = 1'b0; alu_op = 2'b01;
            end
            // j
            6'b000010: begin
                reg_write = 1'b0; mem_to_reg = 1'b0; branch = 1'b0;
                mem_read = 1'b0; mem_write = 1'b0; alu_src = 1'b0;
                reg_dst = 1'b0; jump = 1'b1; alu_op = 2'b00;
            end
            // addi
            6'b001000: begin
                reg_write = 1'b1; mem_to_reg = 1'b0; branch = 1'b0;
                mem_read = 1'b0; mem_write = 1'b0; alu_src = 1'b1;
                reg_dst = 1'b0; jump = 1'b0; alu_op = 2'b00;
            end
            // andi, ori, xori, slti
            6'b001100, 6'b001101, 6'b001110, 6'b001010: begin
                reg_write = 1'b1; mem_to_reg = 1'b0; branch = 1'b0;
                mem_read = 1'b0; mem_write = 1'b0; alu_src = 1'b1;
                reg_dst = 1'b0; jump = 1'b0; alu_op = 2'b11;
            end
            default: begin
                reg_write = 1'b0; mem_to_reg = 1'b0; branch = 1'b0;
                mem_read = 1'b0; mem_write = 1'b0; alu_src = 1'b0;
                reg_dst = 1'b0; jump = 1'b0; alu_op = 2'b00;
            end
        endcase
    end
endmodule
