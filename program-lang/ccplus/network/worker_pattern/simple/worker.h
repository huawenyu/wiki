#ifndef __WORKER_H__SYMBOL
#define __WORKER_H__SYMBOL

#include "at_epoll.h"

int at_ep_worker_handler(struct at_socket_context *ctx, int ev);
int at_worker_init(void);

#endif
