在排查网络问题的时候，有个很常见的需求是获取到TCP连接的信息，例如传输了多少数据、重传率、ACK延迟等等。虽然一些简单的统计功能可以自己实现，例如可以在所有的`send`和`recv`处都加上记录函数以统计收发的字节数。但是这种方式终究还是不太优雅。如果用eBPF，又会难免会涉及到内核态，很麻烦。所以，如果不需要考虑其他类UNIX系统的可移植性的话，可以用Linux的专有接口。

## 接口

```
int getsockopt(int sockfd, int level, int optname,
               void *restrict optval, socklen_t *restrict optlen);
```

需要获取TCP连接信息的时候，`level`填写`IPPROTO_TCP`，`optname`填写`TCP_INFO`。`optval`填写用来存储结果的buffer的指针，`optlen`这个参数既是输入也是输出，用来传入buffer的大小，传出结果的大小。

## 数据结构

对于TCP信息，输出结果是一个结构体`struct tcp_info`。不过这个结构体的定义有两个版本，第一个版本在`<netinet/tcp.h>`中：

```
struct tcp_info
{
  uint8_t	tcpi_state;
  uint8_t	tcpi_ca_state;
  uint8_t	tcpi_retransmits;
  uint8_t	tcpi_probes;
  uint8_t	tcpi_backoff;
  uint8_t	tcpi_options;
  uint8_t	tcpi_snd_wscale : 4, tcpi_rcv_wscale : 4;

  uint32_t	tcpi_rto;
  uint32_t	tcpi_ato;
  uint32_t	tcpi_snd_mss;
  uint32_t	tcpi_rcv_mss;

  uint32_t	tcpi_unacked;
  uint32_t	tcpi_sacked;
  uint32_t	tcpi_lost;
  uint32_t	tcpi_retrans;
  uint32_t	tcpi_fackets;

  /* Times. */
  uint32_t	tcpi_last_data_sent;
  uint32_t	tcpi_last_ack_sent;	/* Not remembered, sorry.  */
  uint32_t	tcpi_last_data_recv;
  uint32_t	tcpi_last_ack_recv;

  /* Metrics. */
  uint32_t	tcpi_pmtu;
  uint32_t	tcpi_rcv_ssthresh;
  uint32_t	tcpi_rtt;
  uint32_t	tcpi_rttvar;
  uint32_t	tcpi_snd_ssthresh;
  uint32_t	tcpi_snd_cwnd;
  uint32_t	tcpi_advmss;
  uint32_t	tcpi_reordering;

  uint32_t	tcpi_rcv_rtt;
  uint32_t	tcpi_rcv_space;

  uint32_t	tcpi_total_retrans;
};
```

这个版本是和FreeBSD等其他类UNIX系统兼容的，提供的信息比较少。

第二个版本在`<linux/tcp.h>`中，是Linux专有的，信息全面一些。因为前面部分的字段是一样的，所以这里只放了额外的字段。

```
struct tcp_info {
    // 同上

	__u64	tcpi_pacing_rate;
	__u64	tcpi_max_pacing_rate;
	__u64	tcpi_bytes_acked;    /* RFC4898 tcpEStatsAppHCThruOctetsAcked */
	__u64	tcpi_bytes_received; /* RFC4898 tcpEStatsAppHCThruOctetsReceived */
	__u32	tcpi_segs_out;	     /* RFC4898 tcpEStatsPerfSegsOut */
	__u32	tcpi_segs_in;	     /* RFC4898 tcpEStatsPerfSegsIn */

	__u32	tcpi_notsent_bytes;
	__u32	tcpi_min_rtt;
	__u32	tcpi_data_segs_in;	/* RFC4898 tcpEStatsDataSegsIn */
	__u32	tcpi_data_segs_out;	/* RFC4898 tcpEStatsDataSegsOut */

	__u64   tcpi_delivery_rate;

	__u64	tcpi_busy_time;      /* Time (usec) busy sending data */
	__u64	tcpi_rwnd_limited;   /* Time (usec) limited by receive window */
	__u64	tcpi_sndbuf_limited; /* Time (usec) limited by send buffer */

	__u32	tcpi_delivered;
	__u32	tcpi_delivered_ce;

	__u64	tcpi_bytes_sent;     /* RFC4898 tcpEStatsPerfHCDataOctetsOut */
	__u64	tcpi_bytes_retrans;  /* RFC4898 tcpEStatsPerfOctetsRetrans */
	__u32	tcpi_dsack_dups;     /* RFC4898 tcpEStatsStackDSACKDups */
	__u32	tcpi_reord_seen;     /* reordering events seen */

	__u32	tcpi_rcv_ooopack;    /* Out-of-order packets received */

	__u32	tcpi_snd_wnd;	     /* peer's advertised receive window after
				      * scaling (bytes)
				      */
};
```

可以看到`<linux/tcp.h>`中的`struct tcp_info`多出了一些很重要的信息，比如收发的字节数，如果要做流量统计的话就非常管用了。

## 示例代码

```
#include <linux/tcp.h>

// int fd = ...;
struct tcp_info tcpi;
int bufsz = sizeof(tcpi);
int ret = getsockopt(fd, IPPROTO_TCP, TCP_INFO, &tcpi, &bufsz);
if (ret != 0) {
    // TODO: error handling
}
printf("fd: %d has received %lu bytes and sent %lu bytes.\n",
       fd, tcpi.tcpi_bytes_receiver, tcpi.tcpi_bytes_sent);
```

