import streamlit as st
import pickle
import re
import nltk
from PIL import Image, ImageOps

nltk.download('punkt')
nltk.download('stopwords')

st.set_page_config(
    page_title="Career Analysis Hunter App",
    page_icon="📄",
    layout="wide",
    #initial_sidebar_state="expanded",
)

#loading models
clf = pickle.load(open('clf.pkl','rb'))
tfidfd = pickle.load(open('tfidf.pkl','rb'))


def clean_resume(resume_text):
    clean_text = re.sub('http\S+\s*', ' ', resume_text)
    clean_text = re.sub('RT|cc', ' ', clean_text)
    clean_text = re.sub('#\S+', '', clean_text)
    clean_text = re.sub('@\S+', '  ', clean_text)
    clean_text = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', clean_text)
    clean_text = re.sub(r'[^\x00-\x7f]', r' ', clean_text)
    clean_text = re.sub('\s+', ' ', clean_text)
    return clean_text

# web app
def main():
    html_temp = """

    <div style="background-color:#164863;padding:2px">

    <h1 style="color:#FFFBF5;text-align:center;font-size: 60px;">Career Analysis Hunter App </h1>

    </div><br>"""

    st.markdown(html_temp,unsafe_allow_html=True)

    #st.markdown('<style>h1{color: red;}</style>', unsafe_allow_html=True)
    #st.markdown("<h1 style='text-align: center; color: #F3EEEA; font-size: 60px;'>Career Analysis Hunter App</h1>", unsafe_allow_html=True)

    #im = Image.open("background.jpg")
    #st.image(im,width=100, caption="Resume", use_column_width=True)
    
    st.markdown("""
        <div style='text-align: left; color:  #F3EEEA;'>
            <h1 style='font-size: 26px;'>Upload Resume</h1>
        </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader('', type=['txt', 'pdf'])
    
    if uploaded_file is not None:
        try:
            resume_bytes = uploaded_file.read()
            resume_text = resume_bytes.decode('utf-8')
        except UnicodeDecodeError:
            # If UTF-8 decoding fails, try decoding with 'latin-1'
            resume_text = resume_bytes.decode('latin-1')

        cleaned_resume = clean_resume(resume_text)
        input_features = tfidfd.transform([cleaned_resume])
        prediction_id = clf.predict(input_features)[0]

        # Map category ID to category name
        category_mapping = {
            15: "Java Developer",
            23: "Testing",
            8: "DevOps Engineer",
            20: "Python Developer",
            24: "Web Designing",
            12: "HR",
            13: "Hadoop",
            3: "Blockchain",
            10: "ETL Developer",
            18: "Operations Manager",
            6: "Data Science",
            22: "Sales",
            16: "Mechanical Engineer",
            1: "Arts",
            7: "Database",
            11: "Electrical Engineering",
            14: "Health and fitness",
            19: "PMO",
            4: "Business Analyst",
            9: "DotNet Developer",
            2: "Automation Testing",
            17: "Network Security Engineer",
            21: "SAP Developer",
            5: "Civil Engineer",
            0: "Advocate",
        }

        category_name = category_mapping.get(prediction_id, "Unknown")

        html_temp = 
        """
            <div style="background-color:#9BBEC8;padding:2px;text-align:center;">
                <h1 style="color:#0F2C59;font-size: 35px;">Resume Analysis Result</h1>
                <h2 style='color: #060047;'>"{}"</h2>
            </div><br>
        """.format(category_name, category_name)

        st.markdown(html_temp, unsafe_allow_html=True)

        prediction_details_html = 
        """
        <div style="background-color:#9BBEC8;padding:2px;text-align:center;">
        """
        if prediction_id in [15, 23, 20, 24, 6, 22, 16, 7, 14, 4, 2, 17, 21, 5]:
            prediction_details_html += f"<p style='color: #001C30; font-size: 22px; font-weight: bold;'>Based on the analysis results, this resume specifically fits a {category_name} profile.</p>"
        elif prediction_id in [8, 12, 13, 3, 10, 18, 1, 11, 19, 9, 0]:
            prediction_details_html += f"<p style='color: #001C30; font-size: 22px; font-weight: bold;'>Based on the analysis results, this resume is related to {category_name}.</p>"
        else:

            prediction_details_html += "<p style='color: black; font-size: 30px; font-weight: bold;'>Based on the analysis results, the category of this resume is not specified.</p>"

        st.markdown(prediction_details_html, unsafe_allow_html=True)

        
if __name__ == "__main__":
    main()
