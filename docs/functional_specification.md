# Functional Specifications
## Background:
The project aims to develop a web-based tool capable of predicting box office revenues for hypothetical movies with reasonable accuracy, leveraging machine learning techniques. The primary goals include the creation of a predictive model trained on two datasets: one containing comprehensive data on over 10k+ movies, including cast and crew details, and another containing corresponding box office information. By analyzing the correlation between cast/crew composition and box office success, the tool seeks to provide users with insights into the potential financial performance of their hypothetical movie projects. Additionally, the application will feature analytical dashboards for visualizing trends and insights from historical movie data, with filters to refine the analysis and enhance decision-making. Through this project, we aim to provide filmmakers and industry professionals with a valuable tool for informed decision-making and planning.

## User Profile:
### *Filmmaker/producer/casting director:*
Highly knowledgeable about the domain with an understanding of movies, cast, crew, genre, and actors that lead to creating a blockbuster. Wants a tool by which they will be able to hypothetically predict a potential script revenue based on the parameters of the film. Able to browse and navigate through the application but has no programming knowledge.

### *Film insurance providers:*
Have an understanding of the economics of making a movie and what are the various risk factors involved in building an insurance product to hedge the risk of investment toward a venture. Wants a tool by which they will be able to hypothetically predict the revenue of a potential movie to have a benchmark to set the terms and conditions of the insurance. Able to browse and navigate through the application, has an understanding of finance and statistics with little to no programming experience.

### *Streaming partners (Platforms like Netflix, and Hulu) / general movie enthusiasts:*
Average knowledge about the domain, mainly from a distribution or viewing perspective. Wants to see the current trending genres of movies and their active period, run analytics, and get trends for different actors, directors, regions, and languages. Able to browse and navigate through the application, filter and view dashboards and might have little to no programming experience.

## Data Sources:
### [IMDb Non-commercial Datasets](https://datasets.imdbws.com/)
IMDb offers subsets of its data for personal and non-commercial use, which can be accessed and downloaded from . Refreshed daily, these datasets are provided in gzipped, tab-separated-values (TSV) formatted files in the UTF-8 character set. The database tables encompass title.akas, title.basics, title.crews, title.principles, title.ratings, and name.basics.

### [Box Office Mojo](https://www.boxofficemojo.com/): 
Utilized in our project, Box Office Mojo serves as a key source for scraping box office collection revenue data. By tapping into its extensive database, we gain valuable insights into movie earnings. This platform offers a rich repository of box office performance data, enabling comprehensive analysis and providing insights into the financial success of films across diverse genres and markets.

### Kaggle - [The Movies Dataset](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset): 
This dataset provides a wealth of information relevant to our project. With comprehensive data on movies, it offers opportunities for in-depth analysis and enriches our understanding of various aspects of the film industry.


# Use-cases:


## For the film producer or casting director:

### Objectives:
The producer wants to find the current revenue trends of movies, while the casting director wants to find the optimal casts for a movie.

### Use-case flow:

***User:*** Requesting for a prediction task<br>
***System:*** In the platform, go to the prediction page, select the “New Project” option to start a prediction task, save the project by renaming the project name

***User:*** Access movie revenue evaluation page<br>
***System:*** Display the 20 top revenue movies in the past as the default display results

***User:*** Adjust the amount by selecting the top 50 ones<br>
***System:*** In the scrolled down bar, switch to display the 50 top revenue movies

***User:*** Go to the next page to see the following results<br>
***System:*** Switch to the next page by clicking the arrows to turn to the next page, displaying the top 51 - 100 revenue movies

***User:*** Add comparisons like selecting those with budgets lower than 50 million<br>
***System:*** Display the filtered results

***User:*** Add filters like genres, ratings, releasing dates, regions<br>
***System:*** Display the filtered results

***User:*** Perform predictions<br>
***System:*** Provide details of a planned film, click on "generate revenue predictions" to receive forecasts on potential revenue based on the provided details
 
***User:*** Clear all input filters<br>
***System:*** Go back to the default display results with the top 50 revenue movies

***User:*** Save the results<br>
***System:*** In the prompt up window ask the user which pages to be selected and save the result in a format being chosen by the user

## For the Insurance Consultant:

### Objectives:
The consultant wants to design an insurance product for the company
### Use-case flow:

***User:*** Requesting for an analytical task<br>
***System:*** In the platform, go to the analysis page, select the “New Project” option to start a prediction task, save the project by renaming the project name

***User:*** Access movie revenue evaluation page<br>
***System:*** Display the 20 top revenue movies in the past as the default display results

***User:*** Adjust the amount by selecting the top 50 ones<br>
***System:*** In the scrolled down bar, switch to display the 50 top revenue movies

***User:*** Go to the next page to see the following results<br>
***System:*** Switch to the next page by clicking the arrows to turn to the next page, displaying the top 51 - 100 revenue movies

***User:*** Add filters like genres, ratings, releasing dates, regions, directors, actors and budgets<br>
***System:*** Display the filtered results

***User:*** Perform analysis<br>
***System:*** Select several desired movies as data input, click on "generate regression analysis" to see to what degree each of the factors will affect the budgets and revenues

***User:*** Calculate the revenue<br>
***System:*** Provide details of a film to see the results of expected budgets and revenues
 
***User:*** Clear all input filters<br>
***System:*** Go back to the default display results with the top 50 revenue movies

***User:*** Save the results<br>
***System:*** In the prompt up window ask the user which pages to be selected and save the result in a format being chosen by the user

