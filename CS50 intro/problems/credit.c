#include <stdio.h>
#include <cs50.h>
#include <math.h>
#include <stdlib.h>

int main (void)


{
    //get a credit card number
    long card;
    do
    {
        card = get_long("Enter a credit card number please: ");
    }
    while (card<pow(10,1) || card>pow(10,25) );

    int sum1;
    int sum2=0;
    int ccd1;
    int ccd2;
    long workcard = card;
    
    while (workcard>0)
    {
        ccd1 = workcard % 10;
        sum1 = ccd1 + sum1 ;
        workcard = workcard / 100 ;
    }

    workcard = card/10;
    while (workcard>0)
    {
        ccd2 = workcard % 10;
        ccd2 = ccd2 * 2;
            if (ccd2 > 9)
            {
                ccd2 = (ccd2%10) + (ccd2/10) ;
                sum2 = ccd2 + sum2 ;
                workcard = workcard / 100 ;
            }
            else
            {
                sum2 = ccd2 + sum2 ;
                workcard = workcard / 100 ;
            }
    }

    int checksum = sum1+sum2;
    
    long cdigits = floor(log10(labs(card))) + 1;
   
   if (checksum % 10 != 0)
   {
       printf("INVALID\n");
   }
   else if ((cdigits == 15) && ((card/10000000000000==34) || (card/10000000000000==37)))
        {
            printf("AMEX\n");
        }
       
    
    else if ((cdigits == 16) && ((card/100000000000000 >50) && (card/100000000000000<56)))
        {
            printf("MASTERCARD\n");
        }
    
    
    else if (((cdigits == 13) ||(cdigits == 16)) && ((card/1000000000000000==4) || (card/1000000000000==4) ))
        {
            printf("VISA\n");
        } 
        
    else
    {
        printf("INVALID\n");
    }
    
}