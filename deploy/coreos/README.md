# CoreOS Images

## Usage

Run the following command in case you made changes to config/$NAME/config.yml:

```
$ make butane CONFIG=base
```

Install it in a device (such as a usb stick):
```
# NOTE: THIS WILL ERASE THE TARGETED ONTENTS OF THE DEVICE
$ make install CONFIg=base FCOS_DEV=/dev/sdb
```
