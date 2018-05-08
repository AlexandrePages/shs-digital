# -*- coding: utf-8 -*-
"""
Spyder Editor

"""
import math

def clean_up_sen(a):
    a = a.replace("- ","")
    a = a.replace(":", " ")
    a = a.replace("\n", "")
    a = a.split(" ")
    return a


#def find_date(lines,DATE):  
#    for i in range(0,len(lines)):
#        for j in range(0,len(Jour)):
#            if Jour[j] in lines[i]:
#                linedate = re.split('\W+',lines[i])
#                for i in range(0,len(linedate)):
#                    for m in range(0,len(Mois)):
#                        if Jour[j] in linedate[i] and Mois[m] in linedate[i+2]:
#                            DATE = linedate[i] +' '+ linedate[i+1] + ' ' + Mois[m] + ' ' + linedate[i+3]
#     
#    return DATE

def find_date(fulltext,sen,index_text):
    DATE = 0
    #AnalyseDate = re.split('\W+',sen)
    AnalyseDate = sen
    for i in range(len(AnalyseDate)):
        if len(AnalyseDate[i]) == 4 and AnalyseDate[i].isdigit():
            DATE = AnalyseDate[i]
        else:
            for j in range(0,index_text):
                AnalyseDate2 = fulltext[j]
                for i in range(0,len(AnalyseDate2)):
                    if len(AnalyseDate2[i]) == 4 and AnalyseDate2[i].isdigit():
                        DATE = AnalyseDate2[i]
    if DATE == 0:
        DATE = 'None'            
    return DATE

def analyse_sen(sen,DateTab):
    TailleSen_= 0
    PaysFinal_ = ""
    for j in range(0,len(sen)):
            AnalyseSen = sen[j]
            AnalyseSen = clean_up_sen(AnalyseSen)
            AnalyseSen = re.split('\W+',sen[j])

            DateTab.append(find_date(sen,AnalyseSen,j)) #FIND DATE
            TailleSen_ += len(AnalyseSen) 
            AnalyseDate = re.split('\W+',sen[j])
#                if len(AnalyseDate[i]) == 4 and AnalyseDate[i].isdigit():
            #for i in range(0,len(AnalyseDate)):
 #                       DATEFinal_ = AnalyseDate[i]
            for i in range(0,len(AnalyseDate)):
                for j in range(0,len(Pays)):
                    if AnalyseDate[i] in Pays:
                            PaysFinal_ = AnalyseDate[i]
            for k in range(0,len(AnalyseSen)):
                SenFull.append(AnalyseSen[k])
    return TailleSen_, DateTab,PaysFinal_


def Occurence(sen,DateTab):
     #sort by occurence
    words = []
    wordsocc = []
    sen_tot_occ = []
    sen_sort = []
    Occ = 0
    for k in range(0,len(sen)):
        sen_sort += clean_up_sen(sen[k])
    #words.append(sen_sort[0])
    for i in range(0,len(sen_sort)):
        if sen_sort[i] not in words:
          words.append(sen_sort[i])
                
    for i in range(0,len(words)):
        Occ = 0
        for j in range(0,len(sen_sort)):
            if words[i] == sen_sort[j]:
                Occ += 1
        wordsocc.append(Occ)
    
    
    for i in range(0,len(sen)):
        sen_tot_occ.append(0)
        for j in range(0,len(words)):
            if words[j] in sen[i]:
                sen_tot_occ[i] += wordsocc[i]
            
    for i in range(0,len(sen)):
        sen_tot_occ[i] = sen_tot_occ[i]/len(sen[i])
            
    T = []
    T = [x for _,x in sorted(zip(sen_tot_occ,sen))]
    Tot_occ = sorted(sen_tot_occ)
    Date = []
    Date = [x for _,x in sorted(zip(sen_tot_occ,DateTab))]
    return T, Tot_occ,Date
    



