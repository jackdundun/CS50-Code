from cs50 import get_int

height = get_int("Height: ")

while height <1  or height > 8:
    height = get_int("Height: ")

for rows in range(height):
        print(" "*(height - rows -1) + ((rows)*"#"+"#" + "  " + (rows)*"#"+"#" ))

