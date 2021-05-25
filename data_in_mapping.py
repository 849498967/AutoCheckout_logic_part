'''
    golden id bytes values lookup table

'''

def id_mapping(mt_design, mt_die, llt_die, mt_file):
    id_expect_dict = {}
    #print(mt_die)
    if "BiCs4p5_256G_2P" in mt_design:
        if (mt_die <= 8) or ((mt_die == 10) and (llt_die in ['DIE 2', 'DIE 3', 'DIE 4', 'DIE 7', 'DIE 8', 'DIE 9'])) \
                or ((mt_die == 9) and (llt_die in ['DIE 2', 'DIE 3', 'DIE 4', 'DIE 5', 'DIE 6', 'DIE 7', 'DIE 8'])):
            id_expect_dict[1] = "0x45"
            id_expect_dict[2] = "0x3C"
            id_expect_dict[3] = "0x98"
            id_expect_dict[4] = "0xB3"
            id_expect_dict[5] = "0xF6"
            id_expect_dict[6] = "0xEB"
            id_expect_dict[7] = "0x08"
            id_expect_dict[8] = "0x1E"
        else:
            id_expect_dict[1] = "0x45"
            id_expect_dict[2] = "0x3E"
            id_expect_dict[3] = "0x99"
            id_expect_dict[4] = "0xB3"
            id_expect_dict[5] = "0xFA"
            id_expect_dict[6] = "0xEB"
            id_expect_dict[7] = "0x08"
            id_expect_dict[8] = "0x1E"
    elif "BiCs4p5_512G_2P" in mt_design:
        if (mt_die <= 8) or ((mt_die == 10) and (llt_die in ['DIE 2', 'DIE 3', 'DIE 4', 'DIE 7', 'DIE 8', 'DIE 9'])):
            id_expect_dict[1] = "0x45"
            id_expect_dict[2] = "0x3E"
            id_expect_dict[3] = "0x98"
            id_expect_dict[4] = "0xB3"
            id_expect_dict[5] = "0xF6"
            id_expect_dict[6] = "0xEB"
            id_expect_dict[7] = "0x08"
            id_expect_dict[8] = "0x1E"
        else:
            id_expect_dict[1] = "0x45"
            id_expect_dict[2] = "0x48"
            id_expect_dict[3] = "0x99"
            id_expect_dict[4] = "0xB3"
            id_expect_dict[5] = "0xFA"
            id_expect_dict[6] = "0xEB"
            id_expect_dict[7] = "0x08"
            id_expect_dict[8] = "0x1E"
    elif "BiCs5_512G_2P" in mt_design:
        if 'S5E' not in mt_file:
            if mt_die == 16:
                id_expect_dict[1] = "0x45"
                id_expect_dict[2] = "0x49"
                id_expect_dict[3] = "0x9A"
                id_expect_dict[4] = "0x03"
                id_expect_dict[5] = "0x7E"
                id_expect_dict[6] = "0x6C"
                id_expect_dict[7] = "0x08"
                id_expect_dict[8] = "0x1E"
            elif mt_die==8:
                id_expect_dict[1] = "0x45"
                id_expect_dict[2] = "0x48"
                id_expect_dict[3] = "0x99"
                id_expect_dict[4] = "0x03"
                id_expect_dict[5] = "0x7A"
                id_expect_dict[6] = "0x6C"
                id_expect_dict[7] = "0x08"
                id_expect_dict[8] = "0x1E"
            elif mt_die <=4:
                id_expect_dict[1] = "0x45"
                id_expect_dict[2] = "0x3E"
                id_expect_dict[3] = "0x98"
                id_expect_dict[4] = "0x03"
                id_expect_dict[5] = "0x76"
                id_expect_dict[6] = "0x6C"
                id_expect_dict[7] = "0x08"
                id_expect_dict[8] = "0x1E"
        else:
            if (mt_die <= 8) or ((mt_die == 10) and (llt_die in ['DIE 2', 'DIE 3', 'DIE 4', 'DIE 7', 'DIE 8', 'DIE 9'])) \
                    or ((mt_die == 9) and (llt_die in ['DIE 2', 'DIE 3', 'DIE 4', 'DIE 5', 'DIE 6', 'DIE 7', 'DIE 8'])):
                id_expect_dict[1] = "0x45"
                id_expect_dict[2] = "0x3E"
                id_expect_dict[3] = "0x98"
                id_expect_dict[4] = "0x03"
                id_expect_dict[5] = "0x76"
                id_expect_dict[6] = "0xEC"        #E6->EC  corrected
                id_expect_dict[7] = "0x08"
                id_expect_dict[8] = "0x1E"
            else:
                id_expect_dict[1] = "0x45"
                id_expect_dict[2] = "0x48"
                id_expect_dict[3] = "0x99"
                id_expect_dict[4] = "0x03"
                id_expect_dict[5] = "0x7A"
                id_expect_dict[6] = "0xEC"        #E6->EC  corrected
                id_expect_dict[7] = "0x08"
                id_expect_dict[8] = "0x1E"
    elif "BiCs5_1024G_2P" in mt_design:
        if 'S5E' not in mt_file:
            if mt_die == 16:
                id_expect_dict[1] = "0x45"
                id_expect_dict[2] = "0x40"
                id_expect_dict[3] = "0x9A"
                id_expect_dict[4] = "0x03"
                id_expect_dict[5] = "0x7E"
                id_expect_dict[6] = "0x6C"
                id_expect_dict[7] = "0x08"
                id_expect_dict[8] = "0x1E"
            elif mt_die==8:
                id_expect_dict[1] = "0x45"
                id_expect_dict[2] = "0x49"
                id_expect_dict[3] = "0x99"
                id_expect_dict[4] = "0x03"
                id_expect_dict[5] = "0x7A"
                id_expect_dict[6] = "0x6C"
                id_expect_dict[7] = "0x08"
                id_expect_dict[8] = "0x1E"
            elif mt_die <=4:
                id_expect_dict[1] = "0x45"
                id_expect_dict[2] = "0x48"
                id_expect_dict[3] = "0x98"
                id_expect_dict[4] = "0x03"
                id_expect_dict[5] = "0x76"
                id_expect_dict[6] = "0x6C"
                id_expect_dict[7] = "0x08"
                id_expect_dict[8] = "0x1E"
        else:
            if (mt_die <= 8) or ((mt_die == 10) and (llt_die in ['DIE 2', 'DIE 3', 'DIE 4', 'DIE 7', 'DIE 8', 'DIE 9'])) \
                    or ((mt_die == 9) and (llt_die in ['DIE 2', 'DIE 3', 'DIE 4', 'DIE 5', 'DIE 6', 'DIE 7', 'DIE 8'])):
                id_expect_dict[1] = "0x45"
                id_expect_dict[2] = "0x48"
                id_expect_dict[3] = "0x98"
                id_expect_dict[4] = "0x03"
                id_expect_dict[5] = "0x76"
                id_expect_dict[6] = "0xEC"
                id_expect_dict[7] = "0x08"
                id_expect_dict[8] = "0x1E"
            else:
                id_expect_dict[1] = "0x45"
                id_expect_dict[2] = "0x49"
                id_expect_dict[3] = "0x99"
                id_expect_dict[4] = "0x03"
                id_expect_dict[5] = "0x7A"
                id_expect_dict[6] = "0xEC"
                id_expect_dict[7] = "0x08"
                id_expect_dict[8] = "0x1E"                           #add by Muarice, for 1T product
    return id_expect_dict
