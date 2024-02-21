import json

def read_or_init_json(filepath="feedback.json"):
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Function to update the JSON file
def update_assignment_json(assignment_number, feedback_file, filepath='feedback.json'):
    data = read_or_init_json(filepath)
    data[str(assignment_number)] = feedback_file
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)

def delete_feedback(assignment_number):
    try:
        data = read_or_init_json()

        if data.get(str(assignment_number)):
            del data[str(assignment_number)]

        with open('feedback.json', 'w') as f:
            json.dump(data, f)

        return True
    except Exception as e:
        print(e)
        return False

def assignment_number_not_provided():
    data = read_or_init_json()

    if data:
        latest_assignment = max(data.keys(), key=int)
        return int(latest_assignment)
    else:
        return None