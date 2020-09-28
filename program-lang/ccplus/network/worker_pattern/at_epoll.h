#ifndef __AT_EPOLL_H__
#define __AT_EPOLL_H__

#include "at_config.h"

/*
 * And every file descriptor added to an epoll instance could have a struct at_socket_context associated with it:
 */
struct at_socket_context;
typedef int (*evt_handler_t)(struct at_socket_context *ctx, int ev);
typedef int (*evt_data_available)(struct at_socket_context *ctx, char *data, int data_len);

struct at_socket_context {
    int fd;
    evt_handler_t handler;
    evt_data_available data_available;
};

int at_set_nonblock(int fd);
void at_ep_add_fd(int epoll_fd, int fd, int enable_et, struct at_socket_context *sock_ctx);
int at_ep_add_event(int epoll_fd, int fd, evt_handler_t handler);
int at_ep_sendfd(int socket, int fd);
int at_ep_recvfd(int socket);
int at_ep_reader_handler(struct at_socket_context *ctx, int ev);

#endif


