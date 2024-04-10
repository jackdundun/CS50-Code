#include <stdio.h>
#include <stdlib.h>
#include <cs50.h>
#include <stdint.h>

#define BLOCK_SIZE 512
 
int main(int argc, char *argv[])
{   // a variable of 1 byte defined
    typedef uint8_t BYTE;
    
    // giving the computer a variable of 1 byte that is an Array of size 512-- this creates the memory space
    BYTE buffer[BLOCK_SIZE];
    FILE *img = NULL;
    char filename[8];
    int counter = 0;
    
    if (argc != 2)
    {
        printf("./recover IMAGENAMETORECOVER.EXTENSION\n");
        return 1;
    }
    
    FILE* inptr = fopen(argv[1], "r");
    if (inptr == NULL)
    {
        printf("forensic image cannot be opened for reading.\n");
        return 1;
    }
    
    
    while (fread(buffer, sizeof(BYTE), BLOCK_SIZE, inptr) || feof(inptr) == 0)
    {
        if ( (buffer[0] == 0xff)  && (buffer[1] == 0xd8)   &&  (buffer[2] == 0xff)   && ( (buffer[3] & 0xf0) == 0xe0 ) )
        {
                if (img != NULL)
                {
                    fclose(img);
                }
                sprintf(filename, "%03i.jpg", counter);
                img = fopen(filename, "w");
                counter++;
        }
        if (img != NULL)
        {
            fwrite(buffer, sizeof(BYTE), BLOCK_SIZE, img);
        }
    }
    if (inptr != NULL)
    {
        fclose(inptr);
    }
    if (img != NULL)
    {
        fclose(img);
    }
        return 0;
}