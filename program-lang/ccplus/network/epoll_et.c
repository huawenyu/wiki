/**
  @note:
  the worker threads epoll_create + epoll_wait, every threads will trigger the events.
 */
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <pthread.h>
#include <sys/epoll.h>

#define MAX_EVENTS 10

void* thr_epoll_wait(void* arg)
{
	int fd = (int) arg;
	struct epoll_event ev, events[MAX_EVENTS];
	int nfds, epollfd;
	int i;

	fprintf(stderr, "sleep\n");
	sleep(1);

	epollfd = epoll_create(10);
	if (epollfd == -1) {
		perror("epoll_create");
		exit(EXIT_FAILURE);
	}

	ev.events = EPOLLIN | EPOLLET;
	ev.data.fd = fd;
	if (epoll_ctl(epollfd, EPOLL_CTL_ADD, fd, &ev) == -1) {
		perror("epoll_ctl ");
		exit(EXIT_FAILURE);
	}

	nfds = epoll_wait(epollfd, events, MAX_EVENTS, -1);
	if (nfds == -1) {
		perror("epoll_pwait");
		exit(EXIT_FAILURE);
	}

	fprintf(stderr, "%lx: get events\n", (unsigned long)pthread_self());
	for (i=0; i < nfds; i++) {
		fprintf(stderr, "%lx: fd=%d\n", (unsigned long)pthread_self(), events[i].data.fd);
	}

	return NULL;
}

int main(void)
{
	int pipefds[2];
	int err;
	pthread_t thr;

	err = pipe(pipefds);
	if (err < 0) {
		perror("pipe ");
		exit(1);
	}
	fprintf(stderr, "pipe fds=%d %d\n", pipefds[0], pipefds[1]);

	err = pthread_create(&thr, NULL, thr_epoll_wait, (void*)pipefds[0]);
	if (err != 0) {
		errno = err;
		perror("pthread_create ");
		exit(1);
	}
	err = pthread_create(&thr, NULL, thr_epoll_wait, (void*)pipefds[0]);
	if (err != 0) {
		errno = err;
		perror("pthread_create ");
		exit(1);
	}

	fprintf(stderr, "write\n");
	write(pipefds[1], "a", 1);

	fprintf(stderr, "pause\n");
	pause();

	return 0;
}
