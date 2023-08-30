from datetime import datetime
from RPA.Excel.Files import Files


class FormatDate:

    MONTH_ABBREVIATIONS = {
        "Jan.": "January", "Feb.": "February", "Mar.": "March",
        "Apr.": "April", "May": "May", "Jun.": "June",
        "Jul.": "July", "Aug.": "August", "Sep.": "September",
        "Oct.": "October", "Nov.": "November", "Dec.": "December"
    }

    # The filteration functionality is not working on https://www.nytimes.com/.
    # So this method will process the date that will be used to filter out articles with in provided date range.
    def process_date(self, date_str):
        current_year = datetime.now().year
        date_str = date_str.strip()
        date_parts = date_str.split()
        if "," in date_str or "." in date_str:
            # Format dates which has . or , like "Feb. 7" or "Sept. 8, 2022".
            month_name = self.MONTH_ABBREVIATIONS.get(date_parts[0], "")
            if not month_name:
                return None
            if len(date_parts) == 2:
                day = int(date_parts[1])
                year = current_year
            else:
                day = int(date_parts[1].replace(",", ""))
                year = int(date_parts[2])
        else:
            # Format dates which don't have . or , Like March 12
            if len(date_parts) < 2:
                return None
            month_name = date_parts[0]
            day = int(date_parts[1])
            year = current_year
        month_number = datetime.strptime(month_name, "%B").month
        date = datetime(year, month_number, day).date()
        return date


class ExcelGenerator:

    def __init__(self):
        self.files = Files()

    # This method will generate Excel file with all the scraped data
    def write_to_excel(self, data):
        wb = self.files.create_workbook()
        wb.create_worksheet("data")
        for entry in data:
            self.files.append_rows_to_worksheet({
                 "Title": [entry["Title"]],
                 "Date": [entry["Date"]],
                 "Description": [entry["Description"]],
                 "Picture_filename": [entry["Picture_filename"]],
                 "Search Phrase Count": [entry["Search Phrase Count"]],
                 "Money in Title": [entry["Money in Title"]],
                 "Money in Description": [entry["Money in Description"]]},
                header=True)
        self.files.save_workbook("output/output.xlsx")
