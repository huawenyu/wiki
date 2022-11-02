#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <netinet/in.h>
#include <arpa/inet.h>

void conv_to12(int in, char **text)
{
	char buf[20];
	int rem = in % 12;
	int len = 0;
	char cur;
	while (in > 0) {
		rem = in % 12;
		in = in / 12;
		if (rem == 10) cur = 'X';
		else if (rem == 11) cur = 'Y';
		else cur = '0' + rem;
		buf[len] = cur;
		len++;
	}
	int cursor = 0;
	char *out = *text;
	for (int i=len-1; i >= 0; i--) {
		out[cursor] = buf[i];
		cursor++;
	}
	out[cursor] = '\0';

}

char * sock_addr(struct sockaddr_in *adr_inet, char *buf,size_t bufsiz) {
	int z;         /* Status return code */
	int len_inet;  /* length */

	/*
	 * Convert address into a string
	 * form that can be displayed:
	 */
	snprintf(buf,bufsiz, "%s:%u",
		 inet_ntoa(adr_inet->sin_addr),
		 (unsigned)ntohs(adr_inet->sin_port));
	return buf;
}

/*
 * Main Program:
 */

int  main(int argc,char **argv,char **envp)
{
	int z; /* Status return code */
	struct sockaddr_in adr_inet;/* AF_INET */
	struct sockaddr_in adr_inet_host;/* AF_INET */
	struct sockaddr_in adr_inet_net;/* AF_INET */
	int len_inet; /* length */
	char buf[64]; /* Work buffer */
	char *pbuf;


	/*
	 * Create an AF_INET address:
	 * See the Usage of the htons function
	 */
	memset(&adr_inet,0,sizeof adr_inet);
	adr_inet.sin_family = AF_INET;
	adr_inet.sin_port = htons(9000);
	//inet_aton ("172.16.80.121", &adr_inet.sin_addr);
	inet_aton ("172.16.80.121", &adr_inet.sin_addr);
	len_inet = sizeof adr_inet;
	adr_inet_host.sin_addr.s_addr = htonl(adr_inet.sin_addr.s_addr);

	//adr_inet_net.sin_addr.s_addr = htonl(adr_inet.sin_addr.s_addr + 1);
	adr_inet_net.sin_addr.s_addr = htonl(adr_inet.sin_addr.s_addr) + 1;

	printf("Address is'%s'\n", sock_addr(&adr_inet, buf, sizeof buf));
	printf("Host is'%s'\n", sock_addr(&adr_inet_host, buf, sizeof buf));
	printf("Net is'%s'\n", sock_addr(&adr_inet_net, buf, sizeof buf));

	pbuf = buf;
	conv_to12(25, &pbuf);
	printf("%s\n", buf);
	return 0;
}

