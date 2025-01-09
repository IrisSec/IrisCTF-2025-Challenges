# Checksumz

This is misc, challenge, not a pwn. You must read the flag in /dev/vda.

**Warning**: This kernel module has serious security issues, and might crash your kernel at any time. Please don't load this on any system that you actually care about. We recommend using the start script, which will execute the module using qemu.

- Running `$ ./start.sh` will start a linux VM with the module loaded in qemu-system-x86_64. This should be as close as possible to the target challenge server.

- If you run `$ ./start.sh --root`, you will get a root shell inside the VM. This might be useful for debugging purposes.

- If you run `$ ./start.sh --debug`, the qemu debug server will be started. You can connect with `$ gdb -x attach.gdb`

### Structure

**artifacts/**  
The compiled kernel, busybox, module and filesystem.  

**chal-module/**  
Source and related files for the challenge module.  

**default/**  
Kernel and busybox config files.  
