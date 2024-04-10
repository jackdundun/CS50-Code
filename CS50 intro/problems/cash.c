#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main (void)

//Cashing function
{
    //get a positive float value
    float change;
    do
    {
        change = get_float("Enter the amount of change needed: ");
    }
    while (change <=0);
    
    //round up the dollars to an integer for ease 
    int changeround = round(change * 100);
    
    
    int coincount = 0;
    while (changeround >= 25 )
    {
        changeround = changeround - 25; 
        coincount++;
    }
    while (changeround >= 10 )
    {
        changeround = changeround - 10; 
        coincount++;
    }
    
    while (changeround >= 5 )
    {
        changeround = changeround - 5; 
        coincount++;
    }
    
    while (changeround >= 1 )
    {
        changeround = changeround - 1; 
        coincount++;
    }
    
    printf("You will need %d coins for this change\n",coincount);
}