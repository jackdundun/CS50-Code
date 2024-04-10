#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>



bool checksum(int argc, string argv);
void scramble(string cipher, string text, string key );


int main(int argc, string argv[])
{
    //check validity of key
    if (checksum(argc, argv[1]) == false)
    {
        return 1;
    }

    string text = get_string("plaintext: ");

    // changing the input text
    char cipher[strlen(text)+1];
    scramble(cipher, text, argv[1]);



}

void scramble(string cipher, string text, string key )
{
    for (int i =0; i < strlen(text); i++)
    {
        if (!isalnum(text[i]) || !isalpha(text[i]) )
        {
            cipher[i] = text [i];
        }

        else if (islower(text[i]))
        {
            cipher[i] = key[(text[i]- 97)];
            cipher[i] = tolower(cipher[i]);
        }

        else if (isupper(text[i]))
        {
            cipher[i] = key[(text[i]- 65)];
            cipher[i] = toupper(cipher[i]);
        }
    }
    cipher [strlen(text)] = '\0';
    printf("ciphertext: %s\n", cipher);
}






bool checksum(int a, string b)
{   int sum = 0;

    if (a != 2)
    {
        printf("Usage: ./substitution KEY\n");
        return false;
    }

    if (strlen(b) != 26)
    {
        printf("Key must contain 26 characters\n");
        return false;
    }
    for (int i = 0; i<strlen(b); i++)
    {    char ch = b[i];
        if (!isalpha(ch))
        {
            printf("Key must only contain alphabetic characters\n");
            return false;
        }
    }
    for (int i =0; i<strlen(b); i++)
    {
        if (islower(b[i]))
        {
            sum = sum + b[i] - 96;
        }
        else
        {
            sum = sum + b[i] - 64;
        }
    }
    if (sum != 351)
    {
        printf("Key must not contain repeated characters.\n");
        return false;
    }
    return true;
}