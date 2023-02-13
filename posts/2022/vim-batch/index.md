<p>首先创建vim脚本，例如，用vim给文本在70列的时候自动断行的脚本如下:</p>
<pre><code>:set tw=70
gggqG
:wq</code></pre>
<p>保存为<code>~/.vim/scripts/wrap</code>，然后可以处理文件：</p>
<pre><code>vim -s ~/.vim/scripts/wrap input.txt</code></pre>
<p>如果要以stdin为输入，stdout为输出，以便放进管道，给其他程序调用，可以用bash脚本包装一下：</p>
<pre><code>#!/bin/bash

BUF=/tmp/$(head -c 15 /dev/urandom | base32)
cat &gt; $BUF
/usr/bin/vim -s ~/.vim/scripts/wrap $BUF 1&gt;/dev/null 2&gt;/dev/null
cat $BUF
rm $BUF</code></pre>
<p>这样一个小工具就完成了。</p>
