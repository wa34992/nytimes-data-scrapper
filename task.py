import os
from RPA.Robocorp.WorkItems import WorkItems
from modules.nytimes.data_extractor import DataExtractor

# Starting process
if __name__ == "__main__":
    extractor = DataExtractor()
    env = os.getenv('ENV')
    if env == 'PROD':
        work_items = WorkItems()
        work_items.get_input_work_item()
        work_item = work_items.get_work_item_variables()
        search_phrase = work_item["variables"]["search_phrase"]
        news_category = work_item["variables"]["news_category"]
        num_months = work_item["variables"]["num_months"]
    else:
        search_phrase = "python"
        news_category = []
        num_months = 3
    extractor.run(search_phrase, news_category, num_months)
