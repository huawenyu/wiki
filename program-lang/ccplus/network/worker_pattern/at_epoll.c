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

/* Set file descriptor to non-congested  */
int at_set_nonblock(int fd)
{
	int old_option = fcntl(fd, F_GETFL);
	int new_option = old_option | O_NONBLOCK;
	fcntl(fd, F_SETFL, new_option);
	return old_option;
}

/* Register EPOLLIN on file descriptor FD into the epoll kernel event table indicated by epoll_fd, and the parameter enable_et specifies whether et mode is enabled for FD */
void at_ep_add_fd(int epoll_fd, int fd, int enable_et, struct at_socket_context *sock_ctx)
{
	/*
	   typedef union epoll_data {
	   void        *ptr;
	   int          fd;
	   uint32_t     u32;
	   uint64_t     u64;
	   } epoll_data_t;

	   struct epoll_event {
	   uint32_t     events;      // Epoll events
	   epoll_data_t data;        // User data variable
	   };
	   */

	struct epoll_event event = {0};

	event.data.ptr = sock_ctx;
	event.events = EPOLLIN; // Registering the fd is readable
	if (enable_et) {
		event.events |= EPOLLET;
	}

	at_set_nonblock(fd);
	// Register the fd with the epoll kernel event table
	epoll_ctl(epoll_fd, EPOLL_CTL_ADD, fd, &event);
}

int at_ep_add_event(int epoll_fd, int fd, evt_handler_t handler)
{
	struct at_socket_context *worker_ctx = NULL;

	worker_ctx = malloc(sizeof(*worker_ctx));
	worker_ctx->fd = fd;
	if (!worker_ctx) {
		at_errexit("malloc socket context fail!");
	}

	worker_ctx->handler = handler;
	at_ep_add_fd(epoll_fd, worker_ctx->fd, ENABLE_ET, worker_ctx);
	return 0;
}

int at_ep_reader_handler(struct at_socket_context *ctx, int ev)
{
	char buf[BUFFER_SIZE + 1];
	char *data = buf;
	int free_len = sizeof(buf) - 1;

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
			int ret = recv(ctx->fd, data, free_len, 0);
			if (ret < 0) {
				/* For non-congested IO, the following condition is true to indicate that the data has been read completely, after which epoll can trigger the EPOLLIN event on sockfd again to drive the next read operation */

				if (errno == EAGAIN) {
					at_echo("read later: EAGAIN\n");
					break;
				} else if (errno == EWOULDBLOCK) {
					at_echo("read later: EWOULDBLOCK\n");
					if (ctx->data_available) {
						ctx->data_available(ctx, buf, sizeof(buf) - 1 - free_len);
					}
					break;
				}

				close(ctx->fd);
				break;
			} else if (ret == 0) {
				at_echo("client closed!\n");
				close(ctx->fd);
			} else { // Not finished, continue reading in a loop
				at_echo("get %d bytes of content: %s\n", ret, buf);
				data += ret;
				free_len -= ret;

				if (free_len == 0) {
					if (ctx->data_available)
						ctx->data_available(ctx, buf, sizeof(buf) - 1);
					data = buf;
					free_len = sizeof(buf) - 1;
				}

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

// send fd by socket
int at_ep_sendfd(int socket, int fd)
{
	struct msghdr msg = { 0 };
	char buf[CMSG_SPACE(sizeof(fd))];
	memset(buf, '\0', sizeof(buf));
	struct iovec io = { .iov_base = "ABC", .iov_len = 3 };

	msg.msg_iov = &io;
	msg.msg_iovlen = 1;
	msg.msg_control = buf;
	msg.msg_controllen = sizeof(buf);

	struct cmsghdr * cmsg = CMSG_FIRSTHDR(&msg);
	cmsg->cmsg_level = SOL_SOCKET;
	cmsg->cmsg_type = SCM_RIGHTS;
	cmsg->cmsg_len = CMSG_LEN(sizeof(fd));

	*((int *) CMSG_DATA(cmsg)) = fd;

	msg.msg_controllen = CMSG_SPACE(sizeof(fd));

	if (sendmsg(socket, &msg, 0) < 0) {
		at_warn("Failed to send message\n");
		return 1;
	}
	return 0;
}

// receive fd from socket
int at_ep_recvfd(int socket)
{
	struct msghdr msg = {0};

	char m_buffer[256];
	struct iovec io = { .iov_base = m_buffer, .iov_len = sizeof(m_buffer) };
	msg.msg_iov = &io;
	msg.msg_iovlen = 1;

	char c_buffer[256];
	msg.msg_control = c_buffer;
	msg.msg_controllen = sizeof(c_buffer);

	if (recvmsg(socket, &msg, 0) < 0)
		at_errexit("Failed to receive message\n");

	struct cmsghdr * cmsg = CMSG_FIRSTHDR(&msg);

	unsigned char * data = CMSG_DATA(cmsg);

	at_echo("About to extract fd\n");
	int fd = *((int*) data);
	at_echo("Extracted fd %d\n", fd);
	return fd;
}

