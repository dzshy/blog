因为Scheme和Lisp系的其他语言一样，过于灵活，因此可以往语言里面加入很多奇怪的东西。甚至，如果想用命令式的方式，像Python一样编写Scheme代码，也是可以的。

这篇文章中的代码都是为GNU Guile和TinyScheme而写的，这两个解释器都支持老式的Lisp宏。这种宏在Common Lisp当中更多见，并不卫生，也不属于任何Scheme标准。但是大多数解释器和编译器都支持。

例如，假如想在Racket中运行，只需要在代码前面加入下面这段语法就可以了：

```
#lang racket

(define-syntax define-macro
  (lambda (x)
    (syntax-case x ()
      ((_ (macro . args) body ...)
       #'(define-macro macro (lambda args body ...)))
      ((_ macro transformer)
       #'(define-syntax macro
           (lambda (y)
             (syntax-case y ()
               ((_ . args)
                (let ((v (syntax->datum #'args)))
                  (datum->syntax y (apply transformer v)))))))))))
```

<h2 id="hello-world">hello, world</h2>

Python代码：

<pre><code>print(&#39;hello, world&#39;)
</code></pre>

函数定义：

<pre><code>(define println
    (lambda x
      (apply display x)
      (newline)))
</code></pre>

最终效果：

<pre><code>(println "hello world")
</code></pre>

<h2 id="def">Def</h2>

Python代码：

<pre><code>def is_even(x):
    if x % 2 == 0:
        return True
    return False
</code></pre>

宏定义：

<pre><code>(define-macro (def form . body)
    `(define ,form
         (call&#47;cc (lambda (return)
            ,@body))))
</code></pre>

最终效果：

<pre><code>(def (is-even x)
    (cond ((= 0 (modulo x))
        (return #t)))
    (return #f))
</code></pre>

<h2 id="while">While</h2>

Python代码：

<pre><code>i = 0
while True:
    i = i + 1
    if x % 2 == 0:
        continue
    print(i)
    if (i &#62; 10):
        break
</code></pre>

宏定义：

<pre><code>(define-macro (while condition . body)
    (let ((loop (gensym)))
        `(call&#47;cc (lambda (break)
            (letrec ((,loop (lambda ()
                (cond (,condition
                    (call&#47;cc (lambda (continue)
                            ,@body))
                    (,loop))))))
                (,loop))))))
</code></pre>

最终效果：

<pre><code>(let ((i 0))
(while #t
    (set! i (+ i 1))
    (cond ((= (modulo i 2) 0)
         (continue)))
    (cond ((&#62; i 10)
        (break)))
    (println i)))
</code></pre>

<h2 id="for">For</h2>

Python代码：

<pre><code>for i in range(0, 10):
    print(i)
</code></pre>

宏和工具函数定义：

<pre><code>(define (iter-get iter)
    (cond ((list? iter)
        (car iter))
    (else
        (iter &#39;get))))

(define (iter-next iter)
    (cond ((list? iter)
        (cdr iter))
    (else
        (iter &#39;next))))

(define (range start end)
    (lambda (method)
        (cond ((eq? &#39;get method)
            (if (&#62;= start end)
                &#39;()
                start))
        ((eq? &#39;next method)
            (range (+ 1 start) end)))))

(define-macro (for i range . body)
    (let ((loop (gensym))
          (iter (gensym)))
    `(call&#47;cc (lambda (break)
        (letrec
            ((,loop (lambda (,iter)
                (if (eq? (iter-get ,iter) &#39;())
                    &#39;()
                    (let ((,i (iter-get ,iter)))
                          (call&#47;cc (lambda (continue)
                             ,@body))
                          (,loop (iter-next ,iter)))))))
            (,loop ,range))))))
</code></pre>

最终效果：

<pre><code>(for i (range 0 10)
    (println i))
</code></pre>

<h2 id="goto">Goto</h2>

这个还是算了吧！

<h2 id="fizz-buzz">Fizz Buzz!</h2>

Python写出来是这样：

<pre><code>for i in range(35):
    if i % 15 == 0:
        print("FizzBuzz")
        continue
    if i % 3 == 0:
        print("Fizz")
        continue
    if i % 5 == 0:
        print("Buzz")
        continue
    print(i)
</code></pre>

用Scheme的话，加上上面的宏，几乎可以一一对应：

<pre><code>(for i (range 1 35)
    (cond ((= 0 (modulo i 15))
        (println "FizzBuzz")
        (continue)))
    (cond ((= 0 (modulo i 3))
        (println "Fizz")
        (continue)))
    (cond ((= 0 (modulo i 5))
        (println "Buzz")
        (continue)))
    (println i))
</code></pre>
