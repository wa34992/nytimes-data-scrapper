from modules.nytimes.data_extractor import DataExtractor

if __name__ == "__main__":
    # Starting process
    extractor = DataExtractor()
    search_phrase = "python"
    news_category = []
    num_months = 3
    extractor.run(search_phrase, news_category, num_months)
