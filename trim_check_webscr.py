from requests import get as requests_get
#import file_read
#import time

def get_trim_with_scr(scr_num):
    # webscr url format
    # http://csj-mp-webtcr01.wdc.com:8080/webtcr/scr/external/testblocks?q=SCR-10051.B5.01.01
    scr_url = 'http://csj-mp-webtcr01.wdc.com:8080/webtcr/scr/external/testblocks?q={}'.format(scr_num)
    # print(scr_url)
    scr_get_trim = requests_get(scr_url)
    scr_get_trim_text = scr_get_trim.json()
    #print(scr_get_trim_text)

    # trim_dict format : {BiCs5_512G_2P : {SCR10473B5p1p0_raw : [[setparmmask, 108, 08, 38], [102, 18, 38]]}, 1T : {}}
    trim_dict = {}
    for scr_get_trim_text_ele in scr_get_trim_text[0]['commands']:
        # design name change to MT format like "BiCs5_512G_2P"
        design_name = 'BiCs' + scr_get_trim_text[0]['scr'][11] + '_' + \
                      scr_get_trim_text_ele['density'].split('_')[0] + '_2P'

        # scr number convert same with test block scr format SCR-10473.B5.01.00 --> SCR10473B5p1p0
        scr_num = scr_get_trim_text[0]['scr']
        """
        # Need to collect different number of digit depends on number is more than 10 or not.
        if int(scr_num[13:15]) >= 10:
            if int(scr_num[16:18]) >= 10:
                scr_mt_format = scr_num[0:3] + scr_num[4:9] + scr_num[10:12] + 'p' + scr_num[13:15] + \
                                'p' + scr_num[16:18]
            else:
                scr_mt_format = scr_num[0:3] + scr_num[4:9] + scr_num[10:12] + 'p' + scr_num[13:15] + \
                                'p' + scr_num[17:18]
        else:
            if int(scr_num[16:18]) >= 10:
                scr_mt_format = scr_num[0:3] + scr_num[4:9] + scr_num[10:12] + 'p' + scr_num[14:15] + \
                                'p' + scr_num[16:18]
            else:
                scr_mt_format = scr_num[0:3] + scr_num[4:9] + scr_num[10:12] + 'p' + scr_num[14:15] + \
                                'p' + scr_num[17:18]
        # change to lowercase same with MT format
        scr_mt_format = scr_mt_format.lower()
        """
        # create dict
        if design_name not in trim_dict:
            trim_dict[design_name] = {}
        if scr_num not in trim_dict[design_name]:
            trim_dict[design_name][scr_num] = []

        # command, address, value, mask to list and append
        parm_list = [scr_get_trim_text_ele['command'], scr_get_trim_text_ele['address'], scr_get_trim_text_ele['value'],
                     scr_get_trim_text_ele['mask'], scr_get_trim_text_ele['comment']]
        trim_dict[design_name][scr_num].append(parm_list)
        # print(scr_num, design_name, scr_mt_format, parm_list)
        # print(scr_get_trim_text_ele)

    return trim_dict


# scr_num = 'SCR-10190.B5.00.00'
# trim_dict_return = get_trim_with_scr(scr_num)
# print(trim_dict_return)
    
# datalog_path = './Datalog/'
# file_read_class = file_read.FileReadClass(datalog_path)
# file_read_class.read_mt_datalog()
# key_dict = file_read_class.mt_class_list[0].key_para_dict

# # print(file_read_class.mt_class_list[0].mt_design)
# #print(key_dict)

# for ele in key_dict:
    
#     # print(ele, key_dict[ele])
#     # scr format change, get trim data from webscr
    
