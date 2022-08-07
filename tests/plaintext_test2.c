// gcc -m32 -fno-stack-protector -z execstack -no-pie plaintext_test2.c -o plaintext_test2

#include <stdio.h>
#include <stdlib.h>

int main(int argc, char const *argv[])
{
	puts("Want me to add some numbers for you?");
	int x;
	int y;
	scanf("%d", &x);
	scanf("%d", &y);

	if (x + y > 100)
	{
		puts("Wow that's a big number!");
		return 0;
	} else {

		char number[3];
		puts("That's a cool number, maybe you can guess my favourite?");
		scanf("%s", number);
		int vuln = atoi(number);

		printf("How did you know %d was my favourite number?", vuln);
	}
	return 0;
}
