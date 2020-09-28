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

extern int epoll_fd;

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

int at_ep_worker_handler(struct at_socket_context *ctx, int ev)
{
	char buf[BUFFER_SIZE];

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
			memset(buf, 0, BUFFER_SIZE);
			int ret = recv(ctx->fd, buf, BUFFER_SIZE - 1, 0);
			if (ret < 0) {
				/* For non-congested IO, the following condition is true to indicate that the data has been read completely, after which epoll can trigger the EPOLLIN event on sockfd again to drive the next read operation */

				if (errno == EAGAIN || errno == EWOULDBLOCK) {
					at_echo("read later!\n");
					break;
				}

				close(ctx->fd);
				break;
			} else if (ret == 0) {
				at_echo("client closed!\n");
				close(ctx->fd);
			} else { //Not finished, continue reading in a loop
				at_echo("get %d bytes of content: %s\n", ret, buf);
				send(ctx->fd, response, response_len, MSG_DONTWAIT);
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

int at_worker_init(void)
{
	response_len = strlen(response);
	return 0;
}

