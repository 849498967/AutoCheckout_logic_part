class TrimTable:
    def __init__(self, name):
        self.name = name
        self.address_dict = {}
        self.original_value_dict = {}
        self.fix_or_trim_dict = {}
        self.trim_value_dict = {}
        self.trim_mask_dict = {}
        self.trim_shift_dict = {}

    def trim_input(self, address, original_value, fix_or_trim, trim_value, trim_mask, trim_shift, mt_class):
        for mt_die_ele in range(0, mt_class[0].mt_die):
            mt_die_ele_name = 'DIE ' + str(mt_die_ele) + '_' + address
            # print(mt_die_ele)
            if 'BiCs4p5_512G_2P' in mt_class[0].mt_design:
                # Apple 132BGA
                if 'BGA132_Apple' in mt_class[0].file_name:
                    # more than equal 8D
                    if mt_class[0].mt_die >= 8:
                        if ('0x020' in address) or ('0x20' in address):
                            trim_value = '0x61'
                            trim_mask = '0xFF'
                        if ('0x0FE' in address) or ('0xFE' in address):
                            trim_value = '0x48'
                            trim_mask = '0xFF'
                    else:
                        if ('0x020' in address) or ('0x20' in address):
                            trim_value = '0x71'
                            trim_mask = '0xFF'
                        if ('0x0FE' in address) or ('0xFE' in address):
                            trim_value = '0x3E'
                            trim_mask = '0xFF'
                # Apple 110BGA S5E
                else:
                    # 10D
                    # print(mt_class[0].mt_die)
                    if mt_class[0].mt_die == 10:
                        if mt_die_ele in [0, 1, 5, 6]:
                            if ('0x020' in address) or ('0x20' in address):
                                trim_value = '0x61'
                                trim_mask = '0xFF'
                            if ('0x0FE' in address) or ('0xFE' in address):
                                trim_value = '0x48'
                                trim_mask = '0xFF'
                        else:
                            if ('0x020' in address) or ('0x20' in address):
                                trim_value = '0x71'
                                trim_mask = '0xFF'
                            if ('0x0FE' in address) or ('0xFE' in address):
                                trim_value = '0x3E'
                                trim_mask = '0xFF'
                    # 9D
                    elif mt_class[0].mt_die == 9:
                        if mt_die_ele in [0, 1]:
                            if ('0x020' in address) or ('0x20' in address):
                                trim_value = '0x61'
                                trim_mask = '0xFF'
                            if ('0x0FE' in address) or ('0xFE' in address):
                                trim_value = '0x48'
                                trim_mask = '0xFF'
                        else:
                            if ('0x020' in address) or ('0x20' in address):
                                trim_value = '0x71'
                                trim_mask = '0xFF'
                            if ('0x0FE' in address) or ('0xFE' in address):
                                trim_value = '0x3E'
                                trim_mask = '0xFF'
                    # more than 8D
                    elif mt_class[0].mt_die > 8:
                        if ('0x020' in address) or ('0x20' in address):
                            trim_value = '0x61'
                            trim_mask = '0xFF'
                        if ('0x0FE' in address) or ('0xFE' in address):
                            trim_value = '0x48'
                            trim_mask = '0xFF'
                    # less and equal than 8D
                    else:
                        if ('0x020' in address) or ('0x20' in address):
                            trim_value = '0x71'
                            trim_mask = '0xFF'
                        if ('0x0FE' in address) or ('0xFE' in address):
                            trim_value = '0x3E'
                            trim_mask = '0xFF'
            elif 'BiCs4p5_256G_2P' in mt_class[0].mt_design:
                # Apple 132BGA
                if 'BGA132_Apple' in mt_class[0].file_name:
                    # more and equal than 8D
                    if mt_class[0].mt_die >= 8:
                        if ('0x020' in address) or ('0x20' in address):
                            trim_value = '0x61'
                            trim_mask = '0xFF'
                        if ('0x0FE' in address) or ('0xFE' in address):
                            trim_value = '0x3E'
                            trim_mask = '0xFF'
                    # less than 8D
                    else:
                        if ('0x020' in address) or ('0x20' in address):
                            trim_value = '0x71'
                            trim_mask = '0xFF'
                        if ('0x0FE' in address) or ('0xFE' in address):
                            trim_value = '0x3C'
                            trim_mask = '0xFF'
                # Apple 110BGA S5E
                else:
                    # 10D
                    if mt_class[0].mt_die == 10:
                        if mt_die_ele in [0, 1, 5, 6]:
                            if ('0x020' in address) or ('0x20' in address):
                                trim_value = '0x61'
                                trim_mask = '0xFF'
                            if ('0x0FE' in address) or ('0xFE' in address):
                                trim_value = '0x3E'
                                trim_mask = '0xFF'
                        else:
                            if ('0x020' in address) or ('0x20' in address):
                                trim_value = '0x71'
                                trim_mask = '0xFF'
                            if ('0x0FE' in address) or ('0xFE' in address):
                                trim_value = '0x3C'
                                trim_mask = '0xFF'
                    # 9D
                    elif mt_class[0].mt_die == 9:
                        if mt_die_ele in [0, 1]:
                            if ('0x020' in address) or ('0x20' in address):
                                trim_value = '0x61'
                                trim_mask = '0xFF'
                            if ('0x0FE' in address) or ('0xFE' in address):
                                trim_value = '0x3E'
                                trim_mask = '0xFF'
                        else:
                            if ('0x020' in address) or ('0x20' in address):
                                trim_value = '0x71'
                                trim_mask = '0xFF'
                            if ('0x0FE' in address) or ('0xFE' in address):
                                trim_value = '0x3C'
                                trim_mask = '0xFF'
                    # more than 8D
                    elif mt_class[0].mt_die > 8:
                        if ('0x020' in address) or ('0x20' in address):
                            trim_value = '0x61'
                            trim_mask = '0xFF'
                        if ('0x0FE' in address) or ('0xFE' in address):
                            trim_value = '0x3E'
                            trim_mask = '0xFF'
                    # less and equal than 8D
                    else:
                        if ('0x020' in address) or ('0x20' in address):
                            trim_value = '0x71'
                            trim_mask = '0xFF'
                        if ('0x0FE' in address) or ('0xFE' in address):
                            trim_value = '0x3C'
                            trim_mask = '0xFF'
            elif 'BiCs5_512G_2P' in mt_class[0].mt_design:                #add by Maurice for B5
                # Apple 132BGA
                if 'S5E' not in mt_class[0].file_name:
                    # more and equal than 8D
                    if mt_class[0].mt_die >= 8:
                        if '0x020' in address:
                            trim_value = '0x60'
                            trim_mask = '0xFF'
                        if '0x015' in address:
                            trim_value = '0x48'
                            trim_mask = '0xFF'
                    # less than 8D
                    else:
                        if '0x020' in address:
                            trim_value = '0x70'
                            trim_mask = '0xFF'
                        if '0x015' in address:
                            trim_value = '0x3E'
                            trim_mask = '0xFF'
                # Apple 110BGA S5E
                else:
                    # 10D
                    if mt_class[0].mt_die == 10:
                        if mt_die_ele in [0, 1, 5, 6]:
                            if '0x020' in address:
                                trim_value = '0x61'
                                trim_mask = '0xFF'
                            if '0x015' in address:
                                trim_value = '0x48'
                                trim_mask = '0xFF'
                        else:
                            if '0x020' in address:
                                trim_value = '0x71'
                                trim_mask = '0xFF'
                            if '0x015' in address:
                                trim_value = '0x3E'
                                trim_mask = '0xFF'
                    # 9D
                    elif mt_class[0].mt_die == 9:
                        if mt_die_ele in [0, 1]:
                            if '0x020' in address:
                                trim_value = '0x61'
                                trim_mask = '0xFF'
                            if '0x015' in address:
                                trim_value = '0x48'
                                trim_mask = '0xFF'
                        else:
                            if '0x020' in address:
                                trim_value = '0x71'
                                trim_mask = '0xFF'
                            if '0x015' in address:
                                trim_value = '0x3E'
                                trim_mask = '0xFF'
                    # more than 8D
                    elif mt_class[0].mt_die > 8:
                        if '0x020' in address:
                            trim_value = '0x61'
                            trim_mask = '0xFF'
                        if '0x015' in address:
                            trim_value = '0x48'
                            trim_mask = '0xFF'
                    # less and equal than 8D
                    else:
                        if '0x020' in address:
                            trim_value = '0x71'
                            trim_mask = '0xFF'
                        if '0x015' in address:
                            trim_value = '0x3E'
                            trim_mask = '0xFF'

            elif 'BiCs5_1024G_2P' in mt_class[0].mt_design:                #add by Maurice for B5
                # Apple 132BGA
                if 'S5E' not in mt_class[0].file_name:
                    # more and equal than 8D
                    if mt_class[0].mt_die >= 8:
                        if '0x020' in address:
                            trim_value = '0x60'
                            trim_mask = '0xFF'
                        if '0x015' in address:
                            trim_value = '0x49'
                            trim_mask = '0xFF'
                    # less than 8D
                    else:
                        if '0x020' in address:
                            trim_value = '0x70'
                            trim_mask = '0xFF'
                        if '0x015' in address:
                            trim_value = '0x48'
                            trim_mask = '0xFF'
                # Apple 110BGA S5E
                else:
                    # 10D
                    if mt_class[0].mt_die == 10:
                        if mt_die_ele in [0, 1, 5, 6]:
                            if '0x020' in address:
                                trim_value = '0x61'
                                trim_mask = '0xFF'
                            if '0x015' in address:
                                trim_value = '0x49'
                                trim_mask = '0xFF'
                        else:
                            if '0x020' in address:
                                trim_value = '0x71'
                                trim_mask = '0xFF'
                            if '0x015' in address:
                                trim_value = '0x48'
                                trim_mask = '0xFF'
                    # 9D
                    elif mt_class[0].mt_die == 9:
                        if mt_die_ele in [0, 1]:
                            if '0x020' in address:
                                trim_value = '0x61'
                                trim_mask = '0xFF'
                            if '0x015' in address:
                                trim_value = '0x49'
                                trim_mask = '0xFF'
                        else:
                            if '0x020' in address:
                                trim_value = '0x71'
                                trim_mask = '0xFF'
                            if '0x015' in address:
                                trim_value = '0x48'
                                trim_mask = '0xFF'
                    # more than 8D
                    elif mt_class[0].mt_die > 8:
                        if '0x020' in address:
                            trim_value = '0x61'
                            trim_mask = '0xFF'
                        if '0x015' in address:
                            trim_value = '0x49'
                            trim_mask = '0xFF'
                    # less and equal than 8D
                    else:
                        if '0x020' in address:
                            trim_value = '0x71'
                            trim_mask = '0xFF'
                        if '0x015' in address:
                            trim_value = '0x48'
                            trim_mask = '0xFF'
            else:
                if mt_class[0].mt_die > 8:
                    if ('0x020' in address) or ('0x20' in address):
                        trim_value = '0x60'
                        trim_mask = '0xFF'
                    if ('0x0FE' in address) or ('0xFE' in address):
                        trim_value = '0x3E'
                        trim_mask = '0xFF'
                # pMLC
                if '170G' in mt_class[0].mt_design:
                    if mt_class[0].mt_die > 8:
                        if '0xF3' in address:
                            trim_value = '0x37'
                            trim_mask = '0xFF'
                    else:
                        if '0xF3' in address:
                            trim_value = '0x35'
                            trim_mask = '0xFF'

            self.address_dict[mt_die_ele_name] = address
            self.original_value_dict[mt_die_ele_name] = original_value
            self.fix_or_trim_dict[mt_die_ele_name] = fix_or_trim
            self.trim_value_dict[mt_die_ele_name] = trim_value
            self.trim_mask_dict[mt_die_ele_name] = trim_mask
            self.trim_shift_dict[mt_die_ele_name] = trim_shift
