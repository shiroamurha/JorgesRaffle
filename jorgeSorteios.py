from bs4 import BeautifulSoup as Soup
from random import choice
import json
import smtplib
import email.message


class jorgeSorteios():

    def __init__(self):
        
        # lists of the respective applicants and dicts of their respective ids

        first_applicants = [
            'Jair Bolsonaro', 'Luiz Inácio Lula da Silva', 'Ciro Gomes', 
            'Pablo Marçal', 'José Maria Eymael'
        ]

        second_applicants = ['Jair Bolsonaro', 'Luiz Inácio Lula da Silva']

        first_applicants_dict = {
            'Jair Bolsonaro':'bolsonaro', 'Luiz Inácio Lula da Silva':'lula', 'Ciro Gomes':'ciro', 
            'Pablo Marçal':'pablo', 'José Maria Eymael':'eymael'
        }

        second_applicants_dict = {'Jair Bolsonaro':'bolsonaro2', 'Luiz Inácio Lula da Silva':'lula2'}

        ###

        html = Soup(open('email.html', 'r').read(), 'html.parser') # getting static source (html of the email)
        
        # raffling of the applicants 
        raffle = [choice(first_applicants), choice(second_applicants)]
        raffle_ = [first_applicants_dict.get(raffle[0]), second_applicants_dict.get(raffle[1])]

        # putting all shit inside the html with DOM
        html.find('a', attrs = {'id':'sorteados'}).string = f'1º: {raffle[0]}  -  2º: {raffle[1]}'

        html.find('a', attrs = {'id':raffle_[0]}).string = str(int(html.find('a', attrs = {'id':raffle_[0]}).text)+1)
        html.find('a', attrs = {'id':raffle_[1]}).string = str(int(html.find('a', attrs = {'id':raffle_[1]}).text)+1)
        html.find('a', attrs = {'id':'raffle'}).string = str(int(html.find('a', attrs = {'id':'raffle'}).text)+1)
        subject = f"Sorteio número {html.find('a', attrs = {'id':'raffle'}).string}"
        
        # dumping the modified html inside email.html file
        open('email.html', 'w').write(f'{html}')

        # sending the email with the modified html as source/data 
        self.send_email(str(html), subject)
    
        

    def send_email(self, html, subject): 
 
        # email data and assets
        msg = email.message.Message()
        msg['Subject'] = subject
        msg['From'] = 'JorgeSorteios.LTDA@gmail.com'
        msg['To'] = 'Jorgecarvalhoduh@gmail.com'
        password = 'im not going to put my password here'

        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(html) # email content inside html param.

        # conecting to gmail server and logging in
        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()
        s.login(msg['From'], password)
        
        # sending the email
        s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))

        # if everything goes ok, then:
        print('E-mail successfully sent') 



if __name__ == "__main__":

    # running the class 
    jorgeSorteios()