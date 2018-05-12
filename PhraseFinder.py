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

def find_date(fulltext,sen,index_text,date_tab):
    DATE = 0
    found = 0
    #AnalyseDate = re.split('\W+',sen)
    AnalyseDate = sen
    for i in range(len(AnalyseDate)):
        if len(AnalyseDate[i]) == 4 and AnalyseDate[i].isdigit():
            DATE = AnalyseDate[i]
            found = 1
    if len(date_tab) != 0 and found == 0:
        DATE = date_tab[len(date_tab)-1]
        found = 0
        return DATE
    if DATE == 0 and found == 0:
        DATE = 'None'            
    return DATE


def find_pays(fulltext,sen,index_text,pays_tab):
    PAYS = 0
    found = 0
    #AnalyseDate = re.split('\W+',sen)
    AnalysePays = sen
    for i in range(len(AnalysePays)):
        if AnalysePays[i] in Pays:
            PAYS = AnalysePays[i]
            found = 1
    if len(pays_tab) != 0 and found == 0:
        PAYS = pays_tab[len(pays_tab)-1]
        found = 0
        return PAYS
    if PAYS == 0 and found == 0:
        PAYS = 'None'            
    return PAYS


def analyse_sen(sen,DateTab,PaysFinal_):
    TailleSen_= 0
    PaysFinal_ = []
    for j in range(0,len(sen)):
            AnalyseSen = sen[j]
            AnalyseSen = clean_up_sen(AnalyseSen)
            AnalyseSen = re.split('\W+',sen[j])
            PaysFinal_.append(find_pays(sen,AnalyseSen,j,PaysFinal_))
            DateTab.append(find_date(sen,AnalyseSen,j,DateTab)) #FIND DATE
            TailleSen_ += len(AnalyseSen) 
            AnalyseDate = re.split('\W+',sen[j])
#                if len(AnalyseDate[i]) == 4 and AnalyseDate[i].isdigit():
            #for i in range(0,len(AnalyseDate)):
 #                       DATEFinal_ = AnalyseDate[i]
            for k in range(0,len(AnalyseSen)):
                SenFull.append(AnalyseSen[k])
    return TailleSen_, DateTab,PaysFinal_


def Occurence(sen,DateTab,PaysTab):
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
    
    Date = []
    Date = [x for _,x in sorted(zip(sen_tot_occ,DateTab))]
    Pays = []
    Pays = [x for _,x in sorted(zip(sen_tot_occ,PaysTab))]
    Tot_occ = sorted(sen_tot_occ)
    return T, Tot_occ,Date,Pays
    



def NameOccExp(Sen,Occ,Name,DateTab,PaysTab):
    for i in range(0,len(Sen)):
        AnalyseName = re.split('\W+',Sen[i])
        for j in range(0,len(AnalyseName)):
            if Name == AnalyseName[j]:
                Occ[i] -= 10
                index = i
                for k in range(0,len(Sen)):
                    if k != index:
                        Occ[k] -= math.exp(-abs(index-k))
    T = []
    T = [x for _,x in sorted(zip(Occ,Sen))]
    Date = []
    Date = [x for _,x in sorted(zip(Occ,DateTab))]
    Pays = []
    Pays = [x for _,x in sorted(zip(Occ,PaysTab))]
    Tot_occ = sorted(Occ)
    return T, Tot_occ,Date,Pays
            
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
TailleSen = 0
PAYS = ""
DATE = ""
DATEFinal = ''
Sorted_sen = []
Sorted_occ = []

import SentenceAnalyzer as SA


def Define_AbsOcc(NS,AO,DT,PF):
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
    Date = []
    Date = [x for _,x in sorted(zip(AO,DT))]
    Pays = []
    Pays = [x for _,x in sorted(zip(AO,PF))]
    AO = sorted(AO)    
    return T,AO,Date,Pays


def find_evenement(Lines, Full, Name):
    DateTab = []
    PaysFinal = []
    #DATE_JOURNAL = find_date(Full,DateTab)
    [TailleSen,DATE,PaysFinal] = analyse_sen(Lines,DateTab,PaysFinal)
    [Sorted_sen, Sorted_occ,DateTab,PaysFinal] = Occurence(Lines,DateTab,PaysFinal)
    [Sorted_sen, Sorted_occ,DateTab,PaysFinal] = NameOccExp(Sorted_sen,Sorted_occ,Name,DateTab,PaysFinal)
    New_Sorted_sen = []
    for i in range(0,len(Sorted_sen)):
        New_Sorted_sen.append(clean_up(Sorted_sen[i]))
    
    NewSortedSen = []
    NewSortedOcc = []
    
    
    
    if len(New_Sorted_sen) >= 10:
        for i in range(0,9):
            NewSortedSen.append(New_Sorted_sen[i])
            NewSortedOcc.append(Sorted_occ[i])
    else:
        NewSortedSen = New_Sorted_sen
        NewSortedOcc = Sorted_occ
    
    
    
    [NewSortedSen,NewSortedOcc,DateTab,PaysFinal] = Define_AbsOcc(NewSortedSen,NewSortedOcc,DateTab,PaysFinal)
    
    
    TempTab = []
    FinalTab = []
    for i in range(0,len(NewSortedSen)):
        TempTab.append(DateTab[i])
        TempTab.append(PaysFinal[i])
        TempTab.append(NewSortedSen[i])
        TempTab.append(NewSortedOcc[i])
        FinalTab.append(TempTab)
        TempTab = []
    return FinalTab
        
import re

with open("pays.txt", 'r') as pays_file:
    Pays = pays_file.read()
    Pays = Pays.split('\n')



    
    
