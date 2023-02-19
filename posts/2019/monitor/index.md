Monitor（管程）是并发程序的同步方式之一。Monitor 至少有两类，Mesa monitor 和 Hoare monitor。Mesa monitor 在 notify 之后会继续运行，Hoare monitor 在 notify 之后会进行 context switch，来到 wait 的地方开始运行，所以在写 wait 的时候，Mesa monitor 需要这样：

<pre><code>while (locked)
    wait();</code></pre>

但是 Hoare Monitor 只需要这样：

<pre><code>if (locked)
    wait();</code></pre>

目前还是 Mesa Monitor 最为常见。

实现 monitor 需要语言层面的支持。Java 有 synchronized 关键字，可以用来实现 monitor，但是 C++ 就没有了，不过还是可以用 condition variable 和 RAII，来模拟 Mesa monitor。

<pre><code>#include &lt;mutex>
#include &lt;condition_variable>

class Monitor{
public:
  Monitor():lk{m, std::defer_lock}{}
  void notify(){cv.notify_one();}
  void broadcast(){cv.notify_all();}
  template&lt;typename F>
  void wait(F pred){cv.wait(lk, pred);};
  std::unique_lock&lt;std::mutex> synchronize()
  {
    return std::unique_lock&lt;std::mutex>{m};
  }
private:
  std::mutex m;
  std::unique_lock&lt;std::mutex> lk;
  std::condition_variable cv;
};</code></pre>

来看一个简单的例子，用 monitor 实现互斥锁。虽然这里例子没什么实际意义，但是足够简单：

<pre><code>// To compile: g++ -std=c++14 -lpthread MonitorLock.cpp
        
#include "Monitor.h"
#include &lt;thread>
#include &lt;iostream>

using namespace std;
class MonitorLock{
public:
    void lock()
    {
        auto lk = m.synchronize(); // unique_lock 会通过 RAII 自动 unlock
        m.wait([&amp;](){return !locked;});
        locked = true;
    }
    void unlock()
    {
        auto lk = m.synchronize();
        locked = false;
        m.notify();
    }
private:
    Monitor m;
    bool locked = false;
};
int main()
{
    MonitorLock m;
    thread t1{[&amp;](){
        for (int i = 1; i &lt;= 30; i++){
            m.lock();
            cout &lt;&lt; \"t1: \" &lt;&lt; i &lt;&lt; endl;
            m.unlock();
        }
    }};
    thread t2{[&amp;](){
        for (int i = 1; i &lt;= 30; i++){
            m.lock();
            cout &lt;&lt; \"t2: \" &lt;&lt; i &lt;&lt; endl;
            m.unlock();
        }
    }};
    t1.join();
    t2.join();
    return 0;
}</code></pre>

另一个例子稍微实用一点，解决生产者消费者问题。

<pre><code>// To compile: g++ -std=c++14 -lpthread ProducerConsumer.cpp
        
#include \"Monitor.h\"
#include &lt;thread>
#include &lt;iostream>
#include &lt;queue>

using namespace std;
template&lt;typename T, int N>
class ProducerConsumer{
public:
    void insert(T&amp; item)
    {
        auto lk = m.synchronize(); 
        m.wait([&amp;](){return items.size() &lt; N;}); // if(!full)
        items.push(item);
        if(items.size()  == 1){
            m.notify();
        }
        cout &lt;&lt; \"insert: \" &lt;&lt; item &lt;&lt; endl;
    }
    T remove()
    {
        auto lk = m.synchronize();
        m.wait([&amp;](){return items.size() > 0;}); // if(!empty)
        auto item = items.front();
        items.pop();
        if(items.size() == N-1){
            m.notify();
        }
        cout &lt;&lt; \"consume: \" &lt;&lt; item &lt;&lt; endl;
        return item;
    }
private:
    Monitor m;
    std::queue&lt;T> items;
};
int main()
{
    ProducerConsumer&lt;int, 10> q;
    thread p{[&amp;](){
        for(int i = 1; i &lt; 30; i++){
            q.insert(i);
        }
    }};
    thread c{[&amp;](){
        for(int i = 1; i &lt; 30; i++){
            auto item = q.remove();
        }
    }};
    p.join();
    c.join();
    return 0;
}</code></pre>

上面的例子只适用于单生产者单消费者问题，如果要解决多生产者多消费者问题，一种做法是设置一个 threshold：

<pre><code>// insert()
if (items.size() >= comsumerThreshold)
      m.broadcast();
// remove()
if(items.size() &lt;= producerThreshold)
      m.broadcast()</code></pre>

或者更细粒度的控制 condition variable 的使用：

<pre><code>// To compile: g++ -std=c++14 -lpthread ProducerConsumer.cpp
        
#include &lt;thread>
#include &lt;iostream>
#include &lt;queue>
#include &lt;mutex>
#include &lt;condition_variable>

using namespace std;
template&lt;typename T, int N>
class ProducerConsumer{
public:
    void insert(T&amp; item)
    {
        std::unique_lock&lt;std::mutex> lk{m};
        insert_cv.wait(lk, [&amp;](){return items.size() &lt; N;}); // if(!full)

        items.push(item);
        remove_cv.notify_one();// 如果这里是Hoare monitor就会跳转到正在wait的remove函数，可惜这里是mesa
        cout &lt;&lt; \"insert: \" &lt;&lt; item &lt;&lt; endl;
    }
    T remove()
    {
        std::unique_lock&lt;std::mutex> lk{m};
        remove_cv.wait(lk, [&amp;](){return items.size() > 0;}); // if(!empty)

        auto item = items.front();
        items.pop();
        insert_cv.notify_one();
        cout &lt;&lt; \"consume: \" &lt;&lt; item &lt;&lt; endl;
        return item;
    }
private:
    mutex m;
    condition_variable insert_cv, remove_cv;
    std::queue&lt;T> items;
};
int main()
{
    ProducerConsumer&lt;int, 10> q;
    thread p{[&amp;](){
        for(int i = 1; i &lt; 30; i++){
            q.insert(i);
        }
    }};
    thread c{[&amp;](){
        for(int i = 1; i &lt; 30; i++){
            auto item = q.remove();
        }
    }};
    p.join();
    c.join();
    return 0;
}</code></pre>
