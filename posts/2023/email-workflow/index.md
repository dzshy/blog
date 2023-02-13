## 需要安装的软件

- Maildrop
- Fetchmail
- Msmtp
- Mutt

上述软件在几乎所有的Linux发行版中都有提供。

```
$ sudo yum install maildrop fetchmail msmtp mutt
```

## 收信

收信要用到两个软件，首先是fetchmail，利用IMAP协议或者POP3协议从服务端下载邮件，然后交给maildrop处理。Unix-like操作系统下用户的邮件默认会存放在`/var/spool/mail/username`。这也是maildrop默认会保存邮件的地方。如果邮件不多，没有特殊的邮件过滤需求，可以不用配置maildrop，用默认设置就好。

至于fetchmail，则配置成从INBOX和JUNK两个目录下用IMAP协议下载未读邮件。同时不删除邮件，只是将邮件设置为已读：

```
poll smtp.example.org proto imap
    username "user@example.org"
    password "xxxxxxxx"
    options ssl keep
    mda "/usr/bin/maildrop";

poll smtp.example.org proto imap
    username "user@example.org"
    password "xxxxxxxx"
    options ssl keep
    folder JUNK
    mda "/usr/bin/maildrop";
```

然后定时运行fetchmail即可检查电子邮件。

## 阅读邮件

阅读邮件的话可以使用mutt，mutt默认会检视`/var/spool/mail/username`文件。为了让邮件按照会话和时间倒序显示，可以设置mutt的邮件排序方式，在`~/.muttrc`中加入：

```
set folder=~/mail
set sort_aux=last-date-received       
set sort=threads
set sort_re
```

对于不要的邮件，可以按d键标记删除；如果要批量移动邮件到其他邮箱文件，可以按t键给邮件打标，然后按一下`;`键，最后按下`s`键移动邮件。

对于含有html邮件或者其他附件的邮件，可以用管道功能交给相应的应用程序显示。

例如，对于HTML邮件，可以按v键进入附件界面，选中`text/html`附件，按下“|”键，然后用一个自定义脚本让firefox可以显示该邮件：

```
#!/bin/bash

cat > /tmp/hmail.html
firefox /tmp/hmail.html
```

至于图片，则可以让Eye of Gnome，或者其他图片浏览器显示：

```
#!/bin/bash

cat > /tmp/img
eog /tmp/img
```

或者直接保存下来：

```
cat > [filename]
```

## 发信

类Unix系统下面默认使用sendmail命令发送邮件，msmtp也提供sendmail兼容的使用方式。首先配置`~/.msmtprc`：

```
account mymail
tls on
auth on
host smtp.exmaple.org
port 587
user user@example.org
from user@example.org
password xxxxxxxx
logfile /home/user/.msmtp.log

account default : mymail
```

然后配置自己的名字，在`~/.muttrc`中加入：

```
set from="Your Fullname Here <user@example.org>"
```

随后，用

```
mutt target@example.org
```

即可开始编辑邮件，最后按y键发送。

## Git邮件工作流

如果要给使用邮件列表的开源项目贡献补丁，就要使用`git send-email`功能。Git默认会使用sendmail发送邮件，如果msmtp配置好了的话，只要直接使用就可以了。

假如要把最近两次commit的内容发送到某个邮件列表，只需要：

```
git send-email --to target@example.org HEAD~2..HEAD
```

## 地址簿

Linux发行版中一般会提供一个命令行的地址簿应用：“abook”。Abook可以和mutt互操作。但是个人觉得并不好用，不如直接用文本文件，用grep检索。所以这里就不再赘述了。

## 为什么要弄得这么麻烦

最后说一下为什么要在终端里面收发邮件。

首先，Email并不是一个复杂的东西，大部分情况下只是纯文本而已。为了这么简单的信息，使用笨重缓慢的客户端，有点大材小用。

其次，在终端里面，用来收发邮件的都是一些传统的Unix工具及其继承者，hack起来很方便，很容易定制需求，例如：自定义一套邮件过滤规则，又或者用脚本给自己发邮件等等。如果是电子邮件的重度用户的话这套工作流会很方便。

