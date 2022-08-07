// gcc -m32 -fno-stack-protector -z execstack -no-pie json_test1.c nxjson.c -o json_test1

#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include "nxjson.h"
#include <strings.h>

#define MAX_SIZE 100

int main(void) {
    char string[MAX_SIZE];
    gets(string);

    const nx_json* json = nx_json_parse_utf8(string);

    const char *value = nx_json_get(json, "value")->text_value;
    printf("%s\n", value);

    nx_json_free(json);
}

// valid json:
// {"this" : "is", "valid" : "json", "with": "a", "value": "!!!"}