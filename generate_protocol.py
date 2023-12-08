import datetime


def generate_file_content():
    with open("protocol_template.py", "r") as template:
        file_content = template.read()

    return file_content


# filename with current data and time in it
file_name = f"protocol_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.py"

# write file content to file (/generated folder)
with open(f"generated/{file_name}", "w") as file:
    file.write(generate_file_content())
