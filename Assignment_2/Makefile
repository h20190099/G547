obj-m := usb.o
kernel_dir = /usr/src/linux-headers-4.8.0-53-generic

all:
	sudo make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules
clean:
	sudo make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean