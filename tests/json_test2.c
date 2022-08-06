// gcc -m32 -fno-stack-protector -z execstack -no-pie json_test2.c nxjson.c -o json_test2

#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include "nxjson.h"
#include <strings.h>

#define MAX_SIZE 2048

int main(void) {
    char string[MAX_SIZE];
    gets(string);

    const nx_json* json = nx_json_parse_utf8(string);

    const int len = (int)nx_json_get(json, "len") -> text_value;
    const nx_json *arr = nx_json_get(json, "numbers");
    for (int i = 0; i < len; i++) {
      const nx_json *item = nx_json_item(arr, i);
      printf("%d: %d\n", i, (int)item->text_value);
    }

    nx_json_free(json);
}

// valid json:
// {"len" : 5, "numbers" : [1, 2, 3, 4, 5]}