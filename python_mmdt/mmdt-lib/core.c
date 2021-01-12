#include "core.h"

UINT32 calc_distance(UINT32 value1, UINT32 value2)
{
    UINT32 distance = 0;
    if (value1 == value2)
        distance = 0;
    else
    {
        for(int i = 0; i < 4; i++)
        {
            unsigned char tmp1 = 0, tmp2 = 0;
            UINT32 tmp3 = 0;
            tmp1 = value1 & 0xff;
            tmp2 = value2 & 0xff;
            tmp3 = (tmp1 - tmp2) * (tmp1 - tmp2);
            distance += tmp3;
            value1 >>= 8;
            value2 >>= 8;
        }
    }

    return distance;
}

double calc_sim(mmdt_data md1, mmdt_data md2, double step)
{
    double sim = 0.0;
    UINT32 distance2 = 0;

    distance2 += calc_distance(md1.main_value1, md2.main_value1);
    distance2 += calc_distance(md1.main_value2, md2.main_value2);
    distance2 += calc_distance(md1.main_value3, md2.main_value3);
    distance2 += calc_distance(md1.main_value4, md2.main_value4);

    sim = 1 - sqrt(distance2) / (double)step;

    return sim;
}

int mmdt_hash(char* filename, mmdt_data *md)
{
    UINT32 *v = NULL;
    v= (UINT32 *) malloc(8 * sizeof(UINT32));
    if (Resample(filename, v, 6, 5, 20971520) == 0)
    {
        printf("%s skip\n", filename);
        if(v)
        {
            free(v);
            v = NULL;
        }
        return 1;
    }

    md->index_value = v[0];
    md->main_value1 = v[1];
    md->main_value2 = v[2];
    md->main_value3 = v[3];
    md->main_value4 = v[4];

    if(v)
    {
        free(v);
        v = NULL;
    }

    return 0;
}

int mmdt_hash_streaming(char* data, UINT32 data_len, mmdt_data *md)
{
    UINT32 *v = NULL;
    v= (UINT32 *) malloc(8 * sizeof(UINT32));
    if (Resample_Data(data, data_len, v, 6, 5, 20971520) == 0)
    {
        printf("skip\n");
        if(v)
        {
            free(v);
            v = NULL;
        }
        return 1;
    }

    md->index_value = v[0];
    md->main_value1 = v[1];
    md->main_value2 = v[2];
    md->main_value3 = v[3];
    md->main_value4 = v[4];

    if(v)
    {
        free(v);
        v = NULL;
    }

    return 0;
}

double mmdt_compare(char *filename1, char *filename2)
{
    double sim = 0.0;
    mmdt_data md1 = {0};
    mmdt_data md2 = {0};

    mmdt_hash(filename1, &md1);
    mmdt_hash(filename2, &md2);
    sim = calc_sim(md1, md2, NORMALIZATION_STANDARD_1);

    return sim;
}

double mmdt_compare_hash(mmdt_data md1, mmdt_data md2)
{
    double sim = 0.0;

    sim = calc_sim(md1, md2, NORMALIZATION_STANDARD_1);

    return sim;
}