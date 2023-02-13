Windows 11修改了右键菜单，把一些“不常用”的功能收进了二级菜单。个人觉得这是一个非常愚蠢的设计，带来的麻烦远多于便利。

所幸可以通过修改注册表恢复成经典样式，在CMD中运行下述命令即可：

```
reg add "HKCU\Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\InprocServer32" /f /ve
```

如果要恢复成Windows 11的默认样式的话：

```
reg delete "HKCU\Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}" /f
```
