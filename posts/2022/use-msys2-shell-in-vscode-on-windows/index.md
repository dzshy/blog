## 批处理脚本

VSCode在Windows下面默认只提供Power Shell、CMD，以及JavaScript调试Shell。但是，我这个GNU/Linux爱好者还是更习惯bash。在Windows上，我还是习惯用MSYS2 Shell来开发一些C或者Python的小软件。所以我决定把MSYS2的Shell加到VSCode里面。

我的MSYS2安装在`C:\msys64`，所以Bash就是`C:\msys64\usr\bin\bash.exe`。另外，我最常用的MSYS2套件是MINGW64。最后形成了这么个批处理脚本：

```
@ECHO OFF
set MSYSTEM=MINGW64
C:\msys64\usr\bin\bash.exe --login -c "cd '%CD%' && exec bash"
```

## VSCode设置

把这个批处理文件存成`C:\Users\dzshy\bin\mingw.bat`，然后就是设置编辑器了。按下Ctrl + Alt + P，再输入"Open Settings"，然后敲回车打开`settings.json`，编辑下面几行：

```
{
    ...
    "terminal.integrated.defaultProfile.windows": "MinGW",
    ...
    "terminal.integrated.profiles.windows": {
        ...
        "MinGW": {
            "path": "C:\\Users\\dzshy\\bin\\mingw.bat",
            "args": []
        }
    },
    ...
}
```

保存之后，按下`Ctrl + ~`应该就能找到MSYS2的Shell选项了。 

## 另外

为了把MSYS2的shell加到文件管理器的右键菜单里面，可以创建这样的一个文件： 

```
Windows Registry Editor Version 5.00

[HKEY_LOCAL_MACHINE\Software\Classes\Directory\Background\shell\mingw64]
@="MinGW 64 Bash Here"
"Icon"="\"C:\\msys64\\mingw64.ico\""

[HKEY_LOCAL_MACHINE\Software\Classes\Directory\Background\shell\mingw64\command]
@="C:\\msys64\\msys2_shell.cmd -mingw64 -where \"%v\""
```

保存为reg文件，比如`mingw64.reg`，然后再打开载入，就可以了。 
