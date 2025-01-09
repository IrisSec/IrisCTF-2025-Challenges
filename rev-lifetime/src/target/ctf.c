#include <ir/ir.h>
#include <target/util.h>

static void ctf_init_state(Data* data) {
    emit_str("data ");
    while(data != NULL) {
        emit_str("%d ", data->v);
        data = data->next;
    }
    emit_line("");
}

#define PSR \
        if(inst->src.type == REG) { \
            emit_line("%d R %d", inst->dst.reg, inst->src.reg); \
        } else { \
            emit_line("%d I %d", inst->dst.reg, inst->src.imm); \
        }

#define PSRJ \
        if(inst->src.type == REG) { \
            emit_str("%d R %d ", inst->dst.reg, inst->src.reg); \
        } else { \
            emit_str("%d I %d ", inst->dst.reg, inst->src.imm); \
        } \
        if(inst->jmp.type == REG) { \
            emit_line("R %d", inst->jmp.reg); \
        } else { \
            emit_line("I %d", inst->jmp.imm); \
        }

static void ctf_emit_inst(Inst* inst) {
    switch (inst->op) {
    case MOV:
        emit_str("MOV ");
        PSR;
        break;

    case ADD:
        emit_str("ADD ");
        PSR;
        break;

    case SUB:
        emit_str("SUB ");
        PSR;
        break;

    case LOAD:
        emit_str("LD ");
        PSR;
        break;

    case STORE:
        emit_str("STR ");
        PSR;
        break;

    case PUTC:
        emit_str("PUT ");
        PSR;
        break;

    case GETC:
        emit_line("GET %d", inst->dst.reg);
        break;

    case EXIT:
        emit_line("EXIT");
        break;

    case EQ:
        emit_str("CMPEQ ");
        PSR;
        break;
    case NE:
        emit_str("CMPNE ");
        PSR;
        break;
    case LT:
        emit_str("CMPLT ");
        PSR;
        break;
    case GT:
        emit_str("CMPGT ");
        PSR;
        break;
    case LE:
        emit_str("CMPLE ");
        PSR;
        break;
    case GE:
        emit_str("CMPGE ");
        PSR;
        break;

    case JEQ:
        emit_str("JEQ ");
        PSRJ;
        break;
    case JNE:
        emit_str("JNE ");
        PSRJ;
        break;
    case JLT:
        emit_str("JLT ");
        PSRJ;
        break;
    case JGT:
        emit_str("JGT ");
        PSRJ;
        break;
    case JLE:
        emit_str("JLE ");
        PSRJ;
        break;
    case JGE:
        emit_str("JGE ");
        PSRJ;
        break;

    case JMP:
        emit_str("JMP ");
        if(inst->jmp.type == REG) {
            emit_line("R %d", inst->jmp.reg);
        } else {
            emit_line("I %d", inst->jmp.imm);
        }
        break;

    case DUMP:
        break; // NOOP

    default:
        error("oops");
  }
}

void target_ctf(Module* module) {
    ctf_init_state(module->data);
    
    int prev_pc = -1;
    for(Inst* inst = module->text; inst; inst = inst->next) {
        if(prev_pc != inst->pc) {
            emit_line("#%d", inst->pc);
        }
        prev_pc = inst->pc;
        ctf_emit_inst(inst);
    }
}
