#Original_value[addr]=A2;	Fix_or_Trim[addr]=00;	Trim_value[addr]=06;	Trim_mask[addr]=07;	Trim_shift[addr]=00;
#Original_value[addr] from DS table...now just keep the format use.
#Fix_or_Trim[addr] from RCN table...define the calculation method
#-------00 only trim----------- all io no trim label
#-------01 only DAC shift------ all io trim label
#-------20 DAC shift + trim---- some io trim label some not
#-------........................other conditions
#Trim_value[addr] parsing from RCN table, set value(HEX)
#Trim_mask[addr] parsing from RCN table, mask value(HEX)
#Trim_shift[addr] parsing from RCN table, shift value(DEC)
import pandas as pd 
import numpy as np
import os
import re

def trimmask(s):  #s list ['[7:6]','[5:3]','[0]']-->F9
    buff = []
    for i in s:
        if ':' in i:
            for j in range(int(i[-2]),int(i[1])+1):
                buff.append(j)
        else:
            buff.append(int(i[1]))
    IO = [0,0,0,0,0,0,0,0]
    for i in buff:
        IO[7-i] = 1
    IO = [str(i) for i in IO]
    #print(IO)
    IOByte = ''.join(IO)
    IOByte_hex = hex(int(IOByte,2))
    if len(IOByte_hex)==4:
        IOByte_hex = IOByte_hex[-2:].upper()
    else:
        IOByte_hex = '0'+IOByte_hex[-1].upper()
    return IOByte_hex
def trimvalue(s):    #s list ['01','02']-->03
    s = list(set(s))  #skip double define, may need highlight if addr double define(e.g. enable in device trim&disable in system trim) in RCN table.
    a = 0
    for i in s:
        a = a^int(i,16)
    a = hex(a)
    if len(a) == 4:
        a = a[-2:].upper()
    else:
        a = '0' + a[-1].upper()
    return a
def Addrformat(s):
    if len(s)>3:
        print('Find wrong addr format! {}--addr length>3, correct to length3'.format(s))
        return s[1:]
    else:
        return s
def DAC_value(s):  # 'Trim+8.DAC'-->+8
    s = str(s)
    if type(s)!=float:
        if 'Trim' in s:
            s = re.match('Trim(.*).DAC',s).group(1).strip()
            return s
        elif 'UROMDC' in s:
            print(s,'  find special trim rule, may need manually check')    #based on DC trim not userrom trim copy, need improve
            s = re.match('UROMDC(.*).DAC',s).group(1).strip()
            return s
        elif 'special' in s.strip().lower():
            print(s,'  find special trim rule, may need manually check')    #special rule, need improve
            return '00'
        else:
            return s

Original_value = {}
Fix_or_Trim = {}
Trim_value = {}
Trim_mask = {}
Trim_shift = {}

filepath = os.getcwd()+'\\trimtable'
DS_ver = input('please enter DS version, like D3,D4....:\n')
dscols = ['F','BQ','BU','BV']
dsheadername = ['IO','Addr','Trim','SET']
kgdcols = ['G','H','N']
kgdheadername = ['Addr (Hex)', 'IO', 'DAC (New)']
for i in os.listdir(filepath):
    if 'DS' in i:
#         if '512G' in i:
#             density = '512GB'
#         else:
#             density = '1024GB'
#         DS_Rev = re.match('.*ev.(.*?)-.*',i).group(1)
#         print(DS_Rev)
        DS_df = pd.read_excel(filepath+'\\'+i,sheet_name=1,header=None,skiprows=6,names=dsheadername,usecols=','.join(dscols))
    elif 'KGD' in i:
        if '512G' in i:
            density = '512GB'
        elif '256G'in i:
            density = '256G'
        else:
            density = '1024GB'
        if re.match('.*[rR][eE][vV](.*?)[_ ].*',i):
            KGD_Rev = re.match('.*[rR][eE][vV](.*?)[_ ].*',i).group(1).strip('0')
        print('Trim_Rev:   '+KGD_Rev+'\n')
        try:
            if 'ESSD' not in i.upper():
                KGD_df = pd.read_excel(filepath+'\\'+i,sheet_name=0,header=None,skiprows=3,names=['Incoming Para'], usecols='F')
            else:
                for ess_row in range(0,10):
                    for ess_col in ['E','F','G']:
                        KGD_df = pd.read_excel(filepath+'\\'+i,sheet_name=0,skiprows=ess_row, usecols=ess_col)
                    
                        if 'Incoming Para' in KGD_df.columns:
                            ess_skiprow = ess_row
                            ess_actcol = ess_col
                            break
                KGD_df = pd.read_excel(filepath+'\\'+i,sheet_name=0,header=None,names=['Incoming Para'],skiprows=ess_skiprow, usecols=ess_actcol)
        except:
            print('please remove restricted access from your RCN table!!!and make sure your RCN table closed\n')
            os.system('pause')
        if 'ESSD' in i.upper():
            DS_Rev = KGD_df['Incoming Para'].tolist()[1].split('\n')[1].split('_')[0]
        else:
            DS_Rev = KGD_df['Incoming Para'].tolist()[-1].split('_')[0]
        #print(DS_Rev)
        if re.match('Rev(.*?)',DS_Rev):
            DS_Rev = re.match('Rev(.*)',DS_Rev).group(1).strip('.')    #FORMAT 1.Revxxx.C_date  2.Revxxx.C
            #print(DS_Rev)
            if DS_Rev[-2]=='0':                                        #Revxxx0.C, want to remove '0'
                DS_Rev = DS_Rev[:-2]+DS_Rev[-1]
        #DS_Rev = DS_Rev[3:7]+DS_Rev[-1]
        print('DS_Rev:     '+DS_Rev+'\n')
        KGD_df = pd.read_excel(filepath+'\\'+i,sheet_name=1,header=None,skiprows=2,names=kgdheadername, usecols=','.join(kgdcols))
    else:
        print('please put 2 trimtables into trimtable folder!!!')
