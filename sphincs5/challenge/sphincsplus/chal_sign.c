
//
//  Based on PQCgenKAT_sign.c
//
//  Created by Bassham, Lawrence E (Fed) on 8/29/17.
//  Copyright © 2017 Bassham, Lawrence E (Fed). All rights reserved.
//
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <sys/param.h>
#include "rng.h"
#include "api.h"

void	fprintBstr(FILE *fp, char *S, unsigned char *A, unsigned long long L);

int main(void) {
    FILE                *fp_req;
    unsigned char       entropy_input[48];
    unsigned char       *m, *sm;
    unsigned long long  mlen, smlen;
    unsigned char       pk[CRYPTO_PUBLICKEYBYTES], sk[CRYPTO_SECRETKEYBYTES];
    int                 ret_val;

    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);

    FILE* urandom = fopen("/dev/urandom", "r");
    fread(entropy_input, 1, 48, urandom);
    fclose(urandom);
    randombytes_init(entropy_input, NULL);
    
    fp_req = fopen("/tmp/sphincs_key", "r");
    fread(pk, 1, CRYPTO_PUBLICKEYBYTES, fp_req);
    fread(sk, 1, CRYPTO_SECRETKEYBYTES, fp_req);
    fclose(fp_req);

    fp_req = fopen("/tmp/sphincs_req", "r");
    fseek(fp_req, 0L, SEEK_END);
    mlen = ftell(fp_req);
    rewind(fp_req);

    m = (unsigned char *)calloc(mlen, sizeof(unsigned char));
    sm = (unsigned char *)calloc(mlen+CRYPTO_BYTES, sizeof(unsigned char));
    fread(m, 1, mlen, fp_req);

    if ( (ret_val = crypto_sign(sm, &smlen, m, mlen, sk)) != 0) {
        printf("crypto_sign returned <%d>\n", ret_val);
        return -1;
    }

    fprintf(stdout, "smlen = %llu\n", smlen);
    fprintBstr(stdout, "sm = ", sm, smlen);
    fprintf(stdout, "\n");

    fclose(fp_req);

    free(m);
    free(sm);
    return 0;
}

void
fprintBstr(FILE *fp, char *S, unsigned char *A, unsigned long long L)
{
	unsigned long long  i;

	fprintf(fp, "%s", S);

	for ( i=0; i<L; i++ )
		fprintf(fp, "%02X", A[i]);

	if ( L == 0 )
		fprintf(fp, "00");

	fprintf(fp, "\n");
}

