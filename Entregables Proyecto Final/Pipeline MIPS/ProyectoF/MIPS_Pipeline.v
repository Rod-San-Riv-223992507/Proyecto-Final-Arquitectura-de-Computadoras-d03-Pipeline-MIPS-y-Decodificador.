module MIPS_Pipeline(
    input clk,
    input reset,
    output [31:0] pc_out,
    output [31:0] instruction_out,
    output [31:0] alu_result_out,
    output [31:0] mem_data_out,
    output [31:0] wb_data_out
);
    
    // === SEÑALES GLOBALES ===
    wire [31:0] pc_next, pc_current, pc_plus_4;
    wire [31:0] instruction;
    
    // === SEÑALES WB ===
    wire mem_wb_reg_write;
    wire [4:0] mem_wb_write_reg;
    wire [31:0] wb_data;
    
    // === ETAPA IF ===
    PC pc(.clk(clk), .reset(reset), .next_pc(pc_next), .current_pc(pc_current));
    MemIns imem(.address(pc_current), .instruction(instruction));
    
    // Sumador para PC+4
    Adder_32bit pc_adder(.a(pc_current), .b(32'd4), .result(pc_plus_4));
    
    // === BUFFER IF/ID ===
    wire [31:0] if_id_pc_plus_4, if_id_instruction;
    IF_ID if_id(.clk(clk), .reset(reset),
        .pc_plus_4_in(pc_plus_4), .instruction_in(instruction),
        .pc_plus_4_out(if_id_pc_plus_4), .instruction_out(if_id_instruction));
    
    // === ETAPA ID ===
    // Unidad de Control
    wire reg_write, mem_to_reg, branch, mem_read, mem_write, alu_src, reg_dst, jump;
    wire [1:0] alu_op;
    UniCon control(.opcode(if_id_instruction[31:26]),
        .reg_write(reg_write), .mem_to_reg(mem_to_reg), .branch(branch),
        .mem_read(mem_read), .mem_write(mem_write), .alu_src(alu_src),
        .reg_dst(reg_dst), .jump(jump), .alu_op(alu_op));
    
    // Banco de Registros
    wire [31:0] read_data1, read_data2;
    Reg_File rf(.clk(clk),
        .read_reg1(if_id_instruction[25:21]), .read_reg2(if_id_instruction[20:16]),
        .write_reg(mem_wb_write_reg), .write_data(wb_data),
        .reg_write(mem_wb_reg_write), .read_data1(read_data1), .read_data2(read_data2));
    
    // Extensión de signo
    wire [31:0] sign_extended;
    Sign_Extend sign_ext(.immediate(if_id_instruction[15:0]), .extended(sign_extended));
    
    // === BUFFER ID/EX ===
    wire id_ex_reg_write, id_ex_mem_to_reg, id_ex_mem_read, id_ex_mem_write;
    wire id_ex_alu_src, id_ex_reg_dst;
    wire [1:0] id_ex_alu_op;
    wire [31:0] id_ex_pc_plus_4, id_ex_read_data1, id_ex_read_data2, id_ex_sign_extended;
    wire [4:0] id_ex_rt, id_ex_rd;
    wire [5:0] id_ex_funct;
    
    ID_EX id_ex(.clk(clk), .reset(reset),
        .reg_write_in(reg_write), .mem_to_reg_in(mem_to_reg),
        .mem_read_in(mem_read), .mem_write_in(mem_write),
        .alu_src_in(alu_src), .reg_dst_in(reg_dst), .alu_op_in(alu_op),
        .pc_plus_4_in(if_id_pc_plus_4), .read_data1_in(read_data1), .read_data2_in(read_data2),
        .sign_extend_in(sign_extended), .rt_in(if_id_instruction[20:16]),
        .rd_in(if_id_instruction[15:11]), .funct_in(if_id_instruction[5:0]),
        .reg_write_out(id_ex_reg_write), .mem_to_reg_out(id_ex_mem_to_reg),
        .mem_read_out(id_ex_mem_read), .mem_write_out(id_ex_mem_write),
        .alu_src_out(id_ex_alu_src), .reg_dst_out(id_ex_reg_dst), .alu_op_out(id_ex_alu_op),
        .pc_plus_4_out(id_ex_pc_plus_4), .read_data1_out(id_ex_read_data1),
        .read_data2_out(id_ex_read_data2), .sign_extend_out(id_ex_sign_extended),
        .rt_out(id_ex_rt), .rd_out(id_ex_rd), .funct_out(id_ex_funct));
    
    // === ETAPA EX ===
    // ALU Control
    wire [3:0] alu_control;
    ALU_Control alu_ctrl(.alu_op(id_ex_alu_op), .funct(id_ex_funct), .alu_control(alu_control));
    
    // MUX para segundo operando ALU
    wire [31:0] alu_b;
    MUX_32bit alu_src_mux(.sel(id_ex_alu_src), .a(id_ex_read_data2), 
                              .b(id_ex_sign_extended), .out(alu_b));
    
    // ALU
    wire [31:0] alu_result;
    wire alu_zero;
    ALU alu(.a(id_ex_read_data1), .b(alu_b), .alu_control(alu_control),
        .result(alu_result), .zero(alu_zero));
    
    // MUX para registro destino
    wire [4:0] write_reg;
    MUX_5bit reg_dst_mux(.sel(id_ex_reg_dst), .a(id_ex_rt), .b(id_ex_rd), .out(write_reg));
    
    // Cálculo de dirección de salto
    wire [31:0] sign_extended_shifted;
    Shift_Left_2 shift_branch(.in(id_ex_sign_extended), .out(sign_extended_shifted));
    
    wire [31:0] branch_target;
    Adder_32bit branch_adder(.a(id_ex_pc_plus_4), .b(sign_extended_shifted), .result(branch_target));
    
    // === BUFFER EX/MEM ===
    wire ex_mem_reg_write, ex_mem_mem_to_reg, ex_mem_mem_read, ex_mem_mem_write, ex_mem_branch;
    wire ex_mem_zero;
    wire [31:0] ex_mem_branch_target, ex_mem_alu_result, ex_mem_read_data2;
    wire [4:0] ex_mem_write_reg;
    
    EX_MEM ex_mem(.clk(clk), .reset(reset),
        .reg_write_in(id_ex_reg_write), .mem_to_reg_in(id_ex_mem_to_reg),
        .mem_read_in(id_ex_mem_read), .mem_write_in(id_ex_mem_write),
        .branch_in(branch), .branch_target_in(branch_target), .zero_in(alu_zero),
        .alu_result_in(alu_result), .read_data2_in(id_ex_read_data2), .write_reg_in(write_reg),
        .reg_write_out(ex_mem_reg_write), .mem_to_reg_out(ex_mem_mem_to_reg),
        .mem_read_out(ex_mem_mem_read), .mem_write_out(ex_mem_mem_write),
        .branch_out(ex_mem_branch), .branch_target_out(ex_mem_branch_target),
        .zero_out(ex_mem_zero), .alu_result_out(ex_mem_alu_result),
        .read_data2_out(ex_mem_read_data2), .write_reg_out(ex_mem_write_reg));
    
    // === ETAPA MEM ===
    // Memoria de datos
    wire [31:0] mem_read_data;
    Mem_Datos dmem(.clk(clk), .address(ex_mem_alu_result),
        .write_data(ex_mem_read_data2), .mem_read(ex_mem_mem_read),
        .mem_write(ex_mem_mem_write), .read_data(mem_read_data));
    
    // Lógica de salto
    wire pcsrc = ex_mem_branch & ex_mem_zero;
    
    // === BUFFER MEM/WB ===
    wire mem_wb_mem_to_reg;
    wire [31:0] mem_wb_read_data, mem_wb_alu_result;
    
    MEM_WR mem_wb(.clk(clk), .reset(reset),
        .reg_write_in(ex_mem_reg_write), .mem_to_reg_in(ex_mem_mem_to_reg),
        .read_data_in(mem_read_data), .alu_result_in(ex_mem_alu_result),
        .write_reg_in(ex_mem_write_reg),
        .reg_write_out(mem_wb_reg_write), .mem_to_reg_out(mem_wb_mem_to_reg),
        .read_data_out(mem_wb_read_data), .alu_result_out(mem_wb_alu_result),
        .write_reg_out(mem_wb_write_reg));
    
    // === ETAPA WB ===
    MUX_32bit mem_to_reg_mux(.sel(mem_wb_mem_to_reg), .a(mem_wb_alu_result), 
                                 .b(mem_wb_read_data), .out(wb_data));
    
    // === LÓGICA DEL PC ===
    MUX_32bit pc_src_mux(.sel(pcsrc), .a(pc_plus_4), .b(ex_mem_branch_target), .out(pc_next));
    
    // === SALIDAS PARA MONITOREO ===
    assign pc_out = pc_current;
    assign instruction_out = instruction;
    assign alu_result_out = alu_result;
    assign mem_data_out = mem_read_data;
    assign wb_data_out = wb_data;

endmodule