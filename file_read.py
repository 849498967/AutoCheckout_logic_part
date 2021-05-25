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
                if re_match(r'LLTSCRIPT START', file_line):
                    self.llt_file_match = True
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
                # max_chips_per_bank/program name/rev/technology/design input
                max_chips_per_bank_match = re_match(r'max_chips_per_bank = (.*)', mt_line)
                if max_chips_per_bank_match:
                    max_chips_per_bank = max_chips_per_bank_match.group(1)
                max_chips_per_bank_match2 = re_match(r'MAX_CHIPS_PER_BANK = (.*)', mt_line)
                if max_chips_per_bank_match2:
                    max_chips_per_bank = max_chips_per_bank_match2.group(1)
                program_name_match = re_match(r'PROGRAMNAME (.*)', mt_line)
                if program_name_match:
                    program_name = program_name_match.group(1)
                program_rev_match = re_match(r'Product Name Changed to {3}= (.*)', mt_line)
                if program_rev_match:
                    program_rev = program_rev_match.group(1)
                program_tech_match = re_match(r'TECHNOLOGY (.*)', mt_line)
                if program_tech_match:
                    program_tech = program_tech_match.group(1)
                program_design_match = re_match(r'DESIGN (.*)', mt_line)
                if program_design_match:
                    program_design = program_design_match.group(1)
                program_die_match = re_match(r'NANDCONFIGDIE ([0-9]*).*', mt_line)
                if program_die_match:
                    program_die = program_die_match.group(1)
                file_name_match = re_match(r'FILE NAME (.*)\.xml', mt_line)
                if file_name_match:
                    file_name = file_name_match.group(1)
                if re_match(r'.*FLOWDESCRIPTIONSTART.*', mt_line):
                    under_mt = True
                    mt_file_number = self.mt_datalog_file_in.name + str(mt_datalog_number)
                    self.mt_datalog_list.append(mt_file_number)
                    current_mt_class = mt_per_die.MTPerDieClass(mt_file_number, program_name, program_rev,
                                                                program_tech, program_design, program_die,
                                                                max_chips_per_bank, file_name)
                    self.mt_class_list.append(current_mt_class)
                    mt_datalog_number += 1
                if re_match(r'.*Test End Action.*', mt_line):
                    under_mt = False
                if under_mt:
                    current_mt_class.mt_line_input(mt_line)

    # jason: read the parsed trim txt file
    def read_trim_table(self):
        for trim_line in self.trim_datalog_file_in:
            revision_check_start = re_match(r'TRIMSTART (.*GB_.[.].*?_TO_.*[.].*)', trim_line)
            # print(revision_check_start.group(1))
            if revision_check_start:
                trim_version_in_table = revision_check_start.group(1)
                self.trim_version_list.append(trim_version_in_table)
                self.trim_class = trim.TrimTable(trim_version_in_table)  # trim.name
                self.trim_class_list.append(self.trim_class)
            trim_data = re_match(r'Original_value\[(.{2,3})]=(.*);\t'  # 2 matches here: addr, value
                                 r'Fix_or_Trim\[.{2,3}]=(.*);\t'
                                 r'Trim_value\[.{2,3}]=(.*);\t'
                                 r'Trim_mask\[.{2,3}]=(.*);\t'
                                 r'Trim_shift\[.{2,3}]=(.*);', trim_line)
            if trim_data:
                # print(trim_data.group(1), trim_data.group(2), trim_data.group(3), trim_data.group(4),
                # trim_data.group(5), trim_data.group(6))
                # jason: add another param: product, hard code hese css for debugging
                self.trim_class.trim_input('0x' + trim_data.group(1), '0x' + trim_data.group(2), trim_data.group(3),
                                           '0x' + trim_data.group(4), '0x' + trim_data.group(5), trim_data.group(6),
                                           self.mt_class_list, "CSS")  # mt_class_list is info read from mt datalog

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
                                                                       self.mt_class_list, self.trim_class_list, self.product)
                    self.llt_class_list.append(current_llt_die_class)
                    if llt_die_start_die_num in 'DIE 0':
                        self.llt_class_die0 = current_llt_die_class
                if current_llt_die_class:
                    current_llt_die_class.llt_line_input(llt_line)
