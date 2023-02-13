<p>因为Windows 11的广告实在太猖獗，所以我还是选择了把Windows全盘抹掉，装上了Fedora Workstation 36。本来我在桌面上用Arch Linux，在服务器上用Ubuntu或者Debian，不过最近几年工作都一直用CentOS，所以又逐渐习惯了红帽系的发行版。</p>
<p>不过Fedora不太能开箱即用，还是要经过一些设置。</p>

<h2 id="关闭自动升级">关闭自动升级</h2>
<p>Fedora Workstation沾染上了Windows的一些恶习，会在后台自动升级。如果习惯了自己<code>yum update</code>的话会感觉很不舒服，需要在设置里面关掉：按Super键唤出Gnome菜单，打开开“Software”，单击右上角菜单，选择“Update Preferences”，然后关闭“Automatic Updates”。</p>
<p>Fedora自动会打开SELinux和Firewalld，这两个如果是普通的桌面电脑的话最好要打开，但是如果是开发机，如果不熟悉这两个组件的话，可能会碰到奇怪的权限或者防火墙问题而不知道怎么解决。如果不是特别在意安全的话，可以考虑暂时关掉。</p>

<h2 id="关闭安全组件">关闭安全组件</h2>
<p>关闭SElinux：编辑<code>/etc/selinux/config</code>，找到<code>SELINUX=...</code>这一行，修改为<code>SELINUX=disabled</code>。</p>
<p>关闭Firewalld：</p>
<pre><code>sudo systemctl stop firewalld
sudo systemctl disable firewalld</code></pre>
<h2 id="软件镜像源">软件镜像源</h2>
<p>Fedora的软件镜像源用的是metalink，理论上会自己选择最快的镜像源。可是因为国内网络的特殊性，即使是这个metalink，有时候都访问不了。这个时候就手动编辑选择镜像源比较好，可以参考<a href="https://mirror.tuna.tsinghua.edu.cn/help/fedora/">TUNA镜像站的帮助文档</a>来修改yum配置。</p>

<h2 id="看视频">看视频</h2>
<p>Fedora自带的Firefox在默认状态下连网页上的视频都看不了，需要安装FFMpeg，但是官方的软件仓库并不提供，需要添加第三方仓库RPMFusion：</p>
<pre><code>sudo yum install \
    https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm \
    https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm</code></pre>
<p>然后可以安装FFMpeg：</p>
<pre><code>sudo yum install ffmpeg</code></pre>
<p>随后应该就可以通过Firefox看网页上的视频了。如果要播放本地视频，可以再安装VLC或者mpv。</p>
<h2 id="关闭网络联通性检查">关闭网络联通性检查</h2>
<p>Fedora的Network Manager会自动通过Fedora的服务器检查互联网联通性。但是国内对Fedora服务器的联通性不太好，所以经常会误报“失去互联网连接”，很烦人，还不如关掉：</p>
<pre><code>sudo yum remove NetworkManager-config-connectivity-fedora</code></pre>

<h2 id="快捷键">快捷键</h2>
<p>我按照自己的习惯（主要是在Windows上面的习惯），重设了一些快捷键，可以在Settings -&gt; Keyboard -&gt; View and Customize Shortcuts中修改。我主要设置了这些：</p>
<ul>
<li>Navigation -&gt; Hide all normal windows： <code>Super</code> + <code>D</code></li>
<li>Screenshots -&gt; Take a screenshot interactively：<code>Shift</code> + <code>Super</code> + <code>S</code></li>
<li>打开gnome-terminal：<code>Super</code> + <code>Enter</code></li>
<li>打开Emoji选择器：<code>Super</code> + <code>;</code></li>
</ul>
<p>其中，emoji选择器我用的是Emoji Picker，可以直接yum安装：</p>
<pre><code>sudo yum install emoji-picker</code></pre>

<h2 id="切换到mate桌面">切换到Mate桌面</h2>
<p>Fedora在桌面环境上比较激进，一直跟随Gnome桌面的最新版本，可是Gnome3的风格实在是和普通的桌面相差太大，而KDE又有点臃肿，所以我更喜欢Gnome2的fork版本：Mate。用yum可以把Gnome卸载掉换成Mate：</p>
<pre><code>sudo yum swap @gnome-desktop @mate-desktop</code></pre>
<p>然后切换桌面管理器，并重启：</p>
<pre><code>sudo systemctl disable gdm
sudo systemctl enable lightdm
sudo reboot</code></pre>
<p>在登录界面选择Mate并登入即可。</p>

<p>不过，这样切换之后，还是有一些Gnome的组件，比如gnome-shell，因为是Fedora工作站的保护软件包，没法被删掉。如果想干净地清理掉Gnome软件，可以把电脑的Fedora的identity修改为server：

<pre><code>sudo yum swap fedora-release-identity-workstation fedora-release-identity-server</code></pre>

<h2>设置Console</h2>

<p>开机的时候的Console的点阵字体，在高分屏上非常小，看着不舒服，可以改成更大号的字体，比如说Terminus：</p>

<pre><code>sudo yum install terminus-console</code></pre>

<p>Console的字体在Fedora中位于/usr/lib/kbd/consolefont/目录。可以修改/etc/vconsole.conf来配置字体：</p>

<pre><code>FONT="ter-v28n"</code></pre>

<p>有了一个看得过去的console之后就可以做一些更激进的事情，比如干脆把desktop manager也去掉，直接用console登入，然后用startx命令启动桌面。</p>

<h2 id="网络代理">网络代理</h2>
<p>然后要安装代理工具，我用的是软件仓库自带的Shadowsocks，和Ubuntu中的libev版不同，这个是Go语言实现的版本：</p>
<pre><code>sudo yum install golang-github-dreamacro-shadowsocks2</code></pre>
<p>然后自己加上了一个systemd的单元（/etc/systemd/system/ss.service），让其开机自动启动：</p>
<pre><code>[Unit]
Description=Shadowsocks Server
After=network.target

[Service]
ExecStart=/usr/bin/bash /usr/local/bin/startss.sh
Restart=on-abort

[Install]
WantedBy=multi-user.target</code></pre>
<p>浏览器可以直接配置成使用这个代理，其他应用可以用proxychains-ng。</p>
