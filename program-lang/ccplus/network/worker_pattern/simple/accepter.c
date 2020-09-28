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

int epoll_fd;

int at_ep_listener_handler(struct at_socket_context *listener_ctx, int ev)
{
	struct at_socket_context *worker_ctx = NULL;
	struct sockaddr_in client_addr;
	socklen_t client_addrlength = sizeof(client_addr);

	for (;;) {
		int child_fd = accept(listener_ctx->fd, (struct sockaddr*)&client_addr, &client_addrlength);
		if (child_fd < 0)
			goto failed;

		worker_ctx = malloc(sizeof(*worker_ctx));
		worker_ctx->fd = child_fd;
		if (!worker_ctx)
			at_errexit("malloc socket context fail!");

		worker_ctx->handler = at_ep_worker_handler;
		at_ep_add_fd(epoll_fd, worker_ctx->fd, ENABLE_ET, worker_ctx);
		worker_ctx = NULL;
	}

	/* add to calling worker's epoll instance or implement some form
	 * of load balancing */
	return 0;

failed:
	if (worker_ctx) {
		free(worker_ctx);
	}
	return -1;
}

int at_ep_dummy_handler(struct at_socket_context* ctx, int ev)
{
	/* handle exit condition async by adding a pipe with its
	 * own handler */
	return 1;
}

int at_accepter_start(const char *ip, int port)
{
	int ret = -1;
	struct sockaddr_in address;
	int option = 1;

	at_warn("listen on %s:%d\n", ip, port);
	bzero(&address, sizeof(address));
	address.sin_family = AF_INET;
	inet_pton(AF_INET, ip, &address.sin_addr);
	address.sin_port = htons(port);

	int listen_fd = socket(PF_INET, SOCK_STREAM, 0);
	if (listen_fd < 0) {
		printf("fail to create socket!\n");
		return -1;
	}

	if (setsockopt(listen_fd, SOL_SOCKET, (SO_REUSEPORT | SO_REUSEADDR),
		       (char*)&option,sizeof(option)) < 0) {
		at_errexit("fail to setsockopt: %s!\n", strerror(errno));
		return -1;
	}

	ret = bind(listen_fd, (struct sockaddr*)&address, sizeof(address));
	if (ret == -1) {
		at_errexit("fail to bind socket: %s!\n", strerror(errno));
		return -1;
	}

	ret = listen(listen_fd, MAX_LISTEN_QUE_SZ);
	if (ret == -1) {
		at_errexit("fail to listen socket! %s\n", strerror(errno));
		return -1;
	}

	struct epoll_event events[MAX_EVENT_NUMBER];
	epoll_fd = epoll_create(MAX_LISTEN_QUE_SZ);
	if (epoll_fd == -1) {
		at_errexit("fail to create epoll! %s\n", strerror(errno));
		return -1;
	}

	struct at_socket_context *ctx;
	ctx = malloc(sizeof(*ctx));
	if (!ctx)
		at_errexit("malloc socket context fail!");
	ctx->handler = at_ep_listener_handler;
	ctx->fd = listen_fd;
	// Add listen file descriptor to event table using ET mode epoll
	at_ep_add_fd(epoll_fd, listen_fd, true, ctx);

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

void at_accepter_init(void)
{
}
