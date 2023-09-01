import os
from RPA.Robocorp.WorkItems import WorkItems
from modules.nytimes.data_extractor import DataExtractor

# Starting process
if __name__ == "__main__":
    extractor = DataExtractor()
    env = os.getenv('ENV')
    print("env----", env)
    if env == 'PROD':
        print("env", env)
        work_items = WorkItems()
        print("work_items", work_items)
        work_items.get_input_work_item()
        print("work_items", work_items)
        work_item = work_items.get_work_item_payload()
        print("work_item", work_item)
        search_phrase = work_item["search_phrase"]
        print("search_phrase", search_phrase)
        news_category = work_item.get("news_category", [])
        num_months = work_item.get("num_months", 1)
    else:
        search_phrase = "python"
        news_category = []
        num_months = 2
        print("search_phrase----", search_phrase)
    extractor.run(search_phrase, news_category, num_months)
