GCC = gcc
CPPFLAGS = -I../../include -I../../../log -I.
CFLAGS = -pipe -O -W -Wall -Wpointer-arith -Wno-unused-parameter -Wno-unused-but-set-variable -Wunused-function -Wno-unused-variable -Wno-unused-value -Werror -g

LIBDIR =
#LIBDIR = \
#		-levent

TGT_client = client
TGT_server = server

OBJ_client = sock_un_clt.o
OBJ_server = sock_un_svr.o

.PHONY: clean cleanobj all

all: $(TGT_client) $(TGT_server) cleanobj ;

$(TGT_client): $(OBJ_client)
	$(GCC) -g -o $@ $^ $(LIBDIR)

$(TGT_server): $(OBJ_server)
	$(GCC) -g -o $@ $^ $(LIBDIR)

$.o: %c
	$(GCC) $(CPPFLAGS) $(CFLAGS) -c $< -o $@

clean:
	rm -rf $(TGT_client) $(TGT_server) \
           $(OBJ_client) $(OBJ_server)

cleanobj:
	rm -rf $(OBJ_client) $(OBJ_server)

