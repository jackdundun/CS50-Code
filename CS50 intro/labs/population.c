#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Explains to the user the calculator
    printf("Welcome to the lama population calculator!\n Please enter a start population size and an end population size \nand it will show the years it takes to reach the end population\n");

    // TODO: Prompt for start size
    int n;
    do
    {
    n = get_int("Please enter an integer above 9: ");
    }
    while (n < 10);

    // TODO: Prompt for end size

    int o;
    do
    {
    o = get_int("Please enter an end population, greater than initial population : ");
    }
    while (n >= o);

    // TODO: Calculate number of years until we reach threshold
    int y = 0;
    while (n<o)
    {
        n = n + n/3 - n/4;
        y++;
    }

    // TODO: Print number of years
        printf("Years: %i", y);
}