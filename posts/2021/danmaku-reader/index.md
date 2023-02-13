<p>最近有成为透明无声系vTuber的打算，为了增加娱乐效果，搞了一个弹幕朗读器。因为不想花太多时间，所以就选了Python，准备快速解决。</p>
<h2 id="如何朗读">如何朗读</h2>
<p>我直接用了Windows操作系统内置的语音合成功能：<a href="https://docs.microsoft.com/en-us/previous-versions/windows/desktop/ms723602(v=vs.85)">SpVoice</a>。用<a href="https://pypi.org/project/pywin32/">PyWin32</a>可以调用该接口。</p>
<p>首先需要安装PyWin32：</p>
<pre><code>pip3 install pywin32</code></pre>
<p>示例代码：</p>
<pre><code>import win32com.client

speaker = win32com.client.Dispatch(&quot;SAPI.SpVoice&quot;)
speaker.Speak(&quot;你好，世界！&quot;)</code></pre>
<h2 id="如何获取弹幕">如何获取弹幕</h2>
<p>Twitch的聊天系统比较有意思，他们在提供聊天机器人接口的竟然用的是<a href="https://dev.twitch.tv/docs/irc/guide#connecting-to-twitch-irc">IRC接口</a>。所以，你甚至可以用nc命令上去直接手工操作：</p>
<pre><code>[dzshy@arch ~]$ nc irc.chat.twitch.tv 6667
&lt; PASS oauth:&lt;Twitch OAuth token&gt;
&lt; NICK &lt;user&gt;
&gt; :tmi.twitch.tv 001 &lt;user&gt; :Welcome, GLHF!
&gt; :tmi.twitch.tv 002 &lt;user&gt; :Your host is tmi.twitch.tv
&gt; :tmi.twitch.tv 003 &lt;user&gt; :This server is rather new
&gt; :tmi.twitch.tv 004 &lt;user&gt; :-
&gt; :tmi.twitch.tv 375 &lt;user&gt; :-
&gt; :tmi.twitch.tv 372 &lt;user&gt; :You are in a maze of twisty passages, all alike.
&gt; :tmi.twitch.tv 376 &lt;user&gt; :&gt;
JOIN #channel</code></pre>
<p>注意登录之后的提示语：</p>
<blockquote>
<p>You are in a maze of twitsy passages，all alike.</p>
</blockquote>
<p>这其实是一个彩蛋，来自70年代PDP-10计算机上的冒险游戏：<em><a href="https://en.wikipedia.org/wiki/Colossal_Cave_Adventure#Maze_of_twisty_little_passages">Colossal Cave Adventure</a></em>，简称<em>Adventure</em>。这是世界上第一部交互式小说，也是第一部冒险游戏和文字冒险游戏。</p>
<p>这款游戏后来在Atari游戏机上还有一个改编的图形版：<em>Adventure</em>，被认为是历史上第一个带彩蛋的游戏（就是《头号玩家》里面的那个）。</p>
<p>因为IRC是一个非常古老而成熟的文本协议，所以开发的时候只需要用Python上的一些IRC开源库即可。Twitch官方就提供了一个Python2实现的机器人的<a href="https://github.com/twitchdev/chatbot-python-sample">例子</a>。稍微改一改即可使用在Python3上。</p>

里面用到了一个Python的[IRC库](https://pypi.org/project/irc/)，需要提前安装上：</p>

<pre><code>pip3 install irc</code></pre>

最后的代码在[这里](./twitch-chat-reader.py.txt)。
