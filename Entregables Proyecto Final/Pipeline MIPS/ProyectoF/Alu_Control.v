module ALU_Control(
    input [1:0] alu_op,
    input [5:0] funct,
    output reg [3:0] alu_control
);
    always @* begin
        case(alu_op)
            2'b00: alu_control = 4'b0010; // add (lw, sw, addi)
            2'b01: alu_control = 4'b0110; // sub (beq)
            2'b10: begin // R-type
                case(funct)
                    6'b100000: alu_control = 4'b0010; // add
                    6'b100010: alu_control = 4'b0110; // sub
                    6'b100100: alu_control = 4'b0000; // and
                    6'b100101: alu_control = 4'b0001; // or
                    6'b101010: alu_control = 4'b0111; // slt
                    default:   alu_control = 4'b0000;
                endcase
            end
            2'b11: begin // I-type lógicas
                case(funct[3:0]) // Usamos parte del opcode
                    4'b1100: alu_control = 4'b0000; // andi
                    4'b1101: alu_control = 4'b0001; // ori
                    4'b1110: alu_control = 4'b0011; // xori
                    4'b1010: alu_control = 4'b0111; // slti
                    default: alu_control = 4'b0000;
                endcase
            end
            default: alu_control = 4'b0000;
        endcase
    end
endmodule
