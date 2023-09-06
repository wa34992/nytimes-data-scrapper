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
        work_item = work_items.get_work_item_payload()
        search_phrase = work_item["search_phrase"]
        news_category = work_item.get("news_category", [])
        num_months = work_item.get("num_months", 3)
    else:
        # in case of development
        search_phrase = "python"
        news_category = []
        num_months = 2
    extractor.run(search_phrase, news_category, num_months)
