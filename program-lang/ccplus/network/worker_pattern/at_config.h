#ifndef __AT_CONFIG_H__
#define __AT_CONFIG_H__

#define MAX_LISTEN_QUE_SZ 1024 // listen queue size
#define MAX_EVENT_NUMBER  1024 // event
#define BUFFER_SIZE       8192 // Buffer Size

/* ET Work mode features: efficient but potentially dangerous */
/* LT Work mode features: robust but inefficient */
#define ENABLE_ET        0    //Enable ET mode

#define WORKER_NUMBER    2

#endif


