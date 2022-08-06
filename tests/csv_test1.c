// gcc -m32 -fno-stack-protector -z execstack -no-pie csv_test1.c split.c fread_csv_line.c csv.c -o csv_test1

#include <stdio.h>
#include "csv.h"

#define MAX_LENGTH 20

int main(void) {
    printf("Enter 5 lines of csv pls\n");
    printf("In the format:\n");
    printf("line_num, message, name\n");

    char line[MAX_LENGTH];
    while (fgets(line, MAX_LENGTH, stdin) != NULL) {
        char **arr = parse_csv(line);
        printf("%s: %s says \"%s\"\n", arr[0], arr[2], arr[1]);
    }

}

// valid csv:
// 1,three,one
// sally,wants,beans