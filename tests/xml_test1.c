// gcc -m32 -fno-stack-protector -z execstack -no-pie -o xml_test1 xml_test1.c xml.c

#include <stdio.h>
#include <stdint.h>
#include "xml.h"

void print_node_recurse(struct xml_node *node);

#define MAX_LENGTH 100

int main(void) {
  char string[MAX_LENGTH];
  gets(string, MAX_LENGTH, stdin);

  struct xml_document *xml = xml_parse_document((uint8_t *)string, strlen(string));
  if (xml == NULL) {
    printf("Enter proper xml darn you\n");
    return 1;
  }

  struct xml_node *root = xml_document_root(xml);
  print_node_recurse(root);
  // printf("%s\n", xml);
}

void print_node_recurse(struct xml_node *node) {
  int children = xml_node_children(node);
  if (children == 0) {
    char buffer1[MAX_LENGTH] = {0};
    char buffer2[MAX_LENGTH] = {0};
    struct xml_string *tagname = xml_node_name(node);
    struct xml_string *content = xml_node_content(node);
    xml_string_copy(tagname, buffer1, MAX_LENGTH);
    xml_string_copy(content, buffer2, MAX_LENGTH);
    printf("%s: %s\n", buffer1, buffer2);
  }
  else {
    
    for (int i = 0; i < children; i++) {
      print_node_recurse(xml_node_child(node, i));
    }
  }
}

// valid xml
// <hello><beans><one>apples</one><two>two</two><three>three</three></beans></hello>
