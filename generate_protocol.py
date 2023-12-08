import os
import json
import datetime
import string
import random

now_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

WELLS = [f"{row}{col}" for row in range(1, 13) for col in string.ascii_uppercase[:8]]

conditions = [{"ingredients": {}}, {"ingredients": {}}, {"ingredients": {}}]


def assign_wells_to_conditions(conditions):
    shuffled = sorted(WELLS, key=lambda k: random.random())
    print(shuffled)

    for idx, well in enumerate(shuffled):
        print(idx, well)

        if "wells" not in conditions[idx % len(conditions)]:
            print("new well")
            conditions[idx % len(conditions)]["wells"] = []

        conditions[idx % len(conditions)]["wells"].append(well)

    return conditions


def generate_file_content(layout_json: str):
    with open("protocol_template.py", "r") as template:
        file_content = template.read()

    insert = (
        f"""layout_json = \"\"\"{layout_json}\"\"\"\nlayout = json.loads(layout_json)"""
    )

    file_content = file_content.replace("# GENERATED CODE INSERT HERE #", insert)

    return file_content


conditions = assign_wells_to_conditions(conditions)

layout_json = json.dumps(conditions, indent=4)

# create a folder for the current generated protocol
folder_name = f"protocol_{now_str}"
os.mkdir(f"generated/{folder_name}")

# write layout to file
with open(f"generated/{folder_name}/layout.json", "w") as layout_file:
    layout_file.write(layout_json)

# filename with current data and time in it (to know what was loaded on the opentrons)
file_name = f"protocol_{now_str}.py"

# write file content to file (/generated folder)
with open(f"generated/{folder_name}/{file_name}", "w") as file:
    file.write(generate_file_content(layout_json))
