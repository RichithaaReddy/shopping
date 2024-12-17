import pandas as pd
import streamlit as st
import plotly.express as px

# Load the dataset (update the path if necessary)
@st.cache_data
def load_data():
    try:
        # Load the CSV file (Update the path to your dataset)
        data = pd.read_csv("https://res.cloudinary.com/dbenkbws8/raw/upload/v1734478084/shopping_behavior_cleaned_dokrjv.csv")
        return data
    except FileNotFoundError:
        st.error("The file 'shopping_behavior.csv' was not found. Please check the file path.")
        return None
    except Exception as e:
        st.error(f"An error occurred while loading the data: {e}")
        return None

# Load the data
data = load_data()

# Check if data was loaded successfully
if data is not None:
    # Display column names to ensure proper access
    st.write("Available Columns:", data.columns)

    # If the required columns are missing, inform the user
    required_columns = ['Category', 'Age_Group', 'Size', 'Purchase Amount (USD)']
    missing_columns = [col for col in required_columns if col not in data.columns]
    
    if missing_columns:
        st.error(f"Column(s) missing from the dataset: {', '.join(missing_columns)}")
        st.write("The columns in your dataset are:", data.columns)  # Print actual column names
    else:
        # If all required columns are present, proceed with the dashboard
        # Adding interactivity to the dashboard

        # User inputs for filtering
        category = st.selectbox('Select Product Category:', options=['All'] + list(data['Category'].unique()))
        age_group = st.selectbox('Select Age Group:', options=['All'] + list(data['Age_Group'].unique()))
        size = st.selectbox('Select Size:', options=['All'] + list(data['Size'].unique()))
        
        # Creating a slider for selecting the purchase amount range (USD)
        purchase_range = st.slider('Select Purchase Amount Range (USD):', 
                                   min_value=int(data['Purchase Amount (USD)'].min()), 
                                   max_value=int(data['Purchase Amount (USD)'].max()), 
                                   value=(50, 200))

        # Filter the data based on user selections
        filtered_data = data.copy()

        if category != 'All':
            filtered_data = filtered_data[filtered_data['Category'] == category]
        if age_group != 'All':
            filtered_data = filtered_data[filtered_data['Age_Group'] == age_group]
        if size != 'All':
            filtered_data = filtered_data[filtered_data['Size'] == size]
        
        filtered_data = filtered_data[(
            filtered_data['Purchase Amount (USD)'] >= purchase_range[0]) & 
            (filtered_data['Purchase Amount (USD)'] <= purchase_range[1])
        ] 

        # Display the filtered dataset
        st.write("Filtered Data", filtered_data)

                ## Bar chart: Purchase Amount by Category and Age Group
        # Group the data by 'Category' and 'Age_Group' to sum the purchase amount
        category_age_purchase = filtered_data.groupby(['Category', 'Age_Group'])['Purchase Amount (USD)'].sum().reset_index()

        # Define a color mapping for the pie chart based on categories
        category_colors = {
            'Electronics': '#FF6347',  # Tomato Red
            'Clothing': '#FFD700',     # Gold
            'Food': '#ADFF2F',         # GreenYellow
            'Home': '#00BFFF',         # DeepSkyBlue
            'Toys': '#8A2BE2',         # BlueViolet
            'Books': '#FF69B4',        # HotPink
            # Add more categories and their colors as needed
        }

        # Create a pie chart showing total purchase amount by category and age group
        fig1 = px.pie(category_age_purchase, 
                    names='Category', 
                    values='Purchase Amount (USD)', 
                    title="Total Purchase Amount by Category and Age Group", 
                    labels={'Purchase Amount (USD)': 'Amount in USD'},
                    color='Category',  # Use 'Category' for coloring
                    color_discrete_map=category_colors)  # Apply different colors based on categories

        # Display the pie chart
        st.plotly_chart(fig1, use_container_width=True)


        # 2. Line plot: Average Purchase Amount vs Age Group
        # Group the data by 'Age_Group' and calculate the mean 'Purchase Amount (USD)'
        age_group_purchase = filtered_data.groupby('Age_Group')['Purchase Amount (USD)'].mean().reset_index()

        # Create the line graph
        fig2 = px.line(age_group_purchase, x='Age_Group', y='Purchase Amount (USD)', 
                    title="Average Purchase Amount vs Age Group", 
                    labels={'Purchase Amount (USD)': 'Amount in USD'},
                    markers=True)  # Add markers for each data point to make it more visible

        # Display the line graph
        st.plotly_chart(fig2, use_container_width=True)


        # 3. Histogram: Distribution of Purchase Amount (USD)
        fig3 = px.histogram(filtered_data, x='Purchase Amount (USD)', nbins=20, 
                             title="Distribution of Purchase Amount (USD)", 
                             labels={'Purchase Amount (USD)': 'Amount in USD'},
                             hover_data=['Purchase Amount (USD)'])  # Hover Data for Interactivity
        fig3.update_layout(bargap=0.2)  # Adjust the gap between bars for better visual appearance
        st.plotly_chart(fig3, use_container_width=True)

else:
    st.warning("No data available to display. Please check the dataset loading process.")
