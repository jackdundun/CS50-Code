import sys
import csv
import re



def main():
    
    if len(sys.argv) != 3:
        print("enter - python file, csv file, text file")
        return 1
    
    csvfile = sys.argv[1]
    textfile = sys.argv[2]
    
    
    with open(csvfile) as f:
        
        reader = csv.reader(f)
        database = []
        for row in reader:
            database.append(row)
    
    
    for i in range (1, len(database)):
        for j in range(1, len(database[0])):
            database[i][j] = int(  database[i][j]  )
    
    with open(textfile) as f:
        reader = csv.reader(f)
        dna = []
        for row in reader:
            dna.append(row)
    dna = str(dna)
    
    dnadatabase = []    
    
    for i in range(1, len(database[0]) ):
        
        groups = re.findall(f"(?:{database[0][i]})+", dna)
        if groups:
            largest = max(groups, key=len)
            dnadatabase.append(  int(len(largest) /  len(database[0][i]))  )
    
    for i in range(1, len(database)):
         if len(set(database[i])  - set(dnadatabase)) == 1:
            print(database[i][0])
            return
    
    
    print("No match")
    return
            
    

if __name__ == "__main__":
    main()