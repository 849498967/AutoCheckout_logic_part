import file_read
import excel_print
from easygui import msgbox
import traceback

#datalog_path = './B5_andy/'
datalog_path = './Datalog/'
# Make to EXE
# "C:\Users\19981\AppData\Local\Programs\Python\Python38\python.exe" "C:\Users\19981\AppData\Local\Programs\Python\Python38\Scripts\pyinstaller.exe" C:\Users\19981\PycharmProjects\MT_single_package_checkout_JHN\main.py --windowed --onefile

# file read and grab data
# print(1)
try:
    file_read_class = file_read.FileReadClass(datalog_path)
except Exception as Error_print:
    msgbox("Cannot find 3 datalogs. Please double check the MT datalog. \n "
           "Please send email to jihyun.nam@wdc.com/Maurice.Mao@wdc.com if you cannot fix the issue \n\n"
           "Error code: \n" + str(traceback.format_exc()),
           title="Error")
# print(2)
try:
    file_read_class.read_mt_datalog()
except Exception as Error_print:
    
    msgbox("MT datalog read error. Please double check the MT datalogs. \n" +
           "Please send email to jihyun.nam@wdc.com/Maurice.Mao@wdc.com if you cannot fix the issue \n\n"
           "Error code: \n" + str(traceback.format_exc()),
           title="Error")
# print(3)
#file_read_class.read_trim_table()
try:
    file_read_class.read_trim_table()
except Exception as Error_print:
    msgbox("Trim table read error. Please double check the Trim table. \n" +
           "Please send email to jihyun.nam@wdc.com/Maurice.Mao@wdc.com if you cannot fix the issue \n\n"
           "Error code: \n" + str(traceback.format_exc()),
           title="Error")
# print(4)
#file_read_class.read_llt_datalog()
try:
    file_read_class.read_llt_datalog()
except Exception as Error_print:
    msgbox("NanoNT datalog read error. Please double check the Nanont datalog. \n" +
           "Please send email to jihyun.nam@wdc.com/Maurice.Mao@wdc.com if you cannot fix the issue \n\n"
           "Error code: \n" + str(traceback.format_exc()),
           title="Error")
# print(5)
try:
    # excel print
    excel_print_class = excel_print.ExcelPrint(file_read_class)
    # print(6)
    excel_print_class.excel_exec()
except Exception as Error_print:
    msgbox("Excel print error.\n" +
           "Please send email to jihyun.nam@wdc.com/Maurice.Mao@wdc.com \n\n"
           "Error code: \n" + str(traceback.format_exc()),
           title="Error")

