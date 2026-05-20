# import the libraries like requests,bs4 and Pandas 
import requests as rq 
from bs4 import BeautifulSoup 
import pandas as pd 
import sys
import lxml
import re
counter=0
all_jobs=[]

#This Function to remove '-' from name of company
def remove_from_company_name(name):
        return name.replace("-","")


# This Function to split the multiple line of job description and requirement to different lines
def split_text(text):
        if pd.isna(text) or not str(text).strip :
                return "N/A"
        text=str(text).strip()
        text=text.replace("\xa0"," ")

        if '*' in text :
                items=re.split(r'\*',text)
        elif re.search(r'\.[A-Z]',text) :
                items=re.split(r'(?<=\.)\s*(?=[A-Z])',text)
        else :
                items=re.split(r'\n+',text)
        
        return [''.join(item.strip().lstrip('-–•▪').strip()) for item in items]
        




# This Function to check if we have multiple elements or one element
def check_len(job_description_or_requirments) :
        if len(job_description_or_requirments) >1 :
                job_des=""
                for e in job_description_or_requirments :
                        job_des = job_des + e.text
                job_description_or_requirments = job_des
        elif len(job_description_or_requirments) == 1 :
        #print(len(job_description))
        #print(job_description.prettify())
                job_description_or_requirments=job_description_or_requirments[0].text
        return job_description_or_requirments


# This function to get job description of every job
def details_info(de_link) :
        try :
                #de_info={}
                #print("https://wuzzuf.net/"+de_link)
                page=rq.get("https://wuzzuf.net/"+de_link)
                soup=BeautifulSoup(page.text,"lxml")
                #print(soup)
                #print("https://wuzzuf.net/"+de_link)
                #print("#"*15)
                job_description=soup.find("div",{"id":"app"}).find_all("section",{"class":"css-5pnqc5"})[0].find("div",{"class":"css-n7fcne"})
                job_requirments=soup.find("div",{"id":"app"}).find_all("section",{"class":"css-5pnqc5"})[1].find("div",{"class":"css-1lqavbg"})
                #print(job_description.prettify())
                #print("#"*15)
                job_description=check_len(job_description.contents)
                job_description=split_text(job_description)
                job_description="\n".join(job_description)
                #print(job_requirments.prettify())
                #print("#"*15)
                job_requirments=check_len(job_requirments.contents)
                job_requirments=split_text(job_requirments)
                job_requirments="\n".join(job_requirments)

                #print(job_description)
                return job_description,job_requirments
        except Exception as e :
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print(f"The Error From details_info Function : {e}")
                print("Line:", exc_tb.tb_lineno)




# this function to get the basic information about the job like job_title,company_name,location and the link to get more information 
# about the job
def job_info(different_jobs):
        try:
                all_jobs=[]
                for job in different_jobs :
                        e={}
                        e["job_title"]=job.find("div",{"class":"css-pkv5jc"}).find("a",{"class":"css-o171kl"}).text
                        company=job.find("div",{"class":"css-pkv5jc"}).find("div",{"class":"css-lptxge"}).find("div",{"class":"css-1k5ee52"}).find("a").text
                        e["company_name"]=remove_from_company_name(company)
                        e["location"]=job.find("div",{"class":"css-pkv5jc"}).find("div",{"class":"css-lptxge"}).find("div",{"class":"css-1k5ee52"}).find("span",{"class":"css-16x61xq"}).text
                        e["time"]=job.find("div",{"class":"css-pkv5jc"}).find("div",{"class":"css-lptxge"}).find("div",{"class":"css-1k5ee52"}).find("div",{"class":["css-eg55jf","css-1jldrig"]}).text
                        de_link=job.find("div",{"class":"css-pkv5jc"}).find("div",{"class":"css-lptxge"}).find("a",{"class":"css-o171kl"}).get("href")
                        e["job description"],e["job requirements"]=details_info(de_link)
                        all_jobs.append(e)
        except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print(f"The Error from job_info Function : {e}")
                print("Line:", exc_tb.tb_lineno)
        return all_jobs

# This Function to save list of dictionaries as excel file

def save_to_excel(all_jobs):
           #print(all_jobs)
           if all_jobs :
                df=pd.DataFrame(all_jobs)
                df.to_excel("all_jobs.xlsx",index=False)


# This Function to get the link of Next Page 
def get_next_link(page) :
        soup=BeautifulSoup(page.text,"lxml")
        next_link=soup.find("div",{"id":"app"}).find("div",{"css-1kyg0q1"}).find("ul",{"class":"css-1pbzzot"}).find_all("li",{"class":"css-1kxf7dm"})[-1].find("a")
        next_link=next_link.get("href")
        #print(next_link)
        #print("#"*15)
        return next_link



# Main Function
def main(link):
        global counter 
        global all_jobs
        try:
                # first we will request the page that we want 
                page =rq.get(link)
                # we will get the title to name the file with this name 
                soup =BeautifulSoup(page.text,"lxml")
                #print(soup)
                name_of_file=soup.find("div",{"id":"app"}).find("h1").text[5:]
                #print(name_of_file)
                # Now we will get the different jobs 
                different_jobs=list(soup.find("div",{"id":"app"}).find("div",{"class","css-1dkg1tz"}).find("div",{"class":"css-9i2afk"}).children)[3].find_all("div",{"class":"css-ghe2tq"})
                jobs=job_info(different_jobs)
                #print(jobs)
                #print("#"*15)
                all_jobs=all_jobs+jobs
                new_link=get_next_link(page) 
                if new_link and counter < 4 :
                        counter=counter+1
                        main(new_link)
                else :
                        save_to_excel(all_jobs)
        except Exception as e :
                print(f"The Error : {e}")


main("https://wuzzuf.net/search/jobs?q=data%20analyst&a=navbg&filters%5Bcountry%5D%5B0%5D=Egypt")
