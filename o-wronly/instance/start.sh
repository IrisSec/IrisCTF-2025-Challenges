#!/bin/bash

chall_specific_parameters="nofgkaslr"

kernel="$(realpath ./artifacts/bzImage)"
initramfs="$(realpath ./artifacts/initramfs.cpio.gz)"
flag="$(realpath ./flag)"

cmdline="oops=panic panic=1 console=ttyS0 quiet $chall_specific_parameters"

qemu-system-x86_64 \
    -kernel "$kernel" \
    -initrd "$initramfs" \
    -append "$cmdline" \
    -nographic -serial tcp:0:1337,server=on -monitor none -nic user,model=virtio-net-pci \
    -no-reboot -snapshot \
    -m 512M \
    -cpu max,+smap,+smep,enforce \
    -drive id=flag,file="./flag",format=raw,if=virtio
