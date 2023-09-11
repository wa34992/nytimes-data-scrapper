# NYTimes Data Scraping Bot

This repository contains a Python-based data scraping bot for the [NYTimes website](https://www.nytimes.com/). The code is well-structured, optimized, and memory-efficient, making it suitable for integration into other applications. It accepts the following parameters:

- `search_phrase` (string, required)
- `news_category` (list, optional, default value is []) example: ["Arts"]
- `num_months` (int, optional, default value is 2)

## Features

- **Automated Data Scraping:** This bot automates the process of scraping data from the [NYTimes website](https://www.nytimes.com/).
- **Search:** It allows you to search for a specific phrase, apply a date range, and sort the results by the newest.
- **Category Selection:** You can specify one or more categories to filter the news articles.
- **Data Extraction with images:** The bot extracts information such as news titles, news descriptions, post date, images, image file names, Search Phrase count, Money in title and Money in description.
- **Data Output:** It saves all the scraped data in an Excel file named `output.xlsx` and the images into an auto created `output` directory. When you run the bot again it will clear the previous data from output directory.
- **Logging:** The bot generates logs to track its activities.

## Local Setup

To set up and run the bot locally, follow these steps:

1. Clone this repository.
2. Create a Python virtual environment (preferred `python=3.9.0`).
3. Activate the virtual environment and run the following command to install the required dependencies: `pip install -r requirements.txt`
4. Run the bot using the following command: `python task.py`


Alternatively, you can also use [RCC command line tool](https://robocorp.com/docs/rcc/installation) or Robocorp code VS code extension.

## Deployment on [Robocorp Control Room](https://cloud.robocorp.com/)

To deploy the bot on the Robocorp Control Room, follow these steps:

1. Go to the Robocorp Control Room and create a robot.
2. Add the link of this repository to the public GIT.
3. Create a process and select the created robot and set ENV variable to PROD.
4. Run the process by providing the parameters mentioned above. The pramaters will be fetched from work items.
5. Data and pictures will be scraped into the `output` directory.

## Output

After successful execution and process completion a directory with name Output will generate that have all the files.

1. `app.log` file contains all the log generated during the process execution.
2. `output.xlsx` file contains all the scrapped data in `data` tab (sheet) of workbook.
3. `pictures` & `pictures.zip` directory contains all the images.


## File Structure

| File/Folder                                      | Description                                                                                                                     |
| ------------------------------------------------- |---------------------------------------------------------------------------------------------------------------------------------|
| `task.py`                                        | Initializes the bot and starts the scraping process.                                                                            |
| `conda.yaml`                                    | Contains configuration settings to set up the environment and define RPA Framework dependencies.                                |
| `robot.yaml`                                    | Includes configuration settings for Robocorp to execute `conda.yaml` and run `task.py`.                                         |
| `Modules/nytimes/browser.py`                   | Contains all the methods related to browser functionality.                                                                      |
| `Modules/nytimes/data_extractor.py`           | Provides a `run` method that calls other methods with logic for searching, scraping, and creating the Excel file for news data. |
| `Modules/utils.py`                             | Includes a `ExcelGenerator` class will generate excel file that contains data.                                                  |
| `Modules/nytimes/__init__.py`                | Contains code to generate logs.                                                                                                 |













