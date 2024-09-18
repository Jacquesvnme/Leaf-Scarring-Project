import csv

data = [
    {'name': 'Nikhil', 'branch': 'COE', 'year': 2, 'cgpa': 9.0},
    {'name': 'Sanchit', 'branch': 'COE', 'year': 2, 'cgpa': 9.1},
    {'name': 'Aditya', 'branch': 'IT', 'year': 2, 'cgpa': 9.3},
    {'name': 'Sagar', 'branch': 'SE', 'year': 1, 'cgpa': 9.5},
    {'name': 'Prateek', 'branch': 'MCE', 'year': 3, 'cgpa': 7.8},
    {'name': 'Sahil', 'branch': 'EP', 'year': 2, 'cgpa': 9.1}
]

# w = overwrite | a = append | x = create file if it doesn't exist
try:
    with open('data.csv', 'w', newline='') as csvfile:
        fieldnames = ['name', 'branch', 'year', 'cgpa']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
except:
    #exception handling if using x to create file that doesn't exists
    print("Error in creating file.\nFile already exists")

# Using Pandas might be better