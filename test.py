import json

# function to add to JSON
def write_json(new_data, filename='data2.json'):
    with open(filename,'r+') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["emp_details"].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)
 
    # python object to be appended
y = {"emp_name":"abc",
     "email": "nikhil@geeksforgeeks.org",
     "job_profile": "Full Time"
    }
     
write_json(y)

#for reading   

with open('data2.json') as user_file:
  file_contents = user_file.read()
  
parsed_json = json.loads(file_contents)
  
for i in parsed_json['emp_details']:
    print(i['emp_name'])