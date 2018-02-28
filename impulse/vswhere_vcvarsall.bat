@echo off

REM echo output we're parsing to locate vcvarsall.bat:
REM vswhere -latest -requires Microsoft.Component.MSBuild

for /f "usebackq tokens=1* delims=: " %%i in (`vswhere -latest -requires Microsoft.Component.MSBuild`) do (
  if /i "%%i"=="installationPath" set InstallDir=%%j
)

set vcvarsall_path=%InstallDir%\VC\Auxiliary\Build\vcvarsall.bat
REM echo vcvarsall.bat should be located at: %vcvarsall_path%

if exist "%vcvarsall_path%" (
  "%vcvarsall_path%" %*
)
