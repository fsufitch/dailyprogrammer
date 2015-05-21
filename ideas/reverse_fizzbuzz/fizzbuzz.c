#include <stdio.h>

int main() {
  int mod3, mod5;
  for (int i=1; i<21; i++) {
    mod3 = i % 3; 
    mod5 = i % 5;
    if (!mod3 && !mod5) printf("fizz buzz\n");
    else if (!mod3) printf("fizz\n");
    else if (!mod5) printf("buzz\n");
    else printf("%d\n", i);
  }
}
