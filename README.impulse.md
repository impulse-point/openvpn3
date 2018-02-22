This is a fork of (https://github.com/OpenVPN/openvpn3).

The purpose of this fork is to provide additional build scripts and configuration files required to produce redistributable library files for various platforms. It also contain project files to build a C# wrapper around this library.

----

The following are my notes from figuring this process out. The actual build steps are on our local bamboo cluster, but these notes represent my experiments figuring out how to configure that. It is left as future work to clean this up for public consumption.

```
# requires:
# visual studio 2015
# git bash
# swig

# git bash
mkdir ~/Desktop/scratch
cd ~/Desktop/scratch
git clone https://github.com/impulse-point/openvpn3.git ovpn3/core
git clone https://github.com/impulse-point/lz4 dependencies/lz4-master
git clone https://github.com/impulse-point/mbedtls dependencies/mbedtls-master
git clone https://github.com/impulse-point/asio dependencies/asio-master
git clone https://github.com/impulse-point/tap-windows6 tap-windows

# cmd
rmdir /S /Q swig
mkdir swig
cd swig
swig -c++ -csharp -I..\ovpn3\core\client -I..\ovpn3\core -outcurrentdir ..\ovpn3\core\javacli\ovpncli.i

# cmd
# replace C style path into parms_local and give it double backslashes to escape properly when read by python
# make sure to replace scratch path with bamboo build dir variable
"C:\Program Files\Git\bin\bash.exe" -c "buildDir=$(echo 'C:\Users\QA\Desktop\scratch' | sed s@\\\\\\\@\\\\\\\\\\\\\\\\@g | sed s@\\\\\\\@\\\\\\\\\\\\\\\\@g); sed s@##BUILD_DIR##@$buildDir@g 'ovpn3\core\impulse\parms_local.py' > ovpn3/core/win/parms_local.py.paths"

# cmd, from dependencies
"C:\Program Files\Git\usr\bin\tar.exe" -cvSf lz4-master.tar lz4-master
"C:\Program Files\Git\usr\bin\bzip2.exe" lz4-master.tar
"C:\Program Files\Git\usr\bin\tar.exe" -cvSf mbedtls-master.tar mbedtls-master
"C:\Program Files\Git\usr\bin\bzip2.exe" mbedtls-master.tar
"C:\Program Files\Git\usr\bin\tar.exe" -cvSf asio-master.tar asio-master
"C:\Program Files\Git\usr\bin\bzip2.exe" asio-master.tar

# cmd, from ovpn3/core/win
# python 2.7.14
rmdir /S /Q bin
# for x86
mkdir bin\x86
"C:\Program Files\Git\bin\bash.exe" -c "sed s@##ARCH##@x86@g parms_local.py.paths > parms_local.py"
"C:\Program Files\Git\bin\bash.exe" -c "sed -i s@##OUTPUT_DLL##@bin\\\\\\\\\\\\\\\\x86\\\\\\\\\\\\\\\\ovpn3.dll@g parms_local.py"
python buildep.py
python build.py ..\..\..\swig\ovpncli_wrap.cxx
# for x64
mkdir bin\x64
"C:\Program Files\Git\bin\bash.exe" -c "sed s@##ARCH##@amd64@g parms_local.py.paths > parms_local.py"
"C:\Program Files\Git\bin\bash.exe" -c "sed -i s@##OUTPUT_DLL##@bin\\\\\\\\\\\\\\\\x64\\\\\\\\\\\\\\\\ovpn3.dll@g parms_local.py"
python buildep.py
python build.py ..\..\..\swig\ovpncli_wrap.cxx

# output
# ovpn3/core/win/bin/x86/ovpn3.dll
# ovpn3/core/win/bin/x64/ovpn3.dll
```