# Bullgon

Test OS deployments in "local" devices.

"Local" as something that is under your desk.

## Usage

### Setup

Setup your bullgon "environment" (as directory) by running:

```sh
bullgon setup
```

It will use the following environment variable priority list:

* `$XDG_CONFIG_HOME/bullgon`
* `$HOME/.config/bullgon` (if `.config` exists)
* `$HOME/.bullgon` (if `.config` does not exist)]

You can also specify whole custom directory by running:

```
bullgon --base-dir /etc/bullgon setup
```

You will always need to use `--base-dir $something` on other commands if so.

### Adding a device

A `devices.d` folder will be created in your base dir so it can contain all
devices to be managed by the tool.

Devices are defined using TOML as the following:

```toml
# Optional fields are using their default values
[device]
mac = "ZZ::ZZ:ZZ:ZZ:ZZ" # mandatory, it's the machine mac address
netmask = "255.255.255.255" # optional
port = 9 # optional
interface = "eth1" # optional
```

Device defintions should use a `.toml` extension.

### Turning (waking) a device

You can run the following command once a device file is in place:

```
bullgon wake $DEVICE_NAME
```

`$DEVICE_NAME` is the filename of your file without the `.toml` extension,
so `desk1-prod.toml` can be turned on by runing  `bullgon wake desk1-prod`.

## License

[MIT](./LICENSE)
