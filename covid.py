import pymysql
import tkinter as tk
import requests
import io
import pandas as pd
import matplotlib.pyplot as plt

# MySQL connection configuration
config = {
    'user': 'root',
    'password': 'milko.1-2002',
    'host': 'localhost',
    'database': 'covid_dataDB',
}

# URL of the CSV file
url = 'https://www.stats.govt.nz/assets/Uploads/Effects-of-COVID-19-on-trade/Effects-of-COVID-19-on-trade-At-15-December-2021-provisional/Download-data/effects-of-covid-19-on-trade-at-15-december-2021-provisional.csv'

# Send a GET request to retrieve the CSV file
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    
    # Decoding the contents of the csv file
    csv = (response.content.decode('utf-8'))
    
    data_frame = pd.read_csv(io.StringIO(csv))

    # Convert the Date column to datetime
    data_frame['Date'] = pd.to_datetime(data_frame['Date'], format='%d/%m/%Y')
    
    # Converting the "Value" column to a numeric data type
    data_frame['Value'] = pd.to_numeric(data_frame['Value'], errors='coerce')

    # Extract the month numbers and store them in a new column
    data_frame['Month'] = data_frame['Date'].dt.month
    
    # Group the data as necessary:
    # 1.(Series Object)
    monthly_turnover = data_frame.groupby(['Month', 'Measure'])['Value'].sum()
    
    #2.(Series Object)
    country_turnover = data_frame.groupby(['Country', 'Measure'])['Value'].sum()
    
    #3(Series Object)
    transp_turnover = data_frame.groupby(['Transport_Mode', 'Measure'])['Value'].sum()
    
    #4.(Series Object)
    daily_turnover = data_frame.groupby(['Weekday', 'Measure'])['Value'].sum()
    
    #5.(Series Object)
    commodity_turnover = data_frame.groupby(['Commodity', 'Measure'])['Value'].sum()
    
    #6.(Series Object)
    top_months = data_frame.groupby('Month')['Value'].sum().nlargest(5)
    
    #7.(Series Object)
    top_categories_perCountry = data_frame.groupby(['Country', 'Commodity'])['Value'].sum()
    
    # Group the data by category of Commodity and Weekday and find the day with the highest turnover by saving the indexes of the max values
    #8.(DataFrame Object)
    commodity_day_turnover = data_frame.groupby(['Commodity', 'Weekday'])['Value'].sum()
    top_day_per_commodity = commodity_day_turnover.groupby('Commodity').idxmax()
    top_days = commodity_day_turnover.loc[top_day_per_commodity]
    top_days = top_days.reset_index() #Reseting the indexes of the top days as it got created with the indexes of another frame
    
    # Method to plot a bar chart of the monthly turnover for each measure
    def plot_monthly_turnover():
        
        monthly_turnover.plot(kind='bar', stacked=True)

        # Set the chart title and axis labels for monthly turnover
        plt.yscale('log')
        plt.title('Total Turnover per Month')
        plt.xlabel('Month')
        plt.ylabel('Turnover')

        # Show the chart
        plt.show()
    
    # Method to plot a bar chart of the country turnover for each measure 
    def plot_country_turnover():
         
        country_turnover.plot(kind = 'bar', stacked = True)
        
        plt.yscale('log')
        plt.title('Total Turnover per Country')
        plt.xlabel('Country')
        plt.ylabel('Turnover')
        
        plt.show()
        
    # Method to plot a bar chart of the transportation mode turnover for each measure
    def plot_transportation_mode_turnover():
        
        transp_turnover.plot(kind = 'bar', stacked = True)
        
        plt.yscale('log')
        plt.title('Total Turnover per Transportation Mode')
        plt.xlabel('Transportation Mode')
        plt.ylabel('Turnover')
        
        plt.show()
            
    # Method to plot a bar chart of the daily turnover for each measure
    def plot_daily_turnover():
        
        daily_turnover.plot(kind = 'bar', stacked = True)
    
        plt.yscale('log')
        plt.title('Total Turnover per Weekday')
        plt.xlabel('Weekday')
        plt.ylabel('Turnover')
        
        plt.show()
    
    # Method to plot a bar chart of the commodity turnover for each measure
    def plot_commodity_turnover():
    
        commodity_turnover.plot(kind = 'bar', stacked = True)
        
        plt.yscale('log')
        plt.title('Total Turnover per Commodity')
        plt.xlabel('Commodity')
        plt.ylabel('Turnover')
        
        plt.show()
        
    # Method to plot a bar chart of the top 5 months with the highest turnover
    def plot_top_months():
        
        top_months.plot(kind = 'bar', stacked = True)
        
        plt.yscale('log')
        plt.title('Top 5 Months with the highest turnover')
        plt.xlabel('Top 5 Months')
        plt.ylabel('Turnover')
        
        plt.show()
    
    # Method to plot a bar chart of the top 5 categories with the highest turnover of each country
    def plot_top_categories_per_country():

        for country in data_frame['Country'].unique():
            top_categories_perCountry_turnover = top_categories_perCountry[country].nlargest(5)
            top_categories_perCountry_turnover.plot(kind = 'bar', stacked = True)
            plt.yscale('log')
            plt.title(f'Top 5 Categories for {country}')
            plt.xlabel('Category')
            plt.ylabel('Turnover')
            
            plt.show()
    
    # Method to plot a bar chart of the top days with the highest turnover of each commodity
    def plot_top_days_turnover():

        plt.bar(top_days['Weekday'] + ',' + top_days['Commodity'], top_days['Value'])
        
        plt.yscale('log')
        plt.title('Day with the Highest Turnover for each Commodity')
        plt.xlabel('Day of the Week - Commodity')
        plt.ylabel('Turnover')
        # Rotate the x-axis tick labels vertically
        plt.xticks(rotation='vertical')
        
        plt.show()
    
    # Create the main window
    window = tk.Tk()
    window.title("COVID-19 Data Analysis")

    # Set the background color of the window
    # Set the window size, center the window and color it
    window.geometry("400x450")
    window.eval('tk::PlaceWindow . center')
    window.configure(bg='Lightblue')
    
    # Add a label at the top of the window
    lbl_menu = tk.Label(window, text="Menu", font=("Arial", 14, "bold"), bg='Lightblue', pady=10)
    lbl_menu.pack()

    # Create buttons for each plot option and call the proper function each time when a button is pressed
    btn_monthly_turnover = tk.Button(window, text="Monthly Turnover", command=plot_monthly_turnover)
    btn_monthly_turnover.pack(pady = 10)

    btn_country_turnover = tk.Button(window, text="Country Turnover", command=plot_country_turnover)
    btn_country_turnover.pack(pady = 10)

    btn_transportation_mode_turnover = tk.Button(window, text="Transportation Mode Turnover", command=plot_transportation_mode_turnover)
    btn_transportation_mode_turnover.pack(pady = 10)

    btn_daily_turnover = tk.Button(window, text="Daily Turnover", command=plot_daily_turnover)
    btn_daily_turnover.pack(pady = 10)

    btn_commodity_turnover = tk.Button(window, text="Commodity Turnover", command=plot_commodity_turnover)
    btn_commodity_turnover.pack(pady = 10)

    btn_top_months = tk.Button(window, text="Top Months", command=plot_top_months)
    btn_top_months.pack(pady = 10)

    btn_top_categories_per_country = tk.Button(window, text="Top Categories Per Country", command=plot_top_categories_per_country)
    btn_top_categories_per_country.pack(pady = 10)

    btn_top_days_turnover = tk.Button(window, text="Top Days By Commodity Turnover", command=plot_top_days_turnover)
    btn_top_days_turnover.pack(pady = 10)
    
    # Run the main event loop
    window.mainloop()
    
    # Connecting to the MySQL database
    connection = pymysql.connect(**config)
    cursor = connection.cursor()
    
    #Inserting the data into the tables
    for (month, measure), turnover in monthly_turnover.items():
        cursor.execute("INSERT INTO MONTHLY_TURNOVER (Month, Measure, Value) VALUES (%s, %s, %s)", (month, measure, turnover))
        
    for (country, measure), turnover in country_turnover.items():
        cursor.execute("INSERT INTO COUNTRY_TURNOVER (Country, Measure, Value) VALUES (%s, %s, %s)", (country, measure, turnover))
        
    for (transportation_mode, measure), turnover in transp_turnover.items():
        cursor.execute("INSERT INTO TRANSPORTATION_TURNOVER (Transportation_Mode, Measure, Value) VALUES (%s, %s, %s)", (transportation_mode, measure, turnover))
        
    for (weekday, measure), turnover in daily_turnover.items():
        cursor.execute("INSERT INTO DAILY_TURNOVER (Weekday, Measure, Value) VALUES (%s, %s, %s)", (weekday, measure, turnover))
        
    for (commodity, measure), turnover in commodity_turnover.items():
        cursor.execute("INSERT INTO COMMODITY_TURNOVER (Commodity, Measure, Value) VALUES (%s, %s, %s)", (commodity, measure, turnover))
        
    for month, turnover in top_months.items():
        cursor.execute("INSERT INTO TOP_MONTHS (Month, Value) VALUES (%s, %s)", (month, turnover))
        
    for (country, commodity), turnover in top_categories_perCountry.items():
        cursor.execute("INSERT INTO TOP_CATEGORIES_PER_COUNTRY (Country, Commodity, Value) VALUES (%s, %s, %s)", (country, commodity, turnover))
        
    for index, row in top_days.iterrows():
        commodity = row['Commodity']
        weekday = row['Weekday']
        turnover = row['Value']
        cursor.execute("INSERT INTO TOP_DAYS (Commodity, Weekday, Value) VALUES (%s, %s, %s)", (commodity, weekday, turnover))
    
    # Commit the changes and close the connection
    connection.commit()
    connection.close()
    
    # Exporting the data into csv files
    monthly_turnover.to_csv('monthly_turnover.csv')
    country_turnover.to_csv('country_turnover.csv')
    transp_turnover.to_csv('transportation_mode_turnover.csv')
    daily_turnover.to_csv('daily_turnover.csv')
    commodity_turnover.to_csv('commodity_turnover.csv')
    top_months.to_csv('top_months.csv')
    top_categories_perCountry.to_csv('top_categories_per_country.csv')
    top_days.to_csv('top_days.csv')
    
else:
    # Print an error message if the request failed
    print('Failed to retrieve the CSV file.')
    