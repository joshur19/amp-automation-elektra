"""
file: tags (setup) file for log styling and storing device address
author: josh
last updated: 19/02/2024
"""

import datetime

sim_addr = 'GPIB0::3::INSTR'
sps_addr = 'GPIB0::7::INSTR'
amp_tag = f"{datetime.datetime.now().strftime("%H:%M:%S")} -- LOG -- Amp Interface: "
main_tag = f'{datetime.datetime.now().strftime("%H:%M:%S")} -- LOG -- Main: '