#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
import os
import time

import sys
sys.setrecursionlimit(10000000) #设置递归限制为一千万

#该文件使用说明
#1、请修改16行和17行文件输入输出位置Location(默认输入、输出位置在本文件所在文件夹)
#2、按照要求选择输出那种变异算子的变异体
#3、如果程序崩溃请将df函数中的延迟注释取消
4
#Please modify the location of the file-------------------------------------------------------------------------Location
infilename = './test.c'
outfilename = './'

infilenameinput = raw_input("Please enter the location of the test file.The default location is\' ./test.c \' :\n")
if infilenameinput != "":
    infilename = infilenameinput

outfilenameinput = raw_input("Please enter the location of the output.The default location is\' ./ \' :\n")
if outfilenameinput != "":
    outfilename = outfilenameinput

#Clear Note Start----------------------------------------------------------------------------------------------ClearNote
def clearNote():
    fp = open(infilename, "r")
    flag = 0
    quote = 0
    re = ""
    for line in fp:
        myline = ""
        length = len(line)
        for index in range(length):
            if flag == 0 and quote == 0 and line[index] == "\"":
                quote = 1
                myline += line[index]
                continue
            if flag == 0 and quote == 1 and line[index] == "\"":
                quote = 0
                myline += line[index]
                continue
            if quote != 1 and flag == 2 and line[index] == "\n":
                flag = 0
            if quote != 1 and flag == 0 and line[index] == "/" and line[index + 1] == "*":
                flag = 1
            if quote != 1 and index > 0 and flag == 1 and line[index - 1] == "/" and line[index - 2] == "*":
                flag = 0
            if quote != 1 and flag == 0 and line[index] == "/" and line[index + 1] == "/":
                flag = 2
            if flag == 1 or flag == 2:
                continue
            myline += line[index]
        re += myline
    fp.close()
    with open(infilename, 'w') as f:
        f.write(re)
    pass
clearNote()
#Clear Note End---------------------------------------------------------------------------------------------------------

#Construct Mutant Operator Classes-----------------------------------------------------------------------OperatorClasses
#Absolute Value Insertion----------------------------------------ABS
abs = ["abs(","("]
pattern_abs = re.compile(r' abs\(')
#Arithmetic Operator Replacement---------------------------------AOR
aor = [" + ", " - ", " * "," / "," % "]
pattern_aor = re.compile(r' \+ | \- | \* | \% | / ')
#Logical Connector Replacement-----------------------------------LCR
lcr = [" && ", " || "]
pattern_lcr = re.compile(r' && | \|\| ')
#Relational Operator Replacement---------------------------------ROR
ror = [" <= "," >= "," == "," != "," > "," < "]
pattern_ror = re.compile(r' <= | >= | < | > | == | != ')
#Unary Operator Insertion----------------------------------------UOI
uoi = ["++","--"]
pattern_uoi = re.compile(r'\+\+|\-\-')
#Construct Mutant Operator Classes--------------------------------------------------------------------------------------

# Read File Contents--------------------------------------------------------------------------------------------readFile
print("loading file \" "+ infilename +" \".....................................................")
with open(infilename) as f:
    contents = f.read()
    time.sleep(1)
# Read File Contents----------------------------------------------------------------------------------------------------

#mkdir-------------------------------------------------------------------------------------------------------------mkdir
filename = ["AOR","LCR","ROR","UOI","ABS"]
def mkdir(path):
    path = path.strip()

    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False
print ("mkdir " + outfilename + "ABS /AOR /LCR /ROR /UOI successed......................................")
for indexfilename in range(0,len(filename)):
    mkdir(outfilename+filename[indexfilename])
#mkdir------------------------------------------------------------------------------------------------------------------


aor_rt = re.split(pattern_aor,contents)
print ("The number of AOR Mutant Operator: " + str(len(aor_rt) -1) + " ; " + "The number of files can be produced: 5^" + str(len(aor_rt) - 1))#, " + "变异算子为分别为:" + str(pattern_aor.findall(contents)))

lcr_rt = re.split(pattern_lcr,contents)
print ("The number of LCR Mutant Operator: " + str(len(lcr_rt) -1) + " ; " + "The number of files can be produced: 2^" + str(len(lcr_rt) - 1))#, " + "变异算子为分别为:" + str(pattern_lcr.findall(contents)))

ror_rt = re.split(pattern_ror,contents)
print ("The number of ROR Mutant Operator: " + str(len(ror_rt) -1) + " ; " + "The number of files can be produced: 6^" + str(len(ror_rt) - 1))#, " + "变异算子为分别为:" + str(pattern_ror.findall(contents)))

uoi_rt = re.split(pattern_uoi,contents)
print ("The number of UOI Mutant Operator: " + str(len(uoi_rt) -1) + " ; " + "The number of files can be produced: 2^" + str(len(uoi_rt) - 1))#, " + "变异算子为分别为:" + str(pattern_uoi.findall(contents)))

abs_rt = re.split(pattern_abs,contents)
print ("The number of ABS Mutant Operator: " + str(len(abs_rt) -1) + " ; " + "The number of files can be produced: 2^" + str(len(abs_rt) - 1))#, " + "变异算子为分别为:" + str(pattern_abs.findall(contents)))


# 构造操作字符串数组
global result
result = []
def constructResult(rt):
    for index in range(0, len(rt)):
        result.append(rt[index])
        result.append(" ")
    pass

global cont
cont = 0
def printme(param,i):
    global cont
    cont += 1
    print ("Start creating the" + str(cont) + "file.............................")
    with open(outfilename + "/" + filename[i] + "/" + str(cont) + '.c', 'w') as f:
        f.write(param)

    return cont

stri = raw_input("AOR input 0;\t   LCR input 1;\t   ROR input 2;\t   UOI input 3;\t   ABS input 4\t\nPlease input: \n")

global maxTime
maxTime= raw_input("Please input the maxTime of output files :  ")

def df(param,r,i):
    global endtime1
    endtime1 = int(round(time.time()*1000))

    if int(maxTime) <= int(endtime1 - starttime):
        return

    if param >= len(result) - 1:
        fileResult = "".join(result)
        printme(fileResult,i)
        # time.sleep(1)
        return

    for index2 in range(0, len(r)):
        result[param] = r[index2]
        df(param + 2, r, i)

if stri == "0":
    starttime = int(round(time.time()*1000))
    constructResult(aor_rt)
    df(1, aor, 0)
    endtime = int(round(time.time()*1000))
if stri == "1":
    starttime = int(round(time.time()*1000))
    constructResult(lcr_rt)
    df(1, lcr, 1)
    endtime = int(round(time.time()*1000))
if stri == "2":
    starttime = int(round(time.time()*1000))
    constructResult(ror_rt)
    df(1, ror, 2)
    endtime = int(round(time.time()*1000))
if stri == "3":
    starttime = int(round(time.time()*1000))
    constructResult(uoi_rt)
    df(1, uoi, 3)
    endtime = int(round(time.time()*1000))
if stri == "4":
    starttime = int(round(time.time()*1000))
    constructResult(abs_rt)
    df(1, abs, 4)
    endtime = int(round(time.time()*1000))


print(str(cont)+"files have been created.  "+"Spend time "+ str(endtime1-starttime) +" ms")
end = raw_input("end")