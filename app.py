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
                .sidebar .sidebar-content {
                    background-color: #ECF0F1;
                }
        </style>
        """, unsafe_allow_html=True)

    st.sidebar.image("ss.png", use_column_width=True)
    st.sidebar.markdown("---")
    selected = option_menu(
        menu_title=None,
        options=["Home", "Spam Mail Detector",
                 "Email Header Analyzer", "IP Tracker", "IP Lookup", "Contact Us"],
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

###########################################################################################################################################################################################################################################################################################################################

if selected == "Spam Mail Detector":

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

    # Display the banner
    st.markdown('<div class="banner">WELCOME TO SPAM MESSAGE DETECTOR</div>',
                unsafe_allow_html=True)

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
            color: #000000;
        }

        .result-header {
            font-size: 24px;
            font-weight: bold;
            margin-top: 20px;
            color: #000000; /* Update text color to white */
        }

        .table {
            margin-top: 20px;
            border-collapse: collapse;
            width: 100%;
            background-color: white;
            color: #000000; /* Update text color to white */
        }

        .table th,
        .table td {
            padding: 8px;
            text-align: left;
            border-bottom: 3px solid #ddd;
        }

        .table th {
            background-color: white;
            color: #000000;
        }

        .table tr:hover {
            background-color: #F5F5F5;
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
                    save_attachment(part, filename)

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
        st.write('<div class="spam-headers">From Domain:</div>', from_domain, unsafe_allow_html=True)

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
            st.markdown(
                '<div class="spam-headers">Your Attachment(s) Have Been Downloaded. Please Check Your Folder.</div>', unsafe_allow_html=True)
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



