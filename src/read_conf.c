# include "utils.h"

#define filename "db.conf"

void menu(){
    printf("===========================\n");
    printf("1 create or update\n");
    printf("2 read\n");
    printf("0 exit");
    printf("===========================\n");
}

int tWrite(){
    
    char key[1024] = {0}, value[1024] = {0};

    printf("key:");
    scanf("%s", key);
    printf("value:");
    scanf("%s", value);
    printf("\n%s = %s\n", key, value);

    return writeCFG(filename/*in*/,key/*in*/,value/*in*/);
}

void tRead(){
    char key[1024] = {0}, *value;

    printf("key:");
    scanf("%s", key);

    readCFG(filename/*in*/,key/*in*/, &value/*out*/);
    if(value == NULL){
        printf("key\n");
        return ;
    }
    printf("\nvalue = %s\n", value);

    if(value != NULL){
        free(value);
        value = NULL;
    }

}
int main(){
    int choose;
    
    while(1){
        choose = 0;
        menu();
        printf("choose:");
        scanf("%d", &choose);
        switch(choose){
            case 1:
                if(tWrite() == -1)
                    return -1;
                break;
            case 2:
                tRead();
                break;
            case 0:
                return 0;
            default: 
                return 0;
        }
    }
    system("pause");
    return 0;
}