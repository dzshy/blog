C++11和C11不约而同地都在新标准中添加了memory order相关的内容，这是伴随多核处理器和越来越大的处理器缓存而产生的需求。在多核处理器中，多个核心间虽然共享主内存（这里不考虑NUMA），但是缓存却是互相独立的。如此，现代的CPU变得像是一个分布式系统了。而memory order，就是这个分布式系统中的一个非常重要的同步机制。

新标准中的memory order包括：

- Acquire
- Release 
- Acquire-Release（简称acq-rel）
- Sequentially-consistent（简称seq-cst）
- Relaxed。

其实还有一个consume，但是主流编译器都没有针对它的实现，都是自动当成 acquire处理的。所以consume可以忽略不计。

首先从acquire和release开始介绍。这两个操作的名字来自于互斥锁的获取和释放。这里，可以用Git来辅助理解。计算机的主内存可以看成是中央的Git仓库，比如GitHub、GitLab之类；而各个CPU的缓存则可以看成是分布在各地的开发者的本地Git仓库。

当一个CPU核心上的线程读写内存的时候，它可能其实读写的是缓存，这些读写操作（load/store）不一定会立刻同步到主内存中。此时，另一个CPU核心上的另一个线程可能也在读写同一段内存，这就会导致发生不一致。如果用Git类比，就是发生了冲突。在Git操作中，我们可以手动解决冲突，但是瞬息万变的CPU自然不会有这种机制，一旦发生了冲突，只会根据先来后到的顺序发生覆盖，可能会产生竞态，严重的话甚至可能导致进程崩溃。

而acquire和release就类似于pull/push。其中，acquire类似于git pull，会将 acquire操作前的主内存状态都拉取下来，保证当前cache的状态是最新的。而 release则类似于git push，会将release操作前对缓存的修改都同步到主内存当中。而acq-rel，则如其名，适用于先读再写的原子操作，在读取前拉取，在写入后同步。这里，我们就可以通过同步和原子操作保证关键的操作不会发生冲突，保证不会有竞态。

不过，在x86/x64这样的架构当中，其实对所有内存中的变量的操作自动就是 acquire-release的，这被称为强内存模型；相反，ARM架构下就没有这种保证了，这类架构被称为弱内存模型。可是，即使在x86/x64中，也不可以掉以轻心，编译器可能会对程序进行一些激进的优化，Load/Store操作可能会有重排。而 acquire和release则会告诉编译器，在这里重排是不允许的。例如，acquire因为需要保证该操作之前的所有读写都会被同步到主内存，所以acquire之后的读写操作不可以被重排到acquire之前；与之类似，release操作之前的读写操作也不可以被重排到release之后。

使用acuqire-release的一个典型场景是智能指针的引用计数。在智能指针离开作用域的时候，引用计数会减去1；如果计数归零，就需要析构并回收内存。这里就有必要用到acquire-release。首先，因为可能需要回收内存，所以要保证其他CPU核心上的操作都在本线程可见，以保证回收行为正确；其次，回收完之后，也要让其他的线程都知道这件事情；同时，这里要禁止编译器随意优化，重排读写顺序。所以，acquire-release就是必要的。

而sequentially-consistent比acquire-release的行为还要严谨，不仅仅会同步到主内存，还会保证所有的CPU核心上的缓存都得到更新，实现了和单核类似的效果，而代价是速度缓慢。为了减少开发者的困惑，seq-cst是C++11中，原子操作的默认行为。相比之下，release不会保证所有的线程都看到当前线程的修改，其它线程只有在acquire的时候才能保证一定会看到release之前的修改。

而relaxed则完全不涉及同步，只是保证了当前进行原子操作的变量的读写是原子的。relaxed常用于引用计数中的加1，因为获取引用绝对不会触发析构和free 操作，所以绝对不会导致double free和leak，只需要对计数变量本身的操作是原子的就可以了。

不过，原子操作和memory order依然是危险的操作，需要慎之又慎。如果条件允许，最好还是能用通信取代共享；如果不可以，绝大多数情况下，mutex和 condvar也够用了。

## 参考

- [Arvid Norberg: The C++ memory model: an intuition - YouTube](https://www.youtube.com/watch?v=OyNG4qiWnmU)
- [std::memory\_order - cppreference.com](https://en.cppreference.com/w/cpp/atomic/memory_order)

