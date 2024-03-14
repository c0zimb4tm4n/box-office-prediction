# box-office-prediction
A tool that aims to predict box office revenue of hypothetical movies based on the cast and crew.

## Project Type:
Tool

## Team Members

#### Apratim Tripathi
#### Trisha Banerjee
#### Rohit Chandiramani
#### Zongze Li


## Question of interest:
We seek to build a web tool that should be able to predict the box office revenues, with resonable accuracy, of hypothetical movies based on a hypothetical cast and crew.

## Goals:
1. Develop a tool for predicting box office collections of hypothetical movies.
2. Utilize two datasets: one containing data of over 5000 movies with complete cast and crew details, and another with their respective box office information.
3. Train a machine learning model on these datasets to understand the correlation between cast/crew composition and box office success.
4. Enable users to input a desired cast and crew for a tentative movie.
5. Use the trained model to predict the potential box office collection of this hypothetical movie.

## Data Set:
1. IMDb and Box Office Mojo Movie/TV/OTT Data (Bulk Data SAMPLE) (AWS Data Exchange Product)
2. IMDb Essential Metadata for Movies/TV/OTT (Bulk Data SAMPLE) (AWS Data Exchange Product)
3. https://www.kaggle.com/datasets/igorkirko/wwwboxofficemojocom-movies-with-budget-listed
4. https://datasets.imdbws.com/

## Software dependencies and license information

All of the necessary implementations in this repository can be carried out using the following software.  All software is open source.

#### Programming language: 

- Python version 3.0 and above 

#### Python packages needed:

- pandas
- NumPy
- scikit-learn
- matplotlib
- seaborn
- CatBoost
- joblib
- beautifulsoup4
- streamlit

#### License Information:

The MIT License is a permissive open-source software license that allows users to freely use, modify, distribute, and sublicense the software without restriction. The MIT license for this project is descriped in full in **LICENSE.txt**.


## Directory Summary

**Examples:** This folder contains an example with images of how to use the tool.

**Box-office-prediction:** This folder contains the models, data cleaning files, packages, tests and streamlit app.

**Data:** This folder contains the data used in analyses with the latest cleaned data.

**Docs:** This folder contains documentations of the project, including technology review and final presentation slides, function specification, component specification, demo, design, and milestone.

**License.txt:** The MIT license used for this project.


## Directory Structure
The package is organized as follows:

```
box-office-prediction (master)  
project/
│
├── Examples/
│   ├── example_images/
│   │   ├── example_image_1
│   │   ├── example_image_2
│   │   ├── example_image_3
│   │   ├── example_image_4
│   │   ├── example_image_5
│   │   ├── example_image_6
│   │   ├── example_image_7
│   │   ├── example_image_8
│   │   ├── example_image_9
│   │   ├── example_image_10
│   │   ├── example_image_11
│   │   └── example_image_12
│   └── README.md
├── box-office-prediction/
│   ├── .streamlit/
│   │   └── config.toml
│   ├── models/
│   │   └── ratingModelv1.joblib
│   ├── notebooks/
│   │   ├── data_cleaning/
|   |   │   ├── Data_Ratings_v1.ipynb
|   |   │   ├── Data_Ratings_v2.ipynb
|   |   │   ├── Data_Ratings_v3.ipynb
|   |   │   ├── __init__.py
|   |   │   ├── data_extraction_EDA.ipynb
|   |   │   └── death-filter.ipynb
│   │   ├── model_training/
|   |   │   ├── Rating_Model.ipynb
|   |   │   ├── Revenue_Model.ipynb
|   |   │   └── __init__.py
│   │   └── __init__.py
│   ├── packages/
│   │   ├── __init__.py
│   │   └── helpers.py
│   ├── .DS_Store
│   ├── __init__.py
│   ├── app.py
│   └── streamlit_app_visual_demo.py
├── data/
│   ├── cleaned/
│   │   ├── data_clean_v5.csv
│   │   └── data_clean_v6.csv
│   ├── raw/
│   │   └── tconsts_prd_company.csv
│   └── InflationCPIs.csv
├── docs/
│   ├── Draft-technology_review_v3.pptx
│   ├── Final Presentation Slides.pdf
│   ├── component_specification.md
│   ├── demo_recorded.webm
│   ├── demo_recorded_.webm
│   ├── diag.png
│   ├── functional_specification.md
│   └── milestone.png
├── .gitignore
├── LICENSE
├── README.md
├── box_office_env.yml
├── requirements.txt
└── setup.py
```

## Tutorial For Using the Tool

#### Step 1: Download the Data

The raw datasets can be found here. For additional data and source data, you can find them from [IMDb](https://datasets.imdbws.com/)

#### Step 2: Install necessary packages, download the model and the app.py file.

#### Step 3: Run the app.py file

Copy the app.py file path and in the terminal, enter command "streamlit run " + copied file path. In the opened website, navigate through tabs to use the desired analytic or predictive features.

**1. Movie Analytics Dashboard** This tab provides analysis and evaluations for actors and actresses. It provides a filter selection for genres and after doing that, one can find the top X actors or actresses for this genre, sorted by revenue. User can also select a specific actor or actress to view his or her historical revenue trend across different genres.

**2. IMDb Movie Ratings Predictor** This tab provides prediction for potential film ratings. It provides a filter selection for genres and a vast selections of actors, actresses, directors, writers and production house from the drop down menu. User can only select one genre as the primary genre and one production company as the production house, but can select up to three for the rest categories. The user would also need to input a runtime length for the movie. After all the inputs, the user can click the predict button to view the predicted ratings and some followed-up analysis.

**3. Box Office Revenue Predictor** This tab provides prediction for potential film revenues. Similar to the ratings predictor, it follows the same inputs as the ratings predictor, and will present the predicted revenues along with some followed-up analysis

For a more detailed explanation of each tab and usage instructions, see the documentation of the app.py file or the examples folder.