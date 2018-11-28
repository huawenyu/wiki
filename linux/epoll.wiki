# Quick Start:

## epoll's edge triggered option
  https://stackoverflow.com/questions/9162712/what-is-the-purpose-of-epolls-edge-triggered-option

  When an FD becomes read or write ready, you might not necessarily want to read (or write) all the data immediately.

Level-triggered epoll will keep nagging you as long as the FD remains ready, whereas edge-triggered won't bother you again until the next time you get an EAGAIN (so it's more complicated to code around, but can be more efficient depending on what you need to do).

Say you're writing from a resource to an FD. If you register your interest for that FD becoming write ready as level-triggered, you'll get constant notification that the FD is still ready for writing. If the resource isn't yet available, that's a waste of a wake-up, because you can't write any more anyway.

If you were to add it as edge-triggered instead, you'd get notification that the FD was write ready once, then when the other resource becomes ready you write as much as you can. Then if write(2) returns EAGAIN, you stop writing and wait for the next notification.

The same applies for reading, because you might not want to pull all the data into user-space before you're ready to do whatever you want to do with it (thus having to buffer it, etc etc). With edge-triggered epoll you get told when it's ready to read, and then can remember that and do the actual reading "as and when".

  - ET is also particularly nice with a multithreaded server on a multicore machine. You can run one thread per core and have all of them call epoll_wait on the same epfd. When data comes in on an fd, exactly one thread will be woken to handle it.
  - In my experiments, ET doesn't guarantee that only one thread wakes up, although it often wakes up only one. The EPOLLONESHOT flag is for this purpose.

## sample of EPOLLET

  As long as you read until you get an EAGAIN error, you will get the event the next time you are calling epoll_wait.

The event is only triggered when there is a change between empty and non-empty (or full and non-full for EPOLLOUT), but that status then remains until the event is delivered via epoll_wait.

On a somewhat related note: if you register for EPOLLIN and EPOLLOUT events and assuming you never fill up the send buffer, you still get the EPOLLOUT flag set in the event returned by epoll_wait each time EPOLLIN is triggered - see https://lkml.org/lkml/2011/11/17/234 for a more detailed explanation.

And finally, the exact behaviour of edge-triggered mode actually depends on the socket type used and isn't really documented anywhere. I did some tests some time ago and documented my findings here: http://cmeerw.org/blog/753.html#753 - in short, for datagram sockets you might get more events than you would expect.

```c

    while (1) {
        nfds = epoll_wait(epollfd, events, MAX_EVENTS, -1);
        if (nfds == -1) {
            perror("epoll_pwait");
            exit(EXIT_FAILURE);
        }

        for (n = 0; n < nfds; ++n) {
            if((events[i].events & EPOLLERR) ||
               (events[i].events & EPOLLHUP) ||
               (!(events[i].events & EPOLLIN))) {
                fprintf(stderr, "epoll error\n");
                close(events[i].data.fd);
                continue;
            }

            if (events[n].data.fd == listen_sock) {
                while (1) {
                    conn_sock = accept(listen_sock,
                                (struct sockaddr *) &local, &addrlen);
                    if (conn_sock == -1) {
                        if ((errno == EAGAIN) ||
                            (errno == EWOULDBLOCK)) {
                            break;
                        }
                        perror("accept");
                        exit(EXIT_FAILURE);
                    }
                    setnonblocking(conn_sock);
                    ev.events = EPOLLIN | EPOLLET;
                    ev.data.fd = conn_sock;
                    if (epoll_ctl(epollfd, EPOLL_CTL_ADD, conn_sock,
                            &ev) == -1) {
                        perror("epoll_ctl: conn_sock");
                        exit(EXIT_FAILURE);
                    }

                    /* continue to accept next client */
                }
            }
            else {
                do_use_fd(events[n].data.fd);
            }
        }
    }

    /* Question:
    In function do_use_fd , i call nonblocked recv in while loop until EAGAIN, the sample code works fine.

    I have a question about this sample code, suppose now I have 50 socket clients connections , suddenly 10 clients writes data at the same time, so epoll_wait() will return 10 and then go to for loop :

        for (n = 0; n < nfds; ++n)

    it will call  do_use_fd(events[n].data.fd); for those 10 clients , suppose n=5 is done , and n=6 is not yet finished , suddenly the file description of event n= 3 has receive new data , after all of those 10 events are done and back to epoll_wait , will I get the event inform me that there is a client has new data to read ? or I will miss it because when event happened , the code not in epoll_wait !!
    */

    void do_use_fd(fd)
    {
        int n = -1;
        while (1) {
            n = recv(fd, iobuf, init_buff_size, MSG_DONTWAIT);
            if (n > 0) {
                LOG(glogfd, LOG_TRACE, "fd[%d] recv len %d\n", fd, n);
                mybuff_setdata(&(curcon->recv_buff), iobuf, n); // this is my func
                if (n == init_buff_size)
                {
                    [LOG](LOG)(glogfd, LOG_DEBUG, "fd[%d] need recv nextloop %d\n", fd, n);
                    continue;
                }
                break;
            }
            if (n == 0) {
                LOG(glogfd, LOG_ERROR, "fd[%d] close %s:%d!\n", fd, ID, LN);
                return do_close(fd);
            }

            if (errno == EINTR) {
                LOG(glogfd, LOG_TRACE, "fd[%d] need recv again!\n", fd);
                continue;
            }
            else if (errno == EAGAIN) {
                LOG(glogfd, LOG_TRACE, "fd[%d] need recv next!\n", fd);
                modify_fd_event(fd, EPOLLIN);   // this is the KEY, add read again
                break;
            }
            else {
                LOG(glogfd, LOG_ERROR, "fd[%d] close %s:%d!\n", fd, ID, LN);
                return do_close(fd);
            }
        }
    }
```

