def age_age_count(input: str):
    inputs = input.split(",")
    count = 0
    print("input->", inputs)
    for i in inputs:
        if "age=" in i:
            p = i.split("age=")
            if int(p[1]) >= 50:
                count += 1
    return count


if __name__ == "__main__":
    input = {
        "data": "key=IAfpk, age=58, key=WNVdi, age=64, key=jp9zt, age=47"
    }
    print(age_age_count(input["data"]))
