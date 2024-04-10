#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

bool checksum(string s);
void scramble(string cipher, string text, int k);

int main(int argc, string argv[])
{  
    //checking the key vailidity - checks if more than 2 strings
    if  ( argc != 2  || !checksum(argv[1]) )
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    
    string text = get_string("plaintext: ");
    
    //ci = (pi + k) % 26
    int k = atoi(argv[1]);
    char cipher[(strlen(text)+1)];
    scramble(cipher, text, k);

    return 0;
}

void scramble(string cipher, string text, int k)
{
    for (int i=0; i<strlen(text); i++)
    {
        if (!isalnum(text[i]) || !isalpha(text[i]))
        {
            cipher[i] = text[i];
        }
        
        else if (islower(text[i]))
        {
        cipher[i] = (((text[i]+ k - 'a') % 26)  + 'a' );
        }
        
        else if (isupper(text[i]))
        {
        cipher[i] = (((text[i]+ k - 'A') % 26)  + 'A' );   
        }
    }
    printf("ciphertext: %s\n", cipher);
}



bool checksum(string text)
{
    for (int i = 0; i < strlen(text); i++ )
    {   char ch = text[i];
        if (!isdigit(ch))
        {
            return false;
        }
    }
    return true;
}




