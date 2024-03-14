# Box Office Prediction  
[![Coverage Status](https://coveralls.io/repos/github/c0zimb4tm4n/box-office-prediction/badge.svg?branch=main)](https://coveralls.io/github/c0zimb4tm4n/box-office-prediction?branch=main)
![Workflow Status](https://github.com/c0zimb4tm4n/box-office-prediction/actions/workflows/build_test.yml/badge.svg)  
Our project introduces an innovative tool designed to aid the movie production industry. Aimed at producers, directors, casting directors, and industry insiders, this tool leverages predictive analytics to forecast the potential revenue of movies that are still in the conceptual phase.

## Project Type  
Tool

## Team Members  
#### Apratim Tripathi
#### Trisha Banerjee
#### Rohit Chandiramani
#### Zongze Li  



## Table of Contents  

- [Key Features](#key-features)
- [Our Goal](#our-goal)
- [Data Sources](#data-sources)
- [Software Dependencies and License Information](#software-dependencies-and-license-information)
- [Directory Summary](#directory-summary)
- [Tutorial For Using the Tool](tutorial-for-using-the-tool)
- [Video Demonstration](video-demonstration)


## Key Features  
#### Revenue Prediction
By inputting data such as actors, actresses, writers, directors, and genres, our tool provides an estimated revenue figure for hypothetical movies.

#### Analytics Dashboard
Users can explore in-depth analytics showing the performance of actors and actresses across various genres over the years. This valuable insight assists in making informed decisions about casting and genre selection.

#### Strategic Decision Making
The tool aids in strategizing the hiring process, focusing on maximizing profits by selecting the ideal combination of talent and genre based on historical data and predictive analysis.


## Our Goal  
To empower industry players with data-driven insights, enabling them to make strategic decisions that enhance profitability and success in the competitive landscape of movie production.


## Data Sources  
#### 1. IMDb Non-Commercial Datasets
The IMDb Non-Commercial Datasets provide subsets of IMDb's movie, TV, and celebrity data for personal and non-commercial use. These datasets, available for download in a gzipped, tab-separated-values (TSV) format, are updated daily and adhere to specific terms and conditions.

Availability: Accessible at https://datasets.imdbws.com/, with updates provided daily.

Datasets Overview:
title.akas.tsv.gz: Alternative titles, regions, languages, and attributes.
title.basics.tsv.gz: Basic title information including type/format, titles, years, runtime, and genres.
title.crew.tsv.gz: Lists directors and writers per title.
title.episode.tsv.gz: Details on TV series episodes.
title.principals.tsv.gz: Principal cast/crew information, roles, and characters.
title.ratings.tsv.gz: Ratings data, including average rating and vote count.
name.basics.tsv.gz: Information on individuals, including names, birth/death years, professions, and notable titles.

Link: [IMDb Data Files](https://datasets.imdbws.com/)

#### 2. Movie Revenues from Box Office Mojo
For a comprehensive analysis of box office trends, we have included data spanning from 1970 to 2023, sourced from Box Office Mojo. This dataset encompasses revenue information for movies released within this timeframe, providing a valuable asset for understanding box office dynamics over the years.

The data was collected through a  web scraping script designed to extract movie revenue information. [Access the Box Office Mojo Scraping Script here](https://raw.githubusercontent.com/c0zimb4tm4n/box-office-prediction/main/scripts/data_extraction_EDA.ipynb)

#### 3. Kaggle: U.S. Inflation Data
To use inflation-corrected revenues, we used this dataset. This dataset encompasses the monthly U.S. Consumer Price Index (CPI), representing the average CPI across all American cities for each month. The CPI is a critical economic indicator, reflecting the average change over time in the prices paid by urban consumers for a market basket of consumer goods and services.

Link: [Kaggle Dataset](https://www.kaggle.com/datasets/varpit94/us-inflation-data-updated-till-may-2021)

## Software Dependencies and License Information  
The project is built using Python 3.0+ and several open-source Python packages such as pandas, NumPy, scikit-learn, and Streamlit. The complete list of dependencies can be found in requirements.txt. This project is licensed under the MIT License, with full details available in LICENSE.txt.


## Directory Summary  
.
├── Examples  
│   └── example_images  
├── box_office_prediction  
│   ├── __pycache__  
│   ├── models  
│   ├── notebooks  
│   └── tests  
│       └── __pycache__  
├── data  
│   ├── cleaned  
│   └── raw  
├── docs  
└── scripts  
    └── __pycache__  


## Tutorial For Using the Tool  

#### Step 1: Cloning the Repository  
To get started with the project on your local machine, first ensure you have Git installed. If not, follow the instructions provided in the [Git Guide](https://docs.conda.io/projects/conda/en/latest/commands/install.html). Once Git is set up, clone the repository to your computer by executing the following command in your terminal

`git clone git@github.com:c0zimb4tm4n/box-office-prediction.git`  


#### Step 2: Navigate to the Project Directory  
Change into the project directory:

`cd box-office-prediction`

#### Step 3: Create the Conda Environment  
Before creating the Conda environment, ensure you have Conda installed. If you need to install Conda, follow the Conda Installation Guide. With Conda installed, create the project environment using:

`conda env create -f box_office_env.yml`

This command reads the box_office_env.yml file and sets up an environment named box_office with all the required Python dependencies.

#### Step 4: Activate the Conda Environment  
Activate the newly created Conda environment:

`conda activate box_office`

#### Step 5: Download Required Models  
Use the gdown command to download necessary machine learning models into the correct project directory:  
`gdown --id 1zea9X4Rbw-2_VmHQlyajNPT3Fd3ngZ5B -O box_office_prediction/models/revenueModelv2.joblib`  
`gdown --id 1ypQ1VkEJp8c3If2941axznVLgST4mSyU -O box_office_prediction/models/ratingModelv2.joblib`

These commands download the revenueModelv2.joblib and ratingModelv2.joblib models required for the application to function.

#### Step 6: Run the Application  
With the environment set up and models downloaded, you can now run the application using Streamlit:
`streamlit run box_office_prediction/app.py`

#### Step 7: Deactivate the Conda Environment  
After using the application, you can deactivate the Conda environment by running:

`conda deactivate`


## Video Demonstration  
Access the demo here for a detailed understanding of the flow of our project.
[Video Download](https://github.com/c0zimb4tm4n/box-office-prediction/blob/main/docs/demo_recorded.webm)
