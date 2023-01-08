import streamlit as st
import numpy as np
import os 
import smtplib as s
from PIL import Image
import pickle


model = pickle.load(open('C:/Users/Mahendranath/ml1/Model/ML_1.pkl', 'rb'))

def run():
    img1 = Image.open('bank.jpeg')
    img1 = img1.resize((700,250))
    st.image(img1,use_column_width=False)
    st.title("Bank Loan Prediction using Machine Learning")

    ## Account No
    account_no = st.text_input('Account number')

    ## Full Name
    fn = st.text_input('Full Name')

    ## Email of sender
    #email_sender=st.text_input("Enter user Email")

    ## Password of sender
    #password=st.text_input("Enter password",type="password")

    ## Email of receiver
    email_reciever=st.text_input("Email")

    #subject=st.text_input("Enter subject")

    ## For gender
    gen_display = ('Female','Male')
    gen_options = list(range(len(gen_display)))
    gen = st.selectbox("Gender",gen_options, format_func=lambda x: gen_display[x])

    ## For Marital Status
    mar_display = ('No','Yes')
    mar_options = list(range(len(mar_display)))
    mar = st.selectbox("Marital Status", mar_options, format_func=lambda x: mar_display[x])

    ## No of dependets
    dep_display = ('No','One','Two','More than Two')
    dep_options = list(range(len(dep_display)))
    dep = st.selectbox("Dependents",  dep_options, format_func=lambda x: dep_display[x])

    ## For edu
    edu_display = ('Not Graduate','Graduate')
    edu_options = list(range(len(edu_display)))
    edu = st.selectbox("Education",edu_options, format_func=lambda x: edu_display[x])

    ## For emp status
    emp_display = ('Job','Business')
    emp_options = list(range(len(emp_display)))
    emp = st.selectbox("Employment Status",emp_options, format_func=lambda x: emp_display[x])

    ## For Property status
    prop_display = ('Rural','Semi-Urban','Urban')
    prop_options = list(range(len(prop_display)))
    prop = st.selectbox("Property Area",prop_options, format_func=lambda x: prop_display[x])

    ## For Credit Score
    cred_display = ('Below 500','Above 500')
    cred_options = list(range(len(cred_display)))
    cred = st.selectbox("Credit Score",cred_options, format_func=lambda x: cred_display[x])

    ## Applicant Monthly Income
    mon_income = st.number_input("Applicant's Monthly Income",value=0)

    ## Co-Applicant Monthly Income
    co_mon_income = st.number_input("Co-Applicant's Monthly Income",value=0)

    ## Loan AMount
    loan_amt = st.number_input("Loan Amount",value=0)

    ## loan duration
    dur_display = ['2 Month','6 Month','8 Month','1 Year','16 Month']
    dur_options = range(len(dur_display))
    dur = st.selectbox("Loan Duration",dur_options, format_func=lambda x: dur_display[x])
    
    ##Loanamount_log
    loanamount_log=np.log(loan_amt)

    ##TotalIncome
    total=mon_income +  co_mon_income
    total_log=np.log(total)

    if st.button("Submit"):
        duration = 0
        if dur == 0:
            duration = 60
        if dur == 1:
            duration = 180
        if dur == 2:
            duration = 240
        if dur == 3:
            duration = 360
        if dur == 4:
            duration = 480
        features = [[account_no, gen, mar, dep, edu, emp, mon_income, co_mon_income, loan_amt, duration, cred, prop]]
        print(features)

        test=[[gen, mar, dep, edu, duration, cred, loanamount_log, total_log]]      
        print(test)
        prediction = model.predict(test)
        lc = [str(i) for i in prediction]
        ans = int("".join(lc))
        if ans == 0:
            st.error(
                "Hello: " + fn +" || "
                "Account number: "+account_no +' || '
                'According to our Calculations, you will not get the loan from Bank'
            )
            body="Hello, {} Account number {}. According to our Calculations, you will not get the loan from Bank".format(fn,account_no)

        else:
            st.success(
                "Hello: " + fn +" || "
                "Account number: "+account_no +' || '
                'Congratulations!! you will get the loan from Bank'
            )
            body="Hello, {} Account number {}. Congratulations!! you will get the loan from Bank".format(fn,account_no)

        email_sender="mnath48320@gmail.com"
        password="Gmail@2pass"
        subject="Loan Prediction"

        if email_reciever!="" and email_sender!="" and password!="":
            print(body)
            connection=s.SMTP('smtp.gmail.com',587)
            connection.starttls()
            connection.login(email_sender,password)
            message="Subject:{}\n\n{}".format(subject,body)
            connection.sendmail(email_sender,email_reciever,message)
            connection.quit()
            st.success("Email sent sucessfully")

run()
