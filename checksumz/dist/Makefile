.PHONY: defaults exploit

ARCH ?= x86_64

kernel:
	$(MAKE) ARCH=$(ARCH) -C $(wildcard ./linux-*/)
	cp "$(wildcard ./linux-*/)/arch/x86/boot/bzImage" "./artifacts"
	cp "$(wildcard ./linux-*/)/vmlinux" "./artifacts"

busybox:
	$(MAKE) -C $(wildcard ./busybox-*/)

busybox-install:
	$(MAKE) -C $(wildcard ./busybox-*/) install

initcpio:
	cd "$(wildcard ./busybox-*/_install/)"; find . -print0 | cpio --null -ov --format=newc | gzip -9 > ../../artifacts/initramfs.cpio.gz

module:
	$(MAKE) ARCH=x86_64 -C $(wildcard ./linux-*/) M=$(realpath ./chal-module) modules
	cp ./chal-module/vuln.ko ./artifacts
	cp ./chal-module/vuln.ko "$(wildcard ./busybox-*/_install/etc/modules)"

clean:
	$(MAKE) -C $(wildcard ./linux-*/) clean
	$(MAKE) -C $(wildcard ./busybox-*/) clean
	$(MAKE) -C $(realpath ./chal-module) clean

prepare: kernel busybox

build: module initcpio

download-kernel:
	wget "https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.10.10.tar.xz" -O linux.tar.xz
	tar xvf linux.tar.xz
	rm linux.tar.xz

download-busybox:
	wget "https://busybox.net/downloads/busybox-1.36.1.tar.bz2" -O busybox.tar.bz2
	tar xvf busybox.tar.bz2
	rm busybox.tar.bz2

download: download-kernel download-busybox

defaults:
	cp "./defaults/kernel_config" "$(wildcard ./linux-*/)/.config"
	cp "./defaults/busybox_config" "$(wildcard ./busybox-*/)/.config"
	mkdir -p artifacts

exploit:
	$(MAKE) -C ./exploit/
