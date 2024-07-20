#include <stdio.h>
#include <string.h>

void win() {
    printf("You have called the win function!\n");
    system("/bin/sh");
}

void vuln() {
    char buffer[40];
    printf("Enter your input: ");
    gets(buffer);
}

int main() {
    vuln();
    return 0;
}
