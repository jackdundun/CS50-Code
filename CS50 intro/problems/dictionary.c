// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include "dictionary.h"
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int BUCKETS = 500;

//variable for word count
unsigned int COUNT = 0; 
//

// Hash table
node *table[BUCKETS];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    node* find = table[hash(word)];
    
    while (find != NULL)
    {
        if (strcasecmp(find->word, table[hash(word)]->word) == 0)
        {   
            return true;
        }
        else
        {
            find = find->next;
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO
    // credit to DJB2 hashing algorithm
    unsigned long hash = 5381;
    int c;
    while ((c = *word++))
    {   
        c = tolower(c);
        hash = (((hash << 5) + hash) + c) %BUCKETS; /* hash * 33 + c */ 
    }
        
    return hash;

}



// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{   
    // TODO
    //variables
    char buffer[LENGTH + 1];
    
    
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {   
        return false;
    }
    
    
    while (fscanf(file, "%s", buffer) != EOF)
    {
        node* n = malloc(sizeof(node));
        if (n == NULL)
        {   
            return false;
        }
        strcpy(n->word, buffer);
        n->next= NULL;
        
        //  hashnum is the hashed words number
        int hashnum = hash(n->word);
        
        // adding the nodes into the array
        if (table[hashnum] == NULL)
        {
            table[hashnum] = n;
        }
        else
        {
            n->next=table[hashnum];
            table[hashnum] = n;    
        }
        COUNT++;
    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return COUNT;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < BUCKETS; i++)
    {
        node *cursor = table[i];
        
        while(cursor != NULL)
        {
            node* tmp = cursor;
            cursor = cursor->next;
            free(tmp);
        }
        table[i] = NULL;
    }
    return true;
}
