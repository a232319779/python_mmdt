/*
 *
 * declarations for the imaging core library
 *
 * Copyright (c) 1997-2005 by Secret Labs AB
 * Copyright (c) 1995-2005 by Fredrik Lundh
 *
 * See the README file for information on usage and redistribution.
 */


#include "imPlatform.h"


#if defined(__cplusplus)
extern "C" {
#endif


#ifndef M_PI
#define M_PI    3.1415926535897932384626433832795
#endif

#ifndef INT_MAX
#define INT_MAX 2147483647
#define INT_MIN (-INT_MAX - 1)
#endif

#ifndef MAX_PATH
#define MAX_PATH 260
#endif

#define THRESHOLD_256   2 * 256 * 256
#define THRESHOLD_128   2 * 128 * 128
#define THRESHOLD_64    2 * 64 * 64

/* -------------------------------------------------------------------- */

/*
 * Image data organization:
 *
 * mode     bytes       byte order
 * -------------------------------
 * 1        1           1
 * L        1           L
 * P        1           P
 * I        4           I (32-bit integer, native byte order)
 * F        4           F (32-bit IEEE float, native byte order)
 * RGB      4           R, G, B, -
 * RGBA     4           R, G, B, A
 * CMYK     4           C, M, Y, K
 * YCbCr    4           Y, Cb, Cr, -
 * Lab      4           L, a, b, -
 *
 * experimental modes (incomplete):
 * LA       4           L, -, -, A
 * PA       4           P, -, -, A
 * I;16     2           I (16-bit integer, native byte order)
 *
 * "P" is an 8-bit palette mode, which should be mapped through the
 * palette member to get an output image.  Check palette->mode to
 * find the corresponding "real" mode.
 *
 * For information on how to access Imaging objects from your own C
 * extensions, see http://www.effbot.org/zone/pil-extending.htm
 */

/* Handles */

typedef struct ImagingMemoryInstance* Imaging;

/* pixel types */
#define IMAGING_TYPE_UINT8 0
#define IMAGING_TYPE_INT32 1
#define IMAGING_TYPE_FLOAT32 2
#define IMAGING_TYPE_SPECIAL 3 /* check mode for details */

#define IMAGING_MODE_LENGTH 6+1 /* Band names ("1", "L", "P", "RGB", "RGBA", "CMYK", "YCbCr", "BGR;xy") */
#define VIRUS_NAME_LENGTH 12 /* */

#define MIN_FILE_LEN 4*1024

typedef struct {
    char *ptr;
    int size;
} ImagingMemoryBlock;

struct ImagingMemoryInstance {

    /* Format */
    char mode[IMAGING_MODE_LENGTH];     /* Band names ("1", "L", "P", "RGB", "RGBA", "CMYK", "YCbCr", "BGR;xy") */
    int type;           /* Data type (IMAGING_TYPE_*) */
    int depth;          /* Depth (ignored in this version) */
    int bands;          /* Number of bands (1, 2, 3, or 4) */
    int xsize;          /* Image dimension. */
    int ysize;

    /* Data pointers */
    UINT8 **image8;     /* Set for 8-bit images (pixelsize=1). */
    INT32 **image32;    /* Set for 32-bit images (pixelsize=4). */

    /* Internals */
    char **image;       /* Actual raster data. */
    char *block;        /* Set if data is allocated in a single block. */
    ImagingMemoryBlock *blocks;     /* Memory blocks for pixel storage */

    int pixelsize;      /* Size of a pixel, in bytes (1, 2 or 4) */
    int linesize;       /* Size of a line, in bytes (xsize * pixelsize) */

    /* Virtual methods */
    void (*destroy)(Imaging im);
};

typedef struct ImagingMemoryArena {
    int alignment;        /* Alignment in memory of each line of an image */
    int block_size;       /* Preferred block size, bytes */
    int blocks_max;       /* Maximum number of cached blocks */
    int blocks_cached;    /* Current number of blocks not associated with images */
    ImagingMemoryBlock *blocks_pool;
    int stats_new_count;           /* Number of new allocated images */
    int stats_allocated_blocks;    /* Number of allocated blocks */
    int stats_reused_blocks;       /* Number of blocks which were retrieved from a pool */
    int stats_reallocated_blocks;  /* Number of blocks which were actually reallocated after retrieving */
    int stats_freed_blocks;        /* Number of freed blocks */
} *ImagingMemoryArena;

/* Objects */
/* ------- */

extern struct ImagingMemoryArena ImagingDefaultArena;

extern Imaging ImagingNew(const char* mode, int xsize, int ysize);
extern Imaging ImagingNewDirty(const char* mode, int xsize, int ysize);
extern Imaging ImagingNew2Dirty(const char* mode, Imaging imOut, Imaging imIn);
extern void    ImagingDelete(Imaging im);

extern Imaging ImagingNewBlock(const char* mode, int xsize, int ysize);
extern Imaging ImagingNewMap(const char* filename, int readonly,
                             const char* mode, int xsize, int ysize);

extern Imaging ImagingNewPrologue(const char *mode,
                                  int xsize, int ysize);
extern Imaging ImagingNewPrologueSubtype(const char *mode,
                                         int xsize, int ysize,
                                         int structure_size);
extern Imaging ImagingResample(Imaging imIn, int xsize, int ysize, int filter, float box[4]);
extern Imaging ImagingCopy(Imaging imIn);

extern int Resample(char *filename, UINT32 *digest, int index_shl, int match_shl, UINT32 max_file_size);
extern int Resample_Data(char *data, UINT32 filelen, UINT32 *digest, int index_shl, int match_shl, UINT32 max_file_size);

/* standard filters */
#define IMAGING_TRANSFORM_NEAREST 0
#define IMAGING_TRANSFORM_BOX 4
#define IMAGING_TRANSFORM_BILINEAR 2
#define IMAGING_TRANSFORM_HAMMING 5
#define IMAGING_TRANSFORM_BICUBIC 3
#define IMAGING_TRANSFORM_LANCZOS 1

extern UINT8 *clip8_lookups;

#if defined(__cplusplus)
}
#endif