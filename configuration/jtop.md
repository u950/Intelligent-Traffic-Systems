A monitoring tool specifically for Jetson devices to view system usage, temperatures, CPU/GPU performance, memory, and more.


sudo apt-get update
sudo apt-get upgrade
```

sudo apt-get install python3-pip
```

## Step 3: Install Jetson-Stats Package

The **jtop** tool is part of the **jetson-stats** package. Install the package using pip3:

```bash
sudo -H pip3 install jetson-stats
```

This will install **jetson-stats**, which includes **jtop** as well as other useful utilities for monitoring your Jetson device.

## Step 4: Running Jtop

Once the installation is complete, you can run **jtop** by typing the following command in your terminal:

```bash
jtop
```

This will start **jtop**, which will display real-time information about your Jetson Nano's CPU/GPU usage, memory, and more.

## Step 5: Updating Jetson-Stats

If you need to update **jtop** or the **jetson-stats** package in the future, use the following command:

```bash
sudo -H pip3 install -U jetson-stats
```

This command will ensure that you always have the latest version.

## Additional Information

- **Jtop** provides a user-friendly interface with detailed information about CPU, GPU, RAM, SWAP, and disk usage.
- You can navigate through **jtop** using arrow keys, and quit using `q`.
- You can also monitor power usage and other stats from the **jtop** interface.

## Uninstall Jtop

If for any reason you want to remove **jtop** from your Jetson Nano, you can uninstall it with:

```bash
sudo -H pip3 uninstall jetson-stats
```

---

