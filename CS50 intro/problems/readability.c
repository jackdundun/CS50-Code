#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>



int level(string text);

int main(void)
{
    string text = get_string("Text: ");

    
    level(text);
    
}



int level(string text)
{
    int sumletter = 0;
    int sumword = 1;
    int sumsen = 0;

    for (int i=0, n=strlen(text); i<n; i++)
    {
        if (isalpha(text[i]) > 0)
        {
            sumletter++;
        }
    }
    
    for (int i=0, n=strlen(text); i<n; i++)
    {
        if (isspace(text[i]) > 0)
        {
            sumword++;
        }
    }
    
    for (int i=0, n=strlen(text); i<n; i++)
    {
        if (text[i] == 33 || 
            text[i] == 46 ||
            text[i] == 63 )
        {
            sumsen++;
        }
    }

    float grade = 0.0588 * ((float)sumletter* (100/(float) sumword)) - 0.296 * ((float)sumsen* (100/(float)sumword )) - 15.8;
    
    if (grade <1)
    {
        printf("Before Grade 1\n");
    }
    
    else if (grade > 15)
    {
        printf("Grade 16+\n");
    }
    
    else
    {
        printf("Grade %i\n", (int)round(grade));
    }

    return 0;
}