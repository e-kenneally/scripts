#!/usr/bin/env python

""" 

Example usage:

python regsummary.py /path/to/correlations

"""

import yaml
import os
import pandas as pd
import base64

def base_64(file):
    data_uri = base64.b64encode(open(file, 'rb').read()).decode('utf-8')
    img_tag = '<img src="data:image/png;base64,{0}" \
        width=350 height=400>'.format(data_uri)
    return img_tag

def get_yaml(directory, outfile_html, outfile_csv):
    keys = []
    correlations = []
    info_config_dataset = []
    subject = []
    df = pd.DataFrame()

    for subdirectory in os.listdir(directory):
        d = os.path.join(directory, subdirectory)
        
        for filename in os.listdir(d):
            f = os.path.join(d, filename)
            if filename == 'sub_optimal.yml':
                with open(f, 'r') as f:
                    reg_data = yaml.load(f, Loader= yaml.FullLoader)
                    for key, value in reg_data.items():
                        keys.append(key)
                        sub = value[0].split('/')[11]
                        subject.append(sub)
                        corr = (value[0]).split(':')
                        correlations.append(corr[0])
                        info_config_dataset.append(subdirectory.split('correlations_')[1])
                        
    list_of_tuples = list(zip(info_config_dataset,subject,keys, correlations))
    df = pd.DataFrame(list_of_tuples,
                    columns=['Info_config_dataset', 'Subject', 'Keys', 'Correlation'])
    df['Correlation'] = df['Correlation'].astype(float)
    df.sort_values(by=['Correlation'], ascending=False, inplace=True)
    df.to_html(outfile_html, index=False)
    df.to_csv(outfile_csv, index=False)


def get_boxplots(directory, outfile_html, outfile_csv):
    
    string = '\n'
    directory = '/ocean/projects/med220004p/shared/summary-regtest/correlations_ccs-options'
    for subdirectory in os.listdir(directory):
        d = os.path.join(directory, subdirectory)
        filelist= [file for file in os.listdir(d) if file.endswith('.png')]
        for x in filelist:
            f = os.path.join(d, x)
            string += base_64(f)

        with open(outfile_html, 'a') as f:
            f.write(string)
    
def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("correlations_dir", type=str, 
                        help="full path of directory with regtest correlation outputs")
    args = parser.parse_args()
    directory = args.correlations_dir
    
    outfile_html = "regsummary.html"
    outfile_csv = "regsummary.csv"
    get_yaml(directory, outfile_html, outfile_csv)
    get_boxplots(directory, outfile_html, outfile_csv)

    #directory = '/ocean/projects/med220004p/shared/regression_test_outputs_v1.8.5/regression_correlations_v1.8.5'

if __name__ == "__main__":
    main()
