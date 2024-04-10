#include <stdio.h>
#include <cs50.h>

//including note to compiler of function later in program
void print (char c, int n);
int main (void)


// The function itself
{
    //get int value from 1 - 8
    int n;
    do
    {
        n = get_int("Please enter a height for the pyramid: ");
    }
    while (n <1 || n> 8);

    //calling the first loop
    //note the loop function in a loop
    for (int i = 0;  i < n; i++)
    {
        print(' ', 7-i);
        print('#', i+1);
        print(' ', 2);
        print('#', i+1);     
        
        //adding a line break at the end
        printf("\n");
    }

}
// Defining the function, printing in a loop
void print(char c, int n)
{
    for (int i = 0; i < n; i++)
    {
        printf("%c", c);
    }
}