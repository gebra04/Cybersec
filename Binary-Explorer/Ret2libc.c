#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void vuln() {
    char buffer[40];
    printf("Enter your input: ");
    gets(buffer);
}

int main() {
    vuln();
    return 0;
}
