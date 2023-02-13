钩子（hooking）是外挂开发中的常用技巧：把一小段机器码（通常是一个jmp指令）放到内存中原本是正常函数的地方，就可以改变这个函数的行为。这个技巧不仅在外挂开发中有用，在软件测试当中也很有用，可以用来mock一个非虚函数。钩子实现起来也非常简单。

比如下面这段代码：

    #include <stdio.h>

    int func()
    {
        printf("hello, beautiful world");
        return 0;
    }

    int main()
    {
        return func();
    }

虽然在这里如果想要修改func函数很简单，但是可以假设其实func函数是在一个动态链接库里面，或者一个静态库里面，我们没有其源代码。这时候就可以利用钩子在运行时修改func函数。

这里以x64架构的Linux为例。一般来说，代码位于`.text`段中，这里的内存是不可以修改的，所以我们用mprotect函数修改这里的内存属性，允许写入这段内存：

    #include <unistd.h>
    #include <sys/mman.h>

    // 假设被钩住的函数是orig_func
    int page_size = getpagesize();
    void *aligned_addr = (void *)(((uintptr_t)orig_func) & (~(page_size - 1)));
    if (mprotect(aligned_addr,
                 page_size * 2,
                 PROT_EXEC | PROT_WRITE | PROT_READ ) != 0) {
        err_log("failed to modify mem props");
        exit(EXIT_FAILURE);
    }

随后写入跳转的机器码，其汇编伪代码如下：

    mov rax, &hook_func
    jmp rax

因为rax寄存器在C/C++的ABI中是用来存储返回值的，可以任意修改，所以这里不用担心修改rax寄存器会改变程序的行为。

具体的程序的话是这样：

    uint8_t hook_mcode[] = {0x48, 0xB8, 0x00, 0x00, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x00, 0xFF, 0xE0};
    *(uintptr_t*)(hook_code + 2) = (uintptr_t)hook_func;
    memcpy(orig_func, hook_mcode, 12);

最后我们得到了完整的代码：

    #include <stdio.h>
    #include <stdlib.h>
    #include <stdint.h>
    #include <string.h>

    #include <unistd.h>
    #include <sys/mman.h>

    int func()
    {
        printf("hello, beautiful world\n");
        return 0;
    }

    int hook_func()
    {
        printf("farewell, cruel world\n");
        return 0;
    }

    void hook(void *orig_func, void *hook_func, uint8_t *mcode_backup)
    {
        int page_size;
        void *aligned_addr;
        uint8_t hook_mcode[12] = {0x48, 0xB8, 0x00, 0x00, 0x00, 0x00, 0x00,
                                  0x00, 0x00, 0x00, 0xFF, 0xE0};
        
        page_size = getpagesize();
        aligned_addr = (void *)(((uintptr_t)orig_func) & (~(page_size - 1)));
        if (mprotect(aligned_addr,
                     page_size * 2,
                     PROT_EXEC | PROT_WRITE | PROT_READ ) != 0) {
            fprintf(stderr, "failed to modify mem props\n");
            exit(EXIT_FAILURE);
        }
        *(uintptr_t*)(hook_mcode + 2) = (uintptr_t)hook_func;
        memcpy(mcode_backup, orig_func, 12);
        memcpy(orig_func, hook_mcode, 12);
    }

    void restore(void *func, uint8_t *mcode)
    {
        memcpy(func, mcode, 12);
    }

    int main()
    {
        uint8_t mcode_backup[12] = {0};
        func();
        hook(func, hook_func, mcode_backup);
        func();
        restore(func, mcode_backup);
        func();
        return 0;
    }

程序运行结果如下：

    hello, beautiful world
    farewell, cruel world
    hello, beautiful world

其中，第一行是原本的函数的输出结果，第二行是被hook之后的输出结果，最后一行是回复之后的输出结果。

