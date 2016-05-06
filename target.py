import peewee, os
import xlrd, datetime
import export_to_excel

from models.model_owner import Owner
from models.model_action import Action

class activities_by_lead:
    def __init__(self):
        self.excel_map = {"owner"          : "D",
                          "subject"        : "E",
                          "activitytype"   : "F",
                          "activitystatus" : "G",
                          "lastupdated"    : "I",
                          "company"        : "J",
                          "firstname"      : "K",
                          "lastname"       : "L"}

        self.excel_spreadsheet = os.path.expanduser("~/VMs/spreadsheets/adjunct/Activities by Lead.xlsx")
        # self.excel_spreadsheet = "C:\\Users\\roger\\Documents\\Programming\\Activities\\adjunct\\Activities by Lead.xlsx"
        self.excel_sheet_name = 'Activity Advanced Find View'

    def export(self):
        export_to_excel.read(self.excel_spreadsheet, self.excel_sheet_name, self)

    def export_row(self, row, row_number, excel_workbook, excel_sheet):
        owner_name = excel_sheet.cell(row, export_to_excel.getColumn(self.excel_map, 'owner')).value
        try:
            owner_object = Owner.select().where(Owner.owner == owner_name).get()
            if not owner_object.active:
                return
        except peewee.DoesNotExist:
            return

        last_updated_date = export_to_excel.get_excel_date_column(row, 'lastupdated', self.excel_map, excel_workbook, excel_sheet)

        row_data = {'Owner': owner_object,
                    'Company': excel_sheet.cell(row, export_to_excel.getColumn(self.excel_map, 'company')).value,
                    'FirstName': excel_sheet.cell(row, export_to_excel.getColumn(self.excel_map, 'firstname')).value,
                    'LastName': excel_sheet.cell(row, export_to_excel.getColumn(self.excel_map, 'lastname')).value,
                    'Subject': excel_sheet.cell(row, export_to_excel.getColumn(self.excel_map, 'subject')).value,
                    'ActivityType': excel_sheet.cell(row, export_to_excel.getColumn(self.excel_map, 'activitytype')).value,
                    'ActivityStatus': excel_sheet.cell(row, export_to_excel.getColumn(self.excel_map, 'activitystatus')).value,
                    'LastUpdated': last_updated_date[export_to_excel.CELL_DATE],
                    'LastUpdatedIsoWeek': last_updated_date[export_to_excel.CELL_ISO_WEEK],
                    'LastUpdatedIsoYear': last_updated_date[export_to_excel.CELL_ISO_YEAR],
                    'LastUpdatedIsoYearWeek': last_updated_date[export_to_excel.CELL_ISO_YEAR_WEEK_SLASH],
                    'RowNumber': row_number,
                    'SourceSpreadsheet': self.excel_spreadsheet,
                    'CrmEntity': 'Lead' }

        action = Action(**row_data)
        action.save()

obj = activities_by_lead()
obj.export()