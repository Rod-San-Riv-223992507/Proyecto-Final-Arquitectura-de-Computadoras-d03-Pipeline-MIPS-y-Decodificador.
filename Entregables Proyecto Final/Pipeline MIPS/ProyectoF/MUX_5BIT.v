module MUX_5bit(
    input sel,
    input [4:0] a,
    input [4:0] b,
    output [4:0] out
);
    assign out = sel ? b : a;
endmodule