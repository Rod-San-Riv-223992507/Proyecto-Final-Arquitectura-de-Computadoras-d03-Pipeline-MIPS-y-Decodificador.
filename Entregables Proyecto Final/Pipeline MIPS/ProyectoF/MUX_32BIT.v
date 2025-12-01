module MUX_32bit(
    input sel,
    input [31:0] a,
    input [31:0] b,
    output [31:0] out
);
    assign out = sel ? b : a;
endmodule
