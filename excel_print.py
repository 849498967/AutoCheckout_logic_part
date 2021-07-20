from datetime import datetime
from xlsxwriter import Workbook as xlsxwriter_Workbook
import matplotlib.pyplot as plt
import os
import numpy as np


class ExcelPrint:
    def __init__(self, file_read_class):
        self.file_read_class = file_read_class
        # create excel folder if not exist
        if not os.path.exists('./excel'):
            os.makedirs('./excel')
        # excel file name
        dt = datetime.now().isoformat()
        product = self.file_read_class.llt_class_list[0].product
        excel_sub_file_name = \
            dt[2] + dt[3] + dt[5] + dt[6] + dt[8] + dt[9] + '_' + dt[11] + dt[12] + dt[14] + dt[15] + dt[17] + dt[18]
        excel_sub_file_name = '_' + file_read_class.folder_name + '_' + excel_sub_file_name
        self.filename = './excel/MT_check_summary_' + product + excel_sub_file_name + '.xlsx'
        self.filename_open = '/excel/MT_check_summary_'+ product + excel_sub_file_name  + '.xlsx'
        self.flow =  self.file_read_class.mt_class_list[0].actualflow_name
        self.wb = xlsxwriter_Workbook(self.filename, options={'default_format_properties': {'font_name': '微软雅黑', 'font_size': 9,}})
        # style list
        self.style1 = self.wb.add_format({'align': 'center', 'valign': 'vcenter', 'border': 1})
        self.style2 = self.wb.add_format({'align': 'center', 'valign': 'vcenter', 'border': 1, 'underline': 1,
                                          'font_color': 'blue'})
        self.style5 = self.wb.add_format({'align': 'center', 'valign': 'vcenter', 'border': 1, 'bold': 1})
        self.style6 = self.wb.add_format({'align': 'center', 'valign': 'vcenter'})
        self.style7 = self.wb.add_format({'align': 'left', 'valign': 'vcenter'})
        self.style8 = self.wb.add_format({'align': 'center', 'valign': 'vcenter', 'num_format': '0.00'})
        self.style9 = self.wb.add_format({'align': 'center', 'valign': 'vcenter', 'num_format': '0.00%'})
        self.conditional_style_pass = self.wb.add_format({'bg_color': '#86ff9b'})
        self.conditional_style_fail = self.wb.add_format({'bg_color': '#ff9986'})
        self.conditional_style_D_BAR = self.wb.add_format({'bg_color': 'yellow'})

        self.wb_dict = {}

        # summary
        self.summary_ws = self.wb.add_worksheet('Summary')
        self.summary_enable = 1
        self.summary_row = 2
        self.summary_col = 1
        self.summary_enable = 1
        self.summary_index = 1
        self.summary_ws.set_column('C:C', 14)
        self.summary_ws.set_column('D:D', 14)
        # por
        self.por_result_summary = ""
        # ID
        self.id_result_summary = ""
        # LWXY
        self.lwxy_result_summary = ""
        # BB
        self.bb_result_summary = ""
        # BC
        self.bc_result_summary = ""
        # TRIM
        self.trim_result_summary = ""
        # UID
        self.uid_result_summary = ""
        # STAMP
        self.stamp_result_summary = ""
        # DIST VT
        self.dist_vt_result_summary = {}
        # mrph
        self.mrph_summary = ""


    def summary(self, dut_match):
        self.summary_ws.merge_range(self.summary_row - 1, self.summary_col, self.summary_row - 1, self.summary_col + 2,
                                    'MT CHECKOUT SUMMARY', self.style1)
        if dut_match == 0:
            self.summary_ws.merge_range(self.summary_row, self.summary_col, self.summary_row, self.summary_col + 2,
                                        'CANNOT FIND MATCH DUT', self.style1)
        if dut_match == 2:
            self.summary_ws.merge_range(self.summary_row, self.summary_col, self.summary_row, self.summary_col + 2,
                                        'CANNOT FIND LLT FILE', self.style1)
        if dut_match == 3:
            self.summary_ws.merge_range(self.summary_row, self.summary_col, self.summary_row, self.summary_col + 2,
                                        'CANNOT FIND MT FILE', self.style1)
        if dut_match == 4:
            self.summary_ws.merge_range(self.summary_row, self.summary_col, self.summary_row, self.summary_col + 2,
                                        'CANNOT FIND LLT/MT FILE', self.style1)

    def por_excel_print(self):
        por_ws = self.wb.add_worksheet('POR')
        por_ws.freeze_panes(3, 1)
        por_row = 3
        por_col = 1
        por_ws.merge_range(1, 1, 1, 2, 'POR', self.style1)
        por_ws.write(2, 1, 'Die', self.style1)
        por_ws.write(2, 2, 'Status', self.style1)
        self.por_result_summary = 'N/A'
        for llt_class_ele in self.file_read_class.llt_class_list:
            por_ws.write(por_row, por_col, llt_class_ele.name, self.style1)
            por_ws.write(por_row, por_col + 1, llt_class_ele.por_data, self.style1)
            if llt_class_ele.por_result != 1:
                self.por_result_summary = 'FAIL'
            else:
                if 'FAIL' not in self.por_result_summary:
                    self.por_result_summary = 'PASS'
            por_row += 1
        por_ws.conditional_format(3, 2, por_row - 1, 2, {'type': 'text', 'criteria': 'containing', 'value': 'E0',
                                                         'format': self.conditional_style_pass})
        por_ws.conditional_format(3, 2, por_row - 1, 2, {'type': 'text', 'criteria': 'containing', 'value': 'F0',
                                                         'format': self.conditional_style_pass})
        por_ws.conditional_format(3, 2, por_row - 1, 2, {'type': 'text', 'criteria': 'not containing', 'value': 'E0',
                                                         'format': self.conditional_style_fail})
        if self.summary_enable:
            self.summary_ws.write(self.summary_row, self.summary_col, self.summary_index, self.style1)
            self.summary_ws.write(self.summary_row, self.summary_col + 1, 'POR', self.style1)
            self.summary_ws.write_url(self.summary_row, self.summary_col + 2,
                                      'internal:por!B2', self.style2)
            self.summary_ws.write(self.summary_row, self.summary_col + 2, self.por_result_summary, self.style2)
            self.summary_index += 1
            self.summary_row += 1

    def id_excel_print(self):
        id_wd = self.wb.add_worksheet('ID')
        id_wd.freeze_panes(3, 1)
        id_row = 1
        id_col = 1
        id_range = 8
        id_total_row = 8
        self.id_result_summary = 'PASS'
        try:
            for llt_class_ele in self.file_read_class.llt_class_list:
                id_wd.merge_range(id_row, id_col, id_row, id_col + 2, llt_class_ele.name, self.style1)
                id_wd.write(id_row + 1, id_col + 0, 'ID', self.style1)
                id_wd.write(id_row + 1, id_col + 1, 'EXPECT', self.style1)
                id_wd.write(id_row + 1, id_col + 2, 'MATCH', self.style1)
                for i in range(1, id_range + 1):
                    id_wd.write(id_row + i + 1, id_col + 0, llt_class_ele.id_dict[str(i)], self.style1)
                    id_wd.write(id_row + i + 1, id_col + 1, llt_class_ele.id_expect[i], self.style1)
                    id_wd.write(id_row + i + 1, id_col + 2, llt_class_ele.id_result[i], self.style1)
                    last_row_num = i

                id_wd.conditional_format(id_row + 2, id_col + 2, id_total_row + last_row_num + 2, id_col + 2,
                                          {'type': 'text', 'criteria': 'containing', 'value': 'Y',
                                           'format': self.conditional_style_pass})
                id_wd.conditional_format(id_row + 2, id_col + 2, id_total_row + id_row + last_row_num + 2, id_col + 2,
                                          {'type': 'text', 'criteria': 'containing', 'value': 'N',
                                           'format': self.conditional_style_fail})
                id_wd.conditional_format(id_row + 2, id_col + 2, id_total_row + id_row + last_row_num + 2, id_col + 2,
                                          {'type': 'text', 'criteria': 'containing', 'value': 'D-BAR',
                                           'format': self.conditional_style_D_BAR})
                id_col += 3
                #print(llt_class_ele.id_result_excel)
                if llt_class_ele.id_result_excel != 1:
                    if llt_class_ele.id_result_excel == 0:
                        self.id_result_summary = 'FAIL'
                    # else:
                    #     if 'FAIL' not in self.id_result_summary:
                    #         self.id_result_summary = 'PASS'
                # else:
                #     self.id_result_summary = 'PASS'

            if self.summary_enable:
                self.summary_ws.write(self.summary_row, self.summary_col, self.summary_index, self.style1)
                self.summary_ws.write(self.summary_row, self.summary_col + 1, 'ID', self.style1)
                self.summary_ws.write_url(self.summary_row, self.summary_col + 2,
                                          'internal:id!B2', self.style2)
                self.summary_ws.write(self.summary_row, self.summary_col + 2, self.id_result_summary, self.style2)
                self.summary_index += 1
                self.summary_row += 1
        except:
            print("id pass")
            if self.summary_enable:
                self.summary_ws.write(self.summary_row, self.summary_col, self.summary_index, self.style1)
                self.summary_ws.write(self.summary_row, self.summary_col + 1, 'ID', self.style1)
                self.summary_ws.write_url(self.summary_row, self.summary_col + 2,
                                          'internal:id!B2', self.style2)
                self.summary_ws.write(self.summary_row, self.summary_col + 2, 'None', self.style2)
                self.summary_index += 1
                self.summary_row += 1
    def lwxy_excel(self):
        try:
            lwxy_ws = self.wb.add_worksheet('LWXY')
            lwxy_ws.freeze_panes(2, 3)
            lwxy_row = 2
            lwxy_col = 1
            lwxy_ws.set_column('D:E', 9.5)
            lwxy_ws.write(1, 1, '#', self.style1)
            lwxy_ws.write(1, 2, 'Die info', self.style1)
            lwxy_ws.write(1, 3, 'MT', self.style1)
            lwxy_ws.write(1, 4, 'LLT', self.style1)
            lwxy_ws.write(1, 5, 'MATCH', self.style1)
            self.lwxy_result_summary = 'N/A'
            for llt_class_ele in self.file_read_class.llt_class_list:
                lwxy_ws.merge_range(lwxy_row, lwxy_col, lwxy_row + 3, lwxy_col, llt_class_ele.name, self.style1)
                lwxy_ws.write(lwxy_row, lwxy_col + 1, 'Lot', self.style1)
                lwxy_ws.write(lwxy_row, lwxy_col + 2, self.file_read_class.mt_class_list[0].lwxy[
                    llt_class_ele.dut_chip_lwxy[0] + '_' + llt_class_ele.dut_chip_lwxy[1] + '_lot'], self.style1)
                lwxy_ws.write(lwxy_row, lwxy_col + 3, llt_class_ele.lot, self.style1)
                lwxy_ws.write(lwxy_row, lwxy_col + 4, llt_class_ele.lwxy_lot_match_result, self.style1)
                lwxy_ws.write(lwxy_row + 1, lwxy_col + 1, 'Wafer', self.style1)
                lwxy_ws.write(lwxy_row + 1, lwxy_col + 2, int(
                    self.file_read_class.mt_class_list[0].lwxy[
                        llt_class_ele.dut_chip_lwxy[0] + '_' + llt_class_ele.dut_chip_lwxy[1] + '_wafer']), self.style1)
                lwxy_ws.write(lwxy_row + 1, lwxy_col + 3, int(llt_class_ele.wafer), self.style1)
                lwxy_ws.write(lwxy_row + 1, lwxy_col + 4, llt_class_ele.lwxy_wafer_match_result, self.style1)
                lwxy_ws.write(lwxy_row + 2, lwxy_col + 1, 'X', self.style1)
                lwxy_ws.write(lwxy_row + 2, lwxy_col + 2, int(
                    self.file_read_class.mt_class_list[0].lwxy[
                        llt_class_ele.dut_chip_lwxy[0] + '_' + llt_class_ele.dut_chip_lwxy[1] + '_x']), self.style1)
                lwxy_ws.write(lwxy_row + 2, lwxy_col + 3, int(llt_class_ele.x_coor), self.style1)
                lwxy_ws.write(lwxy_row + 2, lwxy_col + 4, llt_class_ele.lwxy_x_match_result, self.style1)
                lwxy_ws.write(lwxy_row + 3, lwxy_col + 1, 'Y', self.style1)
                lwxy_ws.write(lwxy_row + 3, lwxy_col + 2, int(
                    self.file_read_class.mt_class_list[0].lwxy[
                        llt_class_ele.dut_chip_lwxy[0] + '_' + llt_class_ele.dut_chip_lwxy[1] + '_y']), self.style1)
                lwxy_ws.write(lwxy_row + 3, lwxy_col + 3, int(llt_class_ele.y_coor), self.style1)
                lwxy_ws.write(lwxy_row + 3, lwxy_col + 4, llt_class_ele.lwxy_y_match_result, self.style1)
                if llt_class_ele.lwxy_match_result != 1:
                    self.lwxy_result_summary = 'FAIL'
                else:
                    if 'FAIL' not in self.lwxy_result_summary:
                        self.lwxy_result_summary = 'PASS'
                lwxy_row += 4
            lwxy_ws.conditional_format(2, 5, lwxy_row - 1, 5, {'type': 'text', 'criteria': 'containing', 'value': 'Y',
                                                               'format': self.conditional_style_pass})
            lwxy_ws.conditional_format(2, 5, lwxy_row - 1, 5, {'type': 'text', 'criteria': 'containing', 'value': 'N',
                                                               'format': self.conditional_style_fail})
            if self.summary_enable:
                self.summary_ws.write(self.summary_row, self.summary_col, self.summary_index, self.style1)
                self.summary_ws.write(self.summary_row, self.summary_col + 1, 'Lot/Wafer/X/Y', self.style1)
                self.summary_ws.write_url(self.summary_row, self.summary_col + 2,
                                          'internal:lwxy!B2', self.style2)
                self.summary_ws.write(self.summary_row, self.summary_col + 2, self.lwxy_result_summary, self.style2)
                self.summary_index += 1
                self.summary_row += 1
        except:
            print("lwxy skipped")
    def bb_excel(self):
        bb_ws = self.wb.add_worksheet('BB')
        bb_ws.freeze_panes(3, 2)
        bb_row = 1
        bb_col = 2
        bb_ws.write(1, 1, 'BB', self.style1)
        bb_ws.write(2, 1, '#', self.style1)
        self.bb_result_summary = 'N/A'
        last_row_num = 0
        for llt_class_ele in self.file_read_class.llt_class_list:
            bb_ws.merge_range(bb_row, bb_col, bb_row, bb_col + 2, llt_class_ele.name, self.style1)
            bb_ws.write(bb_row + 1, bb_col, 'MT BB', self.style1)
            bb_ws.write(bb_row + 1, bb_col + 1, 'LLT BB', self.style1)
            bb_ws.write(bb_row + 1, bb_col + 2, 'MATCH', self.style1)
            for i, mt_bb in enumerate(llt_class_ele.mt_bb_print):
                bb_ws.write(bb_row + i + 2, 1, i + 1, self.style1)
                bb_ws.write(bb_row + i + 2, bb_col, mt_bb, self.style1)
                bb_ws.write(bb_row + i + 2, bb_col + 1, llt_class_ele.llt_bb_print[i], self.style1)
                bb_ws.write(bb_row + i + 2, bb_col + 2, llt_class_ele.bb_result_print[i], self.style1)
                last_row_num = i
            bb_ws.conditional_format(bb_row + 2, bb_col + 2, bb_row + last_row_num + 2, bb_col + 2,
                                     {'type': 'text', 'criteria': 'containing', 'value': 'Y',
                                      'format': self.conditional_style_pass})
            bb_ws.conditional_format(bb_row + 2, bb_col + 2, bb_row + last_row_num + 2, bb_col + 2,
                                     {'type': 'text', 'criteria': 'containing', 'value': 'N',
                                      'format': self.conditional_style_fail})
            bb_ws.conditional_format(bb_row + 2, bb_col + 2, bb_row + last_row_num + 2, bb_col + 2,
                                     {'type': 'text', 'criteria': 'containing', 'value': 'BLK SWAP',
                                      'format': self.conditional_style_D_BAR})
            bb_col += 3
            if llt_class_ele.bb_result != 1:
                self.bb_result_summary = 'FAIL'
            else:
                if 'FAIL' not in self.bb_result_summary:
                    self.bb_result_summary = 'PASS'
        if self.summary_enable:
            self.summary_ws.write(self.summary_row, self.summary_col, self.summary_index, self.style1)
            self.summary_ws.write(self.summary_row, self.summary_col + 1, 'BB', self.style1)
            self.summary_ws.write_url(self.summary_row, self.summary_col + 2,
                                      'internal:bb!B2', self.style2)
            self.summary_ws.write(self.summary_row, self.summary_col + 2, self.bb_result_summary, self.style2)
            self.summary_index += 1
            self.summary_row += 1

    def bc_excel(self):
        bc_ws = self.wb.add_worksheet('BC')
        bc_ws.freeze_panes(3, 2)
        bc_row = 1
        bc_col = 2
        bc_ws.write(1, 1, 'BC', self.style1)
        bc_ws.write(2, 1, '#', self.style1)
        self.bc_result_summary = 'N/A'
        for llt_class_ele in self.file_read_class.llt_class_list:
            # p0
            bc_ws.merge_range(bc_row, bc_col, bc_row, bc_col + 2, llt_class_ele.name + ' P0', self.style1)
            bc_ws.write(bc_row + 1, bc_col, 'MT BC', self.style1)
            bc_ws.write(bc_row + 1, bc_col + 1, 'LLT BC', self.style1)
            bc_ws.write(bc_row + 1, bc_col + 2, 'MATCH', self.style1)
            last_row = 0
            for i, mt_bc in enumerate(llt_class_ele.mt_bc_print_p0):
                bc_ws.write(bc_row + i + 2, 1, i + 1, self.style1)
                bc_ws.write(bc_row + i + 2, bc_col, mt_bc, self.style1)
                bc_ws.write(bc_row + i + 2, bc_col + 1, llt_class_ele.llt_bc_print_p0[i], self.style1)
                bc_ws.write(bc_row + i + 2, bc_col + 2, llt_class_ele.result_bc_p0[i], self.style1)
                last_row = i
            bc_ws.conditional_format(bc_row + 2, bc_col + 2, bc_row + last_row + 2, bc_col + 2,
                                     {'type': 'text', 'criteria': 'containing', 'value': 'Y',
                                      'format': self.conditional_style_pass})
            bc_ws.conditional_format(bc_row + 2, bc_col + 2, bc_row + last_row + 2, bc_col + 2,
                                     {'type': 'text', 'criteria': 'containing', 'value': 'N',
                                      'format': self.conditional_style_fail})
            bc_col += 3
            # p1
            bc_ws.merge_range(bc_row, bc_col, bc_row, bc_col + 2, llt_class_ele.name + ' P1', self.style1)
            bc_ws.write(bc_row + 1, bc_col, 'MT BC', self.style1)
            bc_ws.write(bc_row + 1, bc_col + 1, 'LLT BC', self.style1)
            bc_ws.write(bc_row + 1, bc_col + 2, 'MATCH', self.style1)
            last_row = 0
            for i, mt_bc in enumerate(llt_class_ele.mt_bc_print_p1):
                bc_ws.write(bc_row + i + 2, 1, i + 1, self.style1)
                bc_ws.write(bc_row + i + 2, bc_col, mt_bc, self.style1)
                bc_ws.write(bc_row + i + 2, bc_col + 1, llt_class_ele.llt_bc_print_p1[i], self.style1)
                bc_ws.write(bc_row + i + 2, bc_col + 2, llt_class_ele.result_bc_p1[i], self.style1)
                last_row = i
            bc_ws.conditional_format(bc_row + 2, bc_col + 2, bc_row + last_row + 2, bc_col + 2,
                                     {'type': 'text', 'criteria': 'containing', 'value': 'Y',
                                      'format': self.conditional_style_pass})
            bc_ws.conditional_format(bc_row + 2, bc_col + 2, bc_row + last_row + 2, bc_col + 2,
                                     {'type': 'text', 'criteria': 'containing', 'value': 'N',
                                      'format': self.conditional_style_fail})
            bc_col += 3
            if llt_class_ele.bc_result != 1:
                self.bc_result_summary = 'FAIL'
            else:
                if 'FAIL' not in self.bc_result_summary:
                    self.bc_result_summary = 'PASS'
        if self.summary_enable:
            self.summary_ws.write(self.summary_row, self.summary_col, self.summary_index, self.style1)
            self.summary_ws.write(self.summary_row, self.summary_col + 1, 'BC', self.style1)
            self.summary_ws.write_url(self.summary_row, self.summary_col + 2,
                                      'internal:bc!B2', self.style2)
            self.summary_ws.write(self.summary_row, self.summary_col + 2, self.bc_result_summary, self.style2)
            self.summary_index += 1
            self.summary_row += 1

    def trim_excel(self, trim_exist):
        trim_ws = self.wb.add_worksheet('TRIM')
        if trim_exist:
            trim_ws.freeze_panes(3, 1)
            trim_row = 1
            trim_col = 1
            trim_row_conditional_format = 0
            self.trim_result_summary = 'PASS'
            for llt_class_ele in self.file_read_class.llt_class_list:
                trim_ws.merge_range(trim_row, trim_col, trim_row, trim_col + 7, llt_class_ele.name, self.style1)
                trim_ws.write(trim_row + 1, trim_col + 0, 'ADDR', self.style1)
                trim_ws.write(trim_row + 1, trim_col + 1, 'ROM', self.style1)
                trim_ws.write(trim_row + 1, trim_col + 2, 'UROM', self.style1)
                trim_ws.write(trim_row + 1, trim_col + 3, 'ORIGINAL', self.style1)
                trim_ws.write(trim_row + 1, trim_col + 4, 'SETPARM', self.style1)
                trim_ws.write(trim_row + 1, trim_col + 5, 'MASK', self.style1)
                trim_ws.write(trim_row + 1, trim_col + 6, 'SHIFT', self.style1)
                trim_ws.write(trim_row + 1, trim_col + 7, 'MATCH', self.style1)
                for i, trim_addr in enumerate(llt_class_ele.trim_excel_Addr):
                    trim_row_conditional_format = i
                    trim_ws.write(trim_row + i + 2, trim_col + 0, trim_addr, self.style1)
                    trim_ws.write(trim_row + i + 2, trim_col + 1, llt_class_ele.trim_excel_romfuse[i], self.style1)
                    trim_ws.write(trim_row + i + 2, trim_col + 2, llt_class_ele.trim_excel_userrom[i], self.style1)
                    trim_ws.write(trim_row + i + 2, trim_col + 3, llt_class_ele.trim_excel_original[i], self.style1)
                    trim_ws.write(trim_row + i + 2, trim_col + 4, llt_class_ele.trim_excel_setparmmask_value[i],
                                  self.style1)
                    trim_ws.write(trim_row + i + 2, trim_col + 5, llt_class_ele.trim_excel_mask[i], self.style1)
                    trim_ws.write(trim_row + i + 2, trim_col + 6, llt_class_ele.trim_excel_shift[i], self.style1)
                    trim_ws.write(trim_row + i + 2, trim_col + 7, llt_class_ele.trim_excel_result[i], self.style1)
                trim_ws.conditional_format(trim_row + 2, trim_col + 7, trim_row + trim_row_conditional_format + 2,
                                           trim_col + 7, {'type': 'text', 'criteria': 'containing', 'value': 'Y',
                                                          'format': self.conditional_style_pass})
                trim_ws.conditional_format(trim_row + 2, trim_col + 7, trim_row + trim_row_conditional_format + 2,
                                           trim_col + 7,
                                           {'type': 'text', 'criteria': 'containing', 'value': 'N',
                                            'format': self.conditional_style_fail})
                trim_ws.conditional_format(trim_row + 2, trim_col + 7, trim_row + trim_row_conditional_format + 2,
                                           trim_col + 7,
                                           {'type': 'text', 'criteria': 'containing', 'value': 'BLK SWAP',
                                            'format': self.conditional_style_D_BAR})
                trim_col += 8
                if llt_class_ele.trim_result_acc == 1:
                    if llt_class_ele.trim_result != -1:
                        if 'FAIL' not in self.trim_result_summary:
                            self.trim_result_summary = 'PASS'
                    else:
                        self.trim_result_summary = 'FAIL'
                else:
                    self.trim_result_summary = 'FAIL'
                if not llt_class_ele.trim_version_match:
                    self.trim_result_summary = 'CANNOT FIND TRIM VERSION'
            if self.summary_enable:
                if self.trim_result_summary == 'CANNOT FIND TRIM VERSION':
                    self.summary_ws.set_column(3, 3, width=40)
                self.summary_ws.write(self.summary_row, self.summary_col, self.summary_index, self.style1)
                self.summary_ws.write(self.summary_row, self.summary_col + 1, 'TRIM', self.style1)
                self.summary_ws.write_url(self.summary_row, self.summary_col + 2,
                                          'internal:TRIM!B2', self.style2)
                self.summary_ws.write(self.summary_row, self.summary_col + 2, self.trim_result_summary, self.style2)
                self.summary_index += 1
                self.summary_row += 1
        else:
            trim_ws.merge_range(1, 1, 1, 6, 'CANNOT FIND TRIM FILE', self.style1)
            if self.summary_enable:
                self.summary_ws.write(self.summary_row, self.summary_col, self.summary_index, self.style1)
                self.summary_ws.write(self.summary_row, self.summary_col + 1, 'TRIM', self.style1)
                self.summary_ws.write_url(self.summary_row, self.summary_col + 2,
                                          'internal:TRIM!B2', self.style2)
                self.summary_ws.write(self.summary_row, self.summary_col + 2, 'NO TRIM TABLE', self.style2)
                self.summary_index += 1
                self.summary_row += 1
                
    # def key_para_excel(self):
    #         keypara_ws = self.wb.add_worksheet('KEY_PARA')
    #         keypara_ws .freeze_panes(3, 1)
    #         keypara_row = 1
    #         keypara_col = 1
    #         last_row_num = 0
    #         self.keypara_result_summary = 'PASS'
    #         for llt_class_ele in self.file_read_class.llt_class_list:
    #             keypara_ws.merge_range(keypara_row, keypara_col, keypara_row, keypara_col + 7, llt_class_ele.name, self.style1)
    #             keypara_ws.write(keypara_row + 1, keypara_col + 0, 'TB', self.style1)
    #             keypara_ws.write(keypara_row + 1, keypara_col + 1, 'ADDR', self.style1)
    #             keypara_ws.write(keypara_row + 1, keypara_col + 2, 'ROM', self.style1)
    #             keypara_ws.write(keypara_row + 1, keypara_col + 3, 'TRIM', self.style1)
    #             keypara_ws.write(keypara_row + 1, keypara_col + 4, 'MASK/SHIFT_DAC', self.style1)
    #             keypara_ws.write(keypara_row+ 1, keypara_col + 5, 'REG', self.style1)
    #             keypara_ws.write(keypara_row + 1, keypara_col + 6, 'EXPECT', self.style1)
    #             keypara_ws.write(keypara_row + 1, keypara_col + 7, 'MATCH', self.style1)
    #             for i in range(len(llt_class_ele.key_para_expect)):
    #                 last_row_num = i
    #                 keypara_ws.write(keypara_row + i + 2, keypara_col + 0, llt_class_ele.key_para_tb_copy[i], self.style1)
    #                 keypara_ws.write(keypara_row + i + 2, keypara_col + 1, llt_class_ele.key_para_addr_copy[i],
    #                              self.style1)
    #                 keypara_ws.write(keypara_row + i + 2, keypara_col + 2, llt_class_ele.key_para_rom_copy[i],
    #                              self.style1)
    #                 keypara_ws.write(keypara_row + i + 2, keypara_col + 3, llt_class_ele.key_para_value_copy[i],
    #                              self.style1)
    #                 keypara_ws.write(keypara_row + i + 2, keypara_col + 4, llt_class_ele.key_para_mask_copy[i],
    #                              self.style1)
    #                 keypara_ws.write(keypara_row + i + 2, keypara_col + 5, llt_class_ele.key_para_reg_copy[i],
    #                              self.style1)
    #                 keypara_ws.write(keypara_row + i + 2, keypara_col + 6, llt_class_ele.key_para_expect[i],
    #                              self.style1)
    #                 keypara_ws.write(keypara_row + i + 2, keypara_col + 7, llt_class_ele.key_para_result[i],
    #                              self.style1)
    #
    #             keypara_ws.conditional_format(keypara_row + 2, keypara_col + 7, keypara_row + last_row_num + 2, keypara_col + 7,
    #                                       {'type': 'text', 'criteria': 'containing', 'value': 'Y',
    #                                        'format': self.conditional_style_pass})
    #             keypara_ws.conditional_format(keypara_row + 2, keypara_col + 7, keypara_row + last_row_num + 2, keypara_col + 7,
    #                                       {'type': 'text', 'criteria': 'containing', 'value': 'N',
    #                                        'format': self.conditional_style_fail})
    #             keypara_col += 8
    #             if llt_class_ele.key_para_check_acc == 0:
    #                 self.keypara_result_summary = 'FAIL'
    #             if llt_class_ele.key_para_check_acc == 2:
    #                 self.keypara_result_summary = 'None'
    #
    #         if self.summary_enable:
    #             self.summary_ws.write(self.summary_row, self.summary_col, self.summary_index, self.style1)
    #             self.summary_ws.write(self.summary_row, self.summary_col + 1, 'KEY_PARA', self.style1)
    #             self.summary_ws.write_url(self.summary_row, self.summary_col + 2,
    #                                       'internal:KEY_PARA!B2', self.style2)
    #             self.summary_ws.write(self.summary_row, self.summary_col + 2, self.keypara_result_summary, self.style2)
    #             self.summary_index += 1
    #             self.summary_row += 1
                
    def uid_excel(self):
        # only create the shet for apple and ecb
        if self.file_read_class.llt_class_list[0].product == "CSS" or self.file_read_class.llt_class_list[0].product == "ESS":
            return 1
        else:
            uid_ws = self.wb.add_worksheet('UID')
            uid_ws.freeze_panes(3, 1)
            uid_row = 1
            uid_col = 1
            uid_range = 17
            self.uid_result_summary = 'PASS'
            last_row_num = 0
            try:
                for llt_class_ele in self.file_read_class.llt_class_list:
                    uid_ws.merge_range(uid_row, uid_col, uid_row, uid_col + 8, llt_class_ele.name, self.style1)
                    uid_ws.write(uid_row + 1, uid_col + 0, 'COPY', self.style1)
                    uid_ws.write(uid_row + 1, uid_col + 1, 'WL', self.style1)
                    uid_ws.write(uid_row + 1, uid_col + 2, 'STR', self.style1)
                    uid_ws.write(uid_row + 1, uid_col + 3, 'COL', self.style1)
                    uid_ws.write(uid_row + 1, uid_col + 4, 'SPEC', self.style1)
                    uid_ws.write(uid_row + 1, uid_col + 5, 'UID', self.style1)
                    uid_ws.write(uid_row + 1, uid_col + 6, 'EXPECT', self.style1)
                    uid_ws.write(uid_row + 1, uid_col + 7, 'DBAR', self.style1)
                    uid_ws.write(uid_row + 1, uid_col + 8, 'MATCH', self.style1)
                    uid_copy_row = 0
                    for i in range(uid_range):  # copy0
                        uid_ws.write(uid_copy_row + uid_row + i + 2, uid_col + 0, 1, self.style1)
                        uid_ws.write(uid_copy_row + uid_row + i + 2, uid_col + 1, llt_class_ele.uid_addr_list_copy0[0],
                                     self.style1)
                        uid_ws.write(uid_copy_row + uid_row + i + 2, uid_col + 2, llt_class_ele.uid_addr_list_copy0[1],
                                     self.style1)
                        uid_ws.write(uid_copy_row + uid_row + i + 2, uid_col + 3, llt_class_ele.uid_addr_list_copy0[2],
                                     self.style1)
                        uid_ws.write(uid_copy_row + uid_row + i + 2, uid_col + 4, llt_class_ele.uid_SPEC_excel_print[i],
                                     self.style1)
                        uid_ws.write(uid_copy_row + uid_row + i + 2, uid_col + 5, llt_class_ele.uid_Data_excel_print_copy0[i],
                                     self.style1)
                        uid_ws.write(uid_copy_row + uid_row + i + 2, uid_col + 6, llt_class_ele.uid_Expect_excel_print[i],
                                     self.style1)
                        uid_ws.write(uid_copy_row + uid_row + i + 2, uid_col + 7,
                                     llt_class_ele.uid_Data_bar_excel_print_copy0[i], self.style1)
                        uid_ws.write(uid_copy_row + uid_row + i + 2, uid_col + 8, llt_class_ele.uid_result_excel_copy0[i],
                                     self.style1)
                        last_row_num = i
                    uid_copy_row = uid_range
                    for i in range(uid_range):  # copy1
                        uid_ws.write(uid_copy_row + uid_row + i + 2, uid_col + 0, 2, self.style1)
                        uid_ws.write(uid_copy_row + uid_row + i + 2, uid_col + 1, llt_class_ele.uid_addr_list_copy1[0],
                                     self.style1)
                        uid_ws.write(uid_copy_row + uid_row + i + 2, uid_col + 2, llt_class_ele.uid_addr_list_copy1[1],
                                     self.style1)
                        uid_ws.write(uid_copy_row + uid_row + i + 2, uid_col + 3, llt_class_ele.uid_addr_list_copy1[2],
                                     self.style1)
                        uid_ws.write(uid_copy_row + uid_row + i + 2, uid_col + 4, llt_class_ele.uid_SPEC_excel_print[i],
                                     self.style1)
                        uid_ws.write(uid_copy_row + uid_row + i + 2, uid_col + 5, llt_class_ele.uid_Data_excel_print_copy1[i],
                                     self.style1)
                        uid_ws.write(uid_copy_row + uid_row + i + 2, uid_col + 6, llt_class_ele.uid_Expect_excel_print[i],
                                     self.style1)
                        uid_ws.write(uid_copy_row + uid_row + i + 2, uid_col + 7,
                                     llt_class_ele.uid_Data_bar_excel_print_copy1[i], self.style1)
                        uid_ws.write(uid_copy_row + uid_row + i + 2, uid_col + 8, llt_class_ele.uid_result_excel_copy1[i],
                                     self.style1)
                        last_row_num = i
                    uid_copy_row = uid_range * 2
                    for i in range(uid_range):  # copy2
                        uid_ws.write(uid_copy_row + uid_row + i + 2, uid_col + 0, 3, self.style1)
                        uid_ws.write(uid_copy_row + uid_row + i + 2, uid_col + 1, llt_class_ele.uid_addr_list_copy2[0],
                                     self.style1)
                        uid_ws.write(uid_copy_row + uid_row + i + 2, uid_col + 2, llt_class_ele.uid_addr_list_copy2[1],
                                     self.style1)
                        uid_ws.write(uid_copy_row + uid_row + i + 2, uid_col + 3, llt_class_ele.uid_addr_list_copy2[2],
                                     self.style1)
                        uid_ws.write(uid_copy_row + uid_row + i + 2, uid_col + 4, llt_class_ele.uid_SPEC_excel_print[i],
                                     self.style1)
                        uid_ws.write(uid_copy_row + uid_row + i + 2, uid_col + 5, llt_class_ele.uid_Data_excel_print_copy2[i],
                                     self.style1)
                        uid_ws.write(uid_copy_row + uid_row + i + 2, uid_col + 6, llt_class_ele.uid_Expect_excel_print[i],
                                     self.style1)
                        uid_ws.write(uid_copy_row + uid_row + i + 2, uid_col + 7,
                                     llt_class_ele.uid_Data_bar_excel_print_copy2[i], self.style1)
                        uid_ws.write(uid_copy_row + uid_row + i + 2, uid_col + 8, llt_class_ele.uid_result_excel_copy2[i],
                                     self.style1)
                        last_row_num = i
                    uid_copy_row = uid_range * 3
                    for i in range(uid_range):  # copy3
                        uid_ws.write(uid_copy_row + uid_row + i + 2, uid_col + 0, 4, self.style1)
                        uid_ws.write(uid_copy_row + uid_row + i + 2, uid_col + 1, llt_class_ele.uid_addr_list_copy3[0],
                                     self.style1)
                        uid_ws.write(uid_copy_row + uid_row + i + 2, uid_col + 2, llt_class_ele.uid_addr_list_copy3[1],
                                     self.style1)
                        uid_ws.write(uid_copy_row + uid_row + i + 2, uid_col + 3, llt_class_ele.uid_addr_list_copy3[2],
                                     self.style1)
                        uid_ws.write(uid_copy_row + uid_row + i + 2, uid_col + 4, llt_class_ele.uid_SPEC_excel_print[i],
                                     self.style1)
                        uid_ws.write(uid_copy_row + uid_row + i + 2, uid_col + 5, llt_class_ele.uid_Data_excel_print_copy3[i],
                                     self.style1)
                        uid_ws.write(uid_copy_row + uid_row + i + 2, uid_col + 6, llt_class_ele.uid_Expect_excel_print[i],
                                     self.style1)
                        uid_ws.write(uid_copy_row + uid_row + i + 2, uid_col + 7,
                                     llt_class_ele.uid_Data_bar_excel_print_copy3[i], self.style1)
                        uid_ws.write(uid_copy_row + uid_row + i + 2, uid_col + 8, llt_class_ele.uid_result_excel_copy3[i],
                                     self.style1)
                        last_row_num = i
                    uid_ws.conditional_format(uid_row + 2, uid_col + 8, uid_copy_row + uid_row + last_row_num + 2, uid_col + 8,
                                              {'type': 'text', 'criteria': 'containing', 'value': 'Y',
                                               'format': self.conditional_style_pass})
                    uid_ws.conditional_format(uid_row + 2, uid_col + 8, uid_copy_row + uid_row + last_row_num + 2, uid_col + 8,
                                              {'type': 'text', 'criteria': 'containing', 'value': 'N',
                                               'format': self.conditional_style_fail})
                    uid_ws.conditional_format(uid_row + 2, uid_col + 8, uid_copy_row + uid_row + last_row_num + 2, uid_col + 8,
                                              {'type': 'text', 'criteria': 'containing', 'value': 'D-BAR',
                                               'format': self.conditional_style_D_BAR})
                    uid_col += 9
                    if llt_class_ele.uid_result != 1:
                        if llt_class_ele.uid_result == 0:
                            self.uid_result_summary = 'FAIL'
                        if llt_class_ele.uid_result == 2:
                            if self.uid_result_summary != 'FAIL':
                                self.uid_result_summary = 'D-BAR'
                if self.summary_enable:
                    self.summary_ws.write(self.summary_row, self.summary_col, self.summary_index, self.style1)
                    self.summary_ws.write(self.summary_row, self.summary_col + 1, 'UID', self.style1)
                    self.summary_ws.write_url(self.summary_row, self.summary_col + 2,
                                              'internal:uid!B2', self.style2)
                    self.summary_ws.write(self.summary_row, self.summary_col + 2, self.uid_result_summary, self.style2)
                    self.summary_index += 1
                    self.summary_row += 1
            except:
                    self.summary_ws.write(self.summary_row, self.summary_col, self.summary_index, self.style1)
                    self.summary_ws.write(self.summary_row, self.summary_col + 1, 'UID', self.style1)
                    self.summary_ws.write_url(self.summary_row, self.summary_col + 2,
                                              'internal:uid!B2', self.style2)
                    self.summary_ws.write(self.summary_row, self.summary_col + 2, 'None', self.style2)
                    self.summary_index += 1
                    self.summary_row += 1
    def stamp_excel(self):
        stamp_ws = self.wb.add_worksheet('STAMP')
        stamp_ws.freeze_panes(2, 1)
        stamp_row = 1
        stamp_row_temp = 0
        stamp_col = 1
        self.stamp_result_summary = 'PASS'
        stamp_ws.set_column('C:C', 22)
        stamp_ws.write(stamp_row, stamp_col + 0, 'DIE', self.style1)
        stamp_ws.write(stamp_row, stamp_col + 1, 'STAMP', self.style1)
        stamp_ws.write(stamp_row, stamp_col + 2, 'COPY', self.style1)
        stamp_ws.write(stamp_row, stamp_col + 3, 'p1', self.style1)
        stamp_ws.write(stamp_row, stamp_col + 4, 'P2', self.style1)
        stamp_ws.write(stamp_row, stamp_col + 5, 'P3', self.style1)
        stamp_ws.write(stamp_row, stamp_col + 6, 'P4', self.style1)
        stamp_ws.write(stamp_row, stamp_col + 7, 'P5', self.style1)
        stamp_ws.write(stamp_row, stamp_col + 8, 'P6', self.style1)
        stamp_ws.write(stamp_row, stamp_col + 9, 'P7', self.style1)
        stamp_ws.write(stamp_row, stamp_col + 10, 'P8', self.style1)
        stamp_ws.write(stamp_row, stamp_col + 11, 'EXPECT', self.style1)
        stamp_ws.write(stamp_row, stamp_col + 12, 'MATCH', self.style1)
        last_row_num = 0
        if not self.file_read_class.llt_class_list[0].stamp_excel_print_die:
            if self.summary_enable:
                self.summary_ws.write(self.summary_row, self.summary_col, self.summary_index, self.style1)
                self.summary_ws.write(self.summary_row, self.summary_col + 1, 'STAMP', self.style1)
                self.summary_ws.write_url(self.summary_row, self.summary_col + 2,
                                          'internal:STAMP!B2', self.style2)
                self.summary_ws.write(self.summary_row, self.summary_col + 2, 'None', self.style2)
                self.summary_index += 1
                self.summary_row += 1
        else:
            try:
                for llt_class_ele in self.file_read_class.llt_class_list:
                    for i, stamp_die in enumerate(llt_class_ele.stamp_excel_print_die):
                        stamp_ws.write(stamp_row + stamp_row_temp + 1 + i, stamp_col + 0, stamp_die, self.style1)
                        stamp_ws.write(stamp_row + stamp_row_temp + 1 + i, stamp_col + 1,
                                       llt_class_ele.stamp_excel_print_name[i], self.style1)
                        stamp_ws.write(stamp_row + stamp_row_temp + 1 + i, stamp_col + 2,
                                       llt_class_ele.stamp_excel_print_copy[i], self.style1)
                        stamp_ws.write(stamp_row + stamp_row_temp + 1 + i, stamp_col + 3,
                                       llt_class_ele.stamp_excel_print_data[8 * i + 0], self.style1)
                        stamp_ws.write(stamp_row + stamp_row_temp + 1 + i, stamp_col + 4,
                                       llt_class_ele.stamp_excel_print_data[8 * i + 1], self.style1)
                        stamp_ws.write(stamp_row + stamp_row_temp + 1 + i, stamp_col + 5,
                                       llt_class_ele.stamp_excel_print_data[8 * i + 2], self.style1)
                        stamp_ws.write(stamp_row + stamp_row_temp + 1 + i, stamp_col + 6,
                                       llt_class_ele.stamp_excel_print_data[8 * i + 3], self.style1)
                        stamp_ws.write(stamp_row + stamp_row_temp + 1 + i, stamp_col + 7,
                                       llt_class_ele.stamp_excel_print_data[8 * i + 4], self.style1)
                        stamp_ws.write(stamp_row + stamp_row_temp + 1 + i, stamp_col + 8,
                                       llt_class_ele.stamp_excel_print_data[8 * i + 5], self.style1)
                        stamp_ws.write(stamp_row + stamp_row_temp + 1 + i, stamp_col + 9,
                                       llt_class_ele.stamp_excel_print_data[8 * i + 6], self.style1)
                        stamp_ws.write(stamp_row + stamp_row_temp + 1 + i, stamp_col + 10,
                                       llt_class_ele.stamp_excel_print_data[8 * i + 7], self.style1)
                        stamp_ws.write(stamp_row + stamp_row_temp + 1 + i, stamp_col + 11,
                                       llt_class_ele.stamp_excel_print_expect[i], self.style1)
                        stamp_ws.write(stamp_row + stamp_row_temp + 1 + i, stamp_col + 12,
                                       llt_class_ele.stamp_excel_print_match[i], self.style1)
                        last_row_num = i
                    stamp_row_temp += (last_row_num + 1)
                    if llt_class_ele.stamp_die_result != 1:
                        self.stamp_result_summary = 'FAIL'
                stamp_ws.conditional_format(stamp_row + 1, stamp_col + 12, stamp_row + stamp_row_temp, stamp_col + 12,
                                            {'type': 'text', 'criteria': 'containing', 'value': 'Y',
                                             'format': self.conditional_style_pass})
                stamp_ws.conditional_format(stamp_row + 1, stamp_col + 12, stamp_row + stamp_row_temp, stamp_col + 12,
                                            {'type': 'text', 'criteria': 'containing', 'value': 'N',
                                             'format': self.conditional_style_fail})
                if self.summary_enable:
                    self.summary_ws.write(self.summary_row, self.summary_col, self.summary_index, self.style1)
                    self.summary_ws.write(self.summary_row, self.summary_col + 1, 'STAMP', self.style1)
                    self.summary_ws.write_url(self.summary_row, self.summary_col + 2,
                                              'internal:STAMP!B2', self.style2)
                    self.summary_ws.write(self.summary_row, self.summary_col + 2, self.stamp_result_summary, self.style2)
                    self.summary_index += 1
                    self.summary_row += 1
            except:
                if self.summary_enable:
                    self.summary_ws.write(self.summary_row, self.summary_col, self.summary_index, self.style1)
                    self.summary_ws.write(self.summary_row, self.summary_col + 1, 'STAMP', self.style1)
                    self.summary_ws.write_url(self.summary_row, self.summary_col + 2,
                                              'internal:STAMP!B2', self.style2)
                    self.summary_ws.write(self.summary_row, self.summary_col + 2, 'None', self.style2)
                    self.summary_index += 1
                    self.summary_row += 1
    def dist_vt_excel(self):
        dist_vt_excel_row = 3
        dist_vt_excel_col = 1
        x_tick = [0.4, 0.8, 1.2, 1.6, 2.0, 2.4, 2.8, 3.2, 3.6, 4.0, 4.4, 4.8, 5.2, 5.6, 6.0, 6.4, 6.8]
        llt_class_last = None
        try:
            for llt_class_ele in self.file_read_class.llt_class_list:
                for excel_list_element in llt_class_ele.dist_vt_dict['Excel_list']:
                    if excel_list_element not in self.dist_vt_result_summary:
                        self.dist_vt_result_summary[excel_list_element] = "PASS"
                    if excel_list_element == 'DUMMY WL VT':
                        fig_plt = plt.figure(num=None, figsize=(90.8, 4.38), dpi=100, facecolor='w', edgecolor='k',)
                    else:
                        fig_plt = plt.figure(num=None, figsize=(11.75, 4.38), dpi=100, facecolor='w', edgecolor='k')
                    if llt_class_ele.name in 'DIE 0':
                        self.wb_dict[excel_list_element] = self.wb.add_worksheet(excel_list_element)
                        self.wb_dict[excel_list_element].merge_range(dist_vt_excel_row - 2, dist_vt_excel_col,
                                                                     dist_vt_excel_row - 2, dist_vt_excel_col + 14,
                                                                     llt_class_ele.dist_vt_dict[
                                                                         excel_list_element + '_Title'], self.style1)
                        self.wb_dict[excel_list_element].merge_range(dist_vt_excel_row - 1, dist_vt_excel_col,
                                                                     dist_vt_excel_row - 1, dist_vt_excel_col + 14,
                                                                     llt_class_ele.dist_vt_dict[
                                                                    excel_list_element + '_Comment'], self.style1)
                    #print(excel_list_element)
                    if excel_list_element == 'DUMMY WL VT':
                        for Label_list_element in llt_class_ele.dist_vt_dict[excel_list_element + 'Label_list']:
                            #print(Label_list_element)
                            plt.subplot(181+llt_class_ele.dist_vt_dict[excel_list_element + 'Label_list'].index(Label_list_element))
                            plt.plot(llt_class_ele.dist_vt_dict[excel_list_element + Label_list_element + '_X'],
                                     llt_class_ele.dist_vt_dict[excel_list_element + Label_list_element + '_Y'],
                                     label=llt_class_ele.name + ' ' + Label_list_element)
                            x = llt_class_ele.dist_vt_dict[excel_list_element + Label_list_element + '_X']
                            y = llt_class_ele.dist_vt_dict[excel_list_element + Label_list_element + '_Y']
                            ymax_x = np.argmax(y)
                            # print(x[ymax_x], y[ymax_x])
                            plt.scatter(x[ymax_x], 1, s=20, marker='o')
                            plt.axvline(x=x[ymax_x], color='r', linestyle='--')
                            plt.annotate(str(x[ymax_x]), xy=(x[ymax_x]+0.1, 1.2))
                            plt.xlabel('vt(V)', size='15')
                            plt.ylabel('Population', size='15')
                            plt.axis(xmin=0, xmax=6.8, ymin=1)
                            plt.xticks(x_tick)
                            plt.minorticks_on()
                            plt.grid(True)
                            plt.yscale('log')
                            plt.legend()
                    else:
                        for Label_list_element in llt_class_ele.dist_vt_dict[excel_list_element + 'Label_list']:
                            #print(Label_list_element)
                            #print(llt_class_ele.dist_vt_dict[excel_list_element + 'Label_list'].index(Label_list_element))
                            plt.plot(llt_class_ele.dist_vt_dict[excel_list_element + Label_list_element + '_X'],
                                     llt_class_ele.dist_vt_dict[excel_list_element + Label_list_element + '_Y'],
                                     label=llt_class_ele.name + ' ' + Label_list_element)
                        plt.xlabel('vt(V)', size='15')
                        plt.ylabel('Population', size='15')
                        plt.axis(xmin=0, xmax=6.8, ymin=1)
                        plt.xticks(x_tick)
                        plt.minorticks_on()
                    if "PASS" in llt_class_ele.dist_vt_dict[excel_list_element + '_Result']:
                        plt.title(llt_class_ele.name + ' ' + excel_list_element + ' ' +
                                  llt_class_ele.dist_vt_dict[excel_list_element + '_Result'])
                    else:
                        plt.title(llt_class_ele.name + ' ' + excel_list_element + ' ' +
                                  llt_class_ele.dist_vt_dict[excel_list_element + '_Result'], color="red")
                    plt.grid(True)
                    plt.yscale('log')
                    plt.legend()
                    # plt.rcParams["axes.edgecolor"] = "black"
                    # plt.rcParams["axes.linewidth"] = 1
                    # create figure folder if not exist
                    if not os.path.exists('./figure'):
                        os.makedirs('./figure')
                    figure_file_name = './figure/' + llt_class_ele.name + excel_list_element + '.png'
                    plt.savefig(figure_file_name,bbox_inches='tight')
                    self.wb_dict[excel_list_element].insert_image(dist_vt_excel_row, dist_vt_excel_col, figure_file_name)
                    plt.close(fig_plt)
                    # summary print
                    if "FAIL" in llt_class_ele.dist_vt_dict[excel_list_element + '_Result']:
                        self.dist_vt_result_summary[excel_list_element] = "FAIL"
                dist_vt_excel_row += 21
                llt_class_last = llt_class_ele
            if self.summary_enable:
                for excel_list_element in llt_class_last.dist_vt_dict['Excel_list']:
                    self.summary_ws.write(self.summary_row, self.summary_col, self.summary_index, self.style1)
                    self.summary_ws.write(self.summary_row, self.summary_col + 1, excel_list_element, self.style1)
                    self.summary_ws.write_url(self.summary_row, self.summary_col + 2,
                                              'internal:' + '\'' + excel_list_element + '\'!B2', self.style2)
                    self.summary_ws.write(self.summary_row, self.summary_col + 2,
                                          self.dist_vt_result_summary[excel_list_element], self.style2)
                    self.summary_index += 1
                    self.summary_row += 1
        except:
            if self.summary_enable:
                for excel_list_element in ['ROM VT','UROM VT','FW GB VT','FW BB VT','DUMMY WL VT']:
                    self.summary_ws.write(self.summary_row, self.summary_col, self.summary_index, self.style1)
                    self.summary_ws.write(self.summary_row, self.summary_col + 1, excel_list_element, self.style1)
                    self.summary_ws.write_url(self.summary_row, self.summary_col + 2,
                                              'internal:' + '\'' + excel_list_element + '\'!B2', self.style2)
                    self.summary_ws.write(self.summary_row, self.summary_col + 2,
                                          'None', self.style2)
                    self.summary_index += 1
                    self.summary_row += 1
    def test_time_excel(self):
        test_time_ws = self.wb.add_worksheet(self.flow + '_TT')
        test_time_ws.freeze_panes(1, 0)
        test_time_ws.set_column('A:A', 50)
        test_time_ws.set_column('B:I', 9.5)
        test_time_row = 0
        test_time_col = 0
        # Title print
        test_time_ws.write(test_time_row, test_time_col + 0, 'Test Block', self.style6)
        test_time_ws.write(test_time_row, test_time_col + 1, 'TT(s)', self.style6)
        test_time_ws.write(test_time_row, test_time_col + 2, 'TT(m)', self.style6)
        test_time_ws.write(test_time_row, test_time_col + 3, 'TT(h)', self.style6)
        test_time_ws.write(test_time_row, test_time_col + 4, '%', self.style6)

        test_time_total_sort_dict = self.file_read_class.mt_class_list[0].test_time_dict
        total_tt = 0
        for test_time_dict in test_time_total_sort_dict:
            total_tt += test_time_total_sort_dict[test_time_dict]
        test_time_total_sort_dict['TOTAL'] = total_tt
        # Test time data collect

        # Sorting
        sorted_tt_test_block_list = sorted(test_time_total_sort_dict, key=test_time_total_sort_dict.get,
                                           reverse=True)
        # Print
        i = 1
        for Sorted_TT_test_block in sorted_tt_test_block_list:
            avg_tt = test_time_total_sort_dict[Sorted_TT_test_block]
            test_time_ws.write(test_time_row + i, test_time_col + 0, Sorted_TT_test_block, self.style7)
            test_time_ws.write(test_time_row + i, test_time_col + 1, avg_tt, self.style8)
            test_time_ws.write(test_time_row + i, test_time_col + 2, avg_tt / 60, self.style8)
            test_time_ws.write(test_time_row + i, test_time_col + 3, avg_tt / 3600, self.style8)
            test_time_ws.write(test_time_row + i, test_time_col + 4, avg_tt / total_tt, self.style9)
            i += 1
        # Conditional formatting
        test_time_ws.conditional_format(test_time_row + 2, test_time_col + 4, test_time_row + i, test_time_col + 4,
                                        {'type': '3_color_scale', 'min_color': '#63BE7B', 'max_color': '#F8696B'})
        test_time_ws.conditional_format(test_time_row + 1, test_time_col + 8, test_time_row + i, test_time_col + 8,
                                        {'type': '3_color_scale', 'min_color': '#63BE7B', 'max_color': '#F8696B'})
        if self.summary_enable:
            self.summary_ws.write(self.summary_row, self.summary_col, self.summary_index, self.style1)
            self.summary_ws.write(self.summary_row, self.summary_col + 1, self.flow+'_TT', self.style1)
            self.summary_ws.write_url(self.summary_row, self.summary_col + 2,
                                      'internal:'+self.flow+'_TT!B2', self.style2)
            self.summary_ws.write(self.summary_row, self.summary_col + 2, 'Review', self.style2)
            self.summary_index += 1
            self.summary_row += 1

    def test_time_excel1(self):
        #if no cst datalog will not excute below tt excel print!!!
        try:
            test_time_ws = self.wb.add_worksheet('CST_TT')
            test_time_ws.freeze_panes(1, 0)
            test_time_ws.set_column('A:A', 50)
            test_time_ws.set_column('B:I', 9.5)
            test_time_row = 0
            test_time_col = 0
            # Title print
            test_time_ws.write(test_time_row, test_time_col + 0, 'Test Block', self.style6)
            test_time_ws.write(test_time_row, test_time_col + 1, 'AVG_TT(s)', self.style6)
            test_time_ws.write(test_time_row, test_time_col + 2, 'AVG_TT(m)', self.style6)
            test_time_ws.write(test_time_row, test_time_col + 3, 'AVG_TT(h)', self.style6)
            test_time_ws.write(test_time_row, test_time_col + 4, '%', self.style6)
    
            test_time_total_sort_dict = self.file_read_class.mt_class_list[0].test_time_dict1
            for k,v in test_time_total_sort_dict.items():
                test_time_total_sort_dict[k] = np.mean(v)
            total_tt = 0
            for test_time_dict in test_time_total_sort_dict:
                total_tt += test_time_total_sort_dict[test_time_dict]
            test_time_total_sort_dict['TOTAL'] = total_tt
            # Test time data collect
    
            # Sorting
            sorted_tt_test_block_list = sorted(test_time_total_sort_dict, key=test_time_total_sort_dict.get,
                                               reverse=True)
            # Print
            i = 1
            for Sorted_TT_test_block in sorted_tt_test_block_list:
                avg_tt = test_time_total_sort_dict[Sorted_TT_test_block]
                test_time_ws.write(test_time_row + i, test_time_col + 0, Sorted_TT_test_block, self.style7)
                test_time_ws.write(test_time_row + i, test_time_col + 1, avg_tt, self.style8)
                test_time_ws.write(test_time_row + i, test_time_col + 2, avg_tt / 60, self.style8)
                test_time_ws.write(test_time_row + i, test_time_col + 3, avg_tt / 3600, self.style8)
                test_time_ws.write(test_time_row + i, test_time_col + 4, avg_tt / total_tt, self.style9)
                i += 1
            # Conditional formatting
            test_time_ws.conditional_format(test_time_row + 2, test_time_col + 4, test_time_row + i, test_time_col + 4,
                                            {'type': '3_color_scale', 'min_color': '#63BE7B', 'max_color': '#F8696B'})
            test_time_ws.conditional_format(test_time_row + 1, test_time_col + 8, test_time_row + i, test_time_col + 8,
                                            {'type': '3_color_scale', 'min_color': '#63BE7B', 'max_color': '#F8696B'})
            if self.summary_enable:
                self.summary_ws.write(self.summary_row, self.summary_col, self.summary_index, self.style1)
                self.summary_ws.write(self.summary_row, self.summary_col + 1, 'CST_TT', self.style1)
                self.summary_ws.write_url(self.summary_row, self.summary_col + 2,
                                          'internal:CST_TT!B2', self.style2)
                self.summary_ws.write(self.summary_row, self.summary_col + 2, 'Review', self.style2)
                self.summary_index += 1
                self.summary_row += 1
        except:
            if self.summary_enable:
                self.summary_ws.write(self.summary_row, self.summary_col, self.summary_index, self.style1)
                self.summary_ws.write(self.summary_row, self.summary_col + 1, 'CST_TT', self.style1)
                self.summary_ws.write_url(self.summary_row, self.summary_col + 2,
                                          'internal:CST_TT!B2', self.style2)
                self.summary_ws.write(self.summary_row, self.summary_col + 2, 'None', self.style2)
                self.summary_index += 1
                self.summary_row += 1

    # jason add mrph
    def mrph_excel(self):
        # print("Saving MRPH......")
        if self.file_read_class.llt_class_list[0].product == "CSS":
            [mrph_page, rd_mrph_ver, rd_track_ver, mrph_ver_pf, tracker_ver_pf, exp_mrph_ver, exp_tracker_ver] = \
                self.file_read_class.llt_class_list[0].mrph_list
            # print(mrph_page)
            if mrph_page: # even css sometimes we will skip mrph, so need check this to decide if creating the sheet or not
                worksheet_mrph = self.wb.add_worksheet("MRPH")
                t_format = self.wb.add_format({
                    'bg_color': '#86ff9b',
                })
                f_format = self.wb.add_format({
                    'bg_color': '#F48F8A',
                })
                worksheet_mrph.conditional_format('A1:C100000',
                                                  {'type': 'text',
                                                   'criteria': 'containing',
                                                   'value': 'No error',
                                                   'format': t_format
                                                   })
                worksheet_mrph.conditional_format('A1:C100000',
                                                  {'type': 'text',
                                                   'criteria': 'containing',
                                                   'value': 'file',
                                                   'format': f_format
                                                   })

                worksheet_mrph.conditional_format('B1:G100000',
                                                  {'type': 'text',
                                                   'criteria': 'containing',
                                                   'value': 'Y',
                                                   'format': self.conditional_style_pass
                                                   })
                worksheet_mrph.conditional_format('B1:G100000',
                                                  {'type': 'text',
                                                   'criteria': 'containing',
                                                   'value': 'N',
                                                   'format': self.conditional_style_fail
                                                   })
                count = 1
                worksheet_mrph.write(0, 0, "block-wl-string", self.style1)
                worksheet_mrph.write(0, 1, "UR vs MRPH/page", self.style1)
                worksheet_mrph.set_column("A:A", 30)
                worksheet_mrph.set_column("B:B", 50)
                worksheet_mrph.set_column("C:C", 30)
                worksheet_mrph.set_column("D:D", 30)
                for page in mrph_page:
                    # in case you enable mrph check but somehow you haven't specify your mrph path correctly
                    # so NNT cannot open the golden pattern -> it will print out
                    if mrph_page[page]:
                        if "No error found" in mrph_page[page]:
                            worksheet_mrph.write(count, 0, page, self.style1)
                            worksheet_mrph.write(count, 1, mrph_page[page][0], self.style1)
                            count = count + 1
                        else:
                            for j in range(len(list(mrph_page[page][0]))):
                                worksheet_mrph.write(count + j, 1, " ".join(list(mrph_page[page][0][j])), self.style1)
                            count = count + len(list(mrph_page[page][0]))
                            if len(list(mrph_page[page][0])) == 1:
                                worksheet_mrph.write("A" + str(count + 1 - len(list(mrph_page[page][0]))), page, self.style1)
                            else:
                                worksheet_mrph.merge_range(
                                    "A" + str(count + 1 - len(list(mrph_page[page][0]))) + ":A" + str(count), page, self.style1)

                if rd_mrph_ver:
                    worksheet_mrph.write(0, 2, "WL35 MRPH", self.style1)
                    worksheet_mrph.write(1, 2, rd_mrph_ver, self.style1)
                    worksheet_mrph.write(0, 3, "Expected MRPH", self.style1)
                    worksheet_mrph.write(1, 3, exp_mrph_ver, self.style1)
                    worksheet_mrph.write(0, 4, "PF", self.style1)
                    if mrph_ver_pf == "Y":
                        worksheet_mrph.write(1, 4, mrph_ver_pf, self.style1)
                    else:
                        worksheet_mrph.write(1, 4, mrph_ver_pf, self.style1)

                if rd_track_ver:
                    worksheet_mrph.write(2, 2, "WL41 TRACKER", self.style1)
                    worksheet_mrph.write(3, 2, rd_track_ver, self.style1)
                    worksheet_mrph.write(2, 3, "Expected TRACKER", self.style1)
                    worksheet_mrph.write(3, 3, exp_tracker_ver.upper(), self.style1)
                    worksheet_mrph.write(2, 4, "PF", self.style1)
                    if tracker_ver_pf == "Y":
                        worksheet_mrph.write(3, 4, tracker_ver_pf, self.style1)
                    else:
                        worksheet_mrph.write(3, 4, tracker_ver_pf, self.style1)
                if mrph_ver_pf == "Y" and tracker_ver_pf == "Y":
                    self.mrph_summary = "PASS"
                else:
                    self.mrph_summary = "FAIL"
            else:
                self.mrph_summary = "None"
            self.summary_ws.write(self.summary_row, self.summary_col, self.summary_index, self.style1)
            self.summary_ws.write(self.summary_row, self.summary_col + 1, 'MRPH', self.style1)
            self.summary_ws.write_url(self.summary_row, self.summary_col + 2,
                                      'internal:MRPH!B2', self.style2)
            self.summary_ws.write(self.summary_row, self.summary_col + 2, self.mrph_summary, self.style2)
            self.summary_index += 1
            self.summary_row += 1
        else:
            self.mrph_summary = "None"
            # print("MRPH is skipped!")
            pass
            # self.summary_ws.write(self.summary_row, self.summary_col, self.summary_index, self.style1)
            # self.summary_ws.write(self.summary_row, self.summary_col + 1, 'MRPH', self.style1)
            # self.summary_ws.write_url(self.summary_row, self.summary_col + 2,
            #                           'internal:MRPH!B2', self.style2)
            # self.summary_ws.write(self.summary_row, self.summary_col + 2, 'None', self.style2)
            # self.summary_index += 1
            # self.summary_row += 1

    def close_excel(self):
        if self.summary_enable:
            self.summary_ws.conditional_format(2, 3, self.summary_row - 1, 3,
                                               {'type': 'text', 'criteria': 'containing', 'value': 'PASS',
                                                'format': self.conditional_style_pass})
            self.summary_ws.conditional_format(2, 3, self.summary_row - 1, 3,
                                               {'type': 'text', 'criteria': 'containing', 'value': 'FAIL',
                                                'format': self.conditional_style_fail})
            self.summary_ws.conditional_format(2, 3, self.summary_row - 1, 3,
                                               {'type': 'text', 'criteria': 'containing', 'value': 'D-BAR',
                                                'format': self.conditional_style_D_BAR})
            self.summary_ws.conditional_format(2, 3, self.summary_row - 1, 3,
                                               {'type': 'text', 'criteria': 'containing', 'value': 'NO TRIM TABLE',
                                                'format': self.conditional_style_fail})
        self.wb.close()

    def excel_exec(self):
        # If MT/LLT datalog exist
        if self.file_read_class.mt_datalog_file_match & self.file_read_class.llt_file_match:
            # If DUT match with LLT and MT datalog
            # jason: some times we only want to check trim, CFL is not run?
            if self.file_read_class.llt_class_die0.lwxy_match_dut:
                self.summary(self.file_read_class.llt_class_die0.lwxy_match_dut)
                self.por_excel_print()
                self.id_excel_print()
                self.lwxy_excel()
                self.bb_excel()
                self.bc_excel()
                self.trim_excel(self.file_read_class.trim_file_match)
                # self.key_para_excel()
                self.uid_excel()
                self.stamp_excel()
                self.dist_vt_excel()
                self.mrph_excel()
                self.test_time_excel()
                self.test_time_excel1()
            else:
                self.summary(self.file_read_class.llt_class_die0.lwxy_match_dut)
        # If MT file exist and LLT file miss
        elif self.file_read_class.mt_datalog_file_match & ~self.file_read_class.llt_file_match:
            self.summary(2)
        # If MT file miss and LLT file exist -- there is a situation: we only run CST to check trim
        elif ~self.file_read_class.mt_datalog_file_match & self.file_read_class.llt_file_match:
            self.summary(3)
        # If Both MT and LLT file miss
        else:
            self.summary(4)
        self.close_excel()
        # open excel file
        os.startfile(os.getcwd() + self.filename_open)
