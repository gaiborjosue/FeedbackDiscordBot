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