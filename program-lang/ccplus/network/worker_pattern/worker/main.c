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
#include "accepter.h"

int main(int argc, char* argv[])
{
	if (argc <= 2) {
		printf("usage:  <listen_addr> <port>\n");
		return -1;
	}

	const char* ip = argv[1];
	int port = atoi(argv[2]);

	at_worker_init();
	at_accepter_init();

	at_accepter_start(ip, port);
}

