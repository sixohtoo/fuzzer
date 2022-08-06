// gcc -m32 -fno-stack-protector -z execstack -no-pie csv_test2.c split.c fread_csv_line.c csv.c -o csv_test2

#include <stdio.h>
#include <string.h>
#include "csv.h"

#define MAX_LENGTH 20

void remove_quotations(char *string);

int main(void) {
    printf("Enter 5 lines of csv pls\n");
    printf("In the format:\n");
    printf("line_num, message, name\n");

    char line[MAX_LENGTH];
    while (gets(line, MAX_LENGTH, stdin) != NULL) {
        remove_quotations(line);
        char **arr = parse_csv(line);
        printf("%s: %s says \"%s\"\n", arr[0], arr[2], arr[1]);
    }

}

void remove_quotations(char *string) {
  for (int i = 0; i < strlen(string); i++) {
    if (string[i] == '"') {
      string[i] = '\'';
    }
  }
}

// valid csv:
// 1,three,one
// sally,wants,beans