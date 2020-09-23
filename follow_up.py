
from operator import index
import pandas as pd
import datetime as dt
import smtplib
import ssl
from email.message import EmailMessage
import os

def main(csv ='c:/Users/Rana/Documents/My stuff/Job_apps/follow_up.csv',mail=EmailMessage()):
    df = pd.read_csv(csv)
    
    for idx, x in df[(df['Follow Up']==True)&(df['Followed up?'] == False)].iterrows():
        #print(x)
        strip = x['Follow Up date'].split('/')
        strip = dt.date(int(strip[2]),int(strip[0]),int(strip[1]))
        #print(strip)
        if  strip <= dt.date.today():
            mail['To'] = x['Contact email']  # replace with actual recipient from csv
            
            mail.set_content(x['Follow up message'].format(name = x['Contact name'],
            position= x['Position'], job_board=x['Job-board']))
            
            server.send_message(mail)
            print('sent to:',x['Contact name'])
            df['Followed up?'][idx] = True
        else:
            print(x['Contact email'])
            print(idx)
            df['Followed up?'][idx] = True
            

    print('all done')     
    if input('overwrite and save:\n') == 'y':
        os.remove('c:/Users/Rana/Documents/My stuff/Job_apps/follow_up.csv')
        df.to_csv('c:/Users/Rana/Documents/My stuff/Job_apps/follow_up.csv',index=False)

if __name__ == "__main__":
    

    # gmail port details 
    port = 465
    password = input("your password:\n")
    context = ssl.create_default_context()

    sender = input('your email address:\n')   #your email address 

    msg= EmailMessage()
    msg['Subject'] = 'Follow up'
    msg['From'] = sender

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender, password)
        main(mail=msg)

    print('\nCongrats, you followed up!\n')
    