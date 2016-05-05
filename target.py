import common.helper_common as common
import peewee
import xlrd, datetime
from model_owner import Owner
from model_action import Action

# ISO_WEEK = 1
# ISO_YEAR = 0

excel_map = {"owner"          : "D",
             "subject"        : "E",
             "activitytype"   : "F",
             "activitystatus" : "G",
             "lastupdated"    : "I",
             "company"        : "J",
             "firstname"      : "K",
             "lastname"       : "L"
     }

def read_spreadsheet(excel_sheet):
    i = 1
    for row in range(1, excel_sheet.nrows):
        yield(row)

def populate_dictionary(row, row_number, excel_workbook, excel_sheet, owner_object, source_spreadsheet):
    last_updated_date_cell = excel_sheet.cell(row, common.getColumn(excel_map, 'lastupdated')).value
    last_updated_date = common.convert_excel_date_cell_to_date(last_updated_date_cell, excel_workbook)

    act = {'Owner': owner_object,
           'Company': excel_sheet.cell(row, common.getColumn(excel_map, 'company')).value,
           'FirstName': excel_sheet.cell(row, common.getColumn(excel_map, 'firstname')).value,
           'LastName': excel_sheet.cell(row, common.getColumn(excel_map, 'lastname')).value,
           'Subject': excel_sheet.cell(row, common.getColumn(excel_map, 'subject')).value,
           'ActivityType': excel_sheet.cell(row, common.getColumn(excel_map, 'activitytype')).value,
           'ActivityStatus': excel_sheet.cell(row, common.getColumn(excel_map, 'activitystatus')).value,
           'LastUpdated': last_updated_date[0],
           'LastUpdatedIsoWeek': last_updated_date[1],
           'LastUpdatedIsoYear': last_updated_date[2],
           'RowNumber': row_number,
           'SourceSpreadsheet': source_spreadsheet,
           'CrmEntity': 'Lead'
           }
    return act

def read(excel_file_name, source_spreadsheet):
    excel_workbook = xlrd.open_workbook(excel_file_name)
    excel_sheet = excel_workbook.sheet_by_name('Activity Advanced Find View')
    read_generator = read_spreadsheet(excel_sheet)

    row_number = 1
    for row in read_generator:
        if (row_number == 1 or row_number % 100 == 0):
            print(row_number)

        row_number += 1
        if row_number > 300:
          return


        owner_name = excel_sheet.cell(row, common.getColumn(excel_map, 'owner')).value
        try:
            owner_object = Owner.select().where(Owner.owner == owner_name).get()
        except peewee.DoesNotExist:
            continue

        act = populate_dictionary(row, row_number, excel_workbook, excel_sheet, owner_object, source_spreadsheet)

        action = Action(**act)
        action.save()


read("C:\\Users\\roger\\Documents\\Programming\\Activities\\adjunct\\Activities by Lead.xlsx", 'Activities by Lead.xlsx')