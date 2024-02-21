import json

def read_or_init_json(filepath="feedback.json"):
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Function to update the JSON file
def update_assignment_json(server_name, assignment_number, feedback_file, filepath='feedback.json'):
    data = read_or_init_json(filepath)
    if server_name not in data:
        data[server_name] = {}

    data[server_name][str(assignment_number)] = feedback_file

    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)

def delete_feedback(assignment_number, server_name):
    data = read_or_init_json()
    try:
        if str(assignment_number) in data.get(server_name, {}):
            del data[str(assignment_number)]

            with open('feedback.json', 'w') as f:
                json.dump(data, f, indent=4)

            return True
    except Exception as e:
        print(e)
    
    return False

def assignment_number_not_provided(data, server_name):
    if server_name in data and data[server_name]:
        latest_assignment = max(data[server_name].keys(), key=int)
        return int(latest_assignment)
    else:
        return None