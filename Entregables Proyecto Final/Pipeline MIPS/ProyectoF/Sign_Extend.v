module Sign_Extend(
    input [15:0] immediate,
    output reg [31:0] extended
);
    always @* begin
        extended = { {16{immediate[15]}}, immediate };
    end
endmodule
