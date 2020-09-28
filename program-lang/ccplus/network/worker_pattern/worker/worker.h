#ifndef __WORKER_H__SYMBOL
#define __WORKER_H__SYMBOL

#include "at_config.h"
#include "at_epoll.h"

struct at_ep_worker {
	int status;
	int worker_idx;
	int accepter_fd;
	int worker_fd;
};

int at_ep_worker_handler(struct at_socket_context *ctx, int ev);
int at_worker_init(void);
int at_worker_start(struct at_ep_worker *worker, int worker_idx, int worker_fd);

#endif
