#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <string.h>
#include <fcntl.h>
#include <stdlib.h>
#include <sys/epoll.h>
#include <pthread.h>
#include <errno.h>
#include "at_epoll.h"
#include "at_errexit.h"
#include "worker.h"

static int epoll_fd;
static struct at_ep_worker *worker_self;

char response[BUFFER_SIZE] = "HTTP/1.1 200 OK\r\n\
Date: Mon, 27 Jul 2009 12:28:53 GMT\r\n\
Server: Apache/2.2.14 (Win32)\r\n\
Last-Modified: Wed, 22 Jul 2009 19:15:56 GMT\r\n\
Content-Length: 48\r\n\
Content-Type: text/html\r\n\
Connection: Closed\r\n\
\r\n\
<html>\
<body>\
<h1>Hello, World!</h1>\
</body>\
</html>";

int response_len = 0;

static int at_ep_data_handler(struct at_socket_context *ctx, int ev)
{
	static char _buf[BUFFER_SIZE + 1] = {0};
	static char *data = _buf;
	static char *buf = _buf;
	static char *mark =_buf + BUFFER_SIZE/2;
	static char *end = _buf + BUFFER_SIZE;
	static int data_len = 0;

	void handle_request()
	{
		char *p;

		data[data_len] = '\0';
		p = strstr(data, "\r\n\r\n");
		if (p) {
			int len = p - data + 4;
			data += len;
			data_len -= len;
			if (data > mark) {
				memmove(_buf, data, data_len);
				data = _buf;
				buf = data + data_len;
			}
			send(ctx->fd, response, response_len, MSG_DONTWAIT);
		}
	}

	/* read all available data and process. if incomplete, stash
	 * data in ctx and continue next time handler is called */
	if (!(ev & EPOLLIN)) {
		at_echo("something unexpected happened!\n");
		return -1;
	}

	// ENABLE_ET
	if (true) {
		/* This code will not be triggered repeatedly,
		 * so we cycle through the data to make sure that all the data
		 * in the socket read cache is read out.
		 * This is how we eliminate the potential dangers of the ET model
		 */
		at_echo("et mode: event trigger once!\n");
		for (;;) {
			int ret = recv(ctx->fd, data, end - buf, 0);
			if (ret < 0) {
				/* For non-congested IO, the following condition is true to indicate that the data has been read completely, after which epoll can trigger the EPOLLIN event on sockfd again to drive the next read operation */

				if (errno == EAGAIN) {
					at_echo("read later!\n");
					break;
				} else if (errno == EWOULDBLOCK) {
					handle_request();
					break;
				}

				close(ctx->fd);
				break;
			} else if (ret == 0) {
				at_echo("client closed!\n");
				close(ctx->fd);
			} else { //Not finished, continue reading in a loop
				at_echo("get %d bytes of content: %s\n", ret, buf);
				buf += ret;
				data_len += ret;
				handle_request();
			}
		}
	} else {
		/* Readable with client data
		 * This code is triggered as long as the data in the buffer has not been read.
		 * This is what LT mode is all about: repeating notifications until processing is complete
		 */
		at_echo("lt mode: event trigger once!\n");
		memset(buf, 0, BUFFER_SIZE);
		int ret = recv(ctx->fd, buf, BUFFER_SIZE - 1, 0);
		if(ret <= 0)  { // After reading the data, remember to turn off fd
			close(ctx->fd);
		}
		at_echo("get %d bytes of content: %s\n", ret, buf);
	}
	return 0;
}

int at_ep_connect_handler(struct at_socket_context *ctx, int ev)
{
	if (!worker_self) {
		at_warn("worker: no self info");
		return 1;
	}

	int client_fd = at_ep_recvfd(worker_self->worker_fd);
	if (client_fd < 0) {
		at_warn("worker: receive client fd fail!");
		return 1;
	}

	at_echo("worker: receive a new client fd!");
	at_ep_add_event(epoll_fd, client_fd, at_ep_data_handler);
	return 0;
}

int at_worker_start(struct at_ep_worker *worker, int worker_idx, int listen_fd)
{
	struct epoll_event events[MAX_EVENT_NUMBER];

	epoll_fd = epoll_create(MAX_LISTEN_QUE_SZ);
	if (epoll_fd == -1) {
		at_errexit("fail to create epoll! %s\n", strerror(errno));
		return -1;
	}

	worker_self = worker;
	worker->status = 1;
	worker->worker_idx = worker_idx;
	worker->worker_fd = listen_fd;
	at_ep_add_event(epoll_fd, listen_fd, at_ep_connect_handler);

	for (;;) {
		int i;
		int nfds = epoll_wait(epoll_fd, events, MAX_EVENT_NUMBER, -1);
		for (i = 0; i < nfds; i++) {
			struct at_socket_context *ctx = events[i].data.ptr;
			ctx->handler(ctx, events[i].events);
		}
	}

	close(listen_fd);
	return 0;
}

int at_worker_init(void)
{
	response_len = strlen(response);
	return 0;
}

