#include <stdio.h>
#ifdef _WIN32
#include <Windows.h>
#else
#include <unistd.h>
#endif

int main(void) {
	// sleep(1);
	char buf[50];
	gets(&buf);
	printf("%s", buf);
}