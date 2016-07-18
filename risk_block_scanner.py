#!/usr/bin/env python
#coding=utf-8

#---------------------------------------------
#         Name: blockScanner.py
#       Author: Xing Chen
#         Date: 2016-07-15
#  Description:	blockScanner is a text Scanner
#  which could detect simple circular reference 
#  Support Object-C only now.
#----------------------------------------------

import re
import os
import sys
import fileinput

weak_regex=ur"(\@weakify\(.*\)|\_\_weak(.*)typeof\(self\))"
block_regex=ur"(self\..*\=\s?\^|\[self.*\^)\(.*\).*\{?"
func_regex=ur"(\-|\+)\s?\(.*\).*(\:\s?\(.*\).*)?{?"
singleton_regex=ur"(\+\s?\(.*\)\s?shared.*{?|.*SINGLETON\_FOR\_CLASS\(.*\))"

show_detail=0
show_more=0
show_singleton=0

def scan_files(directory,prefix=None,postfix=None):  
    files_list=[]  
      
    for root, sub_dirs, files in os.walk(directory):  
        for special_file in files:  
            if postfix:  
                if special_file.endswith(postfix):  
                    files_list.append(os.path.join(root,special_file))  
            elif prefix:  
                if special_file.startswith(prefix):  
                    files_list.append(os.path.join(root,special_file))  
            else:  
                files_list.append(os.path.join(root,special_file))  
                            
    return files_list 

def left_bracket_count(line):
    count=0
    for word in line:
        if word=="{":
            count=count+1
        elif word=="}":
            count=count-1

    return count;

def detect_block(file_path):

    global show_detail
    global show_singleton


    line_count=1
    
    block_arr=[] 
    weak_arr=[] 
    func_arr=[]
    potential_arr=[]
    cycref_set=set()
    safe_set=set()

    cycref_map={}
    bracket_map={}
    is_singleton=0

    for line in fileinput.input(file_path):
        # comments code is invalid
        # object-c comments is startswith "//"
        if not line.strip().startswith("//"):
            if re.findall(weak_regex, line):
                weak_arr.append(line_count)
            elif re.findall(func_regex, line):
                func_arr.append(line_count)
            elif re.findall(block_regex, line):
                block_arr.append(line_count);
                potential_arr.append(line_count);

                bracket_map[line_count] = left_bracket_count(line);
                cycref_map[line_count] = 0;

            if re.findall(singleton_regex, line):
                is_singleton=1

            for potential_lc in potential_arr:
                if potential_lc==line_count:
                    continue

                if cycref_map[potential_lc]==0:
                    if re.findall(ur"(\[self\s|self\.)", line):
                        cycref_map[potential_lc]=1

                bracket_map[potential_lc]=bracket_map[potential_lc]+left_bracket_count(line)
                if bracket_map[potential_lc]<=0:
                    if cycref_map[potential_lc]==1:
                        cycref_set.add(potential_lc)
                    else:
                        safe_set.add(potential_lc)
                    break

                # if file_name(file_path)=="SDDJOperationCellTimesMode.m":
                #     print bracket_map[potential_lc]

            # remove potential_arr if it's not cycle reference
            potential_arr = list(set(potential_arr).difference(cycref_set))
            potential_arr = list(set(potential_arr).difference(safe_set))

        line_count=line_count+1
    pass

    #weak_arr detect
    weakified_set=set()

    # last line for last function
    func_arr.append(line_count) 
    for i in range(0, len(func_arr)-1):
        fst_line=func_arr[i]
        sec_line=func_arr[i+1]

        for cr_line in list(cycref_set):
            if cr_line > fst_line and cr_line < sec_line:
                for weak_line in weak_arr:
                    if weak_line > fst_line and weak_line < cr_line:
                        weakified_set.add(cr_line)

    #except for block which weak before perform
    unsafe_arr=list(cycref_set.difference(weakified_set))
    if show_singleton==0 and is_singleton==1:
        unsafe_arr=[]

    if show_detail==1:
        show_detail_info(file_path, unsafe_arr, block_arr, list(cycref_set), list(weakified_set))

    return unsafe_arr

def show_detail_info(file_path, unsafe_arr, block_arr, cycref_arr, weakified_arr):
    global show_more

    cycref_arr.sort()
    weakified_arr.sort()
    unsafe_arr.sort()

    arr_len = len(unsafe_arr)
    if show_more:
        arr_len = len(block_arr)

    if arr_len:
        print file_name(file_path)
        print "All  Block Lines: %s" % block_arr
        print "Self-Block Lines: %s" % cycref_arr
        print "Weak-Block Lines: %s" % weakified_arr
        print "Risk-Block Lines: %s" % unsafe_arr

def file_name(file_path):
    name_arr=file_path.split("/")
    file_name=name_arr[len(name_arr) - 1]
    return file_name

def main():
    # Accoring to Argv as a Scanner Target root path
    root_path=sys.argv[1]

    global show_detail
    global show_more
    global show_singleton
    for arg in sys.argv:
        if arg=="--detail":
            show_detail=1
        elif arg=="--more":
            show_more=1
        elif arg=="--show-singleton":
            show_singleton=1

    total_file_count=0
    total_risk_block_count=0

    for file_path in scan_files(root_path, None, ".m"):
        risk_arr=detect_block(file_path)
        risk_arr_len = len(risk_arr)
        if risk_arr_len:
            total_file_count=total_file_count+1
            total_risk_block_count=total_risk_block_count+risk_arr_len

            if not show_detail:
                print "%s --> %s" % (file_name(file_path), risk_arr)

    print "\nTotal Risk File Count: %d, Total Risk Line Count: %s" % (total_file_count, total_risk_block_count)

main()
