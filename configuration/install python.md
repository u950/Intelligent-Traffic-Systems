## Install python pip3 
```
sudo apt install python3-pip
```

> CUDA path variable ->
> edit in /.bashrc file

```
$ export PATH=${PATH}:/usr/local/cuda/bin
$ export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/local/cuda/lib64

$ nvcc -version
```
