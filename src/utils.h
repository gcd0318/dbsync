# include <stdio.h>
# include <stdlib.h>
# include <string.h>

void trim(char *strIn, char *strOut);

void getValue(char * keyAndValue, char * key, char * value);

int writeCFG(const char *filename/*in*/, const char *key/*in*/, const char *value/*in*/);

void readCFG(const char *filename/*in*/, const char *key/*in*/, const char *value/*out*/);
