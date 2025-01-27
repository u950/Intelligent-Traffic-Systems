## Install python pip3 
```
sudo apt install python3-pip
```
## Swap file 
```
sudo fallocate -l 8G /var/swapfile
sudo chmod 600 /var/swapfile
sudo mkswap /var/swapfile
sudo swapon /var/swapfile
sudo bash -c 'echo "/var/swapfile swap swap defaults 0 0" >> /etc/fstab'
```
### Reboot jetson nano
```
$ sudo reboot
```
### Remove Swapfile
```
sudo swapoff /var/swapfile
sudo nano /etc/fstab
# comment out /var/swapfile swap swap defaults 0 0
sudo rm -rf /var/swapfile
```
### verify swap removal
```
free -h
sudo reboot
```
#set CUDA variable
### CUDA path variable -> edit in /.bashrc file

```
$ export PATH=${PATH}:/usr/local/cuda/bin
$ export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/local/cuda/lib64

$ nvcc -version
```
