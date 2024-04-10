from cs50 import get_int, get_string
from math import trunc




def main():


    card = get_int("Number: ")

    checksum(card)

def checksum(card):
    sum1 = 0 
    sum2 = 0
    numofdigits = len(str(card))
    if numofdigits % 2 == 0:
        j=1
        k=0
        i=0
    else:
        j=1
        k=0
        i=1
    
    for i in range(j, numofdigits, 2):
        check = trunc((card / (10**i)) %10)
        check = check * 2
        if check > 9:
            check = check - 9
        sum1 += check
      
    for i in range(k, numofdigits, 2):
        check = trunc((card / (10**i)) %10)
        sum2 += check

    bothsums = sum1 + sum2
    if bothsums%10 != 0:
        print("INVALID")
        return
    
    firstdigits = int(str(card)[:2])
    
    if numofdigits == 15 and ((firstdigits == 34) or (firstdigits == 37)):
        print("AMEX")
        return
  
    if numofdigits == 16 and ( 51 <= firstdigits <= 55):
        print("MASTERCARD")
        return

    if ((numofdigits == 16) or (numofdigits == 13))  and (int(str(card)[:1]) == 4):
        print("VISA")
        return



if __name__ == "__main__":
    main()