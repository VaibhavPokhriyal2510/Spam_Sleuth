from collections import Counter
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import os
import tempfile
import streamlit as st
from streamlit_option_menu import option_menu
import pickle
import string
from nltk.corpus import stopwords
import nltk
import email
import re
from email.header import decode_header
import dns.resolver
import ipaddress
import base64
import requests
import urllib.parse
import nltk
from geopy.geocoders import Nominatim
import socket
nltk.download('punkt')
nltk.download('stopwords')
from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()

st.markdown("""
<style>
    #MainMenu, header, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
        unsafe_allow_html=True
    )


add_bg_from_local('bg1.jpg')
with st.sidebar:
    st.markdown("""
        <style>
               .css-18e3th9 {
                    padding-top: 0rem;
                    padding-bottom: 10rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
               .css-1d391kg {
                    padding-top: 3.5rem;
                    padding-right: 1rem;
                    padding-bottom: 3.5rem;
                    padding-left: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)

    st.sidebar.image("ss.png", use_column_width=True)
    st.sidebar.markdown("---")
    selected = option_menu(
        menu_title=None,
        options=["Home", "Spam Message Detector",
                 "Email Header Analyzer", "IP Tracker", "IP Lookup", "Analysis","Contact Us"],
        default_index=0,
        menu_icon="cast"
    )
    st.sidebar.markdown("---")
    st.sidebar.image("small.png", use_column_width=True)


if selected == "Home":

    # Custom CSS styles for the banner
    banner_css = """
    <style>
        .banner {
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #000000;
            color: white;
            padding: 10px;
            margin-bottom: 20px;
            border-radius: 5px;
            font-size: 28px;
            font-family: Trebuchet MS;
            font-weight: bold;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
        }
    </style>
    """

    # Custom CSS styles for the main content
    content_css = """
    <style>
        .content {
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #F5F5F5;
            border-radius: 5px;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
        }
    
        .result-header {
            font-size: 24px;
            font-weight: bold;
            margin-top: 20px;
        }
    </style>
    """

    # Render the custom CSS styles
    st.markdown(banner_css + content_css, unsafe_allow_html=True)

    # Display the banner
    st.markdown('<div class="banner">WELCOME TO SPAM SLEUTH</div>',
                unsafe_allow_html=True)
    
    st.markdown(
        """
        <style>
        .spam-headers {
            color: #000000;
            font-size: 16px;
            font-weight: bold;
            text-align: justify;
            padding: 10px;
            font-family: Trebuchet MS;
            border-radius: 5px;
            border: 2px solid black;
        }
        </style>
        """, unsafe_allow_html=True)
    st.markdown('<p class="spam-headers">1.Spam Mail Detector:The Spam Mail Detector is a powerful tool designed to identify and classify spam emails. It leverages advanced algorithms and machine learning techniques to analyze various aspects of an email, including the header, content, and attachments. By using the Spam Mail Detector, forensic investigators can efficiently filter out spam emails from legitimate ones, saving time and resources in their investigations.<br><br> 2.Email Header Analyzer:The Email Header Analyzer is a valuable tool for forensic investigators to extract and analyze critical information from email headers. Email headers contain vital metadata, including sender and recipient details, timestamps, message IDs, and authentication results. By using the Email Header Analyzer, investigators can uncover valuable insights, such as the source of the email, authentication status, and potential indicators of malicious activity.<br><br> 3.IP Tracker:The IP Tracker tool enables forensic investigators to track and trace the origin and geographical location of an IP address. By analyzing the IP address associated with suspicious activities, investigators can gain valuable information about the potential source of an attack or unauthorized access. The IP Tracker tool provides geolocation data, ISP information, and other relevant details that assist in identifying and apprehending cybercriminals.<br><br>4.IP Lookup:The IP Lookup tool is an essential resource for forensic investigators to gather information about an IP address\'s ownership and historical data. By performing an IP lookup, investigators can identify the organization or individual associated with an IP address, along with contact details and network information. This helps investigators in establishing connections, conducting further investigations, and building a comprehensive profile of potential suspects or sources of malicious activity.<br><br> With the combined capabilities of the Spam Mail Detector, Email Header Analyzer, IP Tracker, and IP Lookup tools, forensic investigators have a robust suite of resources at their disposal to conduct thorough investigations, uncover evidence, and track down cybercriminals. These tools streamline the forensic process, enhance efficiency, and provide valuable insights that contribute to the successful resolution of cases.',unsafe_allow_html=True)

###########################################################################################################################################################################################################################################################################################################################

if selected == "Spam Message Detector":
    
    import os
    import redis
    import time

    # Connect to your internal Redis instance using the REDIS_URL environment variable
    # The REDIS_URL is set to the internal Redis URL e.g. redis://red-343245ndffg023:6379
    connection = redis.from_url(os.environ['REDIS_URL'])

    st.markdown('<div style="display: flex; justify-content: center; align-items: center; background-color: #000000; color: white; padding: 10px; margin-bottom: 20px; border-radius: 5px; font-size: 28px; font-family: Trebuchet MS; font-weight: bold; box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);">WELCOME TO SPAM MESSAGE DETECTOR</div>', unsafe_allow_html=True)

    add_selectbox = st.selectbox("Please select the type of message you want to detect.",
    ("None","Email", "Mobile Phone"),index=0)

    if add_selectbox == "Email":

        def transform_text(text):
            text = text.lower()
            text = nltk.word_tokenize(text)

            y = []
            for i in text:
                if i.isalnum():
                    y.append(i)

            text = y[:]
            y.clear()

            for i in text:
                if i not in stopwords.words('english') and i not in string.punctuation:
                    y.append(i)

            text = y[:]
            y.clear()

            for i in text:
                y.append(ps.stem(i))

            return " ".join(y)

    # Custom CSS styles for the banner
        banner_css = """
        <style>
            .banner {
                display: flex;
                justify-content: center;
                align-items: center;
                background-color: #000000;
                color: white;
                padding: 10px;
                margin-bottom: 20px;
                border-radius: 5px;
                font-size: 28px;
                font-family: Trebuchet MS;
                font-weight: bold;
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
            }
        </style>
        """

    # Custom CSS styles for the main content
        content_css = """
        <style>
            .content {
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #F5F5F5;
            border-radius: 5px;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
            }
    
            .result-header {
            font-size: 24px;
            font-weight: bold;
            margin-top: 20px;
            }
        </style>
        """

    # Render the custom CSS styles
        st.markdown(banner_css + content_css, unsafe_allow_html=True)


        def categorize_sector(message):
    # Convert the message to lowercase for case-insensitive matching
            message = message.lower()

    # Define keywords for each sector
            educational_keywords = ['education', 'learn', 'study', 'school','Academic' ,'Degree', 'Institution', 'Education', 'Assessment', 'Certification', 'Coaching', 'Course', 'Course']
            medical_keywords = ['health', 'doctor', 'hospital', 'medicine']
            business_keywords = ['business', 'company', 'entrepreneur', 'product']
            advertisement_keywords = ['promotion', 'discount', 'sale', 'offer']
            travel_keywords=['travel', 'vacation', 'holiday', 'tourism', 'hotel', 'flight', 'destination', 'explore']
            food_keywords = ['food', 'restaurant', 'recipe', 'cook', 'cuisine', 'menu', 'delicious', 'tasty', 'hungry','order']
            technology_keywords = ['technology', 'software', 'hardware', 'computer', 'programming', 'digital', 'innovation', 'network', 'internet', 'gadget', 'tech', 'data', 'coding', 'development', 'app', 'artificialintelligence', 'web', 'technology', 'device', 'algorithm']
            fashion_keywords = ['fashion', 'clothing', 'style', 'design', 'accessories', 'trend', 'apparel', 'dress', 'outfit', 'fashionable', 'model', 'runway', 'fabric', 'couture', 'fashionista', 'brand', 'shopping', 'collection', 'garment', 'stylish']
            sports_keywords = ['sports', 'fitness', 'exercise', 'athletics', 'game', 'training', 'competition', 'sporting', 'athlete', 'workout', 'physical', 'sport', 'champion', 'play', 'stadium', 'sportsmanship', 'active', 'fitness', 'athlete']
            # Add 10 more words to each sector
            educational_keywords.extend(['scholarship', 'online', 'university', 'studyabroad', 'academic', 'knowledge', 'classroom', 'homework', 'lecture', 'assignment'])
            medical_keywords.extend(['healthcare', 'wellbeing', 'pharmaceutical', 'medicalresearch', 'medicine', 'wellness', 'patientcare', 'preventive', 'disease', 'rehabilitation'])
            business_keywords.extend(['entrepreneurship', 'investor', 'leadership', 'management', 'businessgrowth', 'marketanalysis', 'startup', 'entrepreneurial', 'businessplan', 'innovation'])
            advertisement_keywords.extend(['discounts', 'exclusiveoffers', 'shopping', 'limitedtime', 'clearance', 'dealoftheday', 'promotional', 'marketingcampaign', 'brandpromotion', 'shopnow'])
            travel_keywords.extend(['traveldestination', 'adventure', 'holidaypackage', 'touristattraction', 'travelguide', 'exploretheworld', 'travelagency', 'sightseeingtour', 'vacationrental', 'traveler'])
            food_keywords.extend(['restaurantreview', 'cookingtips', 'foodblog', 'culinaryarts', 'foodphotography', 'foodlover', 'tastetest', 'foodculture', 'foodcritic', 'foodtrend'])
            technology_keywords.extend(['innovativetechnology', 'datascience', 'programmingskills', 'techindustry', 'networksecurity', 'artificialintelligence', 'cybersecurity', 'digitaltransformation', 'technologytrends', 'cloudcomputing'])
            fashion_keywords.extend(['fashiondesigner', 'fashionshow', 'luxuryfashion', 'fashionaccessories', 'fashionblogger', 'fashionindustry', 'stylingtips', 'fashionweek', 'fashionbrand', 'fashioninspiration'])
            sports_keywords.extend(['sportsmanship', 'sportstraining', 'sportsnutrition', 'sportsinjury', 'sportspsychology', 'sportsperformance', 'sportscoach', 'sportsfan', 'sportsenthusiast', 'sportsevent'])

    # Check if any keyword is present in the message
            if any(keyword in message for keyword in educational_keywords):
                return 'Educational'
            elif any(keyword in message for keyword in medical_keywords):
                return 'Medical'
            elif any(keyword in message for keyword in business_keywords):
                return 'Business'
            elif any(keyword in message for keyword in advertisement_keywords):
                return 'Advertisement'
            elif any(keyword in message for keyword in travel_keywords):
                return 'Travel'
            elif any(keyword in message for keyword in food_keywords):
                return 'Food Advertisement'
            elif any(keyword in message for keyword in technology_keywords):
                return 'Technology'
            elif any(keyword in message for keyword in fashion_keywords):
                return 'Faishon'
            elif any(keyword in message for keyword in sports_keywords):
                return 'Sports'
            else:
                return 'uncategorized'

    # Load the pre-trained model and vectorizer
        tfidf = pickle.load(open('vectorizer2.pkl', 'rb'))
        model = pickle.load(open('model2.pkl', 'rb'))

        input_sms = st.text_area("Enter the message", key="input_sms", height=150, max_chars=None,
                             help="Type your message here")

        if st.button('Predict', key="predict_button", help="Click to predict"):
            if input_sms.strip() == "":
                st.warning("Please enter something")
            else:
            # Preprocess the input text
                transformed_sms = transform_text(input_sms)

        # Vectorize the preprocessed text
                vector_input = tfidf.transform([transformed_sms])

        # Perform prediction
                result = model.predict(vector_input)[0]
                sector = categorize_sector(input_sms)

                # Store the data in Redis list
                connection.lpush('messages', input_sms)
                connection.lpush('results', str(result))
                connection.lpush('sectors', sector)

        # Display the result
                if result == 1:
                    st.markdown(
                        """
                    <style>
                    .spam-header {
                    color: #00080a;
                    font-size: 28px;
                    font-weight: bold;
                    text-align: center;
                    padding: 10px;
                    font-family: Trebuchet MS;
                    background-color: #ff5252;
                    border-radius: 5px;
                    }
                    </style>
                    """, unsafe_allow_html=True
                    )
                    st.markdown(
                    '<h1 class="spam-header">Be Careful!! It\'s A Spam</h1>', unsafe_allow_html=True)
                    st.markdown(f"<p style='color: #00080a; font-size: 28px; font-weight: bold; text-align: center; padding: 10px; font-family: Trebuchet MS;background-color: #ff5252;border-radius: 5px;'>Categorized Sector: {sector}</p>", unsafe_allow_html=True)
                elif result == 0:
                    st.markdown(
                        """
                    <style>
                    .not-spam-header {
                    color: #00080a;
                    font-size: 28px;
                    font-weight: bold;
                    text-align: center;
                    padding: 10px;
                    font-family: Trebuchet MS;
                    background-color: #b9f6ca;
                    border-radius: 5px;
                    }
                    </style>
                    """, unsafe_allow_html=True
                    )
                    st.markdown(
                    '<h1 class="not-spam-header">It\'s Not A Spam</h1>', unsafe_allow_html=True)
                    st.markdown(f"<p style='color: #00080a; font-size: 28px; font-weight: bold; text-align: center; padding: 10px; font-family: Trebuchet MS;background-color: #b9f6ca;border-radius: 5px;'>Categorized Sector: {sector}</p>", unsafe_allow_html=True)

                
    if add_selectbox == "Mobile Phone":

        def transform_text(text):
            text = text.lower()
            text = nltk.word_tokenize(text)

            y = []
            for i in text:
                if i.isalnum():
                    y.append(i)

            text = y[:]
            y.clear()

            for i in text:
                if i not in stopwords.words('english') and i not in string.punctuation:
                    y.append(i)

            text = y[:]
            y.clear()

            for i in text:
                y.append(ps.stem(i))

            return " ".join(y)

    # Custom CSS styles for the banner
        banner_css = """
        <style>
            .banner {
                display: flex;
                justify-content: center;
                align-items: center;
                background-color: #000000;
                color: white;
                padding: 10px;
                margin-bottom: 20px;
                border-radius: 5px;
                font-size: 28px;
                font-family: Trebuchet MS;
                font-weight: bold;
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
            }
        </style>
        """

    # Custom CSS styles for the main content
        content_css = """
        <style>
            .content {
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #F5F5F5;
            border-radius: 5px;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
            }
    
            .result-header {
            font-size: 24px;
            font-weight: bold;
            margin-top: 20px;
            }
        </style>
        """

    # Render the custom CSS styles
        st.markdown(banner_css + content_css, unsafe_allow_html=True)

    # Load the pre-trained model and vectorizer
        tfidf = pickle.load(open('vectorizer2.pkl', 'rb'))
        model = pickle.load(open('model2.pkl', 'rb'))

        input_sms = st.text_area("Enter the message", key="input_sms", height=150, max_chars=None,
                             help="Type your message here")

        if st.button('Predict', key="predict_button", help="Click to predict"):
            if input_sms.strip() == "":
                st.warning("Please enter something")
            else:
            # Preprocess the input text
                transformed_sms = transform_text(input_sms)

        # Vectorize the preprocessed text
                vector_input = tfidf.transform([transformed_sms])

        # Perform prediction
                result = model.predict(vector_input)[0]
                query = "INSERT INTO messages (content, is_spam) VALUES (%s, %s)"
        

        # Display the result
                if result == 1:
                    st.markdown(
                        """
                    <style>
                    .spam-header {
                    color: #00080a;
                    font-size: 28px;
                    font-weight: bold;
                    text-align: center;
                    padding: 10px;
                    font-family: Trebuchet MS;
                    background-color: #ff5252;
                    border-radius: 5px;
                    }
                    </style>
                    """, unsafe_allow_html=True
                    )
                    st.markdown(
                    '<h1 class="spam-header">Be Careful!! It\'s A Spam.Please Block The User</h1>', unsafe_allow_html=True)
                    st.markdown(f"<p style='color: #00080a; font-size: 28px; font-weight: bold; text-align: center; padding: 10px; font-family: Trebuchet MS;background-color: #ff5252;border-radius: 5px;'>Categorized Sector: {sector}</p>", unsafe_allow_html=True)
                elif result == 0:
                    st.markdown(
                        """
                    <style>
                    .not-spam-header {
                    color: #00080a;
                    font-size: 28px;
                    font-weight: bold;
                    text-align: center;
                    padding: 10px;
                    font-family: Trebuchet MS;
                    background-color: #b9f6ca;
                    border-radius: 5px;
                    }
                    </style>
                    """, unsafe_allow_html=True
                    )
                    st.markdown(
                    '<h1 class="not-spam-header">It\'s Not A Spam</h1>', unsafe_allow_html=True)
                    st.markdown(f"<p style='color: #00080a; font-size: 28px; font-weight: bold; text-align: center; padding: 10px; font-family: Trebuchet MS;background-color: #b9f6ca;border-radius: 5px;'>Categorized Sector: {sector}</p>", unsafe_allow_html=True)




# Hide Streamlit's default footer
st.markdown(
    '<style>#MainMenu {visibility: hidden;}</style>', unsafe_allow_html=True)

#################################################################################################################################################################################################################################################################################################################################################################################################


if selected == "Email Header Analyzer":
    # Custom CSS styles
    custom_css = """
    <style>
        .banner {
            display: flex;
            justify-content: center;
            align-items: center;
            background-color:#000000;
            color: white;
            padding: 10px;
            margin-bottom: 20px;
            border-radius: 5px;
            font-size: 28px;
            font-family: Trebuchet MS;
            font-weight: bold;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
        }

        .content {
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #F5F5F5;
            border-radius: 5px;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
        }

        .result-header {
            font-size: 24px;
            font-weight: bold;
            margin-top: 20px;
            color: white; /* Update text color to white */
        }

        .table {
            margin-top: 20px;
            border-collapse: collapse;
            width: 100%;
            background-color: white;
            color: white; /* Update text color to white */
        }

        .table th,
        .table td {
            padding: 8px;
            text-align: left;
            border-bottom: 3px solid #ddd;
        }

        .table th {
            background-color: white;
            color: white;
        }

        .table tr:hover {
            background-color: #F5F5F5;
        }

        .download-message {
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: white;
            color: black; /* Update text color to white */
            padding: 10px;
            margin-top: 20px;
            border-radius: 5px;
            font-size: 16px;
            font-family: Trebuchet MS;
            font-weight: bold;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
        }

    </style>
    """

    # Render the custom CSS styles
    st.markdown(custom_css, unsafe_allow_html=True)

    def extract_header_details(msg):
        # Extract message ID
        message_id = msg.get('Message-ID')

        # Extract from, to, cc, bcc, date, and subject
        from_address = msg.get('From')
        to_address = msg.get('To')
        cc_address = msg.get('Cc')
        bcc_address = msg.get('Bcc')
        date = msg.get('Date')
        subject = msg.get('Subject')

        # Extract ARC authentication result
        arc_result = msg.get('ARC-Authentication-Results')

        return message_id, from_address, to_address, cc_address, bcc_address, date, subject, arc_result

    def extract_ip_addresses(header):
        # Exclude SMTP ID pattern (e.g., 06.22.03.11) from IP addresses
        smtp_id_pattern = re.compile(r'\b\d{2}\.\d{2}\.\d{2}\.\d{2}\b')
        ip_addresses = re.findall(
            r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b|\b(?:[A-F0-9]{1,4}:){7}[A-F0-9]{1,4}\b', header)
        ip_addresses = [
            ip for ip in ip_addresses if not smtp_id_pattern.match(ip)]
        unique_ip_addresses = list(set(ip_addresses))  # Remove duplicates
        return unique_ip_addresses

    def save_attachment(part, filename):
        with open(filename, "wb") as f:
            f.write(part.get_payload(decode=True))

    def analyze_email(email_content):
        msg = email.message_from_string(email_content)

        # Extract header details
        message_id, from_address, to_address, cc_address, bcc_address, date, subject, arc_result = extract_header_details(
            msg)

        # Extract SPF, DMARC, and DKIM status
        spf_status = get_authentication_status(
            msg.get('Authentication-Results'), 'spf')
        dmarc_status = get_authentication_status(
            msg.get('Authentication-Results'), 'dmarc')
        dkim_status = get_authentication_status(
            msg.get('Authentication-Results'), 'dkim')

        # Extract IP addresses from the whole header
        header = str(msg)
        ip_addresses = extract_ip_addresses(header)

        # Extract attachments
        attachments = []
        if msg.is_multipart():
            for part in msg.get_payload():
                if part.get_content_disposition() and part.get_content_disposition().startswith('attachment'):
                    filename = part.get_filename()
                    attachments.append(filename)

        return message_id, from_address, to_address, cc_address, bcc_address, date, subject, arc_result, spf_status, dmarc_status, dkim_status, ip_addresses, attachments

    def get_authentication_status(header, keyword):
        match = re.search(r'{}=(\S+)'.format(keyword), header)
        if match:
            status = match.group(1)
            return status.lower() == 'pass'
        return False

    # Render the custom CSS styles
    st.markdown(custom_css, unsafe_allow_html=True)

    # Display the banner
    st.markdown('<div class="banner">WELCOME TO EMAIL HEADER ANALYZER</div>',
                unsafe_allow_html=True)
    st.markdown(
        """
        <style>
        .spam-headers {
            color: #000000;
            font-size: 16px;
            font-weight: bold;
            text-align: justify;
            padding: 10px;
            font-family: Trebuchet MS;
            border-radius: 5px;
            border: 2px solid black;
        }
        </style>
        """, unsafe_allow_html=True)
    st.markdown('<p class="spam-headers">STEPS TO DOWNLOAD THE EMAIL HEADER<br><br>1.In Gmail, click on any email.<br> 2.At the top-right of the email display, click on the 3 dots to show more options.<br> 3.Select Show original. This opens a new web browser tab showing the mail with the complete email header.<br> 4.Click download original. <br> 5.Please convert your .eml file to .txt file for analysis</p>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload an email file [Please convert your .eml file to .txt file for analysis]", type=['txt'])
    if uploaded_file is not None:
        email_content = uploaded_file.read().decode('utf-8')
        message_id, from_address, to_address, cc_address, bcc_address, date, subject, arc_result, spf_status, dmarc_status, dkim_status, ip_addresses, attachments = analyze_email(
            email_content)

        # Display the header details
        st.markdown('<div class="banner">Header Details</div>',
                    unsafe_allow_html=True)
        header_data = [{'Field': 'Message ID', 'Value': message_id},
                       {'Field': 'From', 'Value': from_address},
                       {'Field': 'To', 'Value': to_address},
                       {'Field': 'CC', 'Value': cc_address},
                       {'Field': 'Date', 'Value': date},
                       {'Field': 'Subject', 'Value': subject},
                       {'Field': 'ARC Authentication Result', 'Value': arc_result}]
        st.table(header_data)

        # Display the authentication status
        st.markdown('<div class="banner">Authentication Status</div>',
                    unsafe_allow_html=True)
        auth_data = [{'Authentication Mechanism': 'SPF', 'Status': 'Pass' if spf_status else 'Fail'},
                     {'Authentication Mechanism': 'DMARC',
                         'Status': 'Pass' if dmarc_status else 'Fail'},
                     {'Authentication Mechanism': 'DKIM', 'Status': 'Pass' if dkim_status else 'Fail'}]
        st.table(auth_data)

        # Display the sender information
        from_domain = re.search('@[\w.-]+', from_address).group()
        st.markdown('<div class="banner">Sender Information</div>',
                    unsafe_allow_html=True)
        st.write('From Domain:', from_domain)

        # Display the IP addresses
        st.markdown('<div class="banner">IP Addresses</div>',
                    unsafe_allow_html=True)
        if ip_addresses:
            ip_data = {'IP': [], 'IP Version': []}
            for ip in ip_addresses:
                try:
                    ip_version = ipaddress.ip_address(ip).version
                    ip_data['IP'].append(ip)
                    ip_data['IP Version'].append(f'IPv{ip_version}')
                except ValueError:
                    ip_data['IP'].append(ip)
                    ip_data['IP Version'].append('Invalid')
            st.table(ip_data)
        else:
            st.write('No IP addresses found in the email header.')

        # Display the BCC recipients
        st.markdown('<div class="banner">BCC Recipients</div>',
                    unsafe_allow_html=True)
        if bcc_address:
            bcc_recipients = bcc_address.split(',')
            st.write(bcc_recipients)
        else:
            st.write('No BCC recipients found in the email header.')

        # Display the attachments
        st.markdown('<div class="banner">Attachments</div>',
                    unsafe_allow_html=True)
        if attachments:
            for attachment in attachments:
                st.write(attachment)
        # Create a download link for each attachment
                href = f"data:text/plain;charset=utf-8,{urllib.parse.quote(attachment)}"
                st.markdown(
                    f'<a href="{href}" download="{attachment}">Download {attachment}</a>',
                    unsafe_allow_html=True)
            st.markdown(
                '<div class="download-message">Your Attachment(s) Have Been Downloaded. Please Check Your Folder.</div>', unsafe_allow_html=True)
        else:
            st.write('No attachments found in the email.')


############################################################################################################################################################################################################################################################################################################################
if selected == "IP Tracker":
    # Custom CSS styles for the banner
    banner_css = """
    <style>
        .banner {
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #000000;
            color: white;
            padding: 10px;
            margin-bottom: 20px;
            border-radius: 5px;
            font-size: 28px;
            font-family: Trebuchet MS;
            font-weight: bold;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
        }
    </style>
    """

    # Custom CSS styles for the main content
    content_css = """
    <style>
        .content {
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #F5F5F5;
            border-radius: 5px;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
        }

        .result-header {
            font-size: 24px;
            font-weight: bold;
            margin-top: 20px;
        }
    </style>
    """

    # Render the custom CSS styles
    st.markdown(banner_css + content_css, unsafe_allow_html=True)

    # Display the banner
    st.markdown('<div class="banner">WELCOME TO IP TRACKER</div>',
                unsafe_allow_html=True)

    def get_ip_info(ip):
        url = f"http://ip-api.com/json/{ip}"
        response = requests.get(url)
        try:
            data = response.json()
            return data
        except ValueError:
            return None

    def get_pincode(latitude, longitude):
        geolocator = Nominatim(user_agent="IP_Tracker")
        location = geolocator.reverse((latitude, longitude))
        address = location.raw["address"]
        if "postcode" in address:
            return address["postcode"]
        return "Pincode not available"

    # Custom CSS styles
    css = """
    <style>

        .result {
            font-size: 18px;
            font-weight: bold;
            margin-top: 20px;
        }

        .error {
            color: red;
        }
    </style>
    """

    # Render custom CSS
    st.markdown(css, unsafe_allow_html=True)

    # Input IP address
    ip = st.text_input("Enter the target IP address:",
                       value="", key="ip_input", help="Enter Your IP")
    st.markdown(
        "<style>.stTextInput>div>div>input{height: 50px;}</style>", unsafe_allow_html=True)

    if st.button("Track IP", help="Press to get IP Information"):
        if ip:
            ip_info = get_ip_info(ip)
            if ip_info and ip_info["status"] == "success":
                st.success("IP information retrieved successfully!")
                st.markdown("<div class='container'>", unsafe_allow_html=True)
                st.write("<div class='result'>IP:",
                         ip_info["query"], "</div>", unsafe_allow_html=True)
                st.write("<div class='result'>City:",
                         ip_info["city"], "</div>", unsafe_allow_html=True)
                st.write("<div class='result'>ISP:",
                         ip_info["isp"], "</div>", unsafe_allow_html=True)
                st.write("<div class='result'>Country:",
                         ip_info["country"], "</div>", unsafe_allow_html=True)
                st.write("<div class='result'>Region:",
                         ip_info["region"], "</div>", unsafe_allow_html=True)
                st.write("<div class='result'>Time Zone:",
                         ip_info["timezone"], "</div>", unsafe_allow_html=True)
                pincode = get_pincode(ip_info["lat"], ip_info["lon"])
                st.write("<div class='result'>Pincode:", pincode,
                         "</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.markdown(
                    "<div class='error'>Failed to retrieve IP information.</div>", unsafe_allow_html=True)
        else:
            st.markdown(
                "<div class='error'>Please enter a valid IP address.</div>", unsafe_allow_html=True)

############################################################################################################################################################################################################################################################################################################################
if selected == "IP Lookup":
    def get_ip_address(email_address):
        # Extract the domain from the email address
        domain = email_address.split("@")[1]

        # Perform DNS lookup to retrieve the IP address associated with the domain
        try:
            ip_address = socket.gethostbyname(domain)
            return ip_address
        except socket.gaierror:
            return None

    # Custom CSS styles for the banner
    banner_css = """
    <style>
        .banner {
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #000000;
            color: white;
            padding: 10px;
            margin-bottom: 20px;
            border-radius: 5px;
            font-size: 28px;
            font-family: Trebuchet MS;
            font-weight: bold;
        }
    </style>
    """

    # Render the custom CSS styles
    st.markdown(banner_css, unsafe_allow_html=True)

    # Display the banner
    st.markdown('<div class="banner">EMAIL IP LOOKUP</div>',
                unsafe_allow_html=True)

    email_address = st.text_input("Enter the email address")

    if st.button("Get IP Address"):
        if email_address:
            ip_address = get_ip_address(email_address)

            if ip_address:
                st.write("IP Address:", ip_address)
            else:
                st.write("Unable to retrieve IP address.")
        else:
            st.write("Please enter an email address.")

########################################################################################################################################################################################################################################################################################################################################################################################################################################

if selected == "Contact Us":
    # Custom CSS styles for the banner
    banner_css = """
    <style>
        .banner {
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #000000;
            color: white;
            padding: 10px;
            margin-bottom: 20px;
            border-radius: 5px;
            font-size: 28px;
            font-family: Trebuchet MS;
            font-weight: bold;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
        }
        .contact-form button[type="submit"]:hover {
            background-color: #e0e0e0;
        }
    </style>
    """

    # Custom CSS styles for the main content
    content_css = """
    <style>
        .content {
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #F5F5F5;
            border-radius: 5px;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
        }
    
        .result-header {
            font-size: 24px;
            font-weight: bold;
            margin-top: 20px;
        }
    </style>
    """

    # Render the custom CSS styles
    st.markdown(banner_css + content_css, unsafe_allow_html=True)

    # Display the banner
    st.markdown('<div class="banner">Get In Touch With Us!</div>',
                unsafe_allow_html=True)

    contact_form = """
    <form action="https://formsubmit.co/pokhriyal2510@gmail.com" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="Your name" required>
        <input type="email" name="email" placeholder="Your email" required>
        <textarea name="message" placeholder="Your message here"></textarea>
        <button type="submit">Send</button>
    </form>
    """

    st.markdown(contact_form, unsafe_allow_html=True)

    # Use Local CSS File
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    local_css("style.css")

########################################################################################################################################################################################################################################################################################################################################################################################################################################
if selected == "Analysis":
    import os
    import redis

    # Connect to your internal Redis instance using the REDIS_URL environment variable
    # The REDIS_URL is set to the internal Redis URL e.g. redis://red-343245ndffg023:6379
    connection = redis.from_url(os.environ['REDIS_URL'])
    
    import pandas as pd
    import plotly.graph_objects as go
    from streamlit_option_menu import option_menu 

    # Display a bar chart of the sector distribution
    banner_css = """
    <style>
        .banner {
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #000000;
            color: white;
            padding: 10px;
            margin-bottom: 20px;
            border-radius: 5px;
            font-size: 28px;
            font-family: Trebuchet MS;
            font-weight: bold;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
        }
        .contact-form button[type="submit"]:hover {
            background-color: #e0e0e0;
        }
    </style>
    """
    st.markdown(banner_css, unsafe_allow_html=True)
    
    # Retrieve data from Redis
    messages = connection.lrange('messages', 0, -1)
    results = connection.lrange('results', 0, -1)
    sectors = connection.lrange('sectors', 0, -1)

    # Convert data to appropriate types
    messages = [msg.decode() for msg in messages]
    results = [eval(res.decode()) for res in results]
    sectors = [sec.decode() for sec in sectors]

    # Convert data to pandas DataFrame
    df_messages = pd.DataFrame(messages, columns=["content"])
    df_results = pd.DataFrame(results, columns=["results"])
    df_sectors = pd.DataFrame(sectors, columns=["sectors"])

    # Streamlit Analysis

    # Sector distribution
    st.markdown('<div class="banner">SECTOR DISTRIBUTION</div>', unsafe_allow_html=True)
    sector_counts = df_sectors['sectors'].value_counts()
    st.bar_chart(sector_counts)
    

    # Spam & non-spam distribution
    spam_counts = df_results['results'].value_counts()
    fig = go.Figure(data=[go.Pie(labels=spam_counts.index, values=spam_counts.values)])
    st.plotly_chart(fig)


    # Spam vs non-spam count by sector
    spam_counts = df_messages[df_messages['is_spam'] == 1].groupby('sectors')['results'].count()
    non_spam_counts = df_messages[df_messages['is_spam'] == 0].groupby('sectors')['results'].count()

    fig = go.Figure()
    fig.add_trace(go.Bar(x=spam_counts.index, y=spam_counts.values, name='Spam'))
    fig.add_trace(go.Bar(x=non_spam_counts.index, y=non_spam_counts.values, name='Non-Spam'))
    fig.update_layout(barmode='stack', xaxis_title='Sector', yaxis_title='Count')
    st.plotly_chart(fig)
