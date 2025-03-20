import pandas as pd
import numpy as np
import plotly.express as px
from flask import Flask, render_template, request, jsonify
import csv

#Basic Requirement 1
# Set the file path to read the raw data
file_path = 'raw_MessiRonaldo_stats.csv'

# Read the CSV file into a Pandas DataFrame, treat 'no data' as missing values
data = pd.read_csv(file_path, na_values=['no data'], encoding='utf-8')

# Remove rows that contain no data
data = data.dropna()

# Define the columns to be removed
columns_to_remove = ['Liga_Aps', 'Liga_Mins', 'CL_Aps', 'CL_Mins']  # Placeholder column names
# Remove specified columns if they exist, ignoring errors if they don't
data = data.drop(columns=columns_to_remove, errors='ignore')

# Create a new .csv file with the cleaned data
cleaned_file_path = 'cleaned_MessiRonaldo_stats.csv'
data.to_csv(cleaned_file_path, index = False)



#Basic Requirement 2
# Defines the columns without numbers so they can be ignored
non_numeric_cols = ['Season', 'Player']

# Create a python dictionary
stats_dictionary = {}

for col in data.columns: # Check each columns data
    if col not in non_numeric_cols: # Skip the columns without numbers
        stats_data = data[col] # Label the column being viewed as "stats_data"
        
        # Fill the stats_dicionary dictionary with stats from each column
        stats_dictionary[col] = {
             'Mean': stats_data.mean(), # Get the mean of the column
             'Median': stats_data.median(), # Get the median of the column
             'Mode': stats_data.mode().iloc[0] if not stats_data.mode().empty else np.nan, # Get the mode of the column if there is one 
             'Range': stats_data.max() - stats_data.min() # Get the range of the column
}

# Converts the averages to a pandas dataframe to look more presentable when printed
stats_df = pd.DataFrame(stats_dictionary).transpose()
print(stats_df) # Prints the dataframe of the dictionary

# Load the cleaned dataset
stats = pd.read_csv('cleaned_MessiRonaldo_stats.csv')

#Advanced Requirement 1 (All 3 graphs are interactive through plotly, user can hover over points for more information)
# Create a bar chart to visualize the Liga goals per player
bar_chart = px.bar(stats, x='Player', y='Liga_Goals', # Fills in the x and y axis with data from my .csv
               hover_data=['Player', 'Liga_Goals'], color='Player', # Allows user to hover over bar chart and see the players name and goals break down, sets different colours for each player for a better viewing experience
               height=600) # Sets height of chart

bar_chart_html = bar_chart.to_html(full_html=False, include_plotlyjs="cdn")

# Create a pie chart to visualize the proportion of Liga goals per player
pie_chart = px.pie(stats, names='Player', values='CL_Goals',  # Fills the chart with players and their respective goals
                   hover_data=['Player', 'CL_Goals'],  # Shows player name and goal count on hover
                   title="Proportion of CL Goals per Player",  # Adds a title to the chart
                   height=600)  # Sets the height of the chart

pie_chart_html = pie_chart.to_html(full_html=False, include_plotlyjs="cdn")

# Convert 'Season' to a string so it can be read easier as it has a - preventing it becoming an integer 
stats['Season'] = stats['Season'].astype(str)

# Create scatter plot for Liga assists
scatter_plot = px.scatter(stats, x='Season', y='Liga_Asts', 
    hover_data=['Player', 'Liga_Asts'], color='Player', 
    height=600, )

scatter_plot_html = scatter_plot.to_html(full_html=False, include_plotlyjs="cdn")

# Updates the chart to treat 'Seasons' the way it is intended
scatter_plot.update_layout(xaxis_type='category',)



# Show the chart
# bar_chart.show()
# pie_chart.show()
#scatter_plot.show()

#BR 3
app = Flask(__name__)

# Define the main route to render the HTML page with the graphs
@app.route('/')
def index():
    return render_template('index.html',
        bar_chart=bar_chart_html, # Pass the bar chart to the webpage
        pie_chart=pie_chart_html,
        scatter_plot=scatter_plot_html)

@app.route('/suggestions')
def suggestions():
    return render_template('suggestions.html')

@app.route('/recommendations')
def recommendations():
    return render_template('recommendations.html')


# Run the Flask web server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)
