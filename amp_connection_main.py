"""
file: main file that represents the core functionality of switching bands
author: josh
last updated: 19/02/2024
"""

import amp_interface
import tags
import time
import sys

# Create intance of amplifier interface
amp = amp_interface.AmpInterface()

# Function to switch to frequency band 1
def switch_band1():
    cmd = 'BAND1'
    counter = 0
    reset_faults()
    
    status = ['', '']

    if amp.connect(tags.sim_addr):

        # bis zu 10 mal versuchen Band zu wechseln
        while status[1] != 'BAND1' and counter <= 10:
            amp.write_command(cmd)
            time.sleep(2)
            status = ask_status()
            print(tags.main_tag + 'Trying to switch to Band 1...')

            counter += 1
        
        if status[1] == 'BAND1':
            print(tags.main_tag + 'Switched to Band 1.')

        # AMP auf OPR Mode setzen
        if amp.connect(tags.sps_addr):
            amp.write_command('OPER')
            time.sleep(2)
            amp.write_command('OPER')
            time.sleep(1)
            amp.write_command('OPER')
            print(tags.main_tag + 'SPS in OPR Mode.')
        else:
            print(tags.main_tag + 'Error connecting to SPS.')

    else:
        print(tags.main_tag + 'BAND1 - Error connecting to AMP, check GPIB connection.')

# Function to switch to frequency band 2
def switch_band2():
    cmd = 'BAND2'
    counter = 0
    reset_faults()
    
    status = ['', '']

    if amp.connect(tags.sim_addr):

        # bis zu 10 mal versuchen Band zu wechseln
        while status[1] != 'BAND2' and counter <= 10:
            amp.write_command(cmd)
            time.sleep(2)
            status = ask_status()
            print(tags.main_tag + 'Trying to switch to Band 2...')

            counter += 1
        
        if status[1] == 'BAND2':
            print(tags.main_tag + 'Switched to Band 2.')

    else:
        print(tags.main_tag + 'BAND2 - Error connecting to AMP, check GPIB connection.')

# Function to switch to frequency band 3
def switch_band3():
    cmd = 'BAND3'
    counter = 0
    reset_faults()
    
    status = ['', '']

    if amp.connect(tags.sim_addr):

        # bis zu 10 mal versuchen Band zu wechseln
        while status[1] != 'BAND3' and counter <= 10:
            amp.write_command(cmd)
            time.sleep(2)
            status = ask_status()
            print(tags.main_tag + 'Trying to switch to Band 3...')

            counter += 1
        
        if status[1] == 'BAND3':
            print(tags.main_tag + 'Switched to Band 3.')

    else:
        print(tags.main_tag + 'BAND3 - Error connecting to AMP, check GPIB connection.')

# Function to query status of amplifier
def ask_status():
    cmd = 'STS'
    try:
        raw_status = amp.query_command(cmd)
        status = parse_status(raw_status)
        return status
    except:
        print(tags.main_tag + 'Error in STS call')
        return False

# Function to parse raw status response from amplifier
def parse_status(raw_result):

    ## get relevant information from raw status response
    decoded_status = raw_result.decode('ascii')
    cleaned_status = decoded_status.split('\n')
    cleaned_status = [elem.strip('\r') for elem in cleaned_status]

    filtered_status = []
    for elem in cleaned_status:
        try:
            int_elem = int(elem)
            filtered_status.append(int_elem)
        except ValueError:
            continue

    total_sum = sum(filtered_status)
    num_elem = len(filtered_status)

    status_decimal = total_sum // num_elem

    print(tags.main_tag + f'Dezimalantwort: {status_decimal}')

    status_binary = f'{status_decimal:08b}'

    ## parse information from binary number
    if status_binary[3] == '0' and status_binary[4] == '0':
        band = 'BAND1'
    elif status_binary[3] == '0' and status_binary[4] == '1':
        band = 'BAND2'
    elif status_binary[3] == '1' and status_binary[4] == '0':
        band = 'BAND3'

    lcl_rem = 'LOCAL' if status_binary[5] == '0' else 'REMOTE'
    flt = 'FAULT' if status_binary[6] == '1' else 'NO FAULT'
    llo = 'LOCKOUT' if status_binary[7] == '1' else 'NO LOCKOUT'

    return [status_binary, band, lcl_rem, flt, llo]     ## todo: als map überarbeiten für bessere übersicht beim Zugriff

# Send command to amplifier to reset any latched faults
def reset_faults():
    cmd = 'RST'
    if amp.connect(tags.sim_addr):
        amp.write_command(cmd)
        amp.disconnect()
    else:
        print(tags.main_tag + 'RST - Error connecting to AMP.')


  
if __name__ == "__main__":
    
    argument = sys.argv[1]

    if argument == 'BAND1':
        switch_band1()
    elif argument == 'BAND2':
        switch_band2()
    elif argument == 'BAND3':
        switch_band3()

    time.sleep(2)