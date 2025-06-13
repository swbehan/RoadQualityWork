# About Our Project

Despite the wealth of public data on tourism, infrastructure, and travel across the European Union, there's no single platform that makes this information useful for everyday road trippers, policymakers, or researchers. Until now.

Introducing EuroTour- the first unified platform that leverages public data and machine learning to help users understand, compare, and plan European travel based on key national features like road conditions, fuel prices, and tourism activity. Whether you're mapping your next trip, benchmarking your country’s tourism strategy, or modeling inter-country trends, EuroTour empowers you to explore Europe smarter.

# Why EuroTour?
While the EU provides robust datasets covering everything from road quality and fuel prices to GDP and tourism trends, the information is:

- Too technical for casual travelers,

- Too fragmented for national tourism officials,

- And too inconsistent for academic researchers.

EuroTour bridges these gaps by transforming disparate datasets into an intuitive and intelligent platform that generates personalized travel recommendations, country-level dashboards, and cross-national insights all in one place alongside innovative approaches in machine learning.

# Our User Personas

### Casual Tourist / Road Trip Planner
- Wants to plan efficient, scenic, and affordable European road trips.

- Needs help navigating complex data like road density and fuel costs.

- Benefits from personalized country recommendations based on preferences.

### National Director of Tourism
- Responsible for improving and promoting their own country’s tourism infrastructure.

- Wants to benchmark national tourism performance and assess investment outcomes.

- Uses EuroTour's country-specific analytics tools to inform policy and strategy.

### EU Tourism Researcher
- Studies historical and comparative travel trends across multiple countries.

- Needs clean, interoperable data for modeling, publication, or policy analysis.

- Uses EuroTour to explore pan-European trends and correlations over time.

# Overview of Models

In order to implement our goal to approach some of these problems with machine learning, we decided to user a recommender model and a time series linear regression model. Beginning with the recommender model, we wanted to use this to help our European traveler navigate features with complex data like fuel prices, road density, and how populous certain areas are. Based on our user's preferences, the cosine similarity score between their preferences and a country's score is calculated, and the five most similar countries are returned.

As for our second model, we built a time series linear regression in order for users in search of analyzing data on a broader scale of implication to view predictions and historical data on tourism numbers per country. In order to predict three years past the limitations of our dataset, we included a lag of 3 to predict the next three based on the past three. Overall, this model serves to act as a comparative tool in order to explore what a country has done well, can do better, and how it might perform in the future all in one place.

# Instructions for Running/Use
In order to view this project, please complete the instructions below:
- Download our project repository
- In Docker: docker compose build
- docker compose up -d
- In browser, http://localhost:8501