def NameOccExp(Sen,Occ,Name,DateTab):
    for i in range(0,len(Sen)):
        AnalyseName = re.split('\W+',Sen[i])
        for j in range(0,len(AnalyseName)):
            if Name == AnalyseName[j]:
                Occ[i] -= 1
                index = i
                for k in range(0,len(Sen)):
                    if k != index:
                        Occ[k] -= math.exp(-abs(index-k))
    T = []
    T = [x for _,x in sorted(zip(Occ,Sen))]
    Tot_occ = sorted(Occ)
    Date = []
    Date = [x for _,x in sorted(zip(Occ,DateTab))]
    return T, Tot_occ,Date
            
#------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def clean_up(a):
    a = a.replace("- ","")
    a = a.replace("\n","")
    return a
#------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------
#------------------------------------------------------------------------------
Jour = ['LUNDI','MARDI', 'MERCREDI', 'JEUDI', 'VENDREDI', 'SAMEDI','DIMANCHE']
Mois = ['JANVIER', 'FEVRIER', 'MARS', 'AVRIL', 'MAI', 'JUIN','JUILLET', 'AOÛT','AOUT', 'SEPTEMBRE', 'OCTOBRE', 'NOVEMBRE', 'DECEMBRE']
Pays = [];

length_sen = []
sen = []
SenFull = []
TailleSen = 0
senTaille = []
AnalyseSen = []
NewSen = []
PaysFinal = ' '
TailleSen = 0
DATE = ""
DATEFinal = ''
Sorted_sen = []
Sorted_occ = []

import SentenceAnalyzer as SA


def Define_AbsOcc(NS,AO):
    Tense = []
    for i in range(0,len(NS)):
        Words = SA.sen_format(NS[i],SA.load_dico())
        for j in Words:
            AO.append(j.d[0].freqliv)
            Tense.append(j.d[0].cgram)
        if j.d[0].freqliv != 'None':
            AO[i] -= 1/(j.d[0].freqliv+1)
            if 'ADJ' in j.d[0].cgram:
                AO[i] -= 1
            if j.d[0].cgram == 'ADV':
                AO[i] -= 1
            if j.d[0].cgram == 'NOM':
                AO[i] -= 0.2
            if j.d[0].cgram == 'VER':
                AO[i] -= 2
    #        AbsOcc.append(Words.d[0].freqliv)
    #[1].d[0].freqliv)    
    for i in range(0,len(AO)):
        if AO[i] == 'None':
            AO[i] = 0
    T = []
    T = [x for _,x in sorted(zip(AO,NS))]
    AO = sorted(AO)    
    return T,AO


def find_evenement(Lines, Full, Name):
    DATE_JOURNAL = ''
    DateTab = []
    #DATE_JOURNAL = find_date(Full,DateTab)
    [TailleSen,DATE,PaysFinal] = analyse_sen(Lines,DateTab)
    [Sorted_sen, Sorted_occ,DateTab] = Occurence(Lines,DateTab)
    [Sorted_sen, Sorted_occ,DateTab] = NameOccExp(Sorted_sen,Sorted_occ,Name,DateTab)
    New_Sorted_sen = []
    for i in range(0,len(Sorted_sen)):
        New_Sorted_sen.append(clean_up(Sorted_sen[i]))
    if PaysFinal is None:
        PaysFinal = '_NONE_'
    if DATE_JOURNAL is None:
        DATE_JOURNAL = '_NONE_'
    
    NewSortedSen = []
    NewSortedOcc = []
    
    
    
    if len(New_Sorted_sen) >= 10:
        for i in range(0,9):
            NewSortedSen.append(New_Sorted_sen[i])
            NewSortedOcc.append(Sorted_occ[i])
    else:
        NewSortedSen = New_Sorted_sen
        NewSortedOcc = Sorted_occ
    
    
    
    [NewSortedSen,NewSortedOcc] = Define_AbsOcc(NewSortedSen,NewSortedOcc)
    
    
    TempTab = []
    FinalTab = []
    for i in range(0,len(NewSortedSen)):
        TempTab.append(DateTab[i])
        TempTab.append(PaysFinal)
        TempTab.append(NewSortedSen[i])
        TempTab.append(NewSortedOcc[i])
        FinalTab.append(TempTab)
        TempTab = []
    return FinalTab
        
import re

with open("pays.txt", 'r') as pays_file:
    Pays = pays_file.read()
    Pays = Pays.split('\n')



    
    
