<p>FreeBSD、OpenBSD系统都自带了一个<a href="https://github.com/freebsd/freebsd-src/blob/main/sys/sys/tree.h">很好用的红黑树和splay树实现</a>。这个实现只有头文件，无需外部依赖，而且是泛型的。所以想在Linux下面用起来也很简单。</p>
<h2 id="获取头文件">获取头文件</h2>
<p>运行：</p>
<pre><code>curl https://raw.githubusercontent.com/freebsd/freebsd-src/main/sys/sys/tree.h -o tree.h</code></pre>
<p>这个头文件里面包含了<code>sys/cdefs.h</code>，这个文件在Linux里面是没有的。不过，<code>tree.h</code>用这个文件只是为了定义<code>NULL</code>，所以改成<code>stdlib.h</code>就行了。</p>
<pre><code>// #include &lt;sys/cdefs.h&gt;
#include &lt;stdlib.h&gt;</code></pre>
<h2 id="声明">声明</h2>
<p>头文件<code>tree.h</code>中的树实际上全是宏，所以用之前需要先展开。举个例子，如果希望树中的值类型是<code>double</code>，那么就这么声明：</p>
<pre><code>#include &quot;tree.h&quot;

struct double_treenode {
    RB_ENTRY(double_treenode) entry;
    double val;
};

int double_cmp(struct double_treenode *e1, struct double_treenode *e2) {
    if (e1-&gt;val &lt; e2-&gt;val) {
        return -1;
    } else if (e1-&gt;val &gt; e2-&gt;val) {
        return 1;
    }
    return 0;
}

RB_HEAD(double_tree, double_treenode);
RB_PROTOTYPE(double_tree, double_treenode, entry, double_cmp)
RB_GENERATE(double_tree, double_treenode, entry, doubl</code></pre>
<h2 id="操作">操作</h2>
<h3 id="初始化">初始化</h3>
<p>创建树并初始化：</p>
<pre><code>RB_HEAD(double_tree, double_treenode) head;
RB_INIT(&amp;head);</code></pre>
<p>初始化也可以一行完成：</p>
<pre><code>RB_HEAD(double_tree, double_treenode) head = RB_INITIALIZER(&amp;head);</code></pre>
<h3 id="插入">插入</h3>
<pre><code>struct double_treenode *n;
double data[5] = {1.0, 2.0, 3.0, 4.0, 5.0};
for (int i = 0; i &lt; 5; i++) {
    n = malloc(sizeof(struct double_treenode));
    n-&gt;val = data[i];
    RB_INSERT(double_tree, &amp;head, n);    
}</code></pre>
<h3 id="查找和删除">查找和删除</h3>
<pre><code>struct double_treenode find;
find.val = 3.0

struct double_treenode *iter;
iter = RB_FIND(double_tree, &amp;head, &amp;find);

if (iter != NULL) {
    printf(&quot;Found\n&quot;);
    RB_REMOVE(double_tree, &amp;head, iter);
}</code></pre>
<h3 id="遍历">遍历</h3>
<pre><code>RB_FOREACH(iter, double_tree, &amp;head) {
    // Do something on iter-&gt;val
    ...
}</code></pre>
<p>其实，<code>RB_FOREACH(iter, double_tree, &amp;head)</code> 本质上是：</p>
<pre><code>for (iter = RB_MIN(double_tree, &amp;head); iter != NULL; iter = RB_NEXT(double_tree, &amp;head, iter))</code></pre>
<p>用<code>RB_MIN</code>可以取得树中的最小节点；用<code>RB_NEXT</code>可以获取<code>iter</code>的下一个元素；<code>RB_MAX</code>则是最大节点。</p>
<p>如果想用其他的顺序遍历树的话，可以用<code>RB_LEFT</code>和<code>RB_RIGHT</code>。比如说，用前序遍历打印树：</p>
<pre><code>void
print_tree(struct double_treenode *n)
{
    struct double_treenode *left, *right;

    if (n == NULL) {
        printf(&quot;nil&quot;);
        return;
    }
    left = RB_LEFT(n, entry);
    right = RB_RIGHT(n, entry);
    if (left == NULL &amp;&amp; right == NULL)
        printf(&quot;%d&quot;, n-&gt;val);
    else {
        printf(&quot;%d(&quot;, n-&gt;val);
        print_tree(left);
        printf(&quot;,&quot;);
        print_tree(right);
        printf(&quot;)&quot;);
    }
}</code></pre>
<h2 id="其他">其他</h2>
<p>有个很怪的事情，Arch Linux里面有<code>tree.h</code>的man文档，执行<code>man 3 tree</code>就能看到，但是这个头文件本体却找不到。</p>
<p>这篇文章里面只写了红黑树，但是splay树其实也大同小异，就不再赘述了，可以直接去翻<a href="https://www.freebsd.org/cgi/man.cgi?query=tree&amp;sektion=3&amp;format=html">文档</a>。</p>
