python
import os
if not os.path.exists('artifacts/vmlinux'):
    raise ValueError('artifacts/vmlinux not found - are you running this in the task directory?')
end

file artifacts/vmlinux
target remote localhost:1234

python
import gdb
TARGET_MODULE = 'vuln'
if not os.path.exists(f'artifacts/{TARGET_MODULE}.ko'):
    raise ValueError(f'artifacts/{TARGET_MODULE}.ko not found - are you running this in the task directory?')
inferior = gdb.inferiors()[0]
module_struct = { field.name: field.bitpos for field in gdb.parse_and_eval('*(struct module*)0').type.fields() }
shifted_by = module_struct['list'] // 8
module_list = int(gdb.parse_and_eval('&modules'))
head = module_list
target_text_addr = None
while True:
    head = int(gdb.parse_and_eval(f'((struct list_head *) ({head}))->next'))
    module = head - shifted_by
    module_name_addr = int(gdb.parse_and_eval(f'(void *)(&((struct module *) ({module}))->name[0])'))
    module_name = inferior.read_memory(module_name_addr, 32).tobytes() # Could be longer, but oh well
    module_name = module_name.rstrip(b'\0')
    module_load = int(gdb.parse_and_eval(f'((struct module *) ({module}))->mem[0].base')) # 0: MOD_TEXT
    print(module_name)
    if module_name == TARGET_MODULE.encode():
        target_text_addr = module_load
    if head == module_list or target_text_addr is not None:
        break
if target_text_addr is None:
    raise ValueError(f'Module {TARGET_MODULE!r} not found - not loading symbol files')
gdb.execute(f'add-symbol-file artifacts/{TARGET_MODULE}.ko {target_text_addr:#x}')
end
