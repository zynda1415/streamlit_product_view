import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

st.title("🔍 Google Sheets Diagnostic Tool")
st.markdown("---")

st.markdown("""
This tool will help you find the exact name of your Google Sheet and verify the connection.
""")

try:
    # Define the scope
    scope = [
        'https://www.googleapis.com/auth/spreadsheets.readonly',
        'https://www.googleapis.com/auth/drive.readonly'
    ]
    
    # Load credentials from Streamlit secrets
    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scope
    )
    
    # Authorize and connect
    client = gspread.authorize(credentials)
    
    st.success("✅ Successfully connected to Google Sheets API!")
    
    # List all spreadsheets the service account can access
    st.subheader("📋 Accessible Google Sheets")
    st.info("These are all the Google Sheets that are shared with your service account:")
    
    try:
        spreadsheets = client.openall()
        
        if spreadsheets:
            st.success(f"Found {len(spreadsheets)} accessible sheet(s):")
            
            for idx, sheet in enumerate(spreadsheets, 1):
                with st.expander(f"Sheet {idx}: {sheet.title}"):
                    st.write(f"**Title:** `{sheet.title}`")
                    st.write(f"**ID:** `{sheet.id}`")
                    st.write(f"**URL:** {sheet.url}")
                    
                    # Try to get the first few rows
                    try:
                        worksheet = sheet.sheet1
                        data = worksheet.get_all_values()
                        st.write(f"**Rows:** {len(data)}")
                        if data:
                            st.write("**First few rows:**")
                            st.dataframe(data[:5])
                    except Exception as e:
                        st.warning(f"Could not read sheet data: {e}")
        else:
            st.warning("⚠️ No spreadsheets found!")
            st.markdown("""
            ### This means:
            - No Google Sheets are shared with the service account email
            
            ### What to do:
            1. Open your Google Sheet: "Streamlit Sheet product view"
            2. Click the **Share** button (top right)
            3. Add this email: `streamlit-key@gen-lang-client-0089966801.iam.gserviceaccount.com`
            4. Give it **Viewer** or **Editor** access
            5. Click **Done**
            6. Refresh this page
            """)
    
    except Exception as e:
        st.error(f"❌ Error listing spreadsheets: {str(e)}")
        import traceback
        st.code(traceback.format_exc())

except Exception as e:
    st.error(f"❌ Error connecting to Google Sheets: {str(e)}")
    import traceback
    st.code(traceback.format_exc())

st.markdown("---")
st.markdown("""
### Service Account Email:
```
streamlit-key@gen-lang-client-0089966801.iam.gserviceaccount.com
```

### How to Share Your Sheet:
1. Open your Google Sheet
2. Click the **Share** button (top right corner)
3. Enter the email above
4. Select **Viewer** or **Editor** from the dropdown
5. Uncheck "Notify people" (it's a service account, not a real person)
6. Click **Done**
""")
