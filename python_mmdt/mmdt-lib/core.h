#include "imaging.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <dirent.h>
#include <time.h>
#include <libgen.h>
#include <sys/stat.h>
#include <math.h>
// #include <sys/types.h>


#define FUNCTION_TYPE_CALCS 1
#define FUNCTION_TYPE_COMPARES 2
#define FUNCTION_TYPE_CALSSIFY 3
#define FUNCTION_TYPE_CLUSTER 4

#define USE_INDEX_MATCH 5
#define NORMALIZATION_STANDARD_3 4080.0
#define NORMALIZATION_STANDARD_1 1020.0

#ifndef _S_IFDIR
#define _S_IFDIR 0x4000
#endif

#define ERROR_ENCRYPTED 10
#define ERROR_OTHER 100

#ifndef F_OK
#define F_OK 0
#endif

typedef struct _mmdt_data {
    UINT32 index_value;
    UINT32 main_value1;
    UINT32 main_value2;
    UINT32 main_value3;
    UINT32 main_value4;
}mmdt_data;


int mmdt_hash(char *filename, mmdt_data *md);
double mmdt_compare(char *filename1, char *filename2);

int mmdt_hash_streaming(char *data, UINT32 data_len, mmdt_data *md);
double mmdt_compare_hash(mmdt_data md1, mmdt_data md2);