#     if int(ele.split('_scr')[1].split('p')[1]) >= 10:
#         if int(ele.split('_scr')[1].split('p')[2].split('_')[0]) >= 10:
#             scr_format = 'SCR-' + ele.split('_scr')[1][0:5] + '.' + ele.split('_scr')[1][5:7] + '.' + \
#                           ele.split('_scr')[1].split('p')[1] + '.' + ele.split('_scr')[1].split('p')[2].split('_')[0]
#         else:
#             scr_format = 'SCR-' + ele.split('_scr')[1][0:5] + '.' + ele.split('_scr')[1][5:7] + '.' + \
#                           ele.split('_scr')[1].split('p')[1] + '.0' + ele.split('_scr')[1].split('p')[2].split('_')[0]
#     else:
#         if int(ele.split('_scr')[1].split('p')[2].split('_')[0].replace('V','')) >= 10:
#             scr_format = 'SCR-' + ele.split('_scr')[1][0:5] + '.' + ele.split('_scr')[1][5:7] + '.0' + \
#                           ele.split('_scr')[1].split('p')[1] + '.' + ele.split('_scr')[1].split('p')[2].split('_')[0].replace('V','')
#         else:
#             scr_format = 'SCR-' + ele.split('_scr')[1][0:5] + '.' + ele.split('_scr')[1][5:7] + '.0' + \
#                           ele.split('_scr')[1].split('p')[1] + '.0' + ele.split('_scr')[1].split('p')[2].split('_')[0].replace('V','')
#     scr_format = scr_format.upper()
#     # 5 times loops and sleep for API does not response. try 5 times with 5 secs delay.
#     for i in range(5):
#         try:
#             trim_dict_return = get_trim_with_scr(scr_format)
#             break
#         except:
#             time.sleep(5)
#             print("WebSCR API does not response. Try again {} time".format(i + 1))

#     #print(trim_dict_return)

#     for key_mt_ele in key_dict[ele]:
#         webscr_dict = trim_dict_return[file_read_class.mt_class_list[0].mt_design]
#         cal_result = int(key_mt_ele[1], 16)
#         for webscr_trim_ele in webscr_dict[scr_format]:
#             # if address match
#             if key_mt_ele[0].zfill(3) == webscr_trim_ele[1].zfill(3):
#                 # setparmmask
#                 if 'setparmmask' in webscr_trim_ele[0].lower():
#                     # setparmmask = (original & ~mask) | (trim_value & mask)
#                     cal_result = (cal_result & (~int(webscr_trim_ele[3], 16))) | \
#                                           (int(webscr_trim_ele[2], 16) & int(webscr_trim_ele[3], 16))
#                     # maybe not need below. need to double check
#                     #cal_result = cal_result & int(webscr_trim_ele[3], 16)
#                     # if key_mt_ele[0] =='2':
#                     #     print(cal_result)
#                     #     break
#                 # adjparm
#                 if 'adjparm' in webscr_trim_ele[0].lower():
#                     # shift cal
#                     reverse_mask = 255 - int(webscr_trim_ele[3], 16)
#                     cal_result_mask = cal_result & reverse_mask
#                     shift_result = cal_result + int(webscr_trim_ele[2].replace('.',''), 10)

#                     # result
#                     cal_result = cal_result_mask | shift_result
#             # print(1, key_mt_ele, webscr_trim_ele, hex(cal_result))
#         # check pass/fail
#         # print(key_mt_ele[2], int(key_mt_ele[2], 16), cal_result, int(cal_result))
#         if int(key_mt_ele[2], 16) == int(cal_result):
#             print(ele, 'addr=', key_mt_ele[0], 'rom=', key_mt_ele[1], 'reg=',key_mt_ele[2],
#                   'expect=', hex(cal_result).split('x')[1], 'MATCH')
#         else:
#             print(ele, 'addr=', key_mt_ele[0], 'rom=', key_mt_ele[1], 'reg=', key_mt_ele[2],
#                   'expect=', hex(cal_result).split('x')[1], 'NOT MATCH!!!')

# print(file_read_class.mt_class_list[0].key_para_dict)



"""
setparmmask_result = (int(trim_class_element.original_value_dict[trim_addr], 16) &
                      (~int(trim_class_element.trim_mask_dict[trim_addr], 16))) | \
                     (int(trim_class_element.trim_value_dict[trim_addr], 16) &
                      int(trim_class_element.trim_mask_dict[trim_addr], 16))
"""