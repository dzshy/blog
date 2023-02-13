<p>资源安全在C中要比C++中困难不少。C++中有了RAII机制，资源安全可谓得心应手。无怪乎，Stroustrup的《C++程序设计语言》的前半本都在写内存安全和资源安全，而这些也全是用RAII保证的。局部变量一旦出了作用域，其析构函数就被调用了，非常方便。</p>
<p>然而，C语言中就没有这种好用的工具，比如说：</p>
<pre><code>int foo() {
    FILE* fp = fopen(&quot;bar&quot;, &quot;w&quot;);
    if (f == 0) {
        error(&quot;failed to open file&quot;);
        return -1;
    }
    int ret = do_something(fp);
    if (ret &lt; 0) {
        error(&quot;failed to process file&quot;);
        fclose(fp);
        return -1;
    }
    fprintf(fp, &quot;this end it&quot;);
    fclose(fp);
    return 0;
}</code></pre>
<p>这里仅仅是一个简单的例子，<code>fclose</code>在这里程序出现了两次；然而，当程序的控制流繁杂起来的时候，资源回收就变得骇人起来。不似C++中，只需要打开一个<code>ofstream</code>，然后把剩下的交给析构函数就好。</p>
<p>除了C++以外，别的语言中也有类似的机制，比如说Javas和Go里面都有垃圾回收，用来处理内存。至于别的资源，比如文件柄、网络连接、互斥锁等等，在Java里面会用<code>try...catch...finally...</code>处理，而Go语言里面会用<code>defer</code>来处理。</p>
<p>所以C里面应该怎么办呢？所幸，<a href="https://gcc.gnu.org/onlinedocs/gcc/Common-Variable-Attributes.html#Common-Variable-Attributes">gcc提供了一个cleanup扩展</a>，可以用来注册析构函数。上面那个关闭文件的例子就可以用这个扩展重写成下面这样：</p>
<pre><code>void close_file(FILE** fp_ptr) {
    if (*fp_ptr == NULL) return;
    fprintf(*fp_ptr, &quot;file is closed\n&quot;);
    fclose(*fp_ptr);
}

int foo() {
    __attribute__((cleanup(close_file))) FILE* fp = fopen(&quot;bar&quot;, &quot;w&quot;);
    if (fp == NULL) {
        error(&quot;failed to open file&quot;);
        return -1;
    }    
    int ret = do_something(fp);
    if (ret &lt; 0) {
        error(&quot;failed to process file&quot;);
        return -1;
    }
    fprintf(fp, &quot;this end it\n&quot;);
    return 0;
}</code></pre>
<p>有了这个cleanup attribute, <code>close_file</code>就可以自动执行了，省去了手动管理的困扰。</p>
<p>为了让代码更紧凑，还可以加一个词法宏。</p>
<pre><code>#define CLEANUP(func) __attribute__((cleanup(func)))</code></pre>
<p>互斥锁也类似：</p>
<pre><code>pthread_mutex_t mutex;
int count;

void unlock_mutex(pthread_mutex_t **mutex_ptr) {
    pthread_mutex_unlock(*mutex_ptr);
}

void *thread_run(void *arg){
    int i;
    int ret = pthread_mutex_lock(&amp;mutex);
    if (ret != 0) {
        error(&quot;failed to acqure lock&quot;);
        return 0;
    }
    CLEANUP(unlock_mutex) pthread_mutex_t *defer_mutex = &amp;mutex;
    for (i = 0; i &lt; 3; i++) {
        printf(&quot;[%ld]count: %d\n&quot;, pthread_self(), ++count);
    }
    return 0;
}

int main() {
    pthread_t threads[10];
    for (int i = 0; i &lt; 10; i++) {
        int res = pthread_create(&amp;threads[i], NULL, thread_run, NULL);
        if (res) error(&quot;create thread error&quot;);
    }
    for (int i = 0; i &lt; 10; i++) {
        void *ret;
        pthread_join(threads[i], &amp;ret);
    }
    return 0;
}</code></pre>
<p>虽说这是个gcc扩展，不过Clang/LLVM工具链也是支持的。</p>
<p>如果想要更通用的写法，还可以用goto语句实现。虽然goto语句一般被认为一种不好的实践，但是在资源回收这个场景中，其实反而被认为是一种好的做法：</p>
<pre><code>int foo() {
    FILE* fp = fopen(&quot;bar&quot;, &quot;w&quot;);
    if (f == 0) {
        error(&quot;failed to open file&quot;);
        goto clean_0;
    }
    int ret = do_something(fp);
    if (ret &lt; 0) {
        error(&quot;failed to process file&quot;);
        goto clean_1;
    }
    fprintf(fp, &quot;this end it&quot;);
    fclose(fp);
    return 0;

clean_1:
    fclose(fp);
clean_0:
    return -1;
}</code></pre>
<p>或者，也可以尝试用宏：</p>
<pre><code>int foo() {
    FILE* fp = NULL;
    #define DEFER \
        if (fp != NULL) fclose(fp);

    fp = fopen(&quot;bar&quot;, &quot;w&quot;);
    if (f == 0) {
        error(&quot;failed to open file&quot;);
        DEFER return -1;
    }
    int ret = do_something(fp);
    if (ret &lt; 0) {
        error(&quot;failed to process file&quot;);
        DEFER return -1;
    }
    fprintf(fp, &quot;this end it&quot;);
    DEFER return 0;
    #undef DEFER
}</code></pre>
<p>综合起来，感觉还是用goto语句最佳。</p>
<p>另一边，还有一个<a href="http://www.open-std.org/jtc1/sc22/wg14/www/docs/n2895.htm">给C语言加defer的提案</a>，不过能不能进标准谁也不知道，就拭目以待吧。</p>
