module IF_ID(
    input clk,
    input reset,
    input [31:0] pc_plus_4_in,
    input [31:0] instruction_in,
    output reg [31:0] pc_plus_4_out,
    output reg [31:0] instruction_out
);
    always @(posedge clk or posedge reset) begin
        if (reset) begin
            pc_plus_4_out <= 32'b0;
            instruction_out <= 32'b0;
        end else begin
            pc_plus_4_out <= pc_plus_4_in;
            instruction_out <= instruction_in;
        end
    end
endmodule
