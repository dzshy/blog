<p>Go和Rust有个很好用的特性：二进制部署。但是在Linux上，编译出来的二进制文件还是依赖glibc。要是开发机和部署机上的glibc版本不一致就麻烦了。所以，如果要直接二进制部署，glibc也要静态链接上。</p>
<h2 id="go">Go</h2>
<pre><code>go build -tags netgo -ldflags &#39;-extldflags &quot;-static&quot;&#39;</code></pre>
<h2 id="rust">Rust</h2>
<p>Rust这里，我在尝试静态链接glibc的时候佩刀了奇怪的问题，翻了好久StackOverflow也没有解决。所以我决定改成用musl。比如说在Arch Linux上就这么用：</p>
<pre><code>sudo pacman -S musl
rustup target add x86_64-unknown-linux-musl
cargo build --release --target x86_64-unknown-linux-musl</code></pre>
<p>不过因为用了musl，有时候可能会产生兼容问题。</p>
