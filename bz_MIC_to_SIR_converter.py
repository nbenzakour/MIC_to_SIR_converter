#!/usr/bin/python3

#title           :bz_MIC_to_SIR_converter.py
# description     :This script will convert MIC to SIR (Sensitive Intermediate, Resistant),
#                 given MIC conventions (CLSI, EUCAST)
# author          :Nouri L. Ben Zakour
#date            :20190913
# version         :0.1.0
# usage           :bz_MIC_to_SIR_converter.py <infile> <outdir> <scheme> <posid> <species> <full>
#=======================================================================================


import sys
import os
import os.path
import re
import pandas as pd
import time
import datetime
from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser(description='Convert MIC to SIR, given MIC conventions.')

    parser.add_argument('-i', '--infile',
                        required=True,
                        help='Screening data')
    parser.add_argument('-o', '--outdir',

                        required=True,
                        help='Path for outdir')
    parser.add_argument('-s', '--scheme',
                        required=False,
                        default='CLSI',
                        choices=['CLSI', 'EUCAST', 'other'],
                        help='MIC breakpoint convention scheme (default = CLSI_entero_2018)')
    parser.add_argument('-id', '--posid',
                        required=False,
                        default=3,
                        type=int,
                        help='Position of identifying column to return (default = 3)')
    parser.add_argument('-sp', '--species',
                        required=False,
                        default='Entero',
                        choices=['Entero', 'Saureus'],
                        help='Species of interest: Enterobacteriacae (default) or Saureus')
    parser.add_argument('-f', '--full',
                        required=False,
                        default="True",
                        choices=["True", "False"],
                        help='Output includes full description with MIC + SIR conversion (default = True)')
    return parser.parse_args()


def testing(args):
    # verify screening file exists
    if not os.path.isfile(args.infile):
        raise Exception('Strain list was not found')

    # verify scheme data is present
    if not os.path.isfile('data/CLSI_entero_2018.csv'):
        raise Exception('CLSI MIC breakpoints information was not found')
    if not os.path.isfile('data/EUCAST.csv'):
        raise Exception('EUCAST MIC breakpoints information was not found')


def mkdir_outdir(outdir):
    # Creating the output directory if not present
    if not os.path.exists('{}'.format(outdir)):
        os.makedirs('{}'.format(outdir))
        print('Created output directory...')
    else:
        print('==> Output directory already exists')


def load_scheme(scheme):
    # load MIC breakpoint information from schemes provided in data (CLSI and EUCAST, so far)
    if scheme == 'CLSI':
        scheme_data = pd.read_csv('data/CLSI_entero_2018.csv', encoding="UTF-8")

    elif scheme == 'EUCAST':
        scheme_data = pd.read_csv('data/EUCAST.csv', encoding="UTF-8")

    else:
        print('Error: Other scheme not supported yet.')
        sys.exit(2)
    return(scheme_data)


# def convert AB_name(ab):


def parse_MIC(value):
    # strip front signs
    new_value = re.sub('[><=≤≥ ]', '', value)
    if '/' in new_value:
        value_pair = list(new_value.split('/'))
        result = list(map(float, value_pair))
    elif '.' in new_value or new_value.isdigit():
        if float(new_value) < 2000.0:
            result = float(new_value)
        else:
            result = 'ND'
    else:
        result = 'ND'
    # cases where breakpoint cutoff is greater rather than greater or equal to
    # change value to the next breakpoint rank, e.g. >16 is assigned 32
    if result != 'ND' and re.search('>[0-9]', value):
        try:
            result = [x * 2 for x in result]
        except:
            result = result * 2
    return result


def convert_MIC(value, lower, upper):
    if value == 'ND':
        return('ND')
    elif value <= lower:
        return('S')
    elif value >= upper:
        return('R')
    elif value > lower and value < upper:
        return('I')
    else:
        pass


def load_data(infile):
    # load screening data into dataframe, header changed to lower case
    screen_data = pd.read_csv(infile, encoding="UTF-8")
    screen_data = screen_data.fillna('ND')
    screen_data.columns = map(str.lower, screen_data.columns)
    return(screen_data)


def main():
    args = parse_args()
    testing(args)

    # setting up run
    outdir = args.outdir
    infile = args.infile
    scheme = args.scheme
    pos_id = args.posid
    pos_id = pos_id - 1
    full = args.full.lower()

    mkdir_outdir(outdir)

    # create log file
    logfile = open(outdir + '/logfile.txt', 'w+')
    print('Log info stored in:', outdir + '/logfile.txt')

    # loading MIC breakpoint scheme
    print('Loading scheme:', scheme)
    logfile.write('Loading scheme: ' + scheme + '\n')
    df_scheme = load_scheme(scheme)

    # loading screening data
    print('Loading screening data:', infile)
    logfile.write('Loading screening data: ' + infile + '\n')
    logfile.write('-------' + '\n')
    df_data = load_data(infile)

    # create new dataframe
    df_res = pd.DataFrame()
    df_res = pd.concat([df_res.reset_index(drop=True), df_data[df_data.columns[pos_id]]], axis=1)

    # search antibiotics available, iterate through data and convert to SIR into new dataframe
    print('Searching MICs to convert...')
    for row in df_scheme.itertuples():
        # extract antibiotic, parse sensitive and resistant cut-off values
        ab = row[1].lower()
        sval = parse_MIC(row[2])
        rval = parse_MIC(row[4])
        # search for antibiotic in screening data
        if ab in df_data.columns:
            logfile.write(ab + '\t cut-offs are S <= ' + str(sval) + ' and R >= ' + str(rval) + '\n')
            # logfile.write(str(list(df_data[ab])) + '\n')
            # convert to SIR into new dataframe
            # result = df_data[ab].apply(lambda x: 'R' if parse_MIC(x) >= rval else ('S' if parse_MIC(x) <= sval else 'I'))
            result = df_data[ab].apply(lambda x: convert_MIC(parse_MIC(x), sval, rval))
            # logfile.write(str(list(result)) + '\n')
            logfile.write('-------' + '\n')
            if full == "true":
                df_res = pd.concat([df_res.reset_index(drop=True), df_data[ab]], axis=1)
            df_res = pd.concat([df_res.reset_index(drop=True), result], axis=1)
        else:
            logfile.write(ab + '\t not tested' + '\n')
            logfile.write('-------' + '\n')
    # retrieve and append columns concerning metadata and antibiotics not found in CLSI data
    logfile.write('Add columns concerning metadata and antibiotics not found in CLSI data\n')
    print('Retrieving additional metadata...')
    for col in df_data.columns:
        if col not in df_res.columns:
            df_res = pd.concat([df_res, df_data[col]], axis=1)
            logfile.write('Retrieving ' + col + '\n')
    logfile.write('-------' + '\n')

    # recording time for timestamp
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d-%H%M%S')

    # write results to new csv
    outfile = outdir + '/MIC-conversion-results_' + st + '.csv'
    df_res.to_csv(outfile, index=False)
    #print(df_res)

    # finish logging
    print('Writing results to ' + outfile)
    print('---------------------------------------------------')
    print('Thank you for choosing to use MIC_to_SIR_converter!')
    logfile.write('Writing results to ' + outfile + "\n")
    logfile.close()


if __name__ == "__main__":
    main()
