from re import match as re_match


class MTPerDieClass:
    def __init__(self, name, mt_program_name, mt_program_rev, mt_technology, mt_design, mt_die, max_chips_per_bank,
                 file_name):
        self.name = name
        self.mt_program_name = mt_program_name
        self.mt_program_rev = mt_program_rev
        self.mt_technology = mt_technology
        self.mt_design = mt_design
        self.mt_die = int(mt_die)
        self.max_chips_per_bank = int(max_chips_per_bank)
        self.file_name = file_name
        self.temp_dac = []
        self.dutnum = 0
        # max chip adjust for BiCS4 6D and 10D
        if self.max_chips_per_bank < 4:
            self.max_chip_adjust = 4
        else:
            self.max_chip_adjust = 8
        self.active_dut_dict = {}
        self.active_dut_array = []
        self.test_block_name_list = []
        #self.test_block_name_list1 = []
        self.cst_test_tb = None
        self.cst_test_tb_tt = None
        self.lwxy = {}
        self.lwxy_list = []
        self.bb_dict = {}
        self.bc_p0_dict = {}
        self.bc_p1_dict = {}
        self.test_block_name = ""
        self.key_para_dict = {} #add for key_para check by Ji Hyun
        self.gbb_test_block_name_list = []
        self.test_time_dict = {}
        self.test_time_dict1 = {}   #add by Maurice, for cst test time capture
        self.uid_return_dmy = []
        self.bank2_start = False
        self.current_test_block_name = ""
        self.block_offset = 2048
        self.mt_chip = None
        self.dut_bank_chip = set()
        self.date = {'DAY':[],'MONTH':[],'YEAR':[]}
        # 512Gb more than 8D --> need to bank2 offset with 1000
        if self.mt_die > 8:
            if 'BiCs4_512G_2P' in self.mt_design:
                self.block_offset = 4096
        # BiCS4.5
        if 'BiCs4p5_512G_2P' in self.mt_design:
            self.block_offset = 4096
        if 'BiCs4p5_256G_2P' in self.mt_design:
            self.block_offset = 2048
        # BiCS5
        if 'BiCs5_512G_2P' in self.mt_design:
            self.block_offset = 4096
        if 'BiCs5_1024G_2P' in self.mt_design:     #add by Maurice, for 1T product
            self.block_offset = 8192
    def active_dut_tb_name(self, active_dut, test_block_name):
        active_dut_list = str.split(active_dut)
        self.active_dut_dict[test_block_name] = active_dut_list
        self.test_block_name_list.append(test_block_name)

    def lot_wafer_x_y(self, dut, chip, lwxy):
        # 2nd back offset
        if self.bank2_start:
            chip = int(int(chip) + (self.mt_die / 2))
            if chip < 10:
                chip = '0' + str(chip)
        lwxy_split = str.split(lwxy)
        lwxy_combine = lwxy_split[0] + '_' + lwxy_split[1] + '_' + lwxy_split[2] + '_' + lwxy_split[3]
        self.lwxy_list.append(lwxy_combine)
        self.lwxy[str(int(dut)) + '_' + str(int(chip)) + '_wafer'] = lwxy_split[0]
        self.lwxy[str(int(dut)) + '_' + str(int(chip)) + '_x'] = lwxy_split[1]
        self.lwxy[str(int(dut)) + '_' + str(int(chip)) + '_y'] = lwxy_split[2]
        self.lwxy[str(int(dut)) + '_' + str(int(chip)) + '_lot'] = lwxy_split[3]
        self.lwxy[str(int(dut)) + '_' + str(int(chip)) + '_lwxy'] = lwxy_combine
        self.mt_chip = int(chip)
        # print(self.mt_chip)

    def bb_input(self, test_block_name, dut, chip, bb_addr):
        # 2nd back offset
        if self.bank2_start:
            chip = int(int(chip) + (self.mt_die / 2))
        bb_input_combine = test_block_name + '_' + str(dut) + '_' + str(chip)
        if bb_input_combine not in self.bb_dict:
            self.bb_dict[bb_input_combine] = []
        self.bb_dict[bb_input_combine].append(bb_addr)

    def bc_input(self, test_block_name, dut, chip, bc_plane, bc_addr):
        if self.bank2_start:
            chip = int(int(chip) + (self.mt_die / 2))
        bc_input_combine = test_block_name + '_' + str(dut) + '_' + str(chip)
        if bc_input_combine not in self.bc_p0_dict:
            self.bc_p0_dict[bc_input_combine] = []
        if bc_input_combine not in self.bc_p1_dict:
            self.bc_p1_dict[bc_input_combine] = []
        if int(bc_plane) == 0:
            self.bc_p0_dict[bc_input_combine].append(bc_addr)
        if int(bc_plane) == 1:
            self.bc_p1_dict[bc_input_combine].append(bc_addr)

    def bc_0_input(self, test_block_name, dut, chip):
        """
        Assign empty list if there is not any bad column
        :param test_block_name: test_block_name
        :param dut: dut
        :param chip: chip
        :return: NA
        """
        if self.bank2_start:
            chip = int(int(chip) + (self.mt_die / 2))
        bc_input_combine = test_block_name + '_' + str(dut) + '_' + str(chip)
        if bc_input_combine not in self.bc_p0_dict:
            self.bc_p0_dict[bc_input_combine] = []
        if bc_input_combine not in self.bc_p1_dict:
            self.bc_p1_dict[bc_input_combine] = []

    def gbb_test_block_name(self, gbb_test_block_name):
        if gbb_test_block_name not in self.gbb_test_block_name_list:
            self.gbb_test_block_name_list.append(gbb_test_block_name)
    
    def key_para_input(self, test_block_name, dut, bank, chip, key_para_addr, key_para_rom, key_para_reg):
        # 2nd back offset
        if self.bank2_start:
            chip = int(int(chip) + (self.mt_die / 2))
        key_para_input_combine = test_block_name + '_' + str(dut) +'_' + str(bank) + '_' + str(chip)
        if key_para_input_combine not in self.key_para_dict:
            self.key_para_dict[key_para_input_combine] = []
        self.key_para_dict[key_para_input_combine].append([key_para_addr, key_para_rom, key_para_reg])
        self.dut_bank_chip.add('_' + str(dut) +'_' + str(bank) + '_' + str(chip))
    def test_time(self, test_end_tb_name, test_time_tb):
        # todo: Need to add test time for 2 banks program
        if test_end_tb_name not in self.test_time_dict:
            self.test_time_dict[test_end_tb_name] = float(test_time_tb)
        else:
            self.test_time_dict[test_end_tb_name] += float(test_time_tb)
        self.test_block_name_list.append(test_end_tb_name)
    #add by Maurice, for CST TB TT monitor
    def test_time1(self, test_end_tb_name, test_time_tb):
        # todo: Need to add test time for 2 banks program
        if test_end_tb_name not in self.test_time_dict1:
            self.test_time_dict1[test_end_tb_name] = []
            self.test_time_dict1[test_end_tb_name].append(float(test_time_tb))
        else:
            self.test_time_dict1[test_end_tb_name].append(float(test_time_tb))
        #self.test_block_name_list1.append(test_end_tb_name)

    def mt_line_input(self, mt_line):
        # Active dut and test block name
        active_dut_match = re_match(r'\*\*\*\*Active DUTS Before (.*)', mt_line)
        if active_dut_match:
            self.active_dut_array = active_dut_match.group(1)
        test_block_name_match = re_match(r'TESTSTART ([0-9a-zA-Z_]*).*', mt_line)
        if test_block_name_match:
            self.current_test_block_name = test_block_name_match.group(1)
            self.active_dut_tb_name(self.active_dut_array, self.current_test_block_name)

        # More than 8D configure offset
        bank_1_end_match = re_match(r'.*TESTSTART End_of_bank1.*', mt_line)
        if bank_1_end_match:
            self.bank2_start = True

        # Lot, wafer, X, Y
        if re_match(r'tb__175__SLC_RD_urom_xy_loc__nvcc', self.current_test_block_name):
            lwxy_match = re_match(r'DUT(..) {2}CHIP(..)(.*)', mt_line)
            if lwxy_match:
                self.lot_wafer_x_y(lwxy_match.group(1), lwxy_match.group(2), lwxy_match.group(3))
        # BiCS4 format
        if re_match(r'tb__175__SLC_RD_urom_xy_loc_.*__nvcc', self.current_test_block_name):
            lwxy_match = re_match(r'DUT(..) {2}CHIP(..)(.*)', mt_line)
            if lwxy_match:
                self.lot_wafer_x_y(lwxy_match.group(1), lwxy_match.group(2), lwxy_match.group(3))
            lwxy_match2 = re_match(r'DUT(..) BANK(.*) CHIP(..)(.*)', mt_line)
            if lwxy_match2:
                chip = int(int(lwxy_match2.group(3)) + ((int(lwxy_match2.group(2)) - 1) * self.max_chip_adjust))
                if chip < 10:
                    chip = '0' + str(chip)
                self.lot_wafer_x_y(lwxy_match2.group(1), chip, lwxy_match2.group(4))
        # BiCS4.5/5 format
        if re_match(r'tb__120__SLC_RD_urom_xy_loc_.*__nvcc', self.current_test_block_name):
            lwxy_match = re_match(r'DUT(..) {2}CHIP(..)(.*)', mt_line)
            if lwxy_match:
                self.lot_wafer_x_y(lwxy_match.group(1), lwxy_match.group(2), lwxy_match.group(3))
            lwxy_match2 = re_match(r'DUT(..) BANK(.*) CHIP(..)(.*)', mt_line)
            if lwxy_match2:
                chip = int(int(lwxy_match2.group(3)) + ((int(lwxy_match2.group(2)) - 1) * self.max_chip_adjust))
                # print(chip)
                if chip < 10:
                    chip = '0' + str(chip)
                self.lot_wafer_x_y(lwxy_match2.group(1), chip, lwxy_match2.group(4))

        # bb list
        bb_match_not_happen = True
        bb_list_match = re_match(r'DUT(..) CHIP(..) PLANE(..) CHANNEL.* (TB...) FAILBLOCK (0x.*)', mt_line)
        if bb_list_match:
            self.bb_input(self.current_test_block_name, int(bb_list_match.group(1)), int(bb_list_match.group(2)),
                          bb_list_match.group(5))
            bb_match_not_happen = False
        bb_list_match2 = re_match(r'DUT(..) CHIP(..) PLANE(..) (TB...) FAILBLOCK (0x.*)', mt_line)
        if bb_match_not_happen:
            if bb_list_match2:
                self.bb_input(self.current_test_block_name, int(bb_list_match2.group(1)), int(bb_list_match2.group(2)),
                              bb_list_match2.group(5))
                bb_match_not_happen = False
        bb_list_match3 = re_match(r'DUT(..) BANK(.*) CHIP(..) PLANE(..) (TB...) FAILBLOCK (0x.{3,4})', mt_line)
        if bb_match_not_happen:
            if bb_list_match3:
                chip2 = int(int(bb_list_match3.group(3)) + ((int(bb_list_match3.group(2)) - 1) * self.max_chip_adjust))
                #print("chip : ", chip2, int(bb_list_match3.group(3)), int(bb_list_match3.group(2)))
                if chip2 < 10:
                    chip2 = '0' + str(chip2)
                if (int(bb_list_match3.group(2))) != 1:
                    block_address_bank_adjust = int(bb_list_match3.group(6), 16) + \
                                                (self.max_chip_adjust * self.block_offset)
                    self.bb_input(self.current_test_block_name, int(bb_list_match3.group(1)), int(chip2),
                                  hex(block_address_bank_adjust))
                else:
                    self.bb_input(self.current_test_block_name, int(bb_list_match3.group(1)), int(chip2),
                                  bb_list_match3.group(6))
                bb_match_not_happen = False
        bb_list_match4 = re_match(r'DUT(..) BANK(.*) CHIP(..) PLANE(..) (TB...) FAILBLOCK (0x.*) .*', mt_line)
        if bb_match_not_happen:
            if bb_list_match4:
                chip3 = int(int(bb_list_match4.group(3)) + ((int(bb_list_match4.group(2)) - 1) * self.max_chip_adjust))
                if chip3 < 10:
                    chip3 = '0' + str(chip3)
                if (int(bb_list_match4.group(2))) != 1:
                    block_address_bank_adjust2 = int(bb_list_match4.group(6), 16) + \
                                                 (self.max_chip_adjust * self.block_offset)
                    self.bb_input(self.current_test_block_name, int(bb_list_match4.group(1)), int(chip3), 
                                  hex(block_address_bank_adjust2))
                else:
                    self.bb_input(self.current_test_block_name, int(bb_list_match4.group(1)), int(chip3), 
                                  bb_list_match4.group(6))
            bb_match_not_happen = False

        # gbb test, store TB name in list
        gbb_list_match = re_match(r'DUT.. CHIP.. PLANE.. CHANNEL. TB.* {3}ROMFUSE Initially Fail Bad Blk Count =.*',
                                  mt_line)
        gbb_list_match2 = re_match(r'DUT.. {2}ROMFUSE Initially Fail Bad Blk Count =.*New Fail Bad Blk Count =.*',
                                   mt_line)
        if gbb_list_match or gbb_list_match2:
            self.gbb_test_block_name(self.current_test_block_name)
            
        # TESTEND --> test time collect
        test_end = re_match(r'TESTEND ([0-9a-zA-Z_]*).*TESTTIME (.*)s TOTALTIME.*', mt_line)
        if test_end:
            self.test_time(test_end.group(1), test_end.group(2))
        #add by Maurice-->cst test time collect
        if re_match(r'tb__(.*)__.*__.vcc',mt_line):
            self.cst_test_tb = mt_line
            #print(self.cst_test_tb)
        if re_match(r' -- (.*)s',mt_line):
            try:
                self.cst_test_tb_tt = re_match(r' -- (.*)s',mt_line).group(1)
            #print(self.cst_test_tb_tt)
                self.test_time1(self.cst_test_tb,self.cst_test_tb_tt)
            #print(self.test_time_dict1)
            except:
                pass
        # bc list
        bc_list_match = re_match(r'DUT:([0-9]*) CHIP:([0-9]*) PL:([0-9]*) ROM COLUMN\[.*\]=(.*)', mt_line)
        if bc_list_match:
            self.bc_input(self.current_test_block_name, int(bc_list_match.group(1)), int(bc_list_match.group(2)),
                          bc_list_match.group(3), bc_list_match.group(4))
        bc_list_match2 = re_match(r'DUT(..) CHIP(..) PLANE(..) (TB...) FAILCOL 0x(.*)', mt_line)
        if bc_list_match2:
            self.bc_input(self.current_test_block_name, int(bc_list_match2.group(1)), int(bc_list_match2.group(2)),
                          bc_list_match2.group(3), bc_list_match2.group(5))
        bc_list_match3 = re_match(r'DUT(..) BANK(.*) CHIP(..) PLANE(..) (TB...) FAILCOL 0x(.*)', mt_line)
        if bc_list_match3:
            # print(self.current_test_block_name)
            chip4 = int(int(bc_list_match3.group(3)) + ((int(bc_list_match3.group(2)) - 1) * self.max_chip_adjust))
            if chip4 < 10:
                chip4 = '0' + str(chip4)
            self.bc_input(self.current_test_block_name, int(bc_list_match3.group(1)), int(chip4),
                          bc_list_match3.group(4), bc_list_match3.group(6))
        
        # assign 0 for 0 bc DUT/CHIP/Plane
        bc_0_list_match = re_match(r'DUT([0-9]*) CHIP([0-9]*) PLANE([0-9]*) TB([0-9]*) BADCOLS.*', mt_line)
        if bc_0_list_match:
            self.bc_0_input(self.current_test_block_name, int(bc_0_list_match.group(1)), int(bc_0_list_match.group(2)))
        # assign 0 for 0 bc DUT/CHIP/Plane case 2
        bc_0_list_match = re_match(r'DUT([0-9]*) BANK([0-9]*) CHIP([0-9]*) PLANE([0-9]*) TB([0-9]*) BADCOLS.*', mt_line)
        if bc_0_list_match:
            chip5 = int(int(bc_0_list_match.group(3)) + ((int(bc_0_list_match.group(2)) - 1) * self.max_chip_adjust))
            self.bc_0_input(self.current_test_block_name, int(bc_0_list_match.group(1)), chip5)

        # UID data input
        uid_date_match = re_match(r'.*FTDay: \t\t(.*?)\n', mt_line)
        if uid_date_match:
            #print(uid_date_match.group(1))
            self.date['DAY'].append('0x' + uid_date_match.group(1).zfill(2))
        uid_date_match1 = re_match(r'.*FTMon: \t\t(.*?)\n', mt_line)
        if uid_date_match1:
            #print(uid_date_match1.group(1))
            self.date['MONTH'].append('0x' + uid_date_match1.group(1).zfill(2))
        uid_date_match2 = re_match(r'.*FTYear: \t(.*?)\n', mt_line)
        if uid_date_match2:
            #print(uid_date_match2.group(1))
            self.date['YEAR'].append('0x' + uid_date_match2.group(1).zfill(2))
       
        uid_dac_match_dut = re_match(r'DUT(.*?) BANK. CHIP:. \n', mt_line)
        if uid_dac_match_dut:
            self.dutnum = uid_dac_match_dut.group(1)
        uid_dac_match = re_match(r'.*AR3_DAC: \t(.*?)\n', mt_line)
        
        if uid_dac_match:
            #print(uid_dac_match.group(1))
            self.temp_dac.append(self.dutnum + '_' + uid_dac_match.group(1))
        if 'TESTEND tb__139__' in mt_line:
            self.uid_return_dmy.append(self.date['DAY'])
            self.uid_return_dmy.append(self.date['MONTH'])
            self.uid_return_dmy.append(self.date['YEAR'])
            self.uid_return_dmy.append(self.temp_dac)
            #print(self.uid_return_dmy)
        #keypara input
        key_para_list_match = \
            re_match(r'DUT(..) BANK(.) CHIP(..) TB(...) KEY_PARA 	 0x(.*) 		 0x(.*) 		0x(.*) 		.*', mt_line)
        if key_para_list_match:
            self.key_para_input(self.current_test_block_name, int(key_para_list_match.group(1)),int(key_para_list_match.group(2)),
                                int(key_para_list_match.group(3)), key_para_list_match.group(5).upper(),
                                key_para_list_match.group(6).upper(), key_para_list_match.group(7).upper())