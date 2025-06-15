# EuroTour Web Application

Welcome! This repository contains all files needed to launch our EuroTour Web App on your computer!

This project was developed by four Northeastern University Students while on the Summer 2025 Data and Software in International Government and Politics Dialogue of Civilization.

More about the developers can be viewed on the About page on our app.

# What is EuroTour

EuroTour is a comprehensive web application that brings together fragmented E.U. tourism data for three distinct user types: Travelers, Tourism Directors, and Researchers.

While abundant public data exists on road quality, GDP, tourism metrics, and regional factors, no single platform connects these insights meaningfully. EuroTour changes that by synthesizing complex datasets through machine learning algorithms, delivering personalized experiences for each user persona.
- Travelers discover optimized travel destinations and personalized attractions. 
- Tourism Directors use predictive analytics and multi-factor analysis to guide tourism policy. 
- Researchers analyze validated visualizations to conduct comparative studies and publish findings within the academic community

From aspiring tourists to national officials to academic professionals, EuroTour transforms scattered statistics into actionable intelligence.
Welcome to EuroTour: Smarter Travel, Stronger Insights, One Europe.

## Theory to Functionality
In order to implement our idea into a functioning web-app, we implemented 4 aspects to our app. 

### **StreamLit And FrontEnd**
Our group used Streamlit's Python library to create interactive dashboards for each user. We were able to style the frontend using a combination of both streamlit elements and CSS styling. The main focus of using Streamlit was to create a user friendly interface, with the developer-side motivation being the ability to build functional frontends without extensive web development knowledge.
All three personas could view tourism data visualization, enabling users to explore E.U. country metrics through dynamic charts, filters, and predictive analytics displays that streamlit supported.  

### **Flask API**
Utilizing the Flask Library in Python, we implemented a RESTful Flask API to manage database operations through HTTP methods. Implemented GET endpoints to display existing data to the user in the form of a visualization or text, POST endpoints for creating new records, PUT endpoints for updating existing data, and DELETE endpoints for removing entries from the MySQL database. The API served as the backend interface, processing incoming HTTP requests, executing corresponding SQL operations, and returning appropriate JSON responses to maintain seamless frontend-database communication

### **Machine Learning**
EuroTour integrates two sophisticated models to deliver intelligent predictions and personalized recommendations across our platform.

- <u> Traveler Recommendation Model</u>
<br/>
Our recommender model transforms complex European travel data into personalized destination suggestions. Through an intuitive three-question slider interface, users express their preferences across key factors like budget, activity level, and cultural interests. The system employs cosine similarity algorithms to match these preferences against comprehensive country profiles, instantly generating the five most compatible destinations. This approach converts overwhelming datasets into actionable travel insights.

- <u> Tourism Prediction Model </u>
<br/>
Our time series model empowers tourism directors with predictive analytics for strategic planning. Using linear regression with lag-3 dependencies, the system analyzes historical tourism patterns to forecast three-year trajectories for each E.U. country. By extending predictions beyond existing dataset limitations, directors can identify emerging trends, benchmark performance against regional competitors, and develop data-driven policies for sustainable tourism growth.

- <u> Impact </u>
<br/>
Together, these models address distinct user needs: personalized travel discovery for individuals and strategic forecasting for industry professionals, ensuring EuroTour delivers value across all user personas.

### **MySQL DataBase**
MySQL served as our primary data storage solution, managing both historical datasets and application-specific information. We designed tables to house diverse tourism metrics, economic indicators, and infrastructure data sourced from public E.U. databases. The database architecture includes user management tables for authentication and role-based access (Travelers, Tourism Directors, Researchers), as well as user-generated content like research posts. Additionally, we stored model weights and intermediate calculations to optimize our time series prediction performance. MySQL was selected for its relational capabilities and seamless Python integration through the Flask library.

## How to Access

- A GitHub Account
- A terminal-based git client or GUI Git client such as GitHub Desktop or the Git plugin for VSCode.
- VSCode with the Python Plugin
- A distribution of Python running on your laptop. The distribution supported by the course is Anaconda or Miniconda.

## Structure of Our Repo

- The repo is organized into five main directories:
  - `./app` - the Streamlit app
  - `./api` - the Flask REST API
  - `./database-files` - SQL scripts to initialize the MySQL database
  - `./datasets` - folder for storing datasets
  - `./ml-src` - folder for storing ML models
- The repo also contains a `docker-compose.yaml` file that is used to set up the Docker containers for the front end app, the REST API, and MySQL database. This file is used to run the app and API in Docker containers.

## Blog Post
If you are interested in viewing each person's indivudal contributions to the web-app development or want to view our progress through each phase, please vist our Blog Post Repo below!
https://github.com/AidanKelly50/ASMG 

## Contact
If you have any questions regarding the web-app, its development, our choices or desgin, please do not hesitate to ask.

**Our contact Info**
- <u> Sean Behan </u>
<br/>
EMAIL: behan.s@northeastern.edu <br/>
GITHUB: https://github.com/swbehan

- <u>Aidan Kelly</u>
<br/>
EMAIL: kelly.aida@northeastern.edu <br/>
GITHUB: https://github.com/AidanKelly50

- <u>Maria Samos Rivas</u>
<br/>
EMAIL: samosrivas.m@northeastern.edu <br/>
GITHUB: https://github.com/maria1neu

- <u>Gabby Montalvo</u>
<br/>
EMAIL: montalvo.g@northeastern.edu <br/>
GITHUB: https://github.com/gabbymontalvo 