DS_df = DS_df[DS_df['Addr']>='010']         #filter start addr 10 trim
alltrim = {}
for i in DS_df.index:                    
    if DS_df['Addr'][i] not in alltrim:
        alltrim[DS_df['Addr'][i]] = []
        alltrim[DS_df['Addr'][i]].append(DS_df['SET'][i])
        alltrim[DS_df['Addr'][i]].append(DS_df['Trim'][i])
    else:
        alltrim[DS_df['Addr'][i]].append(DS_df['SET'][i])
        alltrim[DS_df['Addr'][i]].append(DS_df['Trim'][i])
        
for k,v in alltrim.items():      #judge Fix_or_Trim value
    if k not in Original_value:
        Original_value[k] = v[0].zfill(2)
        if 'TRIM' not in v:
            Fix_or_Trim[k] = '00'
        elif v.count('TRIM')-v.count(np.nan)<=0:
            Fix_or_Trim[k] = '20'
        elif v.count('TRIM')-v.count(np.nan)>0:
            Fix_or_Trim[k] = '01'      
        else:
            print(k,v)
            print('new')
            
KGD_df = KGD_df[~((KGD_df['DAC (New)']=='DS')|(KGD_df['DAC (New)']=='D/S')|(KGD_df['DAC (New)'].isnull())|(KGD_df['DAC (New)']=='UROMDC'))]
KGD_df['DAC (New)'] = KGD_df['DAC (New)'].apply(DAC_value)
KGD_df =KGD_df[KGD_df['Addr (Hex)']!=' '].astype(str)
KGD_df['Addr (Hex)'] = KGD_df['Addr (Hex)'].apply(Addrformat)
KGD_Addr = KGD_df['Addr (Hex)'].tolist()
for k in Fix_or_Trim.keys():
    Trim_shift[k] = '00'
    Trim_value[k] = []
for i in KGD_df.index:
    if '+' in KGD_df['DAC (New)'][i]:
        Trim_shift[KGD_df['Addr (Hex)'][i]] = KGD_df['DAC (New)'][i][1:].strip().zfill(2)
    elif '-' in KGD_df['DAC (New)'][i]:
        Trim_shift[KGD_df['Addr (Hex)'][i]] = KGD_df['DAC (New)'][i]
    else:
        Trim_value[KGD_df['Addr (Hex)'][i]].append(KGD_df['DAC (New)'][i])
for k in list(Trim_value.keys()):
    Trim_value[k] = trimvalue(Trim_value[k])
for k in Fix_or_Trim.keys():
    if k not in KGD_Addr and Fix_or_Trim[k]==20:
        Trim_value[k] = Original_value[k]
alltrim = {}
DS_df.fillna('NA',inplace=True)
DS_df = DS_df[~(DS_df['Trim']=='TRIM')]
for i in DS_df.index:                    #no only-trimshift addr in DS_df
    if Fix_or_Trim[DS_df['Addr'][i]]=='20' and DS_df['Addr'][i] not in alltrim:
        alltrim[DS_df['Addr'][i]] = []
        alltrim[DS_df['Addr'][i]].append(DS_df['IO'][i])
    elif Fix_or_Trim[DS_df['Addr'][i]]=='20':
        alltrim[DS_df['Addr'][i]].append(DS_df['IO'][i])

for i in KGD_df.index:
    if Fix_or_Trim[KGD_df['Addr (Hex)'][i]]=='20':
        alltrim[KGD_df['Addr (Hex)'][i]] = []
for i in KGD_df.index:
    if (KGD_df['Addr (Hex)'][i] not in alltrim) and ('+' not in KGD_df['DAC (New)'][i]) and ('-' not in KGD_df['DAC (New)'][i]):
        alltrim[KGD_df['Addr (Hex)'][i]] = []
        alltrim[KGD_df['Addr (Hex)'][i]].append(KGD_df['IO'][i])
    elif ('+' not in KGD_df['DAC (New)'][i]) and ('-' not in KGD_df['DAC (New)'][i]):
        alltrim[KGD_df['Addr (Hex)'][i]].append(KGD_df['IO'][i])
for k,v in Fix_or_Trim.items():
    if k not in alltrim.keys():
        Trim_mask[k] = '00'
    else:
        Trim_mask[k] = trimmask(alltrim[k])
for k,v in Trim_value.items():
    if Fix_or_Trim[k] == '20' and k not in KGD_Addr:
        Trim_value[k] = Original_value[k]
        Trim_mask[k] = '00'
    elif Fix_or_Trim[k] == '00' and k not in KGD_Addr:
        Trim_value[k] = '00'
filename = density + '_Trimtable_' + DS_Rev + '_To_'+KGD_Rev+'_'+DS_ver+'.txt'
with open(filename,'a+') as f:
    f.write('TRIMTABLE START\n')
    f.write('TRIMSTART '+density+'_'+DS_Rev+'_TO_'+KGD_Rev+'\n')
    for k in Original_value.keys():
        temp = ['Original_value['+k+']='+Original_value[k],'Fix_or_Trim['+k+']='+Fix_or_Trim[k],'Trim_value['+k+']='+Trim_value[k],'Trim_mask['+k+']='+Trim_mask[k],'Trim_shift['+k+']='+Trim_shift[k]]
        f.write(';\t'.join(temp))
        f.write(';\n')
    f.write('TRIMEND '+density+'_'+DS_Rev+'_TO_'+KGD_Rev+'_'+DS_ver+'\n')
    f.write('TRIMTABLE END\n')
print('Execute done!')
os.system('pause')
