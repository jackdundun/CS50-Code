from cs50 import get_string


text = get_string("Please enter a text: ")

words = len(text.split()) 


letters = (sum(c.isalpha() for c in text))

fullstops = text.count(".") + text.count("?")

L = letters * ( 100/words  )
S = fullstops * ( 100/words )

index = 0.0588 * L - 0.296 * S - 15.8

if 1 < index < 15.5:
    print("Grade " + str(round(index)))
if index < 1:
    print("Before Grade 1")
if index > 16:
    print("Grade 16+")