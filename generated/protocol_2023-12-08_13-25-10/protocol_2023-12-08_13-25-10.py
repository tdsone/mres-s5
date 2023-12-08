import random
from opentrons import protocol_api
import json

layout_json = """[
    {
        "ingredients": {},
        "wells": [
            "10A",
            "2C",
            "9D",
            "6B",
            "7C",
            "9F",
            "1B",
            "12B",
            "5C",
            "1E",
            "12H",
            "12E",
            "6E",
            "7D",
            "4D",
            "8B",
            "6A",
            "5F",
            "4G",
            "9H",
            "3B",
            "7G",
            "8C",
            "3F",
            "2H",
            "7A",
            "8E",
            "9G",
            "11A",
            "3A",
            "11B",
            "4A"
        ]
    },
    {
        "ingredients": {},
        "wells": [
            "12F",
            "1D",
            "11H",
            "10B",
            "10H",
            "7F",
            "8A",
            "3E",
            "3D",
            "4E",
            "2D",
            "2B",
            "11G",
            "12D",
            "12C",
            "10D",
            "1A",
            "8G",
            "2E",
            "6G",
            "9E",
            "11E",
            "10G",
            "8H",
            "12A",
            "7B",
            "3C",
            "9C",
            "5A",
            "10F",
            "1C",
            "9B"
        ]
    },
    {
        "ingredients": {},
        "wells": [
            "6H",
            "8F",
            "2F",
            "5B",
            "5G",
            "6C",
            "4H",
            "3H",
            "6F",
            "5E",
            "1H",
            "1F",
            "4F",
            "12G",
            "4C",
            "9A",
            "3G",
            "11F",
            "7E",
            "6D",
            "1G",
            "11D",
            "2A",
            "2G",
            "10C",
            "8D",
            "5H",
            "11C",
            "4B",
            "5D",
            "7H",
            "10E"
        ]
    }
]"""
layout = json.loads(layout_json)

# user define
num_carbonsources = 2
num_antibio = 2 + 1  # consider 1 for control
num_cond = num_carbonsources * num_antibio

# plate set up
columns = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
rows = ["A", "B", "C", "D", "E", "F", "G", "H"]
layout = [f"{row}{col}" for row in rows for col in columns]
# Shuffle the flat_list in a random order
rand_layout = random.shuffle(layout)

# Initialize empty lists for each condition
conditions = [[] for i in range(num_cond)]

# Divide the flat_list into 6 equal parts and assign to each condition
for i in range(len(layout)):
    conditions[i % 6].append(rand_layout[i])

metadata = {"apiLevel": "2.8"}


def run(protocol: protocol_api.ProtocolContext):
    # import labware

    tiprack_1 = protocol.load_labware("opentrons_96_tiprack_300ul", 10)
    p300 = protocol.load_instrument("p300_single_gen2", "right", tip_racks=[tiprack_1])

    # 96 well plate for media zith rand set up
    target_plate = protocol.load_labware("4ti0136_96_wellplate_2200ul", 1)

    # stocks to make different conditions
    stock_holder = protocol.load_labware(
        "opentrons_10_tuberack_falcon_4x50ml_6x15ml_conical", 9
    )

    # will store different condtions
    slit_reservoir = protocol.load_labware("4ti0131_12_reservoir_21000ul", 5)

    # will be used to pipette inducer
    tiprack_2 = protocol.load_labware("opentrons_96_tiprack_20ul", 11)
    p300 = protocol.load_instrument("p20_multi_gen2", "left", tip_racks=[tiprack_2])

    for n in range(num_cond):
        p20.pick_up_tip()
        for i in range(len(conditions[n])):
            p20.transfer(
                10,
                slit_reservoir[f"A{n + 1}"],
                target_plate[f"{conditions[n][i]}"],
                new_tip="never",
            )
        p20.drop_tip()
