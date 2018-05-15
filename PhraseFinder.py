# -*- coding: utf-8 -*-
"""
Spyder Editor
"""
import math
import re
import SentenceAnalyzer as SA
Pays = []
Capi = []
with open("pays.txt", 'r') as pays_file:
    Pays = pays_file.read()
    Pays = Pays.split('\n')
    
with open("Capitales.txt", 'r') as Capi_file:
    Capi = Capi_file.read()
    Capi = Capi.split('\n')
    
Jour = ['LUNDI','MARDI', 'MERCREDI', 'JEUDI', 'VENDREDI', 'SAMEDI','DIMANCHE']
Mois = ['janvier','février','fevrier','mars','avril','mai','juin','juillet','août','aout','septembre','octobre','novembre','décembre','decembre']


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


def clean_up_sen(a):
    a = a.replace("- ","")
    a = a.replace(":", " ")
    a = a.replace("\n", "")
    a = a.split(" ")
    return a

#------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------
#------------------------------------------------------------------------------



def find_date(fulltext,sen,index_text,date_tab):
    DATE = ''
    DateTab = ['None','None','None']
    found = 0
    AnalyseDate = sen
    for i in range(len(AnalyseDate)):
        if len(AnalyseDate[i]) == 4 and AnalyseDate[i].isdigit():
            DateTab[2] = str(AnalyseDate[i])
            found = 1
        if found == 1:
            for j in range(len(Mois)):
                if AnalyseDate[i].lower() == Mois[j]:
                    if j <2 :
                        DateTab[1] = '0' + str(j+1)
                    if j >= 2 and j <= 8:
                        DateTab[1] = '0' + str(j)
                    if j == 9:
                        DateTab[1] = '0' + str(j-1)
                    if j >= 10:
                        DateTab[1] = str(j-1)
                    if j == 14:
                        DateTab[1] = str(j-2)
                    found = 1
            if (len(AnalyseDate[i]) <= 2 and len(AnalyseDate[i]) > 0) and AnalyseDate[i].isdigit() and i < len(AnalyseDate)-1:
                if AnalyseDate[i+1].lower() in Mois:
                    DateTab[0] = str(AnalyseDate[i])
                    found = 1  
    if len(date_tab) != 0 and found == 0:
        DATE = date_tab[len(date_tab)-1]
        found = 0
        return DATE   
        
    DATE = DateTab[2] + '/' +   DateTab[1]  + '/' +    DateTab[0]
    return DATE

#------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------
#------------------------------------------------------------------------------


def find_pays(fulltext,sen,index_text,pays_tab):
    PAYS = 'None'
    CAP = 'None'
    found = 0
    AnalysePays = sen
    for i in range(len(AnalysePays)):
        if AnalysePays[i] in Pays:
            PAYS = AnalysePays[i]
            found = 1
    for i in range(len(AnalysePays)):
        if AnalysePays[i] in Capi:
            CAP = AnalysePays[i]
            found = 1        
    if len(pays_tab) != 0 and found == 0:
        PAYS = pays_tab[len(pays_tab)-1]
        found = 0
        return PAYS
    if CAP != 'None':
        PAYS = CAP
              
    return PAYS

#------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------
#------------------------------------------------------------------------------



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

            for k in range(0,len(AnalyseSen)):
                SenFull.append(AnalyseSen[k])
    return  DateTab,PaysFinal_


#------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------
#------------------------------------------------------------------------------


def Occurence(sen):
     #sort by occurence
    words = []
    wordsocc = []
    sen_tot_occ = []
    sen_sort = []
    Occ = 0
    for k in range(0,len(sen)):
        sen_sort += clean_up_sen(sen[k])
    for i in range(0,len(sen_sort)):
        if sen_sort[i] not in words:
          words.append(sen_sort[i])
                
    for i in range(0,len(words)):
        Occ = 0
        for j in range(0,len(sen_sort)):
            if words[i] == sen_sort[j]:
                Occ += 0.0001
        wordsocc.append(Occ)
    
    
    for i in range(0,len(sen)):
        sen_tot_occ.append(0)
        for j in range(0,len(words)):
            if words[j] in sen[i]:
                sen_tot_occ[i] -= wordsocc[j]
            
    for i in range(0,len(sen)):
        sen_tot_occ[i] = sen_tot_occ[i]/len(sen[i])
 
    return sen,sen_tot_occ
    

#------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------
#------------------------------------------------------------------------------



def NameOccExp(Sen,Occ,Name):
    for i in range(0,len(Sen)):
            if Name in Sen[i]:
                Occ[i] -= 2
                index = i
                for k in range(0,len(Sen)):
                    if k != index:
                        Occ[k] -= math.exp(-abs(index-k))

    return Occ
            
#------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------
#------------------------------------------------------------------------------



def clean_up(a):
    a = a.replace("- ","")
    a = a.replace("\n","")
    return a

#------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------
#------------------------------------------------------------------------------





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
                AO[i] -= 0.1
            if j.d[0].cgram == 'ADV':
                AO[i] -= 0.1
            if j.d[0].cgram == 'NOM':
                AO[i] -= 0.2
            if j.d[0].cgram == 'VER':
                AO[i] -= 2
    for i in range(0,len(AO)):
        if AO[i] == 'None':
            AO[i] = 0

    return AO

#------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------
#------------------------------------------------------------------------------



def find_evenement(Lines, Full, Name):
    DateTab = []
    PaysFinal = []
    [DATE,PaysFinal] = analyse_sen(Lines,DateTab,PaysFinal)
    [Sorted_sen, Sorted_occ] = Occurence(Lines)
    Sorted_occ = NameOccExp(Sorted_sen,Sorted_occ,Name)
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
    
    
    
    NewSortedOcc = Define_AbsOcc(NewSortedSen,NewSortedOcc)
    
    
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
