import streamlit as st
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import threading
import time
from datetime import datetime
import io

# Initialize session state for data persistence
def init_session_state():
    if 'kindness_data' not in st.session_state:
        st.session_state['kindness_data'] = pd.DataFrame({
            "message": ["Gave a compliment to a stranger", "Helped a friend with homework"],
            "category": ["Compliment", "Helping Others"],
            "timestamp": ["2025-05-09 10:00", "2025-05-09 11:00"],
            "user": ["Anonymous", "Anonymous"]
        })
    if 'saving' not in st.session_state:
        st.session_state['saving'] = False

# Function to save new kindness entry
def save_kindness(message, category, user="Anonymous"):
    st.session_state['saving'] = True
    try:
        # Simulate API call or processing delay
        time.sleep(0.5)
        new_entry = pd.DataFrame({
            "message": [message.strip()],
            "category": [category],
            "timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            "user": [user]
        })
        st.session_state['kindness_data'] = pd.concat(
            [st.session_state['kindness_data'], new_entry], ignore_index=True
        )
    except Exception as e:
        st.error(f"Error saving kindness: {str(e)}")
    finally:
        st.session_state['saving'] = False

# Function to export data as CSV
def export_to_csv(df):
    output = io.BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)
    return output

# Main Streamlit app
def main():
    # Set page configuration for better appearance
    st.set_page_config(page_title="Kindness App", page_icon="🌟", layout="centered")

    # Initialize session state
    init_session_state()

    # Custom CSS for improved styling
    st.markdown("""
        <style>
        .stApp { background-color: #f9f9f9; }
        .kindness-header { color: #ff6f61; font-size: 2.5em; text-align: center; }
        .subheader { color: #4a4a4a; }
        .stButton>button { background-color: #ff6f61; color: white; }
        .stTextArea textarea { border-radius: 10px; }
        </style>
    """, unsafe_allow_html=True)

    # Title and description
    st.markdown('<div class="kindness-header">🌟 Kindness App</div>', unsafe_allow_html=True)
    st.markdown("Spread positivity by sharing kind messages or acts of kindness!", unsafe_allow_html=True)

    # Form to submit kindness
    st.subheader("Share a Kind Act", anchor="share")
    with st.form("kindness_form"):
        message = st.text_area("Describe your kind act or message", max_chars=200, height=100)
        category = st.selectbox("Category", ["Compliment", "Helping Others", "Gratitude", "Other"])
        user = st.text_input("Your Name (optional, default: Anonymous)", max_chars=50)
        col1, col2 = st.columns([1, 3])
        with col1:
            submit_button = st.form_submit_button("Share Kindness")
        
        if submit_button:
            if message.strip():
                user = user.strip() if user.strip() else "Anonymous"
                save_thread = threading.Thread(target=save_kindness, args=(message, category, user))
                save_thread.start()
                st.success("Kindness shared! It will appear shortly.")
            else:
                st.error("Please enter a message.")

    # Display saving status with spinner
    if st.session_state['saving']:
        with st.spinner("Saving your kindness..."):
            time.sleep(0.5)

    # Display kindness entries
    st.subheader("Kindness Board", anchor="board")
    df = st.session_state['kindness_data']
    
    if not df.empty:
        # Filters
        st.markdown("### Filter & Sort")
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            categories = ["All"] + sorted(df['category'].unique().tolist())
            selected_category = st.selectbox("Filter by Category", categories)
        with col2:
            sort_by = st.selectbox("Sort by", ["Timestamp (Newest)", "Timestamp (Oldest)", "Category"])
        with col3:
            st.markdown("### Export")
            csv = export_to_csv(df)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="kindness_data.csv",
                mime="text/csv"
            )

        # Apply filters and sorting
        filtered_df = df if selected_category == "All" else df[df['category'] == selected_category]
        if sort_by == "Timestamp (Newest)":
            filtered_df = filtered_df.sort_values(by="timestamp", ascending=False)
        elif sort_by == "Timestamp (Oldest)":
            filtered_df = filtered_df.sort_values(by="timestamp", ascending=True)
        elif sort_by == "Category":
            filtered_df = filtered_df.sort_values(by="category")

        # Display filtered data in a styled table
        st.dataframe(
            filtered_df[["message", "category", "timestamp", "user"]].style.set_properties(**{
                'text-align': 'left',
                'border-color': '#ff6f61',
                'border-style': 'solid',
                'border-width': '1px'
            }),
            use_container_width=True
        )

        # Visualization: Kindness acts by category
        st.subheader("Kindness Statistics", anchor="stats")
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.countplot(data=df, x='category', hue='category', palette='pastel', ax=ax, legend=False)
        ax.set_xlabel("Category", fontsize=12)
        ax.set_ylabel("Number of Acts", fontsize=12)
        ax.set_title("Kindness Acts by Category", fontsize=14)
        plt.xticks(rotation=45)
        plt.close(fig)  # Close the figure to prevent display in non-Streamlit environments
        st.pyplot(fig)

        # Display total acts
        st.metric("Total Kind Acts", len(df))
    else:
        st.info("No kindness acts shared yet. Be the first to spread positivity!")

    # Footer
    st.markdown("---")
    st.markdown("*Built by Cara for Advanced Python Final Project | Powered by Streamlit*")

if __name__ == "__main__":
    import os
    if os.environ.get("STREAMLIT_SERVER_HEADLESS") or os.environ.get("STREAMLIT_RUN"):
        main()
    else:
        print("Please run this script with 'streamlit run kindness_app.py'")
        


