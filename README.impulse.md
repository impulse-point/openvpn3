This is a fork of (https://github.com/OpenVPN/openvpn3).

The purpose of this fork is to provide additional build scripts and configuration files required to produce redistributable library files for various platforms. It also contain project files to build a C# wrapper around this library.

----

The following are my notes from figuring this process out. The actual build steps are on our local bamboo cluster, but these notes represent my experiments figuring out how to configure that. It is left as future work to clean this up for public consumption.

Windows:

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
"C:\Program Files\Git\usr\bin\tar.exe" --exclude './.git' -cvSf lz4-master.tar lz4-master
"C:\Program Files\Git\usr\bin\bzip2.exe" lz4-master.tar
"C:\Program Files\Git\usr\bin\tar.exe" --exclude './.git' -cvSf mbedtls-master.tar mbedtls-master
"C:\Program Files\Git\usr\bin\bzip2.exe" mbedtls-master.tar
"C:\Program Files\Git\usr\bin\tar.exe" --exclude './.git' -cvSf asio-master.tar asio-master
"C:\Program Files\Git\usr\bin\bzip2.exe" asio-master.tar

# cmd, from ovpn3/core/win
# python 2.7.14
rmdir /S /Q bin
# for x86
mkdir bin\x86
"C:\Program Files\Git\bin\bash.exe" -c "sed s@##ARCH##@x86@g parms_local.py.paths > parms_local.py"
"C:\Program Files\Git\bin\bash.exe" -c "sed -i s@##OUTPUT_DLL##@bin\\\\\\\\\\\\\\\\x86\\\\\\\\\\\\\\\\ovpncli.dll@g parms_local.py"
python buildep.py
python build.py ..\..\..\swig\ovpncli_wrap.cxx
# for x64
mkdir bin\x64
"C:\Program Files\Git\bin\bash.exe" -c "sed s@##ARCH##@amd64@g parms_local.py.paths > parms_local.py"
"C:\Program Files\Git\bin\bash.exe" -c "sed -i s@##OUTPUT_DLL##@bin\\\\\\\\\\\\\\\\x64\\\\\\\\\\\\\\\\ovpncli.dll@g parms_local.py"
python buildep.py
python build.py ..\..\..\swig\ovpncli_wrap.cxx

# output
# ovpn3/core/win/bin/x86/ovpncli.dll
# ovpn3/core/win/bin/x64/ovpncli.dll
```

Mac:

```
# requires:
# wget (installed via homebrew)
# brew install gnu-sed --default-names

export PATH="$(brew --prefix llvm)/bin:$PATH"

mkdir -p ~/Desktop/scratch
cd ~/Desktop/scratch

# expect swig .cs and .cxx files in ~/Desktop/scratch/swig
# download or generate these files here

export O3=$(pwd)/ovpn3
export DL=$(pwd)/dependencies
export DEP_DIR=$(pwd)/ovpn3-build
mkdir -p $DL
mkdir -p $DEP_DIR

git clone https://github.com/impulse-point/openvpn3.git $O3/core

$(brew --prefix gnu-sed)/bin/sed -i 's@export ASIO_VERSION=.*$@export ASIO_VERSION=asio-master@' $O3/core/deps/lib-versions
$(brew --prefix gnu-sed)/bin/sed -i 's@export ASIO_CSUM=.*$@export ASIO_CSUM=cf6efb8638dd510998928d4ad636c9c0cd2a67a160054a0ae49c051ca1cd4f66@' $O3/core/deps/lib-versions
$(brew --prefix gnu-sed)/bin/sed -i -E 's@^URL=[^$]+@URL=https://github.com/impulse-point/asio/archive/@' $O3/core/deps/asio/build-asio
OSX_ONLY=1 $O3/core/deps/asio/build-asio

$(brew --prefix gnu-sed)/bin/sed -i 's@export LZ4_VERSION=.*$@export LZ4_VERSION=lz4-master@' $O3/core/deps/lib-versions
$(brew --prefix gnu-sed)/bin/sed -i 's@export LZ4_CSUM=.*$@export LZ4_CSUM=f888f987020a2ab8a80c5dfb3bc4d3a53739f4029b07a5c9ff8722670073aed1@' $O3/core/deps/lib-versions
$(brew --prefix gnu-sed)/bin/sed -i -E 's@^URL=[^$]+@URL=https://github.com/impulse-point/lz4/archive/@' $O3/core/deps/lz4/build-lz4
OSX_ONLY=1 $O3/core/scripts/mac/build-lz4

$(brew --prefix gnu-sed)/bin/sed -i 's@export MBEDTLS_VERSION=.*$@export MBEDTLS_VERSION=mbedtls-master@' $O3/core/deps/lib-versions
$(brew --prefix gnu-sed)/bin/sed -i 's@export MBEDTLS_CSUM=.*$@export MBEDTLS_CSUM=88de3530c35aab1112bf05f5300baa476d283dbae7afa6613f9b7b7a5ed57d61@' $O3/core/deps/lib-versions
$(brew --prefix gnu-sed)/bin/sed -i -E 's@^URL=.+@URL=https://github.com/impulse-point/mbedtls/archive/${PN}.tar.gz@' $O3/core/deps/mbedtls/build-mbedtls
OSX_ONLY=1 $O3/core/scripts/mac/build-mbedtls

cd $O3/core
. vars/vars-osx
. vars/setpath
export DEP_DIR=$(echo $(cd $O3/../ovpn3-build; pwd))
SWIG_DIR=$(echo $(cd $O3/../swig; pwd))
cd $O3/core/client
MTLS=1 LZ4=1 ASIO=1 ASIO_DIR=$DEP_DIR/asio OUTBIN=ovpncli.dylib EXTRA_CPP="-dynamiclib $SWIG_DIR/ovpncli_wrap.cxx -I$SWIG_DIR -I$O3/core/client -DUSE_TUN_BUILDER" build ovpncli
```