# -*- coding: utf-8 -*-
"""
Serial Dilution Protocol
"""

from opentrons import protocol_api

metadata = {"apiLevel": "2.8"}


def run(protocol: protocol_api.ProtocolContext):
    # Define the labware
    plate = protocol.load_labware(
        "costar3370flatbottomtransparent_96_wellplate_200ul", 3
    )
    tiprack_1 = protocol.load_labware("opentrons_96_tiprack_300ul", 1)
    p300 = protocol.load_instrument("p300_multi_gen2", "left", tip_racks=[tiprack_1])
    reservoir = protocol.load_labware("4ti0131_12_reservoir_21000ul", 2)

    columns = list(range(1, 13))

    fluorescin_location = reservoir["A1"]
    PBS_location = reservoir["A2"]

    # Fill wells {A-H}1 with fluorescin
    p300.pick_up_tip()
    p300.transfer(200, fluorescin_location, plate["A1"], new_tip="never")
    p300.drop_tip()

    # Pipette PBS into wells {A-H}2 to {A-H}12
    p300.pick_up_tip()
    for i in columns[1:]:
        p300.transfer(100, PBS_location, plate[f"A{i}"], new_tip="never")
    p300.drop_tip()

    # Dilute the fluorescin
    p300.pick_up_tip()
    for i in range(1, 12):
        p300.transfer(
            100, plate[f"A{i}"], plate[f"A{i+1}"], mix_after=(3, 50), new_tip="never"
        )
    p300.aspirate(100, plate["A11"])
    p300.drop_tip()
