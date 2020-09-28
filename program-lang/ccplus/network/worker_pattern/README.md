# Doc

 [EPOLL_CTL_DISABLE and multithreaded applications](https://lwn.net/Articles/520012/)
 [epoll example](https://programmer.ink/think/epoll-for-linux-programming.html)
 [epoll pattern](https://stackoverflow.com/questions/21892697/epoll-io-with-worker-threads-in-c)
   If listener sockets are added to all epoll instances,
      the workers would simply accept(2) and the winner would be awarded the connection and process it for its lifetime.

# Usage

Server:

	$ perf record --call-graph dwarf -- ./srv_simple 127.0.0.1 1234

Client benchmark tools:

	### brew install http_load
	### cat urls.txt
			http://127.0.0.1:1234/
	$ http_load -parallel 3000 -fetches 1 -seconds 50 ./urls.txt

# Perf

	$ perf record --call-graph dwarf -- ./srv_simple 127.0.0.1 1234
	$ http_load -parallel 3000 -fetches 1 -seconds 50 ./urls.txt

	# Exit from server-side, get the perf.data, report base on perf.data
	$ perf report -g graph --no-children

# Epoll Mode

## Simple mode - Single thread

## Simple mode multiple worker

## Thread global epoll instance

## Thread different epoll instance

