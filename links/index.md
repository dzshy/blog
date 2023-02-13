<div id="friends">
<ul>
<li><a href="https://unstablebeagle.bearblog.dev/">硅基猫❤️</a></li>
<li><a href="https://chengpeng.space/">Cheng</a></li>
<li><a href="https://nachtzug.xyz/">Nachtzug</a></li>
<li><a href="https://ioover.net/">I/O OVER</a></li>
<li><a href="https://blog.bgme.me/">影子屋</a></li>
<li><a href="https://qwonsuzune.wordpress.com/">小さな砂の部屋</a></li>
<li><a href="https://blog.lycheeee.top/">Lychee’s Blog</a></li>
<li><a href="https://tardislog.wordpress.com/">Boobook</a></li>
<li><a href="https://blog.dctewi.com/">冻葱Tewi</a></li>
<li><a href="https://asaba.sakuragawa.moe/">樱川家::浅羽</a></li>
<li><a href="https://bouvardia0703.github.io/">Bouvardia’s Blog</a></li>
<li><a href="https://blog.pullopen.xyz/">于光年外遥望</a></li>
<li><a href="https://blog.gyara.moe/">岛风造船所</a></li>
<li><a href="https://coccimore.cyou/">苹果核聚变</a></li>

<!--

<li><a href="http://lucyyang719.com">Lucyyang’s blog</a></li>

-->

</ul>
</div>
<p>使用[Fisher-Yates算法](https://en.wikipedia.org/wiki/Fisher%E2%80%93Yates_shuffle)而成乱序。</p>
<script>
var ul = document.querySelector('#friends>ul');
for (var i = ul.children.length; i >= 0; i--) {
    ul.appendChild(ul.children[Math.random() * i | 0]);
}
</script>

<!-- mutual links:

<li><a href="https://unstablebeagle.bearblog.dev/">硅基猫❤️</a></li>
<li><a href="https://nachtzug.xyz/">Nachtzug</a></li>
<li><a href="https://blog.bgme.me/">影子屋</a></li>
<li><a href="https://asaba.sakuragawa.moe/">樱川家::浅羽</a></li>
<li><a href="https://blog.gyara.moe/">岛风造船所</a></li>

-->

