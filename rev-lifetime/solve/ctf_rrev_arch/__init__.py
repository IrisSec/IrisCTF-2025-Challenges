from binaryninja import (Architecture, RegisterInfo, InstructionInfo,
    InstructionTextToken, InstructionTextTokenType, InstructionTextTokenContext,
    BranchType,
    LowLevelILFunction,
    LowLevelILLabel,
    BinaryView,
    SegmentFlag, SectionSemantics,
    log
)

import struct
import json

OP_IDS = {}

#MEM_OFS = 1<<24
MEM_OFS = 0
INST_OFS = 2*1<<28
JT_OFS = 3*1<<28
ENTRY_OFS = 4*1<<28

JUMP_TABLE = []

class CTFRRev(Architecture):
    name = "IrisCTF RRev Chal"
    address_size = 4
    default_int_size = 8
    instr_alignment = 16
    max_instr_length = 16 # bytes

    regs = {
        "A": RegisterInfo("A", 3),
        "B": RegisterInfo("B", 3),
        "C": RegisterInfo("C", 3),
        "D": RegisterInfo("D", 3),
        "SP": RegisterInfo("SP", 3),
        "BP": RegisterInfo("BP", 3)
    }
    reg_nums = ["A", "B", "C", "D", "SP", "BP"]
    stack_pointer = "SP"

    def get_instruction_info(self, data, address):
        if len(data) < 16: return None
        data = struct.unpack("<IIII", data[:16])
        opcode = OP_IDS[data[0]]
        result = InstructionInfo()
        result.length = 16

        #if opcode == "JTENTRY":
        #    result.add_branch(BranchType.UnconditionalBranch, 0)
        if opcode == "JMP":
            if data[1] & 2:
                #result.add_branch(BranchType.IndirectBranch)
                # log.log_info(f"@ {hex(address)} indbrj {opcode} - {data}")
                # if (data[1] >> 2) == 0:
                #     result.add_branch(BranchType.FunctionReturn)
                # else:
                #     result.add_branch(BranchType.IndirectBranch)
                pass
            else:
                result.add_branch(BranchType.UnconditionalBranch, JUMP_TABLE[data[1] >> 2])
        elif opcode[0] == "J":
            if data[1] & 2:
                result.add_branch(BranchType.IndirectBranch)
                log.log_info(f"indbrj {opcode} - {data}")
            else:
                result.add_branch(BranchType.TrueBranch, JUMP_TABLE[data[1] >> 2])
                result.add_branch(BranchType.FalseBranch, address + 16)
    
        return result

    def get_instruction_text(self, data, address):
        if len(data) < 16: return None
        data = struct.unpack("<IIII", data[:16])
        opcode = OP_IDS[data[0]]
        tokens = []

        if opcode in ["JTENTRY","NOP"]:
            tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, opcode.lower()))
        elif opcode == "JMP":
            tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, "jmp"))
            tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, " "))
            if data[1] & 2:
                # tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, self.reg_nums[data[1] >> 2]))
                tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, "nop-ed"))
            else:
                tokens.append(InstructionTextToken(InstructionTextTokenType.PossibleAddressToken, str(JUMP_TABLE[data[1] >> 2]), JUMP_TABLE[data[1] >> 2]))
        elif opcode == "EXIT":
            tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, "exit"))
        elif opcode == "STORE":
            tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, "store"))
            tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, " "))
            if data[1] & 1:
                tokens.append(InstructionTextToken(InstructionTextTokenType.PossibleAddressToken, self.reg_nums[data[2]]))
            else:
                tokens.append(InstructionTextToken(InstructionTextTokenType.PossibleAddressToken, hex(data[2]), data[2]))
            tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, ", "))
            tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, self.reg_nums[data[3]]))
        elif opcode == "LOAD":
            tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, "load"))
            tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, " "))
            tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, self.reg_nums[data[3]]))
            tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, ", "))
            if data[1] & 1:
                tokens.append(InstructionTextToken(InstructionTextTokenType.PossibleAddressToken, self.reg_nums[data[2]]))
            else:
                tokens.append(InstructionTextToken(InstructionTextTokenType.PossibleAddressToken, hex(data[2]), data[2]))
        elif opcode in ["PUTCHAR", "GETCHAR", "POP", "PUSH"]:
            tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, opcode.lower()))
            tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, " "))
            tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, self.reg_nums[data[3]]))
        elif opcode in ["EQ", "NE", "GT", "GE", "LT", "LE", "MOV", "ADD", "SUB"]: # 2 ops
            tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, opcode.lower()))
            tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, " "))
            tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, self.reg_nums[data[3]]))
            tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, ", "))
            if data[1] & 1:
                tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, self.reg_nums[data[2]]))
            else:
                tokens.append(InstructionTextToken(InstructionTextTokenType.IntegerToken, hex(data[2]), data[2]))
        else:
            # jump and 2 operands

            tokens.append(InstructionTextToken(InstructionTextTokenType.InstructionToken, opcode.lower()))
            tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, " "))
            tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, self.reg_nums[data[3]]))
            tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, ", "))
            if data[1] & 1:
                tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, self.reg_nums[data[2]]))
            else:
                tokens.append(InstructionTextToken(InstructionTextTokenType.IntegerToken, hex(data[2]), data[2]))

            tokens.append(InstructionTextToken(InstructionTextTokenType.OperandSeparatorToken, ", "))
            if data[1] & 2:
                tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken, self.reg_nums[data[1] >> 2]))
            else:
                tokens.append(InstructionTextToken(InstructionTextTokenType.PossibleAddressToken, str(JUMP_TABLE[data[1] >> 2]), JUMP_TABLE[data[1] >> 2]))

        return tokens, 16
    
    def emit_indirect_jump(self, dst, il: LowLevelILFunction):
        return il.load(4, il.add(4, il.const(4, JT_OFS), il.mult(4, dst, il.const(3, 4))))

    def get_instruction_low_level_il(self, data, address, il: LowLevelILFunction):
        if len(data) < 16: return None
        data = struct.unpack("<IIII", data[:16])
        opcode = OP_IDS[data[0]]

        if opcode == "JTENTRY":
            #il.append(il.nop())
            il.append(il.set_reg(3, self.reg_nums[0], il.const(3, 0)))
            il.append(il.set_reg(3, self.reg_nums[1], il.const(3, 0)))
            il.append(il.set_reg(3, self.reg_nums[2], il.const(3, 0)))
            il.append(il.set_reg(3, self.reg_nums[3], il.const(3, 0)))
            il.append(il.set_reg(3, self.reg_nums[4], il.const(3, 0)))
            il.append(il.set_reg(3, self.reg_nums[5], il.const(3, 0)))
            #il.append(il.jump(il.const_pointer(4, INST_OFS)))
        elif opcode == "EXIT":
            il.append(il.no_ret())
        elif opcode in ["PUTCHAR", "GETCHAR"]:
            il.append(il.set_reg(3, self.reg_nums[data[3]], il.system_call()))
        elif opcode == "STORE":
            if data[1] & 1:
                addr = il.reg(3, self.reg_nums[data[2]])
            else:
                addr = data[2]

            addr = il.mult(4, addr, il.const(4, 4))
            val = il.reg(3, self.reg_nums[data[3]])
            il.append(il.store(4, addr, val))
        elif opcode == "LOAD":
            if data[1] & 1:
                addr = il.reg(3, self.reg_nums[data[2]])
            else:
                addr = data[2]
            addr = il.mult(4, addr, il.const(4, 4))
            il.append(il.set_reg(3, self.reg_nums[data[3]], il.load(4, addr)))
        elif opcode == "JMP":
            if data[1] & 2:
                # dst = self.emit_indirect_jump(il.reg(3, self.reg_nums[data[1] >> 2]), il)
                pass
            else:
                if data[1] >> 2 >= 609:
                    dst = il.const(4, JUMP_TABLE[data[1] >> 2])
                    il.append(il.jump(dst))
        elif opcode == "MOV":
            if data[1] & 1:
                src = il.reg(3, self.reg_nums[data[2]])
            else:
                src = il.const(3, data[2])
            il.append(il.set_reg(3, self.reg_nums[data[3]], src))
        elif opcode == "ADD":
            if data[1] & 1:
                src = il.reg(3, self.reg_nums[data[2]])
            else:
                src = il.const(3, data[2])
            op = il.add(3, src, il.reg(3, self.reg_nums[data[3]]))
            il.append(il.set_reg(3, self.reg_nums[data[3]], op))
        elif opcode == "SUB":
            if data[1] & 1:
                src = il.reg(3, self.reg_nums[data[2]])
            else:
                src = il.const(3, data[2])
            op = il.sub(3, il.reg(3, self.reg_nums[data[3]]), src)
            il.append(il.set_reg(3, self.reg_nums[data[3]], op))
        elif opcode in ["EQ", "NE", "LT", "LE", "GT", "GE"]:
            if data[1] & 1:
                src = il.reg(3, self.reg_nums[data[2]])
            else:
                src = il.const(3, data[2])
            dst = il.reg(3, self.reg_nums[data[3]])
            if opcode == "EQ": op = il.compare_equal
            elif opcode == "NE": op = il.compare_not_equal
            elif opcode == "LT": op = il.compare_unsigned_less_than
            elif opcode == "LE": op = il.compare_unsigned_less_equal
            elif opcode == "GT": op = il.compare_unsigned_greater_than
            elif opcode == "GE": op = il.compare_unsigned_greater_equal

            il.append(il.set_reg(3, self.reg_nums[data[3]], op(3, dst, src)))
        elif opcode in ["JEQ", "JNE", "JLT", "JLE", "JGT", "JGE"]:
            if data[1] & 1:
                src = il.reg(3, self.reg_nums[data[2]])
            else:
                src = il.const(3, data[2])
            dst = il.reg(3, self.reg_nums[data[3]])
            if opcode == "JEQ": op = il.compare_equal
            elif opcode == "JNE": op = il.compare_not_equal
            elif opcode == "JLT": op = il.compare_unsigned_less_than
            elif opcode == "JLE": op = il.compare_unsigned_less_equal
            elif opcode == "JGT": op = il.compare_unsigned_greater_than
            elif opcode == "JGE": op = il.compare_unsigned_greater_equal

            if data[1] & 2:
                jmp = self.emit_indirect_jump(il.reg(3, self.reg_nums[data[1] >> 2]), il)
            else:
                jmp = il.const(4, JUMP_TABLE[data[1] >> 2])

            comp = op(3, dst, src)
            t = LowLevelILLabel()
            f = LowLevelILLabel()
            il.append(il.if_expr(comp, t, f))
            il.mark_label(t)
            il.append(il.jump(jmp))
            il.mark_label(f)
        elif opcode == "PUSH":
            # if data[1] & 1:
            #     val = il.reg(3, self.reg_nums[data[2]])
            # else:
            #     val = il.const(3, data[2])
            il.append(il.push(4, il.reg(3, self.reg_nums[data[3]])))
        elif opcode == "POP":
            il.append(il.set_reg(3, self.reg_nums[data[3]], il.pop(4)))
        elif opcode == "NOP": pass
        else: raise ValueError("unknown op " + opcode)

        return 16

