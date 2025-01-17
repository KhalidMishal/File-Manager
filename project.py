import sys
import os
import re
import csv
import pandas as pd
from pyfiglet import Figlet


"""
For the future:
- Disallow two files with same name and type
- 
"""
linebreak = "-----------"

def main():

    initialize_csv()

    while True:
        clear()
        title = "Digital Sketchbook"
        subtitle = "Manage your collection of art files through tags and notes"

        response = menu(title, subtitle)
        print("")
        match response:
            case "1":
                save()
            case "2":
                display()
            case "3":
                search()
            case "4":
                clear()
                sys.exit()


def initialize_csv():
    file_path = "./artworks.csv"

    # Check if file exists
    if os.path.isfile(file_path) == False:
        with open("artworks.csv", "w") as csvfile:
            fieldnames = ['name', 'tags', 'type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

    else:
        # Check if file is empty
        csv_file_path = './artworks.csv'
        df = pd.read_csv(csv_file_path) # read csv file
        
        if df.empty:
            create_header()
        else:
            # proceed with reading the file
            print(df.head())
            

# Check if header exists
def create_header():
    with open("artworks.csv", "w") as csvfile:
        fieldnames = ['name', 'tags', 'type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()


def clear(): # Clears the Terminal
    os.system('cls')
    
def save(): # Save a new file
    clear()
    name = input("File name: ")
    if name == "":
        return "Name cannot be empty"
    else:
        user_tags = input("Tags, separated by commas: ")
        user_tags = user_tags.lower().strip()
        if "," in user_tags:
            tags = user_tags.split(",")
        else:
            tags = user_tags
        
        if file_name := re.search(r"[\w\d\s]+\.([\w]+)", name):
            file_type = file_name.group(1)
            print(file_type)
        else:
            file_type = "jpeg"

        with open('artworks.csv', 'a', newline='') as write, open("artworks.csv") as check:
            writer = csv.DictWriter(write, fieldnames=["name", "tags", "type"])
            writer.writerow({"name": name, "tags": tags, "type":file_type})


def display(): # Display all files
    clear()
    with open("artworks.csv") as file:
        reader = csv.DictReader(file)
        for i,row in enumerate(reader):
            print(f"{i+1}. Name: {row['name']} | Tags: {row['tags']} | Type: {row['type']}")
        print(linebreak)

    act = menu2()
    
    match act:
        case "1":
            check_files()
        case "2":
            save()


def check_files():
    file_name = input("What file would you like to delete? ")
    file_name = file_name.lower().strip()

    with open('artworks.csv') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if file_name == row['name']:
                delete(file_name)
        
        print("File does not exist")

def delete(file_name):
    df = pd.read_csv('artworks.csv', index_col='name')
    df = df.drop(file_name)
    df.to_csv('artworks.csv', index=True)

# Search for specific tags
def search():
    clear()
    searches = ["Name", "Tag", "Type"]

    for count, ele in enumerate(searches, start = 1):
        print(count, ele)
    print(linebreak)
    
    options = 3

    while options == 3:
        searching = input("What would you like to search? ")
        match searching:
            case "1":
                options = 0
            case "2":
                options = 1
            case "3":
                options = 2

    search_query = input("Search for: ") 
    results = []

    with open('artworks.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[options] == search_query:
                results.append(row)
            else:
                input("No file found ")
                break

    clear()
    print("Name | Tags | Title")
    for f in results:
        print(f"Name: {f[0]} | Tags: {f[1]} | Type: {f[2]}")
    print(linebreak)
    act = menu2()


def menu(title="Title", subtitle=""):
    print(f"\n{title}")
    print(subtitle)
    print(linebreak)
    options = [
        "1. Save a new art file",
        "2. Display all art files",
        "3. Search",
        "4. Exit"
    ]
    for opt in options:
        print(opt)
    print(linebreak)
    return(input("Selection: "))


def menu2():
    actions = ["Delete a file", "Add a file", "Return to menu"]

    for count, ele in enumerate(actions, start = 1):
        print(count, ele)
    print(linebreak)

    while True:
        if act := input("What would you like to do? "):
            return act
    

if __name__ == "__main__":
    main()
