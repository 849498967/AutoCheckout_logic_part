from re import match as re_match
import re
import data_in_mapping
import trim_check_webscr as tw
import time
import re
'''
    called in file read, need to add product param input from GUI.
    this param will be called in id_match_result method. currently hard code CSS only for debug
'''
class LltPerDieClass:
    """
    Each die LLT datalog collect and analysis
    """

    def __init__(self, name, mt_class, trim_class, product, file_path, mrph_ver, tracker_ver, id7, id8, id6):
        # jason: pre-define these 3 params in case trim is not run
        self.add_112 = '0x00'
        self.add_172 = '0x00'
        self.add_FB = '0x00'

        self.mrph_ver = mrph_ver
        self.tracker_ver = tracker_ver
        self.id7 = id7
        self.id8 = id8
        self.id6 = id6

        self.product = product
        self.flag = 0
        self.name = name
        self.mt_class = mt_class
        self.trim_class = trim_class
        # POR
        self.por_data = None
        self.por_result = None
        # ID
        self.under_id_read = False
        self.id_dict = {}
        self.id_result = {}
        self.id_result_excel = 1
        self.id_expect = {}
        # LWXY
        self.lot = None
        self.wafer = None
        self.x_coor = None
        self.y_coor = None
        self.ds_ver = None
        self.sort_date = None
        self.lwxy = None
        self.lwxy_match_dut = 0
        self.dut_chip_lwxy = None
        self.lwxy_match_result = 0
        self.lwxy_lot_match_result = 'N'
        self.lwxy_wafer_match_result = 'N'
        self.lwxy_x_match_result = 'N'
        self.lwxy_y_match_result = 'N'
        # bb
        self.bb_list = []
        self.mt_bb_print = []
        self.llt_bb_print = []
        self.bb_result = 1
        self.bb_result_print = []
        # BC
        self.bc_result = 1
        self.bc_list_p0 = []
        self.bc_list_p1 = []
        self.mt_bc_print_p0 = []
        self.llt_bc_print_p0 = []
        self.mt_bc_print_p1 = []
        self.llt_bc_print_p1 = []
        self.result_bc_p0 = []
        self.result_bc_p1 = []
        # uid
        self.uid_result = 1
        self.uid_data = None
        self.lot_split = None
        self.trim_version_uid = 'E'
        self.uid_data_list_copy0 = []
        self.uid_data_list_copy1 = []
        self.uid_data_list_copy2 = []
        self.uid_data_list_copy3 = []
        self.uid_data_list_bar_copy0 = []
        self.uid_data_list_bar_copy1 = []
        self.uid_data_list_bar_copy2 = []
        self.uid_data_list_bar_copy3 = []
        self.uid_expect_data = []
        self.uid_data_databar = 0
        self.uid_addr_list_copy0 = []
        self.uid_addr_list_copy1 = []
        self.uid_addr_list_copy2 = []
        self.uid_addr_list_copy3 = []
        self.uid_SPEC_excel_print = ['ID', 'lot[0]', 'lot[1]', 'wafer', 'X', 'Y', 'lot[2]', 'lot[3]', 'DATE', 'MONTH',
                                     'YEAR', 'lot[4]', 'lot[5]', 'lot[6]', 'lot[7]', 'lot[8]', 'AR3 DAC']
        self.uid_Data_excel_print_copy0 = []
        self.uid_Data_excel_print_copy1 = []
        self.uid_Data_excel_print_copy2 = []
        self.uid_Data_excel_print_copy3 = []
        self.uid_Data_bar_excel_print_copy0 = []
        self.uid_Data_bar_excel_print_copy1 = []
        self.uid_Data_bar_excel_print_copy2 = []
        self.uid_Data_bar_excel_print_copy3 = []
        self.uid_Expect_excel_print = []
        self.uid_result_excel_copy0 = []  # 0:match, 1:Data, Databar mismatch, 2:Wrong data
        self.uid_result_excel_copy1 = []  # 0:match, 1:Data, Databar mismatch, 2:Wrong data
        self.uid_result_excel_copy2 = []  # 0:match, 1:Data, Databar mismatch, 2:Wrong data
        self.uid_result_excel_copy3 = []  # 0:match, 1:Data, Databar mismatch, 2:Wrong data
        # UROM stamp
        self.stamp_dict_key = None
        self.stamp_dict_key_list = []
        self.stamp_result = None
        self.stamp_die_result = None
        self.stamp_dict = {}
        self.stamp_excel_print_die = []
        self.stamp_excel_print_name = []
        self.stamp_excel_print_copy = []
        self.stamp_excel_print_data = []
        self.stamp_excel_print_expect = []
        self.stamp_excel_print_match = []
        # dist VT
        # romfuse vt
        self.dist_vt_judge_case1_result = 0
        self.dist_vt_judge_case1_limit1 = 0.7
        self.dist_vt_judge_case1_limit2 = 1.2
        self.dist_vt_judge_case1_limit3 = 1.2
        self.dist_vt_judge_case1_limit4 = 2.1
        self.dist_vt_judge_case1_limit5 = 32
        # userrom vt
        self.dist_vt_judge_case2_result = 0
        self.dist_vt_judge_case2_limit1 = 1.6
        self.dist_vt_judge_case2_limit2 = 2.4
        self.dist_vt_judge_case2_limit3 = 32
        # flash write good block VT
        self.dist_vt_judge_case3_result = 0
        self.dist_vt_judge_case3_limit1 = 0.4
        self.dist_vt_judge_case3_limit2 = 1.8
        # flash write bad block VT
        self.dist_vt_judge_case4_result = 0
        self.dist_vt_judge_case4_limit = 4.0
        self.dist_vt_judge_case5_result = 0
        self.dist_vt_judge_case5_limit = 5.4
        # trim
        self.trim_result = -1
        self.trim_result_acc = 1
        self.trim_version_match = False
        self.trim_userrom_addr_list = []
        self.trim_userrom_value_list = []
        self.trim_romfuse_addr_list = []
        self.trim_romfuse_value_list = []
        self.trim_cal = []
        self.trim_excel_Addr = []
        self.trim_excel_romfuse = []
        self.trim_excel_userrom = []
        self.trim_excel_original = []
        self.trim_excel_setparmmask_value = []
        self.trim_excel_mask = []
        self.trim_excel_shift = []
        self.trim_excel_result = []
        # VT dist
        self.dist_vt_dict = {}
        # key_para
        self.key_para_expect = []
        self.key_para_tb_copy = []
        self.key_para_addr_copy = []
        self.key_para_rom_copy = []
        self.key_para_reg_copy = []
        self.key_para_result = []
        self.key_para_check_acc = 1
        self.key_para_value_copy =[]
        self.key_para_mask_copy =[]

        '''
            mrph dict
        '''
        self.mrph_list = []
        self.llt_file_path = file_path
        # data inout
        self.under_por = False
        self.por_status = None
        self.under_lwxy = False
        self.lot_name = None
        self.wafer_num = None
        self.x_coor_num = None
        self.y_coor_num = None
        self.ds_ver_name = None
        self.sort_date_num = None
        self.under_bb = False
        self.under_bc = False
        self.under_stamp = False
        self.under_vt_dist = False
        self.excel_title = None
        self.label_title = None
        self.temp_vt_x_number_cal = None
        self.temp_vt_y_number_cal = None
        self.under_trim = False
        self.trim_version_name = None
        self.under_uid = False
        self.uid_addr_data = None
        # new 
        #print(self.mt_class[0].mt_die)
        # if 'BGA132' not in self.mt_class[0].file_name and 'BGA315' not in self.mt_class[0].file_name and self.mt_class[0].mt_die >= 8 or self.mt_class[0].mt_die ==5:
        #     self.uid_dac = self.mt_class[0].uid_return_dmy[6]
        #     self.tb_dut_bank_chip = sorted(self.mt_class[0].dut_bank_chip)
        # else:
        try:
            self.uid_dac = self.mt_class[0].uid_return_dmy[3]
            self.tb_dut_bank_chip = sorted(self.mt_class[0].dut_bank_chip)
            self.uid_dac1 = []
        except:
            pass
    @staticmethod
    def hex_upper(integer_num):
        """
        Convert integer to capital case letter hex number
        :param integer_num: integer input
        :return: capital case letter hex number
        """
        hex_transfer = hex(integer_num)
        hex_split = hex_transfer.split('0x')
        hex_split_upper = hex_split[1].upper()
        if integer_num >= 0:
            return '0x' + hex_split_upper
        else:
            return '-0x' + hex_split_upper

    def por(self, result):
        """
        por data collection
        :param result: por result input
        :return: NA
        """
        self.por_data = str(result)
        # print(self.por_data)
        if self.por_data in 'E0' or self.por_data in 'F0':
            self.por_result = 1
        else:
            self.por_result = 0

    def id_input(self, id_dict):
        self.id_dict = id_dict
        # print("id_dict", id_dict)

    def id_match_result(self, add1, add2, add3, product): # addi is used to get the id byte 7/8's value. but CSS and ESS don't support
        try:
            self.id_expect = data_in_mapping.id_mapping(
                self.mt_class[0].mt_design, self.mt_class[0].mt_die, self.name,self.mt_class[0].file_name)
            for id_expect_key in self.id_expect:
                if product == "CSS" or product == "ESS":
                    if id_expect_key == 7:
                        self.id_expect[id_expect_key] = self.id7
                        #print(self.id_expect[id_expect_key])
                    if id_expect_key == 8:
                        self.id_expect[id_expect_key] = self.id8

                    if id_expect_key == 6:
                        self.id_expect[id_expect_key] = self.id6
                        #print(self.id_expect[id_expect_key])
                    if int(self.id_expect[id_expect_key], 16) == int(self.id_dict[str(id_expect_key)], 16):
                        self.id_result[id_expect_key] = 'Y'
                    else:
                        self.id_result[id_expect_key] = 'N'
                        self.id_result_excel = 0
                # print(id_expect_key)
                #print(self.id_expect[id_expect_key])
                # print(self.id_dict)
                # print(self.id_dict[str(id_expect_key)])
                # add---ID byte7/8 revision&maturity &ODT check----Maurice
                else:
                    if id_expect_key == 7:
                        self.id_expect[id_expect_key] = self.hex_upper(int('0x08',16)+(int(add2,16)&int('0x70',16))//16)
                        #print(self.id_expect[id_expect_key])
                    if id_expect_key == 8:
                        self.id_expect[id_expect_key] = self.hex_upper(int('0x1E',16)+(int(add1,16)&int('0x60',16))*2)
                        if (int(add3,16)&int('0x02',16)) != 0:
                            self.id_expect[id_expect_key] = self.hex_upper((int(self.id_expect[id_expect_key],16)&(~int('0x08',16)))|\
                                                         (int('0x00', 16) &int('0x08', 16)))
                        #print(self.id_expect[id_expect_key])
                    if int(self.id_expect[id_expect_key], 16) == int(self.id_dict[str(id_expect_key)], 16):
                        self.id_result[id_expect_key] = 'Y'
                    else:
                        self.id_result[id_expect_key] = 'N'
                        self.id_result_excel = 0
        except:
            print("id pass")
            pass

    def lwxy_input(self, lot, wafer, x_coordinator, y_coordinator, ds_ver, sort_date):
        """
        lot, wafer, X coordinator, Y coordinator data collection
        :param lot: Lot
        :param wafer: Wafer
        :param x_coordinator: X
        :param y_coordinator: Y
        :param ds_ver: DS version
        :param sort_date: DS test date
        :return: NA
        """
        self.lot = lot
        self.wafer = wafer
        self.x_coor = x_coordinator
        self.y_coor = y_coordinator
        self.ds_ver = ds_ver
        self.sort_date = sort_date
        self.lwxy = self.wafer + '_' + self.x_coor + '_' + self.y_coor + '_' + self.lot

    def lwxy_match_dut_result(self):
        """
        Compare with MT datalog LWXY and find which dut and chip number
        :mt_class: MT class input
        :return: NA
        """
        # find match dut and chip number
        # print(self.mt_class[0].lwxy)
        for lwxy_keys, lwxy_values in self.mt_class[0].lwxy.items():
            #print(self.lwxy, lwxy_values)
            if self.lwxy in lwxy_values:
                self.dut_chip_lwxy = lwxy_keys.split('_')
                self.lwxy_match_dut = 1
            #print(self.dut_chip_lwxy)
        # If cannot find lwxy match in datalog, printout error in excel file
        if self.lwxy_match_dut == 1:
            if self.wafer in self.mt_class[0].lwxy[self.dut_chip_lwxy[0] + '_' + self.dut_chip_lwxy[1] + '_wafer']:
                self.lwxy_match_result = 1
                self.lwxy_lot_match_result = 'Y'
            if self.x_coor in self.mt_class[0].lwxy[self.dut_chip_lwxy[0] + '_' + self.dut_chip_lwxy[1] + '_x']:
                self.lwxy_match_result = 1
                self.lwxy_x_match_result = 'Y'
            if self.y_coor in self.mt_class[0].lwxy[self.dut_chip_lwxy[0] + '_' + self.dut_chip_lwxy[1] + '_y']:
                self.lwxy_match_result = 1
                self.lwxy_y_match_result = 'Y'
            if self.lot in self.mt_class[0].lwxy[self.dut_chip_lwxy[0] + '_' + self.dut_chip_lwxy[1] + '_lot']:
                self.lwxy_match_result = 1
                self.lwxy_wafer_match_result = 'Y'

    def bb_split_collect(self, bb_line):
        """
        Bad block data collection
        :param bb_line: bad block address line
        :return: NA
        """
        bb_collect_llt = bb_line.split(',')
        for j, bb_ele in enumerate(bb_collect_llt):
            if j != 0:
                if re_match(r'.*[0-9A-Z].*', bb_ele):
                    self.bb_list.append(bb_ele)

    def bb_match_result(self):
        """
        Compare with MT datalog BB list and make array match and mismatch
        :return: NA
        """
        if self.lwxy_match_dut == 1:
            if 'BiCs4p5' in self.mt_class[0].mt_design:
                # B4.5
                bb_key_name = 'tb__901__REG_RD_bblks_out__nvcc_' + self.dut_chip_lwxy[0] + '_' + self.dut_chip_lwxy[1]
            elif 'BiCs5' in self.mt_class[0].mt_design:
                # B4.5
                bb_key_name = 'tb__901__REG_RD_bblks_out__nvcc_' + self.dut_chip_lwxy[0] + '_' + self.dut_chip_lwxy[1]
                # print(bb_key_name)
            else:
                bb_key_name = 'tb__692__REG_RD_bblks_out__nvcc_' + self.dut_chip_lwxy[0] + '_' + self.dut_chip_lwxy[1]
            mt_bb_cal_list = []
            llt_bb_cal_list = []
            if 'BiCs3_128Gb_2P' in self.mt_class[0].mt_design or 'BiCs3_128G_2P' in self.mt_class[0].mt_design:
                # print(self.mt_class[0].mt_design)
                for MT_bb in self.mt_class[0].bb_dict[bb_key_name]:
                    mt_bb_cal_list.append(int(MT_bb, 16) - 2048 * (int(self.dut_chip_lwxy[1]) - 1))
            elif 'BiCs4_256Gb_2P' in self.mt_class[0].mt_design or 'BiCs4_256G_2P' in self.mt_class[0].mt_design:
                # print(self.mt_class[0].mt_design)
                for mt_bb in self.mt_class[0].bb_dict[bb_key_name]:
                    mt_bb_cal_list.append(int(mt_bb, 16) - 2048 * (int(self.dut_chip_lwxy[1]) - 1))
            elif 'BiCs4p5_256Gb_2P' in self.mt_class[0].mt_design or 'BiCs4p5_256G_2P' in self.mt_class[0].mt_design:
                # print(self.mt_class[0].mt_design)
                for mt_bb in self.mt_class[0].bb_dict[bb_key_name]:
                    # print(mt_bb, self.dut_chip_lwxy[1])
                    mt_bb_cal_list.append(int(mt_bb, 16) - 2048 * (int(self.dut_chip_lwxy[1]) - 1))
            elif 'BiCs5_512Gb_2P' in self.mt_class[0].mt_design or 'BiCs5_512G_2P' in self.mt_class[0].mt_design:
                # print(self.mt_class[0].mt_design)
                for mt_bb in self.mt_class[0].bb_dict[bb_key_name]:
                    # print(mt_bb, self.dut_chip_lwxy[1], int(mt_bb, 16) - 4096 * (int(self.dut_chip_lwxy[1]) - 1))
                    mt_bb_cal_list.append(int(mt_bb, 16) - 4096 * (int(self.dut_chip_lwxy[1]) - 1))
            elif 'BiCs5_1024Gb_2P' in self.mt_class[0].mt_design or 'BiCs5_1024G_2P' in self.mt_class[0].mt_design:
                # print(self.mt_class[0].mt_design)
                for mt_bb in self.mt_class[0].bb_dict[bb_key_name]:
                    # print(mt_bb, self.dut_chip_lwxy[1], int(mt_bb, 16) - 4096 * (int(self.dut_chip_lwxy[1]) - 1))
                    mt_bb_cal_list.append(int(mt_bb, 16) - 8192 * (int(self.dut_chip_lwxy[1]) - 1))
            else:
                for mt_bb in self.mt_class[0].bb_dict[bb_key_name]:
                    # 16D with 2 bank(2 separate flow) chip offset
                    if self.mt_class[0].bank2_start:
                        if int(self.dut_chip_lwxy[1]) <= int((self.mt_class[0].mt_die / 2)):
                            mt_bb_cal_list.append(int(mt_bb, 16) - 4096 * (int(self.dut_chip_lwxy[1]) - 1))
                        else:
                            mt_bb_cal_list.append(int(mt_bb, 16) - 4096 * (int(self.dut_chip_lwxy[1]) - 1 -
                                                                           int(self.mt_class[0].mt_die / 2)))
                    else:
                        # print(mt_bb, self.dut_chip_lwxy[1], int(mt_bb, 16) - 4096 * (int(self.dut_chip_lwxy[1]) - 1))
                        mt_bb_cal_list.append(int(mt_bb, 16) - 4096 * (int(self.dut_chip_lwxy[1]) - 1))

            for llt_bb in self.bb_list:
                llt_bb_cal_list.append(int(llt_bb, 16))
            # print out with soring
            mt_bb_cal_list.sort()
            llt_bb_cal_list.sort()
            mt_bb_index = 0
            llt_bb_index = 0
            bb_while_loop_break = 500
            # print("MT bb list : ", mt_bb_cal_list, len(mt_bb_cal_list))
            # print("LLT bb list : ", llt_bb_cal_list, len(llt_bb_cal_list))

            while mt_bb_index < len(mt_bb_cal_list):
                bb_while_loop_break -= 1
                if bb_while_loop_break == 0:
                    print("BB loop cannot finish")
                    print("MT bb list : ", mt_bb_cal_list)
                    print("LLT bb list : ", llt_bb_cal_list)
                    raise ValueError
                # print(mt_bb_cal_list[mt_bb_index])
                # print('MTbb:', hex(mt_bb_cal_list[mt_bb_index]))
                # print('LLTbb:', hex(llt_bb_cal_list[llt_bb_index]))
                if llt_bb_index < len(llt_bb_cal_list):
                    # match
                    if mt_bb_cal_list[mt_bb_index] == llt_bb_cal_list[llt_bb_index]:
                        self.mt_bb_print.append(self.hex_upper(mt_bb_cal_list[mt_bb_index]))
                        self.llt_bb_print.append(self.hex_upper(llt_bb_cal_list[llt_bb_index]))
                        self.bb_result_print.append('Y')
                        mt_bb_index += 1
                        llt_bb_index += 1
                    ### """
                    ### # swap bb match
                    ### elif (llt_bb_cal_list[llt_bb_index] < 6) & \
                    ###         (mt_bb_cal_list[mt_bb_index] == llt_bb_cal_list[llt_bb_index] + 128):
                    ###     self.mt_bb_print.append(self.hex_upper(mt_bb_cal_list[mt_bb_index]))
                    ###     self.llt_bb_print.append(self.hex_upper(llt_bb_cal_list[llt_bb_index]))
                    ###     self.bb_result_print.append('BLK SWAP')
                    ###     mt_bb_index += 1
                    ###     llt_bb_index += 1
                    ### # swap bb match opposite direction
                    ### elif (mt_bb_cal_list[mt_bb_index] < 6) & \
                    ###         (mt_bb_cal_list[mt_bb_index] + 128 == llt_bb_cal_list[llt_bb_index]):
                    ###     self.mt_bb_print.append(self.hex_upper(mt_bb_cal_list[mt_bb_index]))
                    ###     self.llt_bb_print.append(self.hex_upper(llt_bb_cal_list[llt_bb_index]))
                    ###     self.bb_result_print.append('BLK SWAP')
                    ###     mt_bb_index += 1
                    ###     llt_bb_index += 1
                    ### # make space for swap block match
                    ### elif llt_bb_cal_list[llt_bb_index] < 6:
                    ###     for MT_bb_element in mt_bb_cal_list:
                    ###         if llt_bb_cal_list[llt_bb_index] + 128 == MT_bb_element:
                    ###             self.bb_result_print.append('BLK SWAP')
                    ###             self.llt_bb_print.append(self.hex_upper(llt_bb_cal_list[llt_bb_index]))
                    ###             self.mt_bb_print.append('')
                    ###             llt_bb_index += 1
                    ###             break
                    ### # make space for swap block match
                    ### elif 128 <= mt_bb_cal_list[mt_bb_index] < 134:
                    ###     for llt_bb_element in llt_bb_cal_list:
                    ###         if llt_bb_element + 128 == mt_bb_cal_list[mt_bb_index]:
                    ###             self.bb_result_print.append('BLK SWAP')
                    ###             self.mt_bb_print.append(self.hex_upper(mt_bb_cal_list[mt_bb_index]))
                    ###             self.llt_bb_print.append('')
                    ###             mt_bb_index += 1
                    ###             break
                    ### 
                    elif mt_bb_cal_list[mt_bb_index] > llt_bb_cal_list[llt_bb_index]:
                        self.mt_bb_print.append('')
                        self.llt_bb_print.append(self.hex_upper(llt_bb_cal_list[llt_bb_index]))
                        self.bb_result_print.append('N')
                        self.bb_result = 0
                        llt_bb_index += 1
                    else:
                        self.mt_bb_print.append(self.hex_upper(mt_bb_cal_list[mt_bb_index]))
                        self.llt_bb_print.append('')
                        self.bb_result_print.append('N')
                        self.bb_result = 0
                        mt_bb_index += 1
                else:
                    self.mt_bb_print.append(self.hex_upper(mt_bb_cal_list[mt_bb_index]))
                    self.llt_bb_print.append('')
                    self.bb_result_print.append('N')
                    self.bb_result = 0
                    mt_bb_index += 1
            while llt_bb_index < len(llt_bb_cal_list):
                self.mt_bb_print.append('')
                self.llt_bb_print.append(self.hex_upper(llt_bb_cal_list[llt_bb_index]))
                self.bb_result_print.append('N')
                self.bb_result = 0
                llt_bb_index += 1

    def bc_match_result(self):
        # If cannot find lwxy match in datalog, printout error
        # print(self.mt_class[0].bc_p0_dict)
        if self.lwxy_match_dut == 1:
            if 'BiCs4p5' in self.mt_class[0].mt_design:
                # B4.5
                # print(self.mt_class[0].bc_p0_dict)
                #bc_key_name = 'tb__140__REG_RD_bcols_in__nvcc_' + self.dut_chip_lwxy[0] + '_' + self.dut_chip_lwxy[1]
                bc_key_name = 'AA'
                # print(bc_key_name)
                if bc_key_name not in self.mt_class[0].bc_p0_dict:
                    bc_key_name = 'tb__146__REG_RD_bcols__nvcc_' + self.dut_chip_lwxy[0] + '_' + self.dut_chip_lwxy[1]
                if bc_key_name not in self.mt_class[0].bc_p0_dict:
                    bc_key_name = 'tb__145__REG_RD_bcols__nvcc_' + self.dut_chip_lwxy[0] + '_' + self.dut_chip_lwxy[1]
                if bc_key_name not in self.mt_class[0].bc_p0_dict:
                    bc_key_name = 'tb__144__REG_RD_bcols__nvcc_' + self.dut_chip_lwxy[0] + '_' + self.dut_chip_lwxy[1]
                if bc_key_name not in self.mt_class[0].bc_p0_dict:
                    bc_key_name = 'tb__143__REG_RD_bcols__nvcc_' + self.dut_chip_lwxy[0] + '_' + self.dut_chip_lwxy[1]
                if bc_key_name not in self.mt_class[0].bc_p0_dict:
                    bc_key_name = 'tb__142__REG_RD_bcols__nvcc_' + self.dut_chip_lwxy[0] + '_' + self.dut_chip_lwxy[1]
                if bc_key_name not in self.mt_class[0].bc_p0_dict:
                    bc_key_name = 'tb__141__REG_RD_bcols__nvcc_' + self.dut_chip_lwxy[0] + '_' + self.dut_chip_lwxy[1]
            elif 'BiCs5' in self.mt_class[0].mt_design:
                # B5
                # print(self.mt_class[0].bc_p0_dict)
                bc_key_name = 'AA'
                if bc_key_name not in self.mt_class[0].bc_p0_dict:
                    bc_key_name = 'tb__141__REG_RD_bcols_out__nvcc_' + self.dut_chip_lwxy[0] + '_' + self.dut_chip_lwxy[1]
                if bc_key_name not in self.mt_class[0].bc_p0_dict:
                    bc_key_name = 'tb__140__REG_RD_bcols_in__nvcc_' + self.dut_chip_lwxy[0] + '_' + self.dut_chip_lwxy[1]
                #bc_key_name = 'AA'
                # print(bc_key_name)
            else:
                # B4 and below
                bc_key_name = 'tb__213__REG_RD_bcols__nvcc_' + self.dut_chip_lwxy[0] + '_' + self.dut_chip_lwxy[1]
                if bc_key_name not in self.mt_class[0].bc_p0_dict:
                    bc_key_name = 'tb__210__REG_RD_bcols__nvcc_' + self.dut_chip_lwxy[0] + '_' + self.dut_chip_lwxy[1]
                if bc_key_name not in self.mt_class[0].bc_p0_dict:
                    bc_key_name = 'tb__209__REG_RD_bcols__nvcc_' + self.dut_chip_lwxy[0] + '_' + self.dut_chip_lwxy[1]
                if bc_key_name not in self.mt_class[0].bc_p0_dict:
                    bc_key_name = 'tb__208__REG_RD_bcols__nvcc_' + self.dut_chip_lwxy[0] + '_' + self.dut_chip_lwxy[1]
                if bc_key_name not in self.mt_class[0].bc_p0_dict:
                    bc_key_name = 'tb__207__REG_RD_bcols__nvcc_' + self.dut_chip_lwxy[0] + '_' + self.dut_chip_lwxy[1]
                if bc_key_name not in self.mt_class[0].bc_p0_dict:
                    bc_key_name = 'tb__206__REG_RD_bcols__nvcc_' + self.dut_chip_lwxy[0] + '_' + self.dut_chip_lwxy[1]
                if bc_key_name not in self.mt_class[0].bc_p0_dict:
                    bc_key_name = 'tb__205__REG_RD_bcols_in__nvcc_' + self.dut_chip_lwxy[0] + '_' + self.dut_chip_lwxy[1]

            mt_bc_cal_list = []
            llt_bc_cal_list = []

            # plane 0
            for mt_bc in self.mt_class[0].bc_p0_dict[bc_key_name]:
                mt_bc_cal_list.append(int(mt_bc, 16))
            for llt_bc in self.bc_list_p0:
                llt_bc_cal_list.append(int(llt_bc, 16))

            mt_bc_cal_list.sort()
            llt_bc_cal_list.sort()
            mt_bc_index = 0
            llt_bc_index = 0

            while mt_bc_index < len(mt_bc_cal_list):
                if llt_bc_index < len(llt_bc_cal_list):
                    if mt_bc_cal_list[mt_bc_index] == llt_bc_cal_list[llt_bc_index]:  # match
                        self.mt_bc_print_p0.append(self.hex_upper(mt_bc_cal_list[mt_bc_index]))
                        self.llt_bc_print_p0.append(self.hex_upper(llt_bc_cal_list[llt_bc_index]))
                        self.result_bc_p0.append('Y')
                        mt_bc_index += 1
                        llt_bc_index += 1
                    elif mt_bc_cal_list[mt_bc_index] > llt_bc_cal_list[llt_bc_index]:
                        self.mt_bc_print_p0.append('')
                        self.llt_bc_print_p0.append(self.hex_upper(llt_bc_cal_list[llt_bc_index]))
                        self.result_bc_p0.append('N')
                        self.bc_result = 0
                        llt_bc_index += 1
                    else:
                        self.mt_bc_print_p0.append(self.hex_upper(mt_bc_cal_list[mt_bc_index]))
                        self.llt_bc_print_p0.append('')
                        self.result_bc_p0.append('N')
                        self.bc_result = 0
                        mt_bc_index += 1
                else:
                    self.mt_bc_print_p0.append(self.hex_upper(mt_bc_cal_list[mt_bc_index]))
                    self.llt_bc_print_p0.append('')
                    self.result_bc_p0.append('N')
                    self.bc_result = 0
                    mt_bc_index += 1
            while llt_bc_index < len(llt_bc_cal_list):
                self.mt_bc_print_p0.append('')
                self.llt_bc_print_p0.append(self.hex_upper(llt_bc_cal_list[llt_bc_index]))
                self.result_bc_p0.append('N')
                self.bc_result = 0
                llt_bc_index += 1

            # plane 1
            mt_bc_cal_list_p1 = []
            llt_bc_cal_list_p1 = []
            for mt_bc in self.mt_class[0].bc_p1_dict[bc_key_name]:
                mt_bc_cal_list_p1.append(int(mt_bc, 16))
            for llt_bc in self.bc_list_p1:
                llt_bc_cal_list_p1.append(int(llt_bc, 16))
                mt_bc_cal_list_p1.sort()
                llt_bc_cal_list_p1.sort()
            mt_bc_index = 0
            llt_bc_index = 0
            while mt_bc_index < len(mt_bc_cal_list_p1):
                if llt_bc_index < len(llt_bc_cal_list_p1):
                    if mt_bc_cal_list_p1[mt_bc_index] == llt_bc_cal_list_p1[llt_bc_index]:  # match
                        self.mt_bc_print_p1.append(self.hex_upper(mt_bc_cal_list_p1[mt_bc_index]))
                        self.llt_bc_print_p1.append(self.hex_upper(llt_bc_cal_list_p1[llt_bc_index]))
                        self.result_bc_p1.append('Y')
                        mt_bc_index += 1
                        llt_bc_index += 1
                    elif mt_bc_cal_list_p1[mt_bc_index] > llt_bc_cal_list_p1[llt_bc_index]:
                        self.mt_bc_print_p1.append('')
                        self.llt_bc_print_p1.append(self.hex_upper(llt_bc_cal_list_p1[llt_bc_index]))
                        self.result_bc_p1.append('N')
                        self.bc_result = 0
                        llt_bc_index += 1
                    else:
                        self.mt_bc_print_p1.append(self.hex_upper(mt_bc_cal_list_p1[mt_bc_index]))
                        self.llt_bc_print_p1.append('')
                        self.result_bc_p1.append('N')
                        self.bc_result = 0
                        mt_bc_index += 1
                else:
                    self.mt_bc_print_p1.append(self.hex_upper(mt_bc_cal_list_p1[mt_bc_index]))
                    self.llt_bc_print_p1.append('')
                    self.result_bc_p1.append('N')
                    self.bc_result = 0
                    mt_bc_index += 1
            while llt_bc_index < len(llt_bc_cal_list_p1):
                self.mt_bc_print_p1.append('')
                self.llt_bc_print_p1.append(self.hex_upper(llt_bc_cal_list_p1[llt_bc_index]))
                self.result_bc_p1.append('N')
                self.bc_result = 0
                llt_bc_index += 1

    def bc_split_collect(self, bc_line):
        bc_collect_llt = bc_line.split(',')
        for i, bc_part in enumerate(bc_collect_llt):
            if i != 0:
                if i % 2 == 1:
                    if re_match(r'.*[0-9A-Z].*', bc_part):
                        # print(bc_collect_llt[i+1])
                        if bc_collect_llt[i + 1] in "     00":
                            self.bc_list_p0.append(bc_part)
                            # print('p0 BC:',self.bc_list_p0[-1])
                        if bc_collect_llt[i + 1] in "     01":
                            self.bc_list_p1.append(bc_part)
                            # print('p1 BC',self.bc_list_p1[-1])

    def uid_collect(self, uid_data, uid_addr_input):
        self.uid_data = uid_data
        if uid_addr_input in "WL 11 STRING 0 COLUMN 0":
            uid_addr_split = uid_addr_input.split()
            self.uid_addr_list_copy0.append(self.hex_upper(int(uid_addr_split[1], 16)))
            self.uid_addr_list_copy0.append(self.hex_upper(int(uid_addr_split[3], 16)))
            self.uid_addr_list_copy0.append(self.hex_upper(int(uid_addr_split[5], 16)))
            if self.uid_data_databar % 2 == 0:
                self.uid_data_list_copy0.append('0x' + uid_data)
            else:
                self.uid_data_list_bar_copy0.append('0x' + uid_data)
        if uid_addr_input in "WL 11 STRING 0 COLUMN 200":
            uid_addr_split = uid_addr_input.split()
            self.uid_addr_list_copy1.append(self.hex_upper(int(uid_addr_split[1], 16)))
            self.uid_addr_list_copy1.append(self.hex_upper(int(uid_addr_split[3], 16)))
            self.uid_addr_list_copy1.append(self.hex_upper(int(uid_addr_split[5], 16)))
            if self.uid_data_databar % 2 == 0:
                self.uid_data_list_copy1.append('0x' + uid_data)
            else:
                self.uid_data_list_bar_copy1.append('0x' + uid_data)
        if uid_addr_input in "WL 33 STRING 0 COLUMN 0":
            uid_addr_split = uid_addr_input.split()
            self.uid_addr_list_copy2.append(self.hex_upper(int(uid_addr_split[1], 16)))
            self.uid_addr_list_copy2.append(self.hex_upper(int(uid_addr_split[3], 16)))
            self.uid_addr_list_copy2.append(self.hex_upper(int(uid_addr_split[5], 16)))
            if self.uid_data_databar % 2 == 0:
                self.uid_data_list_copy2.append('0x' + uid_data)
            else:
                self.uid_data_list_bar_copy2.append('0x' + uid_data)
        if uid_addr_input in "WL 33 STRING 0 COLUMN 200":
            uid_addr_split = uid_addr_input.split()
            self.uid_addr_list_copy3.append(self.hex_upper(int(uid_addr_split[1], 16)))
            self.uid_addr_list_copy3.append(self.hex_upper(int(uid_addr_split[3], 16)))
            self.uid_addr_list_copy3.append(self.hex_upper(int(uid_addr_split[5], 16)))
            if self.uid_data_databar % 2 == 0:
                self.uid_data_list_copy3.append('0x' + uid_data)
            else:
                self.uid_data_list_bar_copy3.append('0x' + uid_data)
        if uid_addr_input in "WL 35 STRING 0 COLUMN 0":
            uid_addr_split = uid_addr_input.split()
            self.uid_addr_list_copy2.append(self.hex_upper(int(uid_addr_split[1], 16)))
            self.uid_addr_list_copy2.append(self.hex_upper(int(uid_addr_split[3], 16)))
            self.uid_addr_list_copy2.append(self.hex_upper(int(uid_addr_split[5], 16)))
            if self.uid_data_databar % 2 == 0:
                self.uid_data_list_copy2.append('0x' + uid_data)
            else:
                self.uid_data_list_bar_copy2.append('0x' + uid_data)
        if uid_addr_input in "WL 35 STRING 0 COLUMN 200":
            uid_addr_split = uid_addr_input.split()
            self.uid_addr_list_copy3.append(self.hex_upper(int(uid_addr_split[1], 16)))
            self.uid_addr_list_copy3.append(self.hex_upper(int(uid_addr_split[3], 16)))
            self.uid_addr_list_copy3.append(self.hex_upper(int(uid_addr_split[5], 16)))
            if self.uid_data_databar % 2 == 0:
                self.uid_data_list_copy3.append('0x' + uid_data)
            else:
                self.uid_data_list_bar_copy3.append('0x' + uid_data)
        self.uid_data_databar += 1

    def uid_check_result(self,chip_index):
        uid_range = 17
        dmy_index = 0
        for v in self.uid_dac:
                if str(self.dut_chip_lwxy[0].zfill(2)) in v.split('_')[0].lower():
                    self.uid_dac1.append(v)
                    dmy_index = self.uid_dac.index(v)
        #print(self.uid_dac)
        self.uid_expect_data.append(hex(int('0x45', 16)))  # Vendor ID
        self.lot_split = list(self.lot)
        self.uid_expect_data.append(hex(ord(self.lot_split[0])))  # lot1
        self.uid_expect_data.append(hex(ord(self.lot_split[1])))  # lot2
        self.uid_expect_data.append('0x' + self.wafer)  # wafer
        self.uid_expect_data.append('0x' + self.x_coor)  # X
        self.uid_expect_data.append('0x' + self.y_coor)  # Y
        self.uid_expect_data.append(hex(ord(self.lot_split[2])))  # lot3
        self.uid_expect_data.append(hex(ord(self.lot_split[3])))  # lot4
        #print(self.mt_class[0].uid_return_dmy)
        try:
            # Date from datalog
            self.uid_expect_data.append(self.mt_class[0].uid_return_dmy[0][dmy_index])
            #print(self.uid_expect_data)
            # Month from datalog
            self.uid_expect_data.append(self.mt_class[0].uid_return_dmy[1][dmy_index])
            # Year from datalog
            self.uid_expect_data.append(self.mt_class[0].uid_return_dmy[2][dmy_index])

        # To avoid error due to MT does not have UID information
        except IndexError:
            # Date from datalog
            self.uid_expect_data.append('0x01')
            # Month from datalog
            self.uid_expect_data.append('0x01')
            # Year from datalog
            self.uid_expect_data.append('0x01')
        self.uid_expect_data.append(hex(ord(self.lot_split[4])))  # lot5
        self.uid_expect_data.append(hex(ord(self.lot_split[5])))  # lot6
        self.uid_expect_data.append(hex(ord(self.lot_split[6])))  # lot7
        self.uid_expect_data.append(hex(ord(self.lot_split[7])))  # lot8
        self.uid_expect_data.append(hex(ord(self.lot_split[8])))  # lot9
        # instead of Rev G material with AA pattern /////  VCG_ar3 DAC
        #print(self.trim_version_uid)
        if 'ENT' in self.mt_class[0].mt_program_rev:
            if '256GB' in self.trim_version_uid:
                self.uid_expect_data.append(hex(0) + '0')  
            elif '170GB' in self.trim_version_uid:
                self.uid_expect_data.append(hex(170))  
            else:
                self.uid_expect_data.append(hex(0) + '0')  
                uid_range = 17
        else:
            # DVCG_AR3 DAC add by Maurice
            #print(self.mt_class[0].uid_return_dmy[1])
            #need update!!!w
            #print(self.uid_dac1)
            self.uid_expect_data.append('0x'+ self.uid_dac1[chip_index][-2:].lower())
            #self.uid_dac1.remove(self.uid_dac1[0]) #die by die ,delate the previous die dac value
            uid_range = 17
        #print(self.uid_expect_data)

        # Copy0
        for i in range(uid_range):
            #print(i, self.uid_data_list_copy0[i], self.uid_expect_data[i])
            if self.uid_data_list_copy0[i] in self.uid_expect_data[i]:
                if int(self.uid_data_list_copy0[i], 16) + int(self.uid_data_list_bar_copy0[i], 16) == 255:
                    # uid match
                    self.uid_result_excel_copy0.append('Y')
                # Rev G check
                elif (i == (uid_range - 1)) and '0x0' in self.uid_expect_data[i]:
                    self.uid_result_excel_copy0.append('Y')
                else:
                    # Data, Databar mismatch
                    self.uid_result_excel_copy0.append('D-BAR')
                    if self.uid_result != 0:
                        self.uid_result = 2
            else:
                # Wrong data
                self.uid_result_excel_copy0.append('N')
                self.uid_result = 0
            self.uid_Data_excel_print_copy0.append(self.hex_upper(int(self.uid_data_list_copy0[i], 16)))
            self.uid_Data_bar_excel_print_copy0.append(self.hex_upper(int(self.uid_data_list_bar_copy0[i], 16)))
            self.uid_Expect_excel_print.append(self.hex_upper(int(self.uid_expect_data[i], 16)))
        # print(self.uid_result_copy0)
        # Copy1
        for i in range(uid_range):
            if self.uid_data_list_copy1[i] in self.uid_expect_data[i]:
                if int(self.uid_data_list_copy1[i], 16) + int(self.uid_data_list_bar_copy1[i], 16) == 255:
                    # uid match
                    self.uid_result_excel_copy1.append('Y')
                elif (i == (uid_range - 1)) and '0x0' in self.uid_data_list_copy1[i]:
                    self.uid_result_excel_copy1.append('Y')
                else:
                    # Data, Databar mismatch
                    self.uid_result_excel_copy1.append('D-BAR')
                    if self.uid_result != 0:
                        self.uid_result = 2
            else:
                # Wrong data
                self.uid_result_excel_copy1.append('N')
                self.uid_result = 0
            self.uid_Data_excel_print_copy1.append(self.hex_upper(int(self.uid_data_list_copy1[i], 16)))
            self.uid_Data_bar_excel_print_copy1.append(self.hex_upper(int(self.uid_data_list_bar_copy1[i], 16)))
        # print(self.uid_result_copy1)
        # Copy2
        for i in range(uid_range):
            if self.uid_data_list_copy2[i] in self.uid_expect_data[i]:
                if int(self.uid_data_list_copy2[i], 16) + int(self.uid_data_list_bar_copy2[i], 16) == 255:
                    # uid match
                    self.uid_result_excel_copy2.append('Y')
                elif (i == (uid_range - 1)) and '0x0' in self.uid_data_list_copy2[i]:
                    self.uid_result_excel_copy2.append('Y')
                else:
                    # Data, Databar mismatch
                    self.uid_result_excel_copy2.append('D-BAR')
                    if self.uid_result != 0:
                        self.uid_result = 2
            else:
                # Wrong data
                self.uid_result_excel_copy2.append('N')
                self.uid_result = 0
            self.uid_Data_excel_print_copy2.append(self.hex_upper(int(self.uid_data_list_copy2[i], 16)))
            self.uid_Data_bar_excel_print_copy2.append(self.hex_upper(int(self.uid_data_list_bar_copy2[i], 16)))
        # print(self.uid_result_copy2)
        # Copy3
        for i in range(uid_range):
            if self.uid_data_list_copy3[i] in self.uid_expect_data[i]:
                if int(self.uid_data_list_copy3[i], 16) + int(self.uid_data_list_bar_copy3[i], 16) == 255:
                    # uid match
                    self.uid_result_excel_copy3.append('Y')
                elif (i == (uid_range - 1)) and '0x0' in self.uid_data_list_copy3[i]:
                    self.uid_result_excel_copy3.append('Y')
                else:
                    # Data, Databar mismatch
                    self.uid_result_excel_copy3.append('D-BAR')
                    if self.uid_result != 0:
                        self.uid_result = 2
            else:
                # Wrong data
                self.uid_result_excel_copy3.append('N')
                self.uid_result = 0
                # print(self.uid_result_copy3)
            self.uid_Data_excel_print_copy3.append(self.hex_upper(int(self.uid_data_list_copy3[i], 16)))
            self.uid_Data_bar_excel_print_copy3.append(self.hex_upper(int(self.uid_data_list_bar_copy3[i], 16)))

    def stamp_check_result(self):
        self.stamp_die_result = 1
        for stamp_dict_key_element in self.stamp_dict_key_list:
            self.stamp_result = 'Y'
            data_count = 0
            self.stamp_excel_print_die.append(int(self.stamp_dict[stamp_dict_key_element + '_die']))
            self.stamp_excel_print_name.append(self.stamp_dict[stamp_dict_key_element + '_name'])
            self.stamp_excel_print_copy.append(int(self.stamp_dict[stamp_dict_key_element + '_copy']))
            for data_element in self.stamp_dict[stamp_dict_key_element + '_data']:
                self.stamp_excel_print_data.append(self.hex_upper(int(data_element, 16)))
                # Check with expect data
                if self.stamp_dict[stamp_dict_key_element + '_expect'] in 'ALLAA':
                    if data_element not in 'aa':
                        self.stamp_result = 'N'
                        self.stamp_die_result = 0
                if self.stamp_dict[stamp_dict_key_element + '_expect'] in '~ALLFF':
                    if data_element in 'ff':
                        data_count += 1
                        if data_count == 8:
                            self.stamp_result = 'N'
                            self.stamp_die_result = 0
            self.stamp_excel_print_expect.append(self.stamp_dict[stamp_dict_key_element + '_expect'])
            self.stamp_excel_print_match.append(self.stamp_result)

    def stamp_print(self, stamp_line):
        # stamp name
        stamp_title = re_match(r'(.*) COPY (.*) EXPECT (.*)', stamp_line)
        if stamp_title:
            self.stamp_dict_key = stamp_title.group(1) + stamp_title.group(2)
            self.stamp_dict_key_list.append(self.stamp_dict_key)
            self.stamp_dict[self.stamp_dict_key + '_name'] = stamp_title.group(1)
            self.stamp_dict[self.stamp_dict_key + '_copy'] = stamp_title.group(2)
            self.stamp_dict[self.stamp_dict_key + '_expect'] = stamp_title.group(3)
        stamp_address = re_match(r'.*\*\* DIE (.*) BLK (.*) WL (.*) STRING (.*) COLUMN (.*) \*\*.*', stamp_line)
        if stamp_address:
            self.stamp_dict[self.stamp_dict_key + '_die'] = stamp_address.group(1)
            self.stamp_dict[self.stamp_dict_key + '_blk'] = stamp_address.group(2)
            self.stamp_dict[self.stamp_dict_key + '_wl'] = stamp_address.group(3)
            self.stamp_dict[self.stamp_dict_key + '_str'] = stamp_address.group(4)
            self.stamp_dict[self.stamp_dict_key + '_col'] = stamp_address.group(5)
        stamp_data = re_match(r'Data = (.*)h', stamp_line)
        if stamp_data:
            if self.stamp_dict_key + '_data' not in self.stamp_dict:
                self.stamp_dict[self.stamp_dict_key + '_data'] = []
            self.stamp_dict[self.stamp_dict_key + '_data'].append(stamp_data.group(1))

    # dist VT
    # romfuse VT
    def dist_vt_judge_case1(self, dist_x, dist_y):
        """
        self.dist_vt_judge_case1_result = 0
        self.dist_vt_judge_case1_limit1 = 0.7
        self.dist_vt_judge_case1_limit2 = 1.2
        self.dist_vt_judge_case1_limit3 = 1.2
        self.dist_vt_judge_case1_limit4 = 2.1
        self.dist_vt_judge_case1_limit5 = 32
        """
        ignore_bits_low = 0
        ignore_bits_high = 0
        for i, dist_x_element in enumerate(dist_x):
            if self.dist_vt_judge_case1_limit1 < dist_x_element < self.dist_vt_judge_case1_limit2:
                ignore_bits_low += dist_y[i]
            if self.dist_vt_judge_case1_limit3 < dist_x_element < self.dist_vt_judge_case1_limit4:
                ignore_bits_high += dist_y[i]
        if ignore_bits_low <= self.dist_vt_judge_case1_limit5:
            if ignore_bits_high <= self.dist_vt_judge_case1_limit5:
                self.dist_vt_judge_case1_result = 1
        # print("result", self.dist_vt_judge_case1_result)

    # userrom VT
    def dist_vt_judge_case2(self, dist_x, dist_y):
        """
        self.dist_vt_judge_case2_result=0
        self.dist_vt_judge_case2_limit1 = 1.6
        self.dist_vt_judge_case2_limit2 = 2.4
        self.dist_vt_judge_case2_limit3 = 32
        """
        ignore_bits = 0
        for i, dist_x_element in enumerate(dist_x):
            if self.dist_vt_judge_case2_limit1 < dist_x_element < self.dist_vt_judge_case2_limit2:
                ignore_bits += dist_y[i]
        if ignore_bits <= self.dist_vt_judge_case2_limit3:
            self.dist_vt_judge_case2_result = 1

    # flash write good block VT
    def dist_vt_judge_case3(self, dist_x, dist_y):
        """
        self.dist_vt_judge_case3_result=0
        self.dist_vt_judge_case3_limit1 = 0.4
        self.dist_vt_judge_case3_limit2 = 1.8
        """
        # BiCS4 criteria
        if 'BiCs4_256Gb_2P' in self.mt_class[0].mt_design or 'BiCs4_256G_2P' in self.mt_class[0].mt_design:
            self.dist_vt_judge_case3_limit1 = 1.2
            self.dist_vt_judge_case3_limit2 = 2.8
        if 'BiCs4_512Gb_2P' in self.mt_class[0].mt_design or 'BiCs4_512G_2P' in self.mt_class[0].mt_design:
            self.dist_vt_judge_case3_limit1 = 1.2
            self.dist_vt_judge_case3_limit2 = 3.4
        # BiCS4.5 criteria
        if 'BiCs4p5_256Gb_2P' in self.mt_class[0].mt_design or 'BiCs4p5_256G_2P' in self.mt_class[0].mt_design:
            self.dist_vt_judge_case3_limit1 = 2.4
            self.dist_vt_judge_case3_limit2 = 3.6
        if 'BiCs4p5_512Gb_2P' in self.mt_class[0].mt_design or 'BiCs4p5_512G_2P' in self.mt_class[0].mt_design:
            self.dist_vt_judge_case3_limit1 = 2.4
            self.dist_vt_judge_case3_limit2 = 3.6
        # BiCS5 criteria
        if 'BiCs5_512Gb_2P' in self.mt_class[0].mt_design or 'BiCs5_512G_2P' in self.mt_class[0].mt_design:
            self.dist_vt_judge_case3_limit1 = 2.0                                                            #str0 lower vt 2.4 change to 2.0V
            self.dist_vt_judge_case3_limit2 = 3.6
        if 'BiCs5_1024Gb_2P' in self.mt_class[0].mt_design or 'BiCs5_1024G_2P' in self.mt_class[0].mt_design:
            self.dist_vt_judge_case3_limit1 = 2.0
            self.dist_vt_judge_case3_limit2 = 3.6
        peak_voltage = 0
        temp_peak_voltage = 0
        for i, dist_y_element in enumerate(dist_y):
            if temp_peak_voltage <= dist_y_element:
                peak_voltage = dist_x[i]
                temp_peak_voltage = dist_y_element
        if self.dist_vt_judge_case3_limit1 <= peak_voltage <= self.dist_vt_judge_case3_limit2:
            self.dist_vt_judge_case3_result = 1

    # flash write bad block VT
    def dist_vt_judge_case4(self, dist_x, dist_y):
        """
        self.dist_vt_judge_case4_result = 0
        self.dist_vt_judge_case4_limit = 4.0
        """
        # BiCS4 criteria
        if 'BiCs4_256Gb_2P' in self.mt_class[0].mt_design or 'BiCs4_256G_2P' in self.mt_class[0].mt_design:
            self.dist_vt_judge_case4_limit = 2.4
        if 'BiCs4_512Gb_2P' in self.mt_class[0].mt_design or 'BiCs4_512G_2P' in self.mt_class[0].mt_design:
            self.dist_vt_judge_case4_limit = 2.4
        peak_voltage = 0
        temp_peak_voltage = 0
        for i, dist_y_element in enumerate(dist_y):
            if temp_peak_voltage <= dist_y_element:
                peak_voltage = dist_x[i]
                temp_peak_voltage = dist_y_element
        if self.dist_vt_judge_case4_limit <= peak_voltage:
            self.dist_vt_judge_case4_result = 1

    def dist_vt_judge_case5(self, dist_x, dist_y):
        """
        self.dist_vt_judge_case4_result = 0
        self.dist_vt_judge_case4_limit = 4.0
        """
        peak_voltage = 0
        temp_peak_voltage = 0
        for i, dist_y_element in enumerate(dist_y):
            if temp_peak_voltage <= dist_y_element:
                peak_voltage = dist_x[i]
                temp_peak_voltage = dist_y_element
        if self.dist_vt_judge_case5_limit <= peak_voltage:
            self.dist_vt_judge_case5_result = 1

    def dist_vt_xy(self, dist_vt_x, temp_dist_vt_y_cal, dist_vt_y_cal, excel_title, label_title):
        if 'Excel_list' not in self.dist_vt_dict:
            self.dist_vt_dict['Excel_list'] = []
        if excel_title not in self.dist_vt_dict['Excel_list']:
            self.dist_vt_dict['Excel_list'].append(excel_title)
        if excel_title + 'Label_list' not in self.dist_vt_dict:
            self.dist_vt_dict[excel_title + 'Label_list'] = []
        if label_title not in self.dist_vt_dict[excel_title + 'Label_list']:
            self.dist_vt_dict[excel_title + 'Label_list'].append(label_title)
        if float(dist_vt_x) != 6.800:
            if excel_title + label_title + '_X' not in self.dist_vt_dict:
                self.dist_vt_dict[excel_title + label_title + '_X'] = []
            self.dist_vt_dict[excel_title + label_title + '_X'].append(float(dist_vt_x))
        if excel_title + label_title + '_Y' not in self.dist_vt_dict:
            self.dist_vt_dict[excel_title + label_title + '_Y'] = []
        self.dist_vt_dict[excel_title + label_title + '_Y'].append(abs(int(temp_dist_vt_y_cal) - int(dist_vt_y_cal)))
    # 3 KEYS in dist_vt_dict: Excel_list(excel title list), Label_list: list of excel title_label list. tit, Result/title list
    def dist_vt_result(self):
        for excel_list_element in self.dist_vt_dict['Excel_list']:
            # print(excel_list_element)
            if (excel_list_element + '_Result') not in self.dist_vt_dict:
                self.dist_vt_dict[excel_list_element + '_Result'] = 'PASS'
            for label_list_element in self.dist_vt_dict[excel_list_element + 'Label_list']:
                if excel_list_element in 'UROM VT':
                    self.dist_vt_judge_case2(self.dist_vt_dict[excel_list_element + label_list_element + '_X'],
                                             self.dist_vt_dict[excel_list_element + label_list_element + '_Y'])
                    self.dist_vt_dict[excel_list_element + label_list_element + '_Result'] = \
                        self.dist_vt_judge_case2_result
                    if self.dist_vt_judge_case2_result != 1:
                        self.dist_vt_dict[excel_list_element + '_Result'] = 'FAIL'
                    self.dist_vt_dict[excel_list_element + '_Title'] = 'Userrom VT'
                    self.dist_vt_dict[
                        excel_list_element + '_Comment'] = 'PASS condition : Less than ' + str(
                        self.dist_vt_judge_case2_limit3) + 'bits ignore between ' + str(
                        self.dist_vt_judge_case2_limit1) + 'V and ' + str(self.dist_vt_judge_case2_limit2) + 'V'
                if excel_list_element in 'ROM VT':
                    self.dist_vt_judge_case1(self.dist_vt_dict[excel_list_element + label_list_element + '_X'],
                                             self.dist_vt_dict[excel_list_element + label_list_element + '_Y'])
                    self.dist_vt_dict[excel_list_element + label_list_element + '_Result'] = \
                        self.dist_vt_judge_case1_result
                    if self.dist_vt_judge_case1_result != 1:
                        self.dist_vt_dict[excel_list_element + '_Result'] = 'FAIL'
                    self.dist_vt_dict[excel_list_element + '_Title'] = 'Romfuse VT'
                    self.dist_vt_dict[excel_list_element + '_Comment'] = \
                        'PASS condition : Less than ' + str(self.dist_vt_judge_case1_limit5) + 'bits ignore between ' + \
                        str(self.dist_vt_judge_case1_limit1) + 'V and ' + str(self.dist_vt_judge_case1_limit2) + \
                        'V, Less than ' + str(self.dist_vt_judge_case1_limit5) + 'bits ignore between ' + \
                        str(self.dist_vt_judge_case1_limit3) + 'V and ' + str(self.dist_vt_judge_case1_limit4) + 'V'

                if excel_list_element in 'FW GB VT':
                    self.dist_vt_judge_case3(self.dist_vt_dict[excel_list_element + label_list_element + '_X'],
                                             self.dist_vt_dict[excel_list_element + label_list_element + '_Y'])
                    self.dist_vt_dict[
                        excel_list_element + label_list_element + '_Result'] = self.dist_vt_judge_case3_result
                    if self.dist_vt_judge_case3_result != 1:
                        self.dist_vt_dict[excel_list_element + '_Result'] = 'FAIL'
                    self.dist_vt_dict[excel_list_element + '_Title'] = 'Flash Write Good Block VT'
                    self.dist_vt_dict[
                        excel_list_element + '_Comment'] = \
                        'PASS condition : Peak dist voltage is between ' + str(self.dist_vt_judge_case3_limit1) + \
                        'V to ' + str(self.dist_vt_judge_case3_limit2) + 'V'
                if excel_list_element in 'FW BB VT':
                    self.dist_vt_judge_case4(self.dist_vt_dict[excel_list_element + label_list_element + '_X'],
                                             self.dist_vt_dict[excel_list_element + label_list_element + '_Y'])
                    self.dist_vt_dict[
                        excel_list_element + label_list_element + '_Result'] = self.dist_vt_judge_case4_result
                    if self.dist_vt_judge_case4_result != 1:
                        self.dist_vt_dict[excel_list_element + '_Result'] = 'FAIL'
                    self.dist_vt_dict[excel_list_element + '_Title'] = 'Flash Write Bad Block VT'
                    self.dist_vt_dict[excel_list_element + '_Comment'] = \
                        'PASS condition : Peak dist voltage is higher than ' + str(self.dist_vt_judge_case4_limit) + 'V'
                if excel_list_element in 'DUMMY WL VT':
                    self.dist_vt_judge_case5(self.dist_vt_dict[excel_list_element + label_list_element + '_X'],
                                             self.dist_vt_dict[excel_list_element + label_list_element + '_Y'])
                    self.dist_vt_dict[
                        excel_list_element + label_list_element + '_Result'] = self.dist_vt_judge_case4_result
                    if self.dist_vt_judge_case5_result != 1:
                        self.dist_vt_dict[excel_list_element + '_Result'] = 'Monitor'
                    self.dist_vt_dict[excel_list_element + '_Title'] = 'Dummy WL VT'
                    self.dist_vt_dict[excel_list_element + '_Comment'] = \
                        'PASS condition : Peak dist voltage is higher than ' + str(self.dist_vt_judge_case5_limit) + 'V'

    # trim
    def trim_userrom_input(self, trim_userrom_addr, trim_userrom_value):
        self.trim_userrom_addr_list.append(trim_userrom_addr)
        self.trim_userrom_value_list.append(trim_userrom_value)

    def trim_romfuse_input(self, trim_romfuse_addr, trim_romfuse_value):
        self.trim_romfuse_addr_list.append(trim_romfuse_addr)
        self.trim_romfuse_value_list.append(trim_romfuse_value)

    def trim_check(self, trim_version_name, trim_class):
        self.trim_version_uid = trim_version_name
        # trim version loop
        for trim_class_element in trim_class:
            # trim version exist
            if trim_class_element.name in trim_version_name:
                self.trim_version_match = True
                # Address loop
                for trim_addr in trim_class_element.address_dict:
                    # print(self.name, trim_addr, trim_addr.split('_')[1])
                    if self.name == trim_addr.split('_')[0]:
                        # Start address(0x10) --> 0 for index
                        # print(trim_class_element.address_dict)
                        inc = int(trim_addr.split('_')[1], 16) - 16
                        # print(trim_addr, inc, trim_class_element.original_value_dict[trim_addr], trim_class_element.fix_or_trim_dict[trim_addr])
                        if self.hex_upper(int(trim_addr.split('_')[1], 16)) not in self.trim_excel_Addr:
                            self.trim_excel_Addr.append(self.hex_upper(int(trim_addr.split('_')[1], 16)))
                        # trim(Shift)
                        # print(inc, trim_class_element.fix_or_trim_dict)
                        if int(trim_class_element.fix_or_trim_dict[trim_addr], 10) == 1:
                            shift_result = hex(int(self.trim_userrom_value_list[inc], 16) + int(
                                trim_class_element.trim_shift_dict[trim_addr], 10))               #fix dac dec
                            self.trim_cal.append(shift_result)
                            if int(shift_result, 16) == int(self.trim_romfuse_value_list[inc], 16):
                                # trim match
                                self.trim_excel_result.append('Y')
                                self.trim_result = 1
                            else:
                                # trim mismatch
                                self.trim_excel_result.append('N')
                                self.trim_result = 0
                                self.trim_result_acc = 0
                            # Append to list for excel
                            self.trim_excel_romfuse.append(self.hex_upper(int(self.trim_romfuse_value_list[inc], 16)))
                            self.trim_excel_userrom.append(self.hex_upper(int(self.trim_userrom_value_list[inc], 16)))
                            self.trim_excel_original.append('')
                            self.trim_excel_setparmmask_value.append('')
                            self.trim_excel_mask.append('')
                            #self.trim_excel_shift.append(self.hex_upper(int(trim_class_element.trim_shift_dict[trim_addr], 16)))
                            self.trim_excel_shift.append(trim_class_element.trim_shift_dict[trim_addr])
                        # special trim Case 10
                        elif int(trim_class_element.fix_or_trim_dict[trim_addr], 10) == 10:
                            special10_mask = (int(self.trim_userrom_value_list[inc], 16)) & 56
                            # print('incoming:', inc, self.hex_upper(inc), self.trim_userrom_value_list[inc])
                            if special10_mask == 56:
                                shift_value = -56
                                shift_result = hex(int(self.trim_userrom_value_list[inc], 16) + shift_value)
                                # print('1:',shift_result)
                            elif special10_mask != 24 and special10_mask != 32:
                                shift_value = 8
                                shift_result = hex(int(self.trim_userrom_value_list[inc], 16) + shift_value)
                                # print('2:',shift_result)
                            else:
                                shift_value = 0
                                shift_result = hex(int(self.trim_userrom_value_list[inc], 16) + shift_value)
                            # print('3:',shift_result)
                            self.trim_cal.append(shift_result)
                            if int(shift_result, 16) == int(self.trim_romfuse_value_list[inc], 16):
                                # trim match
                                self.trim_excel_result.append('Y')
                                self.trim_result = 1
                            else:
                                # trim mismatch
                                self.trim_excel_result.append('N')
                                self.trim_result = 0
                                self.trim_result_acc = 0
                            # Append for excel
                            self.trim_excel_romfuse.append(self.hex_upper(int(self.trim_romfuse_value_list[inc], 16)))
                            self.trim_excel_userrom.append(self.hex_upper(int(self.trim_userrom_value_list[inc], 16)))
                            self.trim_excel_original.append('')
                            self.trim_excel_setparmmask_value.append('')
                            self.trim_excel_mask.append('')
                            self.trim_excel_shift.append(self.hex_upper(shift_value))
                        # special trim Case 11
                        elif int(trim_class_element.fix_or_trim_dict[trim_addr], 10) == 11:
                            special11_mask = (int(self.trim_userrom_value_list[inc], 16)) & 7
                            # print('incoming:', self.trim_userrom_value_list[inc])
                            if special11_mask == 7:
                                shift_value = -7
                                shift_result = hex(int(self.trim_userrom_value_list[inc], 16) + shift_value)
                                # print('1:',shift_result)
                            elif special11_mask != 3 and special11_mask != 4:
                                shift_value = 1
                                shift_result = hex(int(self.trim_userrom_value_list[inc], 16) + shift_value)
                                # print('2:',shift_result)
                            else:
                                shift_value = 0
                                shift_result = hex(int(self.trim_userrom_value_list[inc], 16) + shift_value)
                            # print('3:',shift_result)
                            self.trim_cal.append(shift_result)
                            if int(shift_result, 16) == int(self.trim_romfuse_value_list[inc], 16):
                                # trim match
                                self.trim_excel_result.append('Y')
                                self.trim_result = 1
                            else:
                                # trim mismatch
                                self.trim_excel_result.append('N')
                                self.trim_result = 0
                                self.trim_result_acc = 0
                            # Append for excel
                            self.trim_excel_romfuse.append(self.hex_upper(int(self.trim_romfuse_value_list[inc], 16)))
                            self.trim_excel_userrom.append(self.hex_upper(int(self.trim_userrom_value_list[inc], 16)))
                            self.trim_excel_original.append('')
                            self.trim_excel_setparmmask_value.append('')
                            self.trim_excel_mask.append('')
                            self.trim_excel_shift.append(self.hex_upper(shift_value))
                        # special trim Case 12
                        elif int(trim_class_element.fix_or_trim_dict[trim_addr], 10) == 12:
                            special12_mask = (int(self.trim_userrom_value_list[inc], 16)) & 224
                            # print('incoming:', self.trim_userrom_value_list[inc])
                            if special12_mask == 224:
                                shift_value = -224
                                shift_result = hex(int(self.trim_userrom_value_list[inc], 16) + shift_value)
                                # print('1:',shift_result)
                            elif special12_mask != 96 and special12_mask != 128:
                                shift_value = 32
                                shift_result = hex(int(self.trim_userrom_value_list[inc], 16) + shift_value)
                                # print('2:',shift_result)
                            else:
                                shift_value = 0
                                shift_result = hex(int(self.trim_userrom_value_list[inc], 16) + shift_value)
                            # print('3:',shift_result)
                            self.trim_cal.append(shift_result)
                            if int(shift_result, 16) == int(self.trim_romfuse_value_list[inc], 16):
                                # trim match
                                self.trim_excel_result.append('Y')
                                self.trim_result = 1
                            else:
                                # trim mismatch
                                self.trim_excel_result.append('N')
                                self.trim_result = 0
                                self.trim_result_acc = 0
                            # Append for excel
                            self.trim_excel_romfuse.append(self.hex_upper(int(self.trim_romfuse_value_list[inc], 16)))
                            self.trim_excel_userrom.append(self.hex_upper(int(self.trim_userrom_value_list[inc], 16)))
                            self.trim_excel_original.append('')
                            self.trim_excel_setparmmask_value.append('')
                            self.trim_excel_mask.append('')
                            self.trim_excel_shift.append(self.hex_upper(shift_value))
                        # special trim Case 20
                        elif int(trim_class_element.fix_or_trim_dict[trim_addr], 10) == 20:
                            """
                            original_mask = int(trim_class_element.original_value_dict[trim_addr], 16) & \
                                            int(trim_class_element.trim_mask_dict[trim_addr], 16)
                            romfuse_mask = int(self.trim_romfuse_value_list[inc], 16) & int(
                                trim_class_element.trim_mask_dict[trim_addr], 16)
                            setparmmask_result = (original_mask &
                                                  (~int(trim_class_element.trim_mask_dict[trim_addr], 16))) | \
                                                 (int(trim_class_element.trim_value_dict[trim_addr], 16) &
                                                  int(trim_class_element.trim_mask_dict[trim_addr], 16))
                            self.trim_cal.append(setparmmask_result)

                            # mask
                            reverse_mask = 255 - int(trim_class_element.trim_mask_dict[trim_addr], 16)
                            userrom_mask = int(self.trim_userrom_value_list[inc], 16) & reverse_mask
                            romfuse_mask = int(self.trim_romfuse_value_list[inc], 16) & reverse_mask
                            shift_result = hex(userrom_mask + int(trim_class_element.trim_shift_dict[trim_addr], 16))
                            # self.trim_cal.append(shift_result)
                            # print(self.hex_upper(inc + 16), int(shift_result, 16), romfuse_mask)
                            """
                            # setparm cal
                            #print(trim_addr,int(self.trim_userrom_value_list[inc], 16),int(trim_class_element.trim_shift_dict[trim_addr], 10))
                            setparmmask_result = (int(self.trim_userrom_value_list[inc], 16) &
                                                  (~int(trim_class_element.trim_mask_dict[trim_addr], 16))) | \
                                                 (int(trim_class_element.trim_value_dict[trim_addr], 16) &
                                                  int(trim_class_element.trim_mask_dict[trim_addr], 16))
                            #print('debug2', setparmmask_result, int(trim_class_element.trim_mask_dict[trim_addr], 16))
                            setparmmask_result_masking = setparmmask_result & \
                                                         int(trim_class_element.trim_mask_dict[trim_addr], 16)
                            # shift cal
                            reverse_mask = 255 - int(trim_class_element.trim_mask_dict[trim_addr], 16)
                            #print(int(self.trim_userrom_value_list[inc], 16))
                            userrom_mask = int(self.trim_userrom_value_list[inc], 16) & reverse_mask
                            shift_result = userrom_mask + int(trim_class_element.trim_shift_dict[trim_addr], 10)  #fix by Maurice

                            # result
                            result_trim_cal = setparmmask_result_masking | shift_result
                            #print(trim_addr,hex(result_trim_cal))
                            self.trim_cal.append(result_trim_cal)

                            if result_trim_cal == int(self.trim_romfuse_value_list[inc], 16):
                                # trim match
                                self.trim_excel_result.append('Y')
                                self.trim_result = 1
                            else:
                                # trim mismatch
                                self.trim_excel_result.append('N')
                                self.trim_result = 0
                                self.trim_result_acc = 0
                                # print('debug', trim_addr, '#', result_trim_cal, '#', int(self.trim_romfuse_value_list[inc], 16), setparmmask_result_masking, shift_result, int(self.trim_userrom_value_list[inc], 16), reverse_mask)
                            # Append for excel
                            self.trim_excel_romfuse.append(self.hex_upper(int(self.trim_romfuse_value_list[inc], 16)))
                            self.trim_excel_userrom.append(self.hex_upper(int(self.trim_userrom_value_list[inc], 16)))
                            self.trim_excel_original.append(
                                self.hex_upper(int(trim_class_element.original_value_dict[trim_addr], 16)))
                            self.trim_excel_setparmmask_value.append(
                                self.hex_upper(int(trim_class_element.trim_value_dict[trim_addr], 16)))
                            self.trim_excel_mask.append(self.hex_upper(int(trim_class_element.trim_mask_dict[trim_addr], 16)))
                            #self.trim_excel_shift.append(self.hex_upper(int(trim_class_element.trim_shift_dict[trim_addr], 16)))
                            self.trim_excel_shift.append(trim_class_element.trim_shift_dict[trim_addr])
                        # special trim Case 21
                        elif int(trim_class_element.fix_or_trim_dict[trim_addr], 10) == 21:
                            special21_mask = (int(self.trim_userrom_value_list[inc], 16)) & 7
                            special_not_mask = int(self.trim_userrom_value_list[inc], 16) - special21_mask
                            shift_value = 0
                            if special21_mask == 4:
                                shift_result = hex(4 + special_not_mask)
                            elif special21_mask == 0:
                                shift_result = hex(7 + special_not_mask)
                            else:
                                shift_value = -1
                                shift_result = hex(int(self.trim_userrom_value_list[inc], 16) + shift_value)
                            self.trim_cal.append(shift_result)
                            if int(shift_result, 16) == int(self.trim_romfuse_value_list[inc], 16):
                                # trim match
                                self.trim_excel_result.append('Y')
                                self.trim_result = 1
                            else:
                                # trim mismatch
                                self.trim_excel_result.append('N')
                                self.trim_result = 0
                                self.trim_result_acc = 0
                            # Append for excel
                            self.trim_excel_romfuse.append(self.hex_upper(int(self.trim_romfuse_value_list[inc], 16)))
                            self.trim_excel_userrom.append(self.hex_upper(int(self.trim_userrom_value_list[inc], 16)))
                            self.trim_excel_original.append('')
                            self.trim_excel_setparmmask_value.append('')
                            self.trim_excel_mask.append('')
                            self.trim_excel_shift.append(self.hex_upper(shift_value))
                        # special trim Case 22
                        elif int(trim_class_element.fix_or_trim_dict[trim_addr], 10) == 22:
                            special22_mask = (int(self.trim_userrom_value_list[inc], 16)) & 7
                            special_not_mask = int(self.trim_userrom_value_list[inc], 16) - special22_mask
                            shift_value = 0
                            if special22_mask == 7:
                                shift_result = hex(7 + special_not_mask)
                            elif special22_mask == 0:
                                shift_result = hex(7 + special_not_mask)
                            else:
                                shift_value = -1
                                shift_result = hex(int(self.trim_userrom_value_list[inc], 16) + shift_value)
                            # print('3:',shift_result)
                            self.trim_cal.append(shift_result)
                            if int(shift_result, 16) == int(self.trim_romfuse_value_list[inc], 16):
                                # trim match
                                self.trim_excel_result.append('Y')
                                self.trim_result = 1
                            else:
                                # trim mismatch
                                self.trim_excel_result.append('N')
                                self.trim_result = 0
                                self.trim_result_acc = 0
                            # Append for excel
                            self.trim_excel_romfuse.append(self.hex_upper(int(self.trim_romfuse_value_list[inc], 16)))
                            self.trim_excel_userrom.append(self.hex_upper(int(self.trim_userrom_value_list[inc], 16)))
                            self.trim_excel_original.append('')
                            self.trim_excel_setparmmask_value.append('')
                            self.trim_excel_mask.append('')
                            self.trim_excel_shift.append(self.hex_upper(shift_value))
                        # special trim Case 23
                        elif int(trim_class_element.fix_or_trim_dict[trim_addr], 10) == 23:
                            # addr 52
                            special23_mask = (int(self.trim_userrom_value_list[inc], 16)) & int('0x20', 16)
                            special_not_mask = int(self.trim_userrom_value_list[inc], 16) - special23_mask
                            inc_55 = int('0x55', 16) - 16
                            # addr 55
                            addr55_mask_value = (int(self.trim_userrom_value_list[inc_55], 16)) & int('0x38', 16)
                            shift_value = 0
                            # if addr 52[5] == 1
                            if special23_mask == int('0x20', 16):
                                shift_value = -int('0x20', 16)
                                shift_result = hex(int(self.trim_userrom_value_list[inc], 16) + shift_value)
                            elif addr55_mask_value == int('0x20', 16):
                                shift_value = int('0x0', 16)
                                shift_result = hex(int(self.trim_userrom_value_list[inc], 16) + shift_value)
                            else:
                                shift_value = int('0x20', 16)
                                shift_result = hex(int(self.trim_userrom_value_list[inc], 16) + shift_value)
                            # print('3:',shift_result)
                            self.trim_cal.append(shift_result)
                            if int(shift_result, 16) == int(self.trim_romfuse_value_list[inc], 16):
                                # trim match
                                self.trim_excel_result.append('Y')
                                self.trim_result = 1
                            else:
                                # trim mismatch
                                self.trim_excel_result.append('N')
                                self.trim_result = 0
                                self.trim_result_acc = 0
                            # Append for excel
                            self.trim_excel_romfuse.append(self.hex_upper(int(self.trim_romfuse_value_list[inc], 16)))
                            self.trim_excel_userrom.append(self.hex_upper(int(self.trim_userrom_value_list[inc], 16)))
                            self.trim_excel_original.append('')
                            self.trim_excel_setparmmask_value.append('')
                            self.trim_excel_mask.append('')
                            self.trim_excel_shift.append(self.hex_upper(shift_value))
                        # special trim Case 24
                        elif int(trim_class_element.fix_or_trim_dict[trim_addr], 10) == 24:
                            special24_mask = (int(self.trim_userrom_value_list[inc], 16)) & int('0x38', 16)
                            special_not_mask = int(self.trim_userrom_value_list[inc], 16) - special24_mask
                            inc_52 = int('0x52', 16) - 16
                            addr52_mask_value = (int(self.trim_userrom_value_list[inc_52], 16)) & int('0x20', 16)
                            shift_value = 0
                            # address 55[3:5] == 1000, address 52[5] == 0 --> no change
                            if special24_mask == int('0x20', 16) & addr52_mask_value == 0:
                                shift_value = 0
                                shift_result = hex(int(self.trim_userrom_value_list[inc], 16) + shift_value)
                            # address 55[3:5] == 0000, address 52[5] == 0 --> +38 DAC
                            elif (special24_mask == 00) & (addr52_mask_value == 0):
                                shift_value = int('0x38', 16)
                                shift_result = hex(int(self.trim_userrom_value_list[inc], 16) + shift_value)
                            # address 52[5] == 0 --> -8 DAC
                            elif addr52_mask_value == 0:
                                shift_value = -int('0x08', 16)
                                shift_result = hex(int(self.trim_userrom_value_list[inc], 16) + shift_value)
                            # address 52[5] == 1 --> no change
                            else:
                                shift_value = 0
                                shift_result = hex(int(self.trim_userrom_value_list[inc], 16) + shift_value)
                            # print('3:',shift_value, self.trim_userrom_value_list[inc_52], addr52_mask_value, shift_result)
                            self.trim_cal.append(shift_result)
                            if int(shift_result, 16) == int(self.trim_romfuse_value_list[inc], 16):
                                # trim match
                                self.trim_excel_result.append('Y')
                                self.trim_result = 1
                            else:
                                # trim mismatch
                                self.trim_excel_result.append('N')
                                self.trim_result = 0
                                self.trim_result_acc = 0
                            # Append for excel
                            self.trim_excel_romfuse.append(self.hex_upper(int(self.trim_romfuse_value_list[inc], 16)))
                            self.trim_excel_userrom.append(self.hex_upper(int(self.trim_userrom_value_list[inc], 16)))
                            self.trim_excel_original.append('')
                            self.trim_excel_setparmmask_value.append('')
                            self.trim_excel_mask.append('')
                            self.trim_excel_shift.append(self.hex_upper(shift_value))
                        # special trim Case 25
                        elif int(trim_class_element.fix_or_trim_dict[trim_addr], 10) == 25:
                            inc_e7 = int('0xE6', 16) - 16
                            addr_e7_mask_value = (int(self.trim_userrom_value_list[inc_e7], 16)) & int('0x80', 16)
                            shift_value = 0
                            # address E7[7] == 0 then + 2. DAC
                            if addr_e7_mask_value == 0:
                                shift_value = 2
                                shift_result = hex(int(self.trim_userrom_value_list[inc], 16) + shift_value)
                            # address E7[7] == 1 then + 1. DAC
                            elif addr_e7_mask_value == 128:
                                shift_value = 1
                                shift_result = hex(int(self.trim_userrom_value_list[inc], 16) + shift_value)
                            else:
                                shift_value = 0
                                print("ERROR!!!")
                                shift_result = hex(int(self.trim_userrom_value_list[inc], 16) + shift_value)
                            # print('3:',shift_value, self.trim_userrom_value_list[inc_e7], addr_e7_mask_value, shift_result)
                            self.trim_cal.append(shift_result)
                            if int(shift_result, 16) == int(self.trim_romfuse_value_list[inc], 16):
                                # trim match
                                self.trim_excel_result.append('Y')
                                self.trim_result = 1
                            else:
                                # trim mismatch
                                self.trim_excel_result.append('N')
                                self.trim_result = 0
                                self.trim_result_acc = 0
                            # Append for excel
                            self.trim_excel_romfuse.append(self.hex_upper(int(self.trim_romfuse_value_list[inc], 16)))
                            self.trim_excel_userrom.append(self.hex_upper(int(self.trim_userrom_value_list[inc], 16)))
                            self.trim_excel_original.append('')
                            self.trim_excel_setparmmask_value.append('')
                            self.trim_excel_mask.append('')
                            self.trim_excel_shift.append(self.hex_upper(shift_value))
                        # special trim Case 26
                        elif int(trim_class_element.fix_or_trim_dict[trim_addr], 10) == 26:
                            special25_mask = (int(self.trim_userrom_value_list[inc], 16)) & int('0x40', 16)
                            inc_e7 = int('0xE6', 16) - 16
                            addr_e7_mask_value = (int(self.trim_userrom_value_list[inc_e7], 16)) & int('0x40', 16)
                            shift_value = 0
                            # address E7[6] == 0 then - 1. DAC
                            if addr_e7_mask_value == 0:
                                shift_value = -1
                                shift_result = hex(int(self.trim_userrom_value_list[inc], 16) + shift_value)
                            # address E7[6] == 1 then - 3. DAC
                            elif addr_e7_mask_value == 64:
                                shift_value = -3
                                shift_result = hex(int(self.trim_userrom_value_list[inc], 16) + shift_value)
                            else:
                                shift_value = 0
                                print("ERROR!!!")
                                shift_result = hex(int(self.trim_userrom_value_list[inc], 16) + shift_value)
                            # print('3:',shift_value, self.trim_userrom_value_list[inc_e7], addr_e7_mask_value, shift_result)
                            self.trim_cal.append(shift_result)
                            if int(shift_result, 16) == int(self.trim_romfuse_value_list[inc], 16):
                                # trim match
                                self.trim_excel_result.append('Y')
                                self.trim_result = 1
                            else:
                                # trim mismatch
                                self.trim_excel_result.append('N')
                                self.trim_result = 0
                                self.trim_result_acc = 0
                            # Append for excel
                            self.trim_excel_romfuse.append(self.hex_upper(int(self.trim_romfuse_value_list[inc], 16)))
                            self.trim_excel_userrom.append(self.hex_upper(int(self.trim_userrom_value_list[inc], 16)))
                            self.trim_excel_original.append('')
                            self.trim_excel_setparmmask_value.append('')
                            self.trim_excel_mask.append('')
                            self.trim_excel_shift.append(self.hex_upper(shift_value))
                        # special trim Case 27
                        elif int(trim_class_element.fix_or_trim_dict[trim_addr], 10) == 27:
                            special25_mask = (int(self.trim_userrom_value_list[inc], 16)) & int('0x80', 16)
                            inc_e7 = int('0xE7', 16) - 16
                            addr_e7_mask_value = (int(self.trim_userrom_value_list[inc_e7], 16)) & int('0x80', 16)
                            shift_value = 0
                            # address E7[7] == 0 then + 2. DAC
                            if addr_e7_mask_value == 0:
                                shift_value = 0
                                shift_result = hex(int(self.trim_userrom_value_list[inc], 16) + shift_value)
                            # address E7[7] == 1 then + 1. DAC
                            elif addr_e7_mask_value == 128:
                                shift_value = -3
                                shift_result = hex(int(self.trim_userrom_value_list[inc], 16) + shift_value)
                            else:
                                shift_value = 0
                                print("ERROR!!!")
                                shift_result = hex(int(self.trim_userrom_value_list[inc], 16) + shift_value)
                            # print('3:',shift_value, self.trim_userrom_value_list[inc_e7], addr_e7_mask_value, shift_result)
                            self.trim_cal.append(shift_result)
                            if int(shift_result, 16) == int(self.trim_romfuse_value_list[inc], 16):
                                # trim match
                                self.trim_excel_result.append('Y')
                                self.trim_result = 1
                            else:
                                # trim mismatch
                                self.trim_excel_result.append('N')
                                self.trim_result = 0
                                self.trim_result_acc = 0
                            # Append for excel
                            self.trim_excel_romfuse.append(self.hex_upper(int(self.trim_romfuse_value_list[inc], 16)))
                            self.trim_excel_userrom.append(self.hex_upper(int(self.trim_userrom_value_list[inc], 16)))
                            self.trim_excel_original.append('')
                            self.trim_excel_setparmmask_value.append('')
                            self.trim_excel_mask.append('')
                            self.trim_excel_shift.append(self.hex_upper(shift_value))
                        # special trim Case 28
                        elif int(trim_class_element.fix_or_trim_dict[trim_addr], 10) == 28:
                            special25_mask = (int(self.trim_userrom_value_list[inc], 16)) & int('0x40', 16)
                            inc_e7 = int('0xE7', 16) - 16
                            addr_e7_mask_value = (int(self.trim_userrom_value_list[inc_e7], 16)) & int('0x40', 16)
                            shift_value = 0
                            # address E7[6] == 0 then - 1. DAC
                            if addr_e7_mask_value == 0:
                                shift_value = -4
                                shift_result = hex(int(self.trim_userrom_value_list[inc], 16) + shift_value)
                            # address E7[6] == 1 then - 3. DAC
                            elif addr_e7_mask_value == 64:
                                shift_value = -7
                                shift_result = hex(int(self.trim_userrom_value_list[inc], 16) + shift_value)
                            else:
                                shift_value = 0
                                print("ERROR!!!")
                                shift_result = hex(int(self.trim_userrom_value_list[inc], 16) + shift_value)
                            # print('3:',shift_value, self.trim_userrom_value_list[inc_e7], addr_e7_mask_value, shift_result)
                            self.trim_cal.append(shift_result)
                            if int(shift_result, 16) == int(self.trim_romfuse_value_list[inc], 16):
                                # trim match
                                self.trim_excel_result.append('Y')
                                self.trim_result = 1
                            else:
                                # trim mismatch
                                self.trim_excel_result.append('N')
                                self.trim_result = 0
                                self.trim_result_acc = 0
                            # Append for excel
                            self.trim_excel_romfuse.append(self.hex_upper(int(self.trim_romfuse_value_list[inc], 16)))
                            self.trim_excel_userrom.append(self.hex_upper(int(self.trim_userrom_value_list[inc], 16)))
                            self.trim_excel_original.append('')
                            self.trim_excel_setparmmask_value.append('')
                            self.trim_excel_mask.append('')
                            self.trim_excel_shift.append(self.hex_upper(shift_value))
                        # special trim Case 29
                        elif int(trim_class_element.fix_or_trim_dict[trim_addr], 10) == 29:
                            special25_mask = (int(self.trim_userrom_value_list[inc], 16)) & int('0x40', 16)
                            inc_e6 = int('0xE6', 16) - 16
                            addr_e6_mask_value = (int(self.trim_userrom_value_list[inc_e6], 16)) & int('0x40', 16)
                            shift_value = 0
                            # address E7[6] == 0 then - 1. DAC
                            if addr_e6_mask_value == 0:
                                shift_value = -1
                                shift_result = hex(int(self.trim_userrom_value_list[inc], 16) + shift_value)
                            # address E7[6] == 1 then - 2. DAC
                            elif addr_e6_mask_value == 64:
                                shift_value = -2
                                shift_result = hex(int(self.trim_userrom_value_list[inc], 16) + shift_value)
                            else:
                                shift_value = 0
                                print("ERROR!!!")
                                shift_result = hex(int(self.trim_userrom_value_list[inc], 16) + shift_value)
                            # print('3:',shift_value, self.trim_userrom_value_list[inc_e6], addr_e6_mask_value, shift_result)
                            self.trim_cal.append(shift_result)
                            if int(shift_result, 16) == int(self.trim_romfuse_value_list[inc], 16):
                                # trim match
                                self.trim_excel_result.append('Y')
                                self.trim_result = 1
                            else:
                                # trim mismatch
                                self.trim_excel_result.append('N')
                                self.trim_result = 0
                                self.trim_result_acc = 0
                            # Append for excel
                            self.trim_excel_romfuse.append(self.hex_upper(int(self.trim_romfuse_value_list[inc], 16)))
                            self.trim_excel_userrom.append(self.hex_upper(int(self.trim_userrom_value_list[inc], 16)))
                            self.trim_excel_original.append('')
                            self.trim_excel_setparmmask_value.append('')
                            self.trim_excel_mask.append('')
                            self.trim_excel_shift.append(self.hex_upper(shift_value))
                        # special 30
                        elif int(trim_class_element.fix_or_trim_dict[trim_addr], 10) == 30:
                            # addr 52
                            special23_mask = (int(self.trim_userrom_value_list[inc], 16)) & int('0x20', 16)
                            special_not_mask = int(self.trim_userrom_value_list[inc], 16) - special23_mask
                            inc_55 = int('0x55', 16) - 16
                            # addr 55
                            addr55_mask_value = (int(self.trim_userrom_value_list[inc_55], 16)) & int('0x38', 16)
                            shift_value = 0
                            # if addr 52[5] == 0 --> Change it to 1
                            if special23_mask == int('0x0', 16):
                                shift_value = int('0x20', 16)
                                shift_result = hex(int(self.trim_userrom_value_list[inc], 16) + shift_value)
                            # if addr52[5] == 1 -->
                            elif addr55_mask_value == int('0x18', 16):
                                shift_value = int('0x0', 16)
                                shift_result = hex(int(self.trim_userrom_value_list[inc], 16) + shift_value)
                            else:
                                shift_value = -int('0x20', 16)
                                shift_result = hex(int(self.trim_userrom_value_list[inc], 16) + shift_value)
                            # print('3:',shift_result)
                            self.trim_cal.append(shift_result)
                            if int(shift_result, 16) == int(self.trim_romfuse_value_list[inc], 16):
                                # trim match
                                self.trim_excel_result.append('Y')
                                self.trim_result = 1
                            else:
                                # trim mismatch
                                self.trim_excel_result.append('N')
                                self.trim_result = 0
                                self.trim_result_acc = 0
                            # Append for excel
                            self.trim_excel_romfuse.append(self.hex_upper(int(self.trim_romfuse_value_list[inc], 16)))
                            self.trim_excel_userrom.append(self.hex_upper(int(self.trim_userrom_value_list[inc], 16)))
                            self.trim_excel_original.append('')
                            self.trim_excel_setparmmask_value.append('')
                            self.trim_excel_mask.append('')
                            self.trim_excel_shift.append(self.hex_upper(shift_value))
                        # special trim Case 31
                        elif int(trim_class_element.fix_or_trim_dict[trim_addr], 10) == 31:
                            special24_mask = (int(self.trim_userrom_value_list[inc], 16)) & int('0x38', 16)
                            special_not_mask = int(self.trim_userrom_value_list[inc], 16) - special24_mask
                            inc_52 = int('0x52', 16) - 16
                            addr52_mask_value = (int(self.trim_userrom_value_list[inc_52], 16)) & int('0x20', 16)
                            shift_value = 0
                            # address 55[3:5] == 0111, address 52[5] == 0 --> no change
                            if (special24_mask == int('0x18', 16)) & (addr52_mask_value == int('0x20', 16)):
                                shift_value = 0
                                shift_result = hex(int(self.trim_userrom_value_list[inc], 16) + shift_value)
                            # address 55[3:5] == 1111, address 52[5] == 1 --> -0x38 DAC
                            elif (special24_mask == int('0x38', 16)) & (addr52_mask_value == int('0x20', 16)):
                                shift_value = -int('0x38', 16)
                                shift_result = hex(int(self.trim_userrom_value_list[inc], 16) + shift_value)
                            # address 52[5] == 1 --> +0x8 DAC
                            elif addr52_mask_value == int('0x20', 16):
                                shift_value = int('0x08', 16)
                                shift_result = hex(int(self.trim_userrom_value_list[inc], 16) + shift_value)
                            # address 52[5] == 0 --> no change
                            else:
                                shift_value = 0
                                shift_result = hex(int(self.trim_userrom_value_list[inc], 16) + shift_value)
                            # print('3:',shift_value, self.trim_userrom_value_list[inc_52], addr52_mask_value, shift_result)
                            self.trim_cal.append(shift_result)
                            if int(shift_result, 16) == int(self.trim_romfuse_value_list[inc], 16):
                                # trim match
                                self.trim_excel_result.append('Y')
                                self.trim_result = 1
                            else:
                                # trim mismatch
                                self.trim_excel_result.append('N')
                                self.trim_result = 0
                                self.trim_result_acc = 0
                            # Append for excel
                            self.trim_excel_romfuse.append(self.hex_upper(int(self.trim_romfuse_value_list[inc], 16)))
                            self.trim_excel_userrom.append(self.hex_upper(int(self.trim_userrom_value_list[inc], 16)))
                            self.trim_excel_original.append('')
                            self.trim_excel_setparmmask_value.append('')
                            self.trim_excel_mask.append('')
                            self.trim_excel_shift.append(self.hex_upper(shift_value))
                        # setparmmask
                        else:
                            setparmmask_result = (int(self.trim_userrom_value_list[inc], 16) &
                                                  (~int(trim_class_element.trim_mask_dict[trim_addr], 16))) | \
                                                 (int(trim_class_element.trim_value_dict[trim_addr], 16) &
                                                  int(trim_class_element.trim_mask_dict[trim_addr], 16))
                            #print(trim_addr,setparmmask_result)
                            self.trim_cal.append(setparmmask_result)
                            # print(trim_class_element.original_value_dict[trim_addr])
                            # print(self.trim_romfuse_value_list)
                            # print(inc,self.hex_upper(inc), self.trim_romfuse_value_list[inc], int(self.trim_romfuse_value_list[inc], 16), setparmmask_result,trim_class_element.original_value_dict[trim_addr],  trim_class_element.trim_value_dict[trim_addr], trim_class_element.trim_mask_dict[trim_addr])
                            if setparmmask_result == int(self.trim_romfuse_value_list[inc], 16):
                                self.trim_excel_result.append('Y')  # trim match
                                self.trim_result = 1
                            else:
                                if 'BiCs3' in self.mt_class[0].mt_design:
                                    # Addr 12(Block swap --> Skip to check)
                                    if inc == 2:
                                        self.trim_excel_result.append('BLK SWAP')  # trim mismatch
                                        self.trim_result_acc = 0
                                        self.trim_result = 0
                                    else:
                                        self.trim_excel_result.append('N')  # trim mismatch
                                        self.trim_result = 0
                                        self.trim_result_acc = 0
                                else:
                                    self.trim_excel_result.append('N')  # trim mismatch
                                    self.trim_result = 0
                                    self.trim_result_acc = 0
                                # Addr 12(Block swap --> Skip to check)
                            # Append for excel
                            self.trim_excel_romfuse.append(self.hex_upper(int(self.trim_romfuse_value_list[inc], 16)))
                            self.trim_excel_userrom.append(self.hex_upper(int(self.trim_userrom_value_list[inc], 16)))
                            self.trim_excel_original.append(
                                self.hex_upper(int(trim_class_element.original_value_dict[trim_addr], 16)))
                            self.trim_excel_setparmmask_value.append(
                                self.hex_upper(int(trim_class_element.trim_value_dict[trim_addr], 16)))
                            self.trim_excel_mask.append(self.hex_upper(int(trim_class_element.trim_mask_dict[trim_addr], 16)))
                            self.trim_excel_shift.append('')
    def key_para_check(self,chip_index):
        
        key_dict = {}
        for k,v in self.mt_class[0].key_para_dict.items():
            if self.tb_dut_bank_chip[chip_index] in k:
                key_dict[k] = v
        #self.tb_dut_bank_chip.remove(self.tb_dut_bank_chip[0])
        #print(key_dict)
        #print(self.mt_class[0].mt_design)
        if key_dict == {}:
            self.key_para_check_acc = 2
            #print(self.key_para_check_acc)
        for ele in key_dict:
            # print(ele, key_dict[ele])
            # scr format change, get trim data from webscr
            if int(ele.split('_scr')[1].split('p')[1]) >= 10:
                if int(ele.split('_scr')[1].split('p')[2].split('_')[0]) >= 10:
                    scr_format = 'SCR-' + ele.split('_scr')[1][0:5] + '.' + ele.split('_scr')[1][5:7] + '.' + \
                                 ele.split('_scr')[1].split('p')[1] + '.' + ele.split('_scr')[1].split('p')[2].split('_')[0]
                else:
                    scr_format = 'SCR-' + ele.split('_scr')[1][0:5] + '.' + ele.split('_scr')[1][5:7] + '.' + \
                                 ele.split('_scr')[1].split('p')[1] + '.0' + ele.split('_scr')[1].split('p')[2].split('_')[0]
            else:
                if int(ele.split('_scr')[1].split('p')[2].split('_')[0].replace('V','')) >= 10:
                    scr_format = 'SCR-' + ele.split('_scr')[1][0:5] + '.' + ele.split('_scr')[1][5:7] + '.0' + \
                                 ele.split('_scr')[1].split('p')[1] + '.' + ele.split('_scr')[1].split('p')[2].split('_')[0].replace('V','')
                else:
                    scr_format = 'SCR-' + ele.split('_scr')[1][0:5] + '.' + ele.split('_scr')[1][5:7] + '.0' + \
                                 ele.split('_scr')[1].split('p')[1] + '.0' + ele.split('_scr')[1].split('p')[2].split('_')[0].replace('V','')
            scr_format = scr_format.upper()
            # 5 times loops and sleep for API does not response. try 5 times with 5 secs delay.
            for i in range(5):
                try:
                    trim_dict_return = tw.get_trim_with_scr(scr_format)
                    break
                except:
                    time.sleep(5)
                    print("WebSCR API does not response. Try again {} time".format(i + 1))
        
            #print(trim_dict_return)
        
            for key_mt_ele in key_dict[ele]:
                webscr_dict = trim_dict_return[self.mt_class[0].mt_design]
                cal_result = int(key_mt_ele[1], 16)
                for webscr_trim_ele in webscr_dict[scr_format]:
                    # if address match
                    if key_mt_ele[0].zfill(3) == webscr_trim_ele[1].zfill(3):
                        # setparmmask
                        if 'setparmmask' in webscr_trim_ele[0].lower():
                            # setparmmask = (original & ~mask) | (trim_value & mask)
                            cal_result = (cal_result & (~int(webscr_trim_ele[3], 16))) | \
                                                 (int(webscr_trim_ele[2], 16) & int(webscr_trim_ele[3], 16))
                            # maybe not need below. need to double check
                            #cal_result = cal_result & int(webscr_trim_ele[3], 16)
                            # if key_mt_ele[0] =='2':
                            #     print(cal_result)
                            #     break
                        # adjparm
                        if 'adjparm' in webscr_trim_ele[0].lower() and '.' in webscr_trim_ele[2]:
                            # shift cal
                            reverse_mask = 255 - int(webscr_trim_ele[3], 16)
                            cal_result_mask = cal_result & reverse_mask
                            shift_result = cal_result + int(webscr_trim_ele[2].replace('.',''), 10)
                            cal_result = cal_result_mask | shift_result
                        elif 'adjparm' in webscr_trim_ele[0].lower() and ('.' not in webscr_trim_ele[2]):
                            reverse_mask = 255 - int(webscr_trim_ele[3], 16)
                            cal_result_mask = cal_result & reverse_mask
                            shift_result = cal_result + int(webscr_trim_ele[2], 16)
                            # result
                            cal_result = cal_result_mask | shift_result
                        self.key_para_value_copy.append(webscr_trim_ele[2])
                        self.key_para_mask_copy.append(webscr_trim_ele[3])
                        
                    # print(1, key_mt_ele, webscr_trim_ele, hex(cal_result))
                # check pass/fail
                # print(key_mt_ele[2], int(key_mt_ele[2], 16), cal_result, int(cal_result))
                if int(key_mt_ele[2], 16) == int(cal_result):
                    self.key_para_expect.append(hex(cal_result).split('x')[1].upper())
                    self.key_para_tb_copy.append(ele)
                    self.key_para_addr_copy.append(key_mt_ele[0])
                    self.key_para_rom_copy.append(key_mt_ele[1])
                    self.key_para_reg_copy.append(key_mt_ele[2])
                    self.key_para_result.append('Y')
                    #print(ele, 'addr=', key_mt_ele[0], 'rom=', key_mt_ele[1], 'reg=',key_mt_ele[2],
                          #'expect=', hex(cal_result).split('x')[1], 'MATCH')
                else:
                    self.key_para_expect.append(hex(cal_result).split('x')[1].upper())
                    self.key_para_tb_copy.append(ele)
                    self.key_para_addr_copy.append(key_mt_ele[0])
                    self.key_para_rom_copy.append(key_mt_ele[1])
                    self.key_para_reg_copy.append(key_mt_ele[2])
                    self.key_para_result.append('N')
                    self.key_para_check_acc = 0
                    #print(ele, 'addr=', key_mt_ele[0], 'rom=', key_mt_ele[1], 'reg=', key_mt_ele[2],
                          #'expect=', hex(cal_result).split('x')[1], 'NOT MATCH!!!')
        #print(self.key_para_expect)
        #print(file_read_class.mt_class_list[0].key_para_dict)

    def check_mrph(self):
        try:
            with open(self.llt_file_path) as f:
                mrph_log = f.read()
            mrph_page_pattern = re.compile(r"MORPHEOUS CHECK ON PLANE_(\d+) WL_(\d+) STR_(\d+) FOR"
                                           r" DIE_(\d+) WITH PATTERN.*?Verify XDL data vs. pattern(.*?)END OF PAGE",
                                           re.S)
            page_result_list = re.findall(mrph_page_pattern, mrph_log)
            # print(page_result_list)
            page_result_dict = {}
            for each_string in page_result_list:
                # print(each_string)
                page = "block " + each_string[0] + " wl " + each_string[1] + " string " + each_string[2]
                page_result_dict[page] = []
                no_error = re.findall(r"No error found", each_string[-1])
                if no_error:  # no error
                    page_result_dict[page].append(no_error[0])
                    # print(no_error)
                else:
                    error = re.findall(r"(Column [0-9A-Z]+): (XDLData = [0-9A-Z]+), (Pattern File = [0-9A-Z]+)",
                                       each_string[-1])
                    if error:
                        page_result_dict[page].append(error)
                    # print(error)
            # print(page_result_list)
            version_pattern = re.compile(r"READ THE MRPH VERSION(.*?)END MRPH VERSION READ", re.S)
            # print("reading the MRPH version......(only plane 0 currently)")
            data_list_blk_0 = re.findall(version_pattern, mrph_log)[0]
            data_list_blk_1 = re.findall(version_pattern, mrph_log)[1]
            byte_list_blk_0 = re.findall(r"Data = (.*?)h", data_list_blk_0)
            byte_list_blk_1 = re.findall(r"Data = (.*?)h", data_list_blk_0)

            track_version_pattern = re.compile(r"READ THE MT TRACK VERSION:(.*?)END MT TRACK VERSION READ", re.S)
            mt_track_version_blk_0 = re.findall(track_version_pattern, mrph_log)[0]
            track_byte_list_blk_0 = re.findall(r"Data = (.*?)h", mt_track_version_blk_0)

            for eachbyte_idx in range(len(byte_list_blk_0)):
                if byte_list_blk_0[eachbyte_idx] in ['0', '1', '2', '3', '4', '5', '6', '7',
                                                     '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']:
                    byte_list_blk_0[eachbyte_idx] = '0' + byte_list_blk_0[eachbyte_idx]
            # print(byte_list_blk_0)
            mrph_version = (byte_list_blk_0[0] + byte_list_blk_0[2] + byte_list_blk_0[4] + byte_list_blk_0[6]).upper()

            for eachbyte_idx in range(len(track_byte_list_blk_0)):
                if track_byte_list_blk_0[eachbyte_idx] == '0':
                    track_byte_list_blk_0[eachbyte_idx] = '00'
            # print(track_byte_list_blk_0)
            mt_track_version = track_byte_list_blk_0[0].upper().zfill(2) + track_byte_list_blk_0[1].upper()
            if mt_track_version == self.tracker_ver.upper():
                tracker_ver_pf = "Y"
            else:
                tracker_ver_pf = "N"

            if mrph_version == self.mrph_ver.upper():
                mrph_version_pf = "Y"
            else:
                mrph_version_pf = "N"
            # print(mt_track_version)
            self.mrph_list = [page_result_dict, mrph_version, mt_track_version, mrph_version_pf, tracker_ver_pf, self.mrph_ver, self.tracker_ver]
        except:
            # print("Skip MRPH check")
            self.mrph_list = [None, None, None, None, None, None, None]
        # print(self.mrph_list)

    '''
        jaoson: decode the NNT datalog line by line
    '''
    def llt_line_input(self, llt_line):
        # jason: add product name
        # Only check E0 status after print POR
        if re_match(r'TESTSTART POR', llt_line):
            self.under_por = True
        por2 = re_match(r'.*Status = (..)', llt_line)
        if por2:
            self.por_status = por2.group(1)
        por_end = re_match(r'TESTEND POR', llt_line)
        # After check status and disable por status check to avoid other Status data in por class
        if self.under_por and por_end:
            self.por(self.por_status)
            self.under_por = False

        # ID Read
        if re_match(r'TESTSTART ID READ', llt_line):
            self.under_id_read = True
        id_in = re_match(r'.*([1-9]).. Data = (0x.{1,2})', llt_line)
        if id_in:
            self.id_dict[id_in.group(1)] = id_in.group(2)
        id_read_end = re_match(r'TESTEND XY READ', llt_line)
        if self.under_id_read and id_read_end:
            self.id_input(self.id_dict)
            self.under_id_read = False

        # Lot, Wafer, X, Y, DS Ver, Sort_date
        if re_match(r'TESTSTART XY READ', llt_line):
            self.under_lwxy = True
        lot = re_match(r'.*Lot ID {7}: (.*)\..*', llt_line)
        if lot:
            self.lot_name = lot.group(1)
        wafer = re_match(r'.*Wafer Num {4}: (..)', llt_line)
        if wafer:
            self.wafer_num = wafer.group(1)
        x_coor = re_match(r'.*X {12}: (..)', llt_line)
        if x_coor:
            self.x_coor_num = x_coor.group(1)
        y_coor = re_match(r'.*Y {12}: (..)', llt_line)
        if y_coor:
            self.y_coor_num = y_coor.group(1)
        ds_ver = re_match(r'.*Prg Name&Ver : (.\...).*', llt_line)
        if ds_ver:
            self.ds_ver_name = ds_ver.group(1)
        ds_ver2 = re_match(r'.*DS Prog Ver {2}: (.*)', llt_line)
        if ds_ver2:
            self.ds_ver_name = ds_ver2.group(1)
        sort_date = re_match(r'.*Sorted Date {2}: (../../..),*', llt_line)
        if sort_date:
            self.sort_date_num = sort_date.group(1)
        lwxy_end = re_match(r'TESTEND XY READ', llt_line)
        if self.under_lwxy and lwxy_end:
            self.lwxy_input(self.lot_name, self.wafer_num, self.x_coor_num, self.y_coor_num, self.ds_ver_name,
                            self.sort_date_num)
            self.under_lwxy = False

        # Bad block
        if re_match(r'TESTSTART BB', llt_line):
            self.under_bb = True
        bb_llt_line = re_match(r' {5}.\d,.*', llt_line)
        if self.under_bb and bb_llt_line:
            self.bb_split_collect(llt_line)
        if re_match(r'TESTEND BB', llt_line):
            self.under_bb = False

        # Bad column
        if re_match(r'TESTSTART BC', llt_line):
            self.under_bc = True
        bc_llt_line = re_match(r'.*\d,.*\d,.*', llt_line)
        if self.under_bc and bc_llt_line:
            self.bc_split_collect(llt_line)
        if re_match(r'TESTEND BC', llt_line):
            self.under_bc = False

        # UROM Stamp
        if re_match(r'TESTSTART UROMSTAMP', llt_line):
            self.under_stamp = True
        if self.under_stamp:
            self.stamp_print(llt_line)
        if re_match(r'TESTEND UROMSTAMP', llt_line):
            self.under_stamp = False
        # VT DIST check
        if re_match(r'TESTSTART VT DIST CHECK', llt_line):
            self.under_vt_dist = True
        excel_title_match = re_match(r'TESTSTART (.* VT)', llt_line)
        if excel_title_match:
            self.excel_title = excel_title_match.group(1)
        label_title_match = re_match(r'LABEL:(.*)', llt_line)
        if label_title_match:
            self.label_title = label_title_match.group(1)
        vt_xy_data = re_match(r'.*(.\.....) {4}(.*)', llt_line)
        if self.under_vt_dist and vt_xy_data:
            # 2 inputs(previous xy and current xy)
            if vt_xy_data.group(1) not in "0.0000":
                self.dist_vt_xy(self.temp_vt_x_number_cal, self.temp_vt_y_number_cal, vt_xy_data.group(2),
                                self.excel_title, self.label_title)
            self.temp_vt_x_number_cal = vt_xy_data.group(1)
            self.temp_vt_y_number_cal = vt_xy_data.group(2)
        if re_match(r'TESTEND VT DIST CHECK', llt_line):
            self.under_vt_dist = False

        # Trim
        if re_match(r'TESTSTART TRIM', llt_line):
            self.under_trim = True
        if self.under_trim:
            trim_version = re_match(r'(.*GB_.[.].*?_TO_.*[.].*).*', llt_line)
            if trim_version:
                self.trim_version_name = trim_version.group(1)
                #print(self.trim_version_name)
            trim_userrom_read = re_match(r'Parameter (0x.{2,3}): Value = DUT.*: (0x..)', llt_line)
            if trim_userrom_read:
                self.trim_userrom_input(trim_userrom_read.group(1), trim_userrom_read.group(2))
            trim_romfuse_read = re_match(r'Parameter Address (0x.{2,3}) : Value = (0x..)', llt_line)
            if trim_romfuse_read:
                self.trim_romfuse_input(trim_romfuse_read.group(1), trim_romfuse_read.group(2))
                #add for ID revision check
                # jason: if trim is not run, self.add_112 will be un-defined!!! pre-define these 3 param value at begining
                if trim_romfuse_read.group(1) == '0x112':
                    self.add_112 = trim_romfuse_read.group(2)
                    #print(trim_romfuse_read.group(2))
                elif trim_romfuse_read.group(1) == '0x172':
                    self.add_172 = trim_romfuse_read.group(2)
                elif trim_romfuse_read.group(1) == '0x175':
                    self.add_FB = trim_romfuse_read.group(2)
                    #print(trim_romfuse_read.group(2))
        if re_match(r'TESTEND TRIM', llt_line):
            self.under_trim = False
            if self.trim_version_name:
                self.trim_check(self.trim_version_name, self.trim_class)

        # UID
        if re_match(r'TESTSTART UID', llt_line):
            self.under_uid = True
        if self.under_uid:
            uid_addr = re_match(r'\*\*\*\*\*\* DIE.*BLK.*(WL.*STRING.*COLUMN.*) \*\*\*\*\*\*', llt_line)
            if uid_addr:
                self.uid_addr_data = uid_addr.group(1)
            uid_llt_line = re_match(r'Data = (.*)h', llt_line)
            if uid_llt_line:
                if int(uid_llt_line.group(1), 16) < 16:
                    self.uid_collect('0' + uid_llt_line.group(1), self.uid_addr_data)
                else:
                    self.uid_collect(uid_llt_line.group(1), self.uid_addr_data)
        if re_match(r'TESTEND uid', llt_line):
            self.under_uid = False

        # Die end
        if re_match(r'.*TESTEND DIE.*', llt_line):
            current_die = re_match(r'.*TESTEND DIE (.*)', llt_line).group(1)
            print('Die'+current_die+'    validating~')
            # print(11)
            try:
                self.lwxy_match_dut_result()
            except:
                pass
            # print(111)
            # try:
            self.id_match_result(self.add_112,self.add_172,self.add_FB, product=self.product)
            # except:
            #     print("id check fail")
            #     pass
            # print(12)
            try:
                self.bb_match_result()
            except:
                pass
            # print(13)
            try:
                self.bc_match_result()
            except:
                pass
            
            # print(14)
            try:
                self.stamp_check_result()
            # print(15)
            except:
                pass
            try:
                self.dist_vt_result()
            except:
                pass
            # print(16)
            try:
                self.uid_check_result(int(current_die))
            except:
                pass
            # print(17)
            #try:
            self.key_para_check(int(current_die))
            #except:
                #pass
