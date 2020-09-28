TARGET  = $(shell basename $(CURDIR))
CC      = gcc
LDFLAGS = -lm -lpthread
CFLAGS  = -g -O0 -Wall -I../

VPATH=../
SRC = $(wildcard *.c) $(wildcard ../*.c)
OBJ = $(SRC:.c=.o)
HDR = $(wildcard *.h) $(wildcard ../*.h)

.PHONY: default all clean
default: $(TARGET)
all: default

$(TARGET): $(OBJ)
	$(CC) $^ $(LDFLAGS) -o $@

%.o: %.c $(HDR)
	$(CC) $(CFLAGS) -c $< -o $@

run: $(TARGET)
	./$(TARGET)

clean:
	rm -f perf.data
	rm -f quickfix*
	rm -f *.o
	rm -f ../*.o
	rm -f $(TARGET)

