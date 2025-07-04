import streamlit as st
import pandas as pd

# Load data
df = pd.read_parquet('summer-products.pqt')

# Set page config
st.set_page_config(page_title="SmartLook Fashion Recommender", layout="centered")

# Title
st.title("👗 SmartLook: AI Fashion Recommender")

# User Inputs
season = st.text_input("Select Season", "Summer")
style = st.text_input("Enter Style (e.g., Casual, Elegant, Sporty)", "Casual")
color = st.text_input("Preferred Color", "black")
size = st.text_input("Preferred Size (e.g., M, L, XL)", "XL")

user_input = {
    'season': season,
    'style': style,
    'color': color,
    'size': size
}

# --- Filter Logic ---
def filter_recommendations(df, user_input):
    filtered_df = df.copy()

    # Filter by season (theme)
    if user_input.get('season'):
        filtered_df = filtered_df[filtered_df['theme'].str.contains(user_input['season'], case=False, na=False)]

    # Filter by style (tags)
    if user_input.get('style'):
        filtered_df = filtered_df[filtered_df['tags'].str.contains(user_input['style'], case=False, na=False)]

    # Filter by color
    if user_input.get('color'):
        filtered_df = filtered_df[filtered_df['product_color'].str.contains(user_input['color'], case=False, na=False)]

    # Filter by size
    if user_input.get('size'):
        filtered_df = filtered_df[filtered_df['product_variation_size_id'].str.contains(user_input['size'], case=False, na=False)]

    return filtered_df

# --- Ranking Logic ---
def rank_recommendations(filtered_df):
    ranked_df = filtered_df.sort_values(by=['rating', 'units_sold'], ascending=[False, False])
    return ranked_df

# --- Get Top Recommendations ---
def get_top_recommendations(ranked_df, top_n=5):
    return ranked_df.head(top_n)

# --- Main Logic ---
filtered_df = filter_recommendations(df, user_input)

if filtered_df.empty:
    st.warning("⚠️ No matching products found. Try changing your filters.")
else:
    ranked_df = rank_recommendations(filtered_df)
    top_recommendations = get_top_recommendations(ranked_df)

    st.subheader("Top Recommendations:")
    for item in top_recommendations.to_dict(orient="records"):
        st.markdown(f"**🛍️ {item['title']}**  \n⭐ Rating: {item['rating']} | 🛒 Sold: {item['units_sold']}")
