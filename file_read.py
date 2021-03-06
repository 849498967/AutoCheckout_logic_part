from os import listdir as os_listdir
from re import match as re_match
import mt_per_die
import trim
import llt_per_die
from easygui import msgbox
import re


class FileReadClass:
    """
    File read class
    """

    def __init__(self, path):
        self.mt_datalog_file_in = None
        self.llt_datalog_file_in = None
        self.trim_datalog_file_in = None
        self.mt_datalog_file_match = False
        self.llt_file_match = False
        self.trim_file_match = False
        self.mt_datalog_list = []
        self.mt_class_list = []
        self.trim_version_list = []
        self.trim_class = None
        self.trim_class_list = []
        self.llt_class_list = []
        self.llt_class_die0 = None
        self.folder_name = path.split('/')[1]
        # Jason: add product read
        self.product = None
        self.product_match = None
        self.mrph_ver = ""
        self.tracker_ver = ""
        self.id_7 = ""
        self.id_8 = ""

        # jason add llt file name for mrph use
        self.nnt_file_name = None

        for filename in os_listdir(path):
            file_in = open(path + filename, 'r', encoding='utf8', errors='ignore')
            file_loop = file_in
            for file_line in file_loop:
                if re_match(r'FLOWDESCRIPTIONSTART', file_line):
                    self.mt_datalog_file_match = True
                    # file close and open again for BiCS4 to grap "max_chips_per_bank = 3" data
                    file_in.close()
                    file_in = open(path + filename, 'r', encoding='utf8', errors='ignore')
                    # end

                    self.mt_datalog_file_in = file_in
                    break
                if re_match(r'.*T5851 UFS Swift Pro PROGRAM.*', file_line):
                    self.mt_datalog_file_match = True
                    # file close and open again for BiCS4 to grap "max_chips_per_bank = 3" data
                    file_in.close()
                    file_in = open(path + filename, 'r', encoding='utf8', errors='ignore')
                    # end

                    self.mt_datalog_file_in = file_in
                    break     
                if re_match(r'LLTSCRIPT START', file_line):
                    self.llt_file_match = True
                    self.nnt_file_name = path + filename
                    nnt_contents = file_in.read()
                    # jason: match the product name once find the nnt datalog
                    self.product = re.findall(r'PRODUCT TYPE IS: (.*?)\n', nnt_contents)[0]
                    print(self.product)
                    file_in.close()
                    file_in = open(path + filename, 'r', encoding='utf8', errors='ignore')
                    self.llt_datalog_file_in = file_in
                    break
                if re_match(r'TRIMTABLE START', file_line):
                    self.trim_file_match = True
                    self.trim_datalog_file_in = file_in
                    break

                if re_match(r'MRPH VER: (.*?)\n', file_line):
                    self.mrph_ver = re_match(r'MRPH VER: (.*?)\n', file_line).group(1)
                    print("mrph read from config:", self.mrph_ver)

                if re_match(r'MT TRACKER VER: (.*?)\n', file_line):
                    self.tracker_ver = re_match(r'MT TRACKER VER: (.*?)\n', file_line).group(1)
                    print("tracker ver read from config:", self.tracker_ver)

                if re_match(r'ID7: (.*?)\n', file_line):
                    self.id_7 = re_match(r'ID7: (.*?)\n', file_line).group(1)
                    print("id7 read from config:", self.id_7)

                if re_match(r'ID8: (.*?)\n', file_line):
                    self.id_8 = re_match(r'ID8: (.*?)\n', file_line).group(1)
                    print("id8 read from config:", self.id_8)

                #if re_match(r'ID6: (.*?)\n', file_line):
                    #self.id_6 = re_match(r'ID6: (.*?)\n', file_line).group(1)
                    #print("id6 read from config:", self.id_6)



    def read_mt_datalog(self):
        # Skip if datalog is not exist and print error in excel
        if self.mt_datalog_file_match & self.llt_file_match:
            mt_datalog_number = 0
            under_mt = False
            max_chips_per_bank = 0
            program_name = None
            program_rev = None
            program_tech = None
            program_design = None
            program_die = None
            file_name = None
            current_mt_class = None
            for mt_line in self.mt_datalog_file_in:
                # max_chips_per_bank/program name/rev/technology/design input/flow
                actualflowname_match = re_match(r'Flow:(.*)', mt_line)
                if actualflowname_match:
                    actualflowname = actualflowname_match.group(1).strip()
                actualflowname_match1 = re_match(r'FOLDERNAME (.*)', mt_line)
                if actualflowname_match1:
                    actualflowname = actualflowname_match1.group(1).split('_')[-1].strip()
                max_chips_per_bank_match = re_match(r'max_chips_per_bank = (.*)', mt_line)
                if max_chips_per_bank_match:
                    max_chips_per_bank = max_chips_per_bank_match.group(1)
                max_chips_per_bank_match2 = re_match(r'MAX_CHIPS_PER_BANK = (.*)', mt_line)
                if max_chips_per_bank_match2:
                    max_chips_per_bank = max_chips_per_bank_match2.group(1)
                max_chips_per_bank_match3 = re_match(r'Die Count: (.*)', mt_line)
                if max_chips_per_bank_match3:
                    program_die = max_chips_per_bank_match3.group(1)
                    max_chips_per_bank = str(int(max_chips_per_bank_match3.group(1))//2)
                    program_tech = 'BICS4p5'
                    # program_design = 'iNAND_BiCs4p5_512G_2P'
                # print(max_chips_per_bank)
                # print(program_die)
                program_name_match = re_match(r'PROGRAMNAME (.*)', mt_line)
                if program_name_match:
                    program_name = program_name_match.group(1)
                program_name_match = re_match(r'ECOTS_SD_CST_FILE: /home/fsdiag/Whale/testfiles/(.*)', mt_line)
                if program_name_match:
                    program_name = program_name_match.group(1)    
                # print(program_name)
                program_rev_match = re_match(r'Product Name Changed to {3}= (.*)', mt_line)
                if program_rev_match:
                    program_rev = program_rev_match.group(1)
                program_rev_match = re_match(r'Product: (.*)', mt_line)                            #iNand use the CDT tp name to classify the Cap&Generation  iNAND_BiCs4p5_512G_2P
                if program_rev_match:
                    if program_rev_match.group(1).split('_')[0][2] == 'E' and program_rev_match.group(1).split('_')[0][-3] == 'I' and program_rev_match.group(1).split('_')[0][3:5] == '12':
                        program_rev = 'iNAND_BiCs4p5_512G_2P'
                        program_design = 'iNAND_BiCs4p5_512G_2P'
                    elif program_rev_match.group(1).split('_')[0][2] == 'E' and program_rev_match.group(1).split('_')[0][-3] == 'I' and program_rev_match.group(1).split('_')[0][3:5] == '56':
                        program_rev = 'iNAND_BiCs4p5_256G_2P'
                        program_design = 'iNAND_BiCs4p5_256G_2P'
                    else:
                        pass
                # if program_rev_match:
                #     program_rev = program_rev_match.group(1)
                #     program_design = program_rev_match.group(1)
                    # print(program_design)
                # print(program_rev)
                program_tech_match = re_match(r'TECHNOLOGY (.*)', mt_line)
                if program_tech_match:
                    program_tech = program_tech_match.group(1)
                # program_tech_match = re_match(r'Die type: (.*)', mt_line)
                # if program_tech_match:
                #     program_tech = program_tech_match.group(1)
                #     program_design = program_tech_match.group(1)
                # # print(program_tech)
                # print(program_design)
                program_design_match = re_match(r'DESIGN (.*)', mt_line)
                if program_design_match:
                    program_design = program_design_match.group(1)
                program_die_match = re_match(r'NANDCONFIGDIE ([0-9]*).*', mt_line)
                if program_die_match:
                    program_die = program_die_match.group(1)
                file_name_match = re_match(r'FILE NAME (.*)\.xml', mt_line)
                if file_name_match:
                    file_name = file_name_match.group(1)
                file_name_match = re_match(r'Load Recipe:/home/fsdiag/download/tspr7/src/../recipe/(.*)\.xml', mt_line)
                if file_name_match:
                    file_name = file_name_match.group(1)
                # print(file_name)
                if re_match(r'.*FLOWDESCRIPTIONSTART.*', mt_line):
                    under_mt = True
                    mt_file_number = self.mt_datalog_file_in.name + str(mt_datalog_number)
                    self.mt_datalog_list.append(mt_file_number)
                    current_mt_class = mt_per_die.MTPerDieClass(mt_file_number, program_name, program_rev,
                                                                program_tech, program_design, program_die,
                                                                max_chips_per_bank, file_name,actualflowname)
                    self.mt_class_list.append(current_mt_class)
                    mt_datalog_number += 1
                # if re_match(r'Start Test: tb_cdtTest .*', mt_line):
                if re_match(r'TestNum_30 Print_Datalog_LDPC__nvcc', mt_line):
                    under_mt = True
                    mt_file_number = self.mt_datalog_file_in.name + str(mt_datalog_number)
                    self.mt_datalog_list.append(mt_file_number)
                    current_mt_class = mt_per_die.MTPerDieClass(mt_file_number, program_name, program_rev,
                                                                program_tech, program_design, program_die,
                                                                max_chips_per_bank, file_name,actualflowname)
                    self.mt_class_list.append(current_mt_class)
                    mt_datalog_number += 1
                if re_match(r'.*Test End Action.*', mt_line):
                    under_mt = False
                # if re_match(r'.*Test Time (tb_cdtTest).*', mt_line):
                if re_match(r'END_OF_FLOW (S9)', mt_line):
                    under_mt = False
                if under_mt:
                    current_mt_class.mt_line_input(mt_line)

    # jason: read the parsed trim txt file
    def read_trim_table(self):
        for trim_line in self.trim_datalog_file_in:
            # modify because B4 no B!
            revision_check_start = re_match(r'TRIMSTART (.*G[B]{0,1}_.[.].*?_TO_.*[.].*)', trim_line)
            # print(revision_check_start.group(1))
            if revision_check_start:
                trim_version_in_table = revision_check_start.group(1)
                # print(trim_version_in_table)
                self.trim_version_list.append(trim_version_in_table)
                self.trim_class = trim.TrimTable(trim_version_in_table)  # trim.name
                self.trim_class_list.append(self.trim_class)
            trim_data = re_match(r'Original_value\[(.{2,3})]=(.*);\t'  # 2 matches here: addr, value
                                 r'Fix_or_Trim\[.{2,3}]=(.*);\t'
                                 r'Trim_value\[.{2,3}]=(.*);\t'
                                 r'Trim_mask\[.{2,3}]=(.*);\t'
                                 r'Trim_shift\[.{2,3}]=(.*);', trim_line)
            if trim_data:
                # === debug ===
                # print(trim_data.group(1), trim_data.group(2), trim_data.group(3), trim_data.group(4),
                # trim_data.group(5), trim_data.group(6))
                # jason: add another param: product, hard code here css for debugging
                self.trim_class.trim_input('0x' + trim_data.group(1), '0x' + trim_data.group(2), trim_data.group(3),
                                           '0x' + trim_data.group(4), '0x' + trim_data.group(5), trim_data.group(6),
                                           self.mt_class_list, self.product)  # mt_class_list is info read from mt datalog

    def read_llt_datalog(self):
        # Skip if datalog is not exist and print error in excel
        # print(self.mt_class_list[1].uid_return_dmy)
        current_llt_die_class = None
        if self.mt_datalog_file_match & self.llt_file_match:
            for i, llt_line in enumerate(self.llt_datalog_file_in):
                # print(i, llt_line)
                # TESTSTART DIE, DIE to class
                llt_die_start = re_match(r'TESTSTART (DIE (.*))', llt_line)
                if llt_die_start:
                    llt_die_start_die_num = llt_die_start.group(1)
                    # print(self.product)
                    current_llt_die_class = llt_per_die.LltPerDieClass(llt_die_start_die_num,
                                                                       self.mt_class_list, self.trim_class_list,
                                                                       self.product, file_path=self.nnt_file_name,
                                                                       id7=self.id_7, id8=self.id_8,
                                                                       mrph_ver=self.mrph_ver,
                                                                       tracker_ver=self.tracker_ver)
                                                                       #id6=self.id_6)
                    self.llt_class_list.append(current_llt_die_class)
                    if llt_die_start_die_num in 'DIE 0':
                        # check mrph only if die 0
                        current_llt_die_class.check_mrph()
                        self.llt_class_die0 = current_llt_die_class
                if current_llt_die_class:
                    current_llt_die_class.llt_line_input(llt_line)
