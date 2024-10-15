
## Installing OpenCV.
Jetson Nano's default memory (4 GB RAM + 2 GB swap) is insufficient for a quick build.<br/>
In this case, the compilation will be done by 1 core, which will take a long time.<br/>
It would be best to allocate more memory to your Nano for the fast 4-core build.<br/>
```

# OpenCV 4.9.0 -> 8.5 GB!
# OpenCV 4.8.0 -> 8.5 GB!
# OpenCV 4.7.0 -> 8.5 GB!

# If not, enlarge your swap space as explained in the guide, 
# or only 1 core is used for the compilation.
$ free -m

$ wget https://github.com/Qengineering/Install-OpenCV-Jetson-Nano/raw/main/OpenCV-4-8-0.sh
$ sudo chmod 755 ./OpenCV-4-8-0.sh
$ ./OpenCV-4-8-0.sh
```
:point_right: Don't forget to reset your swap memory afterward.

------------

If you want to beautify OpenCV with the Qt5 GUI, you need to
- $ sudo apt-get install qt5-default
- Set the -D WITH_QT=**ON** \ (± line 62) in the script<br/>
 
before running the script on your Nano

------------

OpenCV will be installed in the `/usr` directory, all files will be copied to the following locations:<br/>

- `/usr/bin` - executable files<br/>
- `/usr/lib/aarch64-linux-gnu` - libraries (.so)<br/>
- `/usr/lib/aarch64-linux-gnu/cmake/opencv4` - cmake package<br/>
- `/usr/include/opencv4` - headers<br/>
- `/usr/share/opencv4` - other files (e.g. trained cascades in XML format)<br/>

------------
