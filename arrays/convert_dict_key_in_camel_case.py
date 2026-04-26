data = {
    "first_name": "akshay_Kumar",
    "department_details": {"section_name": "c", "capacity_values": {"test": 1}},
    "more_details": [{"c_s": 1}, {"is": 2}]
}


def convert_word_to_camel(key):
    keys = key.split("_")
    k = keys[0]
    k = k +''.join(str(keys[j]).capitalize() for j in range(1, len(keys)))

    return k

def convert_camel_case(data):
    if type(data) == dict:
        value_data = {}
        for key , value in data.items():
            value_data[convert_word_to_camel(key)] = convert_camel_case(value)
        return value_data
        # return {convert_word_to_camel(key): convert_camel_case(value) for key , value in data.items()}
    elif type(data) == list:
        list_data = []
        for data_array in data:
            list_data.append(convert_camel_case(data_array))
        return list_data
        # return [convert_camel_case(data_array) for data_array in data]
    else:
        return data


"""
Problem -
You are given a nested data structure (a mix of dictionaries and lists) where all dictionary keys are in snake_case.

Your task is to convert all keys into camelCase, while preserving:

* The original structure (nested dictionaries & lists)
* The values (unchanged)

example -> 
data = {
    "first_name": "akshay",
    "department_details": {
        "section_name": "c",
        "capacity_values": {"test": 1}
    },
    "more_details": [
        {"c_s": 1},
        {"is": 2}
    ]
}

Soln - 
{
    "firstName": "akshay",
    "departmentDetails": {
        "sectionName": "c",
        "capacityValues": {"test": 1}
    },
    "moreDetails": [
        {"cS": 1},
        {"is": 2}
    ]
}


Summary -
Recursively walks through:
	•	dict: converts all keys using convert_word_to_camel
	•	list: applies same function on each item
	•	other types: returned as-is

✅ Best Practices
	•	Use recursion for nested structures
	•	Consider memoization if processing large trees repeatedly
	•	Make it robust to handle None, non-string keys if needed in the future

"""
print(convert_camel_case(data))




                    


