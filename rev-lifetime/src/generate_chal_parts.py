NUM_TO_GEN = 100
INP_SIZE = 16
import string
import random
import os
chars = string.ascii_letters + string.digits

def generate_part(idx):
    # something relatively easy for symbolic execution, do a few random transforms then check byte equality
    inp_idxs = list(range(INP_SIZE))
    random.shuffle(inp_idxs)

    f = open(f"chal_parts/{idx}.eir", "w")
#     f.write("""#include <stdio.h>

# const char* pre = "I'm worker #""" + str(idx) + """! Gimme some text: ";

# int main() {
#     int input[16] = {0};
#     puts(pre);
#     for(int i = 0; i < 16; i++) input[i] = getchar();

#     int check = 0;
#     int t = 0;
# """)
    wtext = "I'm worker #" + str(idx) + "! Gimme some text: "
    
    f.write(".data\n" + ".long 0\n" * (INP_SIZE + 4))
    f.write("""
    .S1:
    .string "Wow!\\n"
    .S2:
    .string "Something wasn't quite right.\\n"
    .S3:
    .string \"""" + wtext + """\"
.text
# SP - ret addr A - str ptr B - str len
puts:
    .putsloop:
    load C, A
    putc C
    add A, 1
    sub B, 1
    jne .putsloop, B, 0
    jmp SP
main:
    mov A, .S3
    mov B, """ + str(len(wtext)) + """
    mov SP, .L1
    jmp puts
    .L1:
""")
    for i in range(INP_SIZE):
        f.write(f"getc A\nstore A, {i}\n")
    
    # A - check
    # B - temp
    f.write("mov A, 0\n")

    target_string = "".join(random.choice(chars) for _ in range(INP_SIZE))

    for inp_idx in inp_idxs:
        expected_val = ord(target_string[inp_idx])
        # f.write(f"t = input[{inp_idx}];\n")
        f.write(f"load B, {inp_idx}\n")
        for _ in range(5):
            ch = random.randrange(2)
            rval = random.randrange(1<<24)
            if ch == 0:
                expected_val += rval
                # f.write(f"t += {rval};")
                f.write(f"add B, {rval}\n")
            elif ch == 1:
                expected_val -= rval
                # f.write(f"t -= {rval};")
                f.write(f"sub B, {rval}\n")
            # elif ch == 2:
            #     expected_val ^= rval
            #     f.write(f"t ^= {rval};")
            expected_val &= 0xffffff
        # f.write(f"check += t != {expected_val};\n")
        f.write(f"ne B, {expected_val}\n")
        f.write(f"add A, B\n")

#     f.write("""
#     if(check) puts("Something wasn't quite right.\\n");
#     else puts("Wow!\\n");
    
#     return 0;
# }
# """)

    f.write("""
    jeq .ok, A, 0
    mov A, .S2
    mov B, 30
    mov SP, .mainend
    jmp puts
    .ok:
    mov A, .S1
    mov B, 5
    mov SP, .mainend
    jmp puts
    .mainend:
    exit
""")

    f.close()

    #os.system(f"out/8cc -S -I. -Ilibc -Iout ./chal_parts/{idx}.c -o chal_parts/{idx}.eir")
    print(f"out/elc -ctf ./chal_parts/{idx}.eir > ./chal_parts/{idx}.ctf")
    os.system(f"out/elc -ctf ./chal_parts/{idx}.eir > ./chal_parts/{idx}.ctf")
    os.system(f"python3 compile_ctf_to_c.py chal_parts/{idx}.ctf chal_parts/{idx}_ctf.c")
    os.system(f"gcc chal_parts/{idx}_ctf.c -o chal_parts/{idx}_ctf.exe")

    print(f"out/8cc -S -I. -Ilibc -Iout ./chal_parts/{idx}_ctf.c -o chal_parts/{idx}_ctf.eir")
    os.system(f"out/8cc -S -I. -Ilibc -Iout ./chal_parts/{idx}_ctf.c -o chal_parts/{idx}_ctf.eir")
    # os.system(f"python3 delete_long_mem.py chal_parts/{idx}_ctf.eir chal_parts/{idx}_ctf2.eir")
    print(f"out/elc -ctf ./chal_parts/{idx}_ctf.eir > ./chal_parts/{idx}_ctf.ctf")
    os.system(f"out/elc -ctf ./chal_parts/{idx}_ctf.eir > ./chal_parts/{idx}_ctf.ctf")
    print(f"python3 compile_ctf_to_c2.py chal_parts/{idx}_ctf.ctf chal_parts/{idx}_ctf_ctf.c")
    os.system(f"python3 compile_ctf_to_c2.py chal_parts/{idx}_ctf.ctf chal_parts/{idx}_ctf_ctf.c")
    print(f"gcc chal_parts/{idx}_ctf_ctf.c -o chal_parts/{idx}_ctf_ctf.exe")
    os.system(f"gcc chal_parts/{idx}_ctf_ctf.c -o chal_parts/{idx}_ctf_ctf.exe")

    print(idx, target_string)

for i in range(NUM_TO_GEN):
    generate_part(i)