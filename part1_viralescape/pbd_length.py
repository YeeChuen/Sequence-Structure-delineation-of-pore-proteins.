'''
cp -r MUSCLE_joball.sbatch /work/ratul/chuen/viral_escape
cp -r pbd_checkclusterfamily.py /work/ratul/chuen/viral_escape
cp -r pbd_checknamelength.py /work/ratul/chuen/viral_escape
cp -r pbd_filterRNA.py /work/ratul/chuen/viral_escape
cp -r pbd_findlength.py /work/ratul/chuen/viral_escape
cp -r pbd_heatmap.py /work/ratul/chuen/viral_escape
cp -r pbd_length.py /work/ratul/chuen/viral_escape
cp -r pbd_muscle_one.py /work/ratul/chuen/viral_escape
cp -r pbd_scatter_dash.py /work/ratul/chuen/viral_escape
cp -r requirements /work/ratul/chuen/viral_escape
cp -r sbatch_output /work/ratul/chuen/viral_escape
cp -r sbatch_script /work/ratul/chuen/viral_escape
cp -r test_fas /work/ratul/chuen/viral_escape
cp -r test_msa /work/ratul/chuen/viral_escape


cp -r PoreDB_data_includeRNA /work/ratul/chuen/viral_escape
cp -r PoreDB_nonRNA /work/ratul/chuen/viral_escape
cp -r __pycache__ /work/ratul/chuen/viral_escape
cp -r python_script /work/ratul/chuen/viral_escape
cp -r test_CD-HIT_1 /work/ratul/chuen/viral_escape
cp -r test_CD-HIT_1.clstr /work/ratul/chuen/viral_escape
cp -r ----- /work/ratul/chuen/viral_escape

'''

# Author/s: Yee Chuen Teh
# Title: pbd_length.py 
# Project: Chowdhury Lab Viral Escape
# Description: filter dataset base of sequence length, equal, less than, and able to plot barchart based on selection
# Reference:
'''
TODO: write your reference here
Usage:
python pbd_length.py --f PoreDB_nonRNA/PoreDB_nonRNA_le1000.fas --t non --s n --l 1000
python pbd_length.py --f PoreDB_old/PoreDB.fas --t non --s y
python pbd_length.py --f PoreDB_nonRNA/PoreDB_nonRNA_le1000.fas --t non --s n
python pbd_length.py --f PoreDB_nonRNA/Muscle_3W5B_1 --t non --s y
'''
# Updates:  (2/8/2023)
'''
    - fixed split_des_seq() function where the last index of name_list is a sequence.
'''

#____________________________________________________________________________________________________
# imports 
    # TODO: write your imports here
import argparse
import os
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import make_axes_locatable

#____________________________________________________________________________________________________
# set ups 
    # TODO: write your functions here
def fas_to_list(path):
    fas_list = []
    with open (path, "r") as f:
        a_temp = f.read()
        b_temp = a_temp.split("\n")
        if b_temp[len(b_temp)-1] == "":
            b_temp.pop()
        fas_list =  b_temp
    
    while "" in fas_list:
        fas_list.remove("")
    # check if the file is in FAS format, if yes, odd index description, even index sequence
    FAS = True
    for i in range(len(fas_list)):
        if i%2 == 0:
            if fas_list[i][0] != ">":
                #print("file read is not FASTA, converting the list to FAS")
                FAS = False
                break
    if FAS == False:   
        c_temp = []
        sequence = ""
        for p in fas_list:
            if p == "":
                continue
            if p[0] == ">":
                    sequence = ""
                c_temp.append(p)
            else:
                sequence += p
        c_temp.append(sequence)
        fas_list = c_temp
    else:
        print("file read is FASTA, proceed as usual")
    
    return fas_list


def split_des_seq(fas_list):
    seq_list = []
    name_list = []
    sequence = ""
    for p in fas_list:
        if p == "":
            continue
        if p[0] == ">":
            if sequence != "":
                seq_list.append(sequence)
                sequence = ""
            name_list.append(p)
        else:
            sequence += p
    seq_list.append(sequence)
    #name_list.append(p)

    return [name_list, seq_list]