CTFRRev.register()

class CTFRRevView(BinaryView):
    name = "IRCV"
    long_name = "IrisCTF RRev Chal View"

    def __init__(self, data):
        BinaryView.__init__(self, file_metadata=data.file, parent_view=data)
        self.data = data

    def init(self):
        global JUMP_TABLE
        global OP_IDS
        self.arch = Architecture["IrisCTF RRev Chal"]
        self.platform = self.arch.standalone_platform

        # jt2_sz = struct.unpack("<I", self.data[8:8+4])[0]
        # self.add_auto_segment(JT2_OFS, jt2_sz, 8+4, jt2_sz, SegmentFlag.SegmentContainsCode | SegmentFlag.SegmentExecutable)

        ofs = 8
        ops_sz = struct.unpack("<I", self.data[ofs:ofs+4])[0]
        OP_IDS = json.loads(self.data[ofs+4:ofs+4+ops_sz].decode())
        for k in list(OP_IDS): OP_IDS[int(k)] = OP_IDS[k]

        ofs += 4 + ops_sz
        inst_sz = struct.unpack("<I", self.data[ofs:ofs+4])[0]
        self.add_auto_segment(INST_OFS-16, inst_sz, ofs+4, inst_sz, SegmentFlag.SegmentContainsCode | SegmentFlag.SegmentExecutable | SegmentFlag.SegmentReadable)
        self.add_auto_section("text", INST_OFS, inst_sz, SectionSemantics.ReadOnlyCodeSectionSemantics)

        ofs += 4 + inst_sz
        data_sz = struct.unpack("<I", self.data[ofs:ofs+4])[0]
        self.add_auto_segment(MEM_OFS, data_sz, ofs+4, data_sz, SegmentFlag.SegmentContainsData | SegmentFlag.SegmentReadable | SegmentFlag.SegmentWritable)
        self.add_auto_section("memory", MEM_OFS, 4 * 1<<24, SectionSemantics.ReadWriteDataSectionSemantics)

        ofs += 4 + data_sz
        jt_sz = struct.unpack("<I", self.data[ofs:ofs+4])[0]
        self.add_auto_segment(JT_OFS, jt_sz, ofs+4, jt_sz, SegmentFlag.SegmentContainsData | SegmentFlag.SegmentReadable)
        self.add_auto_section("jump_table", JT_OFS, jt_sz, SectionSemantics.ReadOnlyDataSectionSemantics)

        # unpack jump table
        jt = []
        for i in range(ofs+4, ofs+jt_sz+4, 4):
            jt.append(struct.unpack("<I", self.data[i:i+4])[0])
        JUMP_TABLE = jt

        # ofs += 4 + jt_sz
        # self.add_auto_segment(ENTRY_OFS, 16, ofs, 16, SegmentFlag.SegmentContainsCode | SegmentFlag.SegmentExecutable | SegmentFlag.SegmentReadable)
        # self.add_auto_section("entry_code", ENTRY_OFS, 16, SectionSemantics.ReadOnlyCodeSectionSemantics)

        log.log_info(f"{inst_sz} {data_sz} {jt_sz}")
        log.log_info(f"jt{len(jt)} = {jt}")

        self.add_entry_point(INST_OFS-16, self.platform)

        return True

    @classmethod
    def is_valid_for_data(self, data):
        return data.read(0, 8) == b"ICTFCHAL"

    def perform_is_executable(self):
        return True
    
    def perform_get_entry_point(self):
        return 0
    
    def perform_get_address_size(self):
        return 4

CTFRRevView.register()