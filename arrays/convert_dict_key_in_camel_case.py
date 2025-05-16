data = {
    "first_name": "akshay",
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
        return {convert_word_to_camel(key): convert_camel_case(value) for key , value in data.items()}
    elif type(data) == list:
        return [convert_camel_case(data_array) for data_array in data]
    else:
        return data


print(convert_camel_case(data))




                    