def check_length(c_temp):
    '''count the frequence of the protein sequence length, and then report it.
    lastly return the highest frequency (int)'''
    ''' input is 2D list, c_temp[0] is description, c_temp[1] is sequence only'''
    dict = {}
    seq_list = c_temp[1]
    max_freq = 0
    maxfreq_length = 0
    max_length = 0

    for s in seq_list:
        length = len(s)
        max_length = max(length, max_length)
        if length in dict:
            dict[length]+=1
        else:
            dict[length] = 1
        if dict[length] >max_freq:
            max_freq = dict[length]
            maxfreq_length = length

    myKeys = list(dict.keys())
    myKeys.sort()
    sorted_key = {i: dict[i] for i in myKeys}

    for k in sorted_key:
        print("Frequency of protein with length {}: {}".format(str(k), str(dict[k])))

    print("Highest protein frequence with length {}: {}".format(str(maxfreq_length), str(max_freq)))
    print("total number of protein in selected file: {}".format(str(len(seq_list))))

    return [int(max_freq), int(max_length)]



def extract_length(c_temp, name, length, type):
    check = length
    name_list = c_temp[0]
    seq_list = c_temp[1]
    a = []
    filename = ""
    if type == "eq":
        for i in range(len(seq_list)):
            if len(seq_list[i]) == check:
                a.append(name_list[i])
                a.append(seq_list[i])
        filename = name + "_eq{}.fas".format(str(length))
    if type == "le":
        for i in range(len(seq_list)):
            if len(seq_list[i]) <= check:
                a.append(name_list[i])
                a.append(seq_list[i])
        filename = name + "_le{}.fas".format(str(length))

    with open(filename, 'a') as f:
        for p in a:
            f.write(p+"\n")            

def barchart(c_temp, target_length, show):
    '''c_temp is a list where index 0 is name, index 1 is seq'''
    seq = c_temp[1]
    dict = {}
    target = 0
    for s in seq:
        length = len(s)
        if length <= target_length:
            target+=1
            if length in dict:
                dict[length]+=1
            else:
                dict[length] = 1

    myKeys = list(dict.keys())
    myKeys.sort()
    data = {i: dict[i] for i in myKeys}

    frac = int(target)/int(len(seq))
    percentile = frac*100
    print("percentile of protein under length {}: {}  ({}/{})".format(str(target_length), str(percentile), str(target), str(len(seq))))
    
    if show == "y":
        # create bar chart
        plt.bar(data.keys(), data.values(), color='g')

        # add labels and title
        plt.xlabel('Protein with sequence of length')
        plt.ylabel('frequency')
        plt.title('Bar Chart of Protein Sequence Length frequency.')

        plt.show()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--f', type=str, required=True)     # file location
    parser.add_argument('--t', type=str, required=True)     # generate/extract target type (eq (equal),le(less than equal), all(both)  etc)
    parser.add_argument('--s', type=str, required=True)    # check if this runs in cluster, so it might show (y,n)
    parser.add_argument('--l', type=int, required=False)    # tha target length
    args = parser.parse_args()

    allow = ["non", "le", "eq", "all"]
    if args.t not in allow:
        print("argument for \"--t\" invalid, use shown below")
        print(allow)
        return

    f_path = args.f
    a_temp = f_path.split("/")
    dir = a_temp[0]
    global name
    if "." in a_temp[1]:
        b_temp = a_temp[1].split(".")
        name = b_temp[0]
    else:
        name = a_temp[1]

    path = os.getcwd()
    to_path = path+"/"+dir
    os.chdir(to_path)

    fas_list = fas_to_list(a_temp[1])
    c_temp = split_des_seq(fas_list)

    d_temp = check_length(c_temp)
    max_freq = d_temp[0]
    max_length = d_temp[1]

    if "--l" in sys.argv:
            barchart(c_temp, args.l, args.s)
    else:
            barchart(c_temp, max_length, args.s)

    if args.t == "non":
        print("--- not extracting file ---")
        pass
    elif args.t == "le" or  args.t == "all":
        print("--- creating a \"less than file\" ---")
        if "--l" in sys.argv:
            extract_length(c_temp, name, args.l, args.t)
        else:
            extract_length(c_temp, name, max_freq, args.t)
    elif args.t == "eq" or args.t == "all":
        print("--- creating a \"equal\" than file ---")
        if "--l" in sys.argv:
            extract_length(c_temp, name, args.l, args.t)
        else:
            extract_length(c_temp, name, max_freq, args.t)

    pass

#____________________________________________________________________________________________________
# main 
if __name__ == "__main__":
    print("\n-------------------- START of \"<pbd_length.py>\" script --------------------")
    # TODO: write your code here
    main()
    print("-------------------- END of \"<pbd_length.py>\" script --------------------\n")