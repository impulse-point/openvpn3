PARMS = {
    "OVPN3" : "##BUILD_DIR##\\ovpn3",
    "TAP" : "##BUILD_DIR##\\tap-windows",
    "DEP" : "##BUILD_DIR##\\dependencies",
    "BUILD" : "##BUILD_DIR##\\ovpn3-build",
    "LIB_VERSIONS" : {
        "asio" : "asio-master",
        "lz4" : "lz4-master",
        "mbedtls" : "mbedtls-master"
    },
    "ARCH" : "##ARCH##",
    "CPP_EXTRA" : "..\\client\\ovpncli.cpp /LD /Fe##OUTPUT_DLL## /I..\\..\\..\\swig -I..\\client -DUSE_TUN_BUILDER"
}