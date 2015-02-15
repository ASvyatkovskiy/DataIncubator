#!/usr/bin/env python 

from ROOT import *
from array import array
import numpy as np

#read the ASCII files into the arrays
itable_cpp = open('cpp.txt').readlines()
cpp_list = [()]
cpp_dict = {}

itable_java = open('java.txt').readlines()
java_list = [()]
java_dict = {}

itable_python = open('python.txt').readlines()
python_list = [()]
python_dict = {}

icount = 0
for icpp in itable_cpp:
    cpp_list.append((icount,icpp.split(",")[0].lstrip(' '),icpp.split(",")[1].lstrip(" ").rstrip('\n')))
    cpp_dict[icpp.split(",")[0].lstrip(' ')] = icpp.split(",")[1].lstrip(" ").rstrip('\n')
    icount += 1

icount = 0
for ijava in itable_java:
    #cpp_list.append((icpp.split()[1],icpp.split()[3]))
    java_list.append((icount,ijava.split(",")[0].lstrip(' '),ijava.split(",")[1].lstrip(" ").rstrip('\n')))
    java_dict[ijava.split(",")[0].lstrip(' ')] = ijava.split(",")[1].lstrip(" ").rstrip('\n')
    icount += 1

icount = 0
for ipython in itable_python:
    #cpp_list.append((icpp.split()[1],icpp.split()[3]))
    python_list.append((icount,ipython.split(",")[0].lstrip(' '),ipython.split(",")[1].lstrip(" ").rstrip('\n')))
    python_dict[ipython.split(",")[0].lstrip(' ')] = ipython.split(",")[1].lstrip(" ").rstrip('\n')
    icount += 1

#cinvert to histograms
def FillHisto(list_tuples,h):
    i = 0
    for iline in range(1,len(list_tuples)):
        #print list_tuples[iline][2], " ", h.GetNbinsX()
        #h.Fill(i/2.,list_tuples[iline][2])
        h.SetBinContent(i+1,Double(list_tuples[iline][2])) 
        h.SetBinError(i+1,Double(0.))
        i = i+1

xAxis = [0,  1,  2,  3,  4,  5,  6,  7,  8,  9,  10,  11,  12,  13,  14,  15,  16,  17,  18,  19,  20,  21,  22,  23,  24,  25,  26,  27,  28,  29,  30,  31,  32,  33,  34,  35,  36,  37,  38,  39,  40,  41,  42,  43,  44,  45,  46,  47,  48,  49,  50,  51,  52,  53,  54,  55,  56,  57,  58,  59,  60,  61,  62,  63,  64,  65,  66,  67,  68,  69,  70,  71,  72,  73,  74,  75,  76,  77,  78,  79,  80,  81,  82,  83,  84,  85,  86,  87,  88,  89,  90,  91,  92,  93,  94,  95,  96,  97,  98,  99, 100]

h_id_rank_cpp = TH1D('h_id_rank_cpp','h_id_rank_cpp',100,array('d',xAxis))
h_id_rank_java = TH1D('h_id_rank_java','h_id_rank_java',100,array('d',xAxis))
h_id_rank_python = TH1D('h_id_rank_python','h_id_rank_python',100,array('d',xAxis))

#print len(cpp_list), " ", len(java_list), " ", len(python_list)
#print cpp_list
#print java_list

'''
FillHisto(cpp_list,h_id_rank_cpp)
FillHisto(java_list,h_id_rank_java)
FillHisto(python_list,h_id_rank_python)

c = TCanvas()
h_id_rank_cpp.SetLineColor(kRed)
h_id_rank_java.SetLineColor(kGreen)
h_id_rank_python.SetLineColor(kBlue)

h_id_rank_cpp.GetXaxis().SetTitle("Expert rank")
h_id_rank_cpp.GetYaxis().SetTitle("PageRank")

h_id_rank_cpp.Draw()
h_id_rank_java.Draw('same')
h_id_rank_python.Draw('same')

leg= TLegend(0.60,0.65,0.90,0.85)
leg.SetTextFont(72)
leg.SetTextSize(0.060)
leg.SetBorderSize(0)
leg.SetFillColor(0)
leg.AddEntry(h_id_rank_cpp,'C++','l')
leg.AddEntry(h_id_rank_java,'Java','l')
leg.AddEntry(h_id_rank_python,'Python','l')

leg.Draw('same')

c.SaveAs('test.png')
'''


corre_matrix = TH2D('corre_matrix','corre_matrix',3,0,3,3,0,3)

#find set intersections
#diagonal elements are 100% by construction
for i in range(3):
    corre_matrix.SetBinContent(i+1,i+1,1.)

set_user_id_python =  set()
set_user_id_java = set()
set_user_id_cpp = set()

for item in range(1,len(cpp_list)):
    set_user_id_cpp.add(cpp_list[item][1])  

for item in range(1,len(java_list)):
    set_user_id_java.add(java_list[item][1])

for item in range(1,len(python_list)):
    set_user_id_python.add(python_list[item][1])

#find set intersections
corr_mat_python_cpp = set_user_id_python.intersection(set_user_id_cpp)
corr_mat_java_cpp = set_user_id_java.intersection(set_user_id_cpp)
corr_mat_python_java = set_user_id_python.intersection(set_user_id_java)

#calculate net page ranks for users from intersections
python_python = 0.
cpp_cpp = 0.
java_java = 0.
python_java= 0.
java_python= 0.
cpp_java= 0.
java_cpp= 0.
python_cpp= 0.
cpp_python= 0.

for item in range(1,len(python_list)):
    python_python = python_python + float(python_list[item][2])

for item in range(1,len(cpp_list)):
    cpp_cpp = cpp_cpp + float(cpp_list[item][2])

for item in range(1,len(java_list)):
    java_java = java_java + float(java_list[item][2])

for element in corr_mat_python_cpp:
    python_cpp = python_cpp + float(cpp_dict[element])

cpp_python = python_cpp
cpp_python = cpp_python/python_python
python_cpp = python_cpp/cpp_cpp

corre_matrix.SetBinContent(1,3,cpp_python)
corre_matrix.SetBinContent(3,1,python_cpp)

for element in corr_mat_java_cpp:
    java_cpp = java_cpp + float(cpp_dict[element])

cpp_java = java_cpp
cpp_java = cpp_java/java_java
java_cpp = java_cpp/cpp_cpp

corre_matrix.SetBinContent(1,2,cpp_java)
corre_matrix.SetBinContent(2,1,java_cpp)

for element in corr_mat_python_java:
    python_java = python_java + float(java_dict[element])

java_python = python_java
java_python = java_python/python_python
python_java = python_java/java_java

corre_matrix.SetBinContent(2,3,java_python)
corre_matrix.SetBinContent(3,2,python_java)


c = TCanvas()
corre_matrix.GetXaxis().SetTitle("Prog. lang.")
corre_matrix.GetYaxis().SetTitle("Prog. lang.")

corre_matrix.Draw('COLZTEXT')
corre_matrix.SaveAs('test2.png')


f = TFile("out.root","recreate")
f.cd()
corre_matrix.Write('corre')
f.Close()
