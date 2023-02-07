from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import requests
import csv
import re
import pandas as pd

start_url = "https://doctu.ru"

driver = webdriver.Chrome("C:\\Users\\pc\\PycharmProjects\\AvitoToCSV\\chromedriver.exe")

doctor1_file = pd.read_csv("doctors.csv",sep="|")

error_urls = [
"https://doctu.ru/msk/doctor/shvabauehr-viktorija-ehduardovna",
"https://doctu.ru/msk/doctor/vasileva-tatjana-vladimirovna-8",
"https://doctu.ru/msk/doctor/rjabceva-anastasija-vladimirovna",
"https://doctu.ru/msk/doctor/akhverdjan-karen-karlenovich",
"https://doctu.ru/msk/doctor/lambehrt-lika-georgievna",
"https://doctu.ru/msk/doctor/aslanjan-viktorija-ehduardovna",
"https://doctu.ru/msk/doctor/sogomonjan-ani-arshalujjsovna",
"https://doctu.ru/msk/doctor/baklan-jana-jurevna",
"https://doctu.ru/msk/doctor/czin-lin"
]

def get_line(url):
    try:
        driver.get(url)
        sleep(2)

        soup = BeautifulSoup(driver.page_source, "lxml")

        img_url = start_url + soup.find("div", {"class": "doc-info"}).find("div", {"class": "avatar"}).find("img", {"src": True})["src"]

        img = requests.get(img_url).content
        with open(f"{img_url.split('/')[-1]}", "wb") as file:
            file.write(img)

        fio = ""
        if(soup.find("div", {"class": "doc-info"}).find("h1")):
            fio = soup.find("div", {"class": "doc-info"}).find("h1").text

        spec = ""
        if(soup.find("div", {"class": "doc-info"}).find("div", {"class": "specialty"})):
            spec = soup.find("div", {"class": "doc-info"}).find("div", {"class": "specialty"}).text.strip()

        exp = ""
        cat = ""
        # if(soup.find("div", {"class": "doc-info"}).find("div", {"class": "experience"})):
        #     exp_and_cat = soup.find("div", {"class": "doc-info"}).find("div", {"class": "experience"}).text.split(",")
        #     exp = re.findall(r'\b\d+\b', exp_and_cat[0])
        #     if (len(exp_and_cat) > 1):
        #         for i in range(1,len(exp_and_cat)):
        #             cat += exp_and_cat[i].strip()+","

        clinic = ""
        if(soup.find("section", {"id": "docRevEdu"}).find("a", {"class": "clinic-name"})):
            clinic = soup.find("section", {"id": "docRevEdu"}).find("a", {"class": "clinic-name"}).text

        tel = ""
        if(soup.find("section", {"id": "docRevEdu"}).find("div", {"class": "doc-info"}).find("a", {"itemprop": "telephone"})):
            tel = soup.find("section", {"id": "docRevEdu"}).find("div", {"class": "doc-info"}).find("a", {
                "itemprop": "telephone"}).text

        education = ""
        add_education = ""

        if(soup.find("section", {"id": "docRevEdu"}).findAll("div", {"class": "school"})):
            schools = soup.find("section", {"id": "docRevEdu"}).findAll("div", {"class": "school"})

            for school in schools:
                if (len(school["class"]) == 1):
                    education += school.text.strip().replace('\n', "").replace('\xa0', " ") + ";"

        if(soup.find("section", {"id": "docRevEdu"}).findAll("div", {"class": "training"})):
            courses = soup.find("section", {"id": "docRevEdu"}).findAll("div", {"class": "training"})

            for course in courses:
                add_education += course.text.strip().replace('\n', "").replace('\xa0', " ") + ";"

        line = {
            "fio": fio,
            "spec": spec,
            "exp": exp,
            "cat": cat,
            "clinic": clinic,
            "tel": tel,
            "education": education,
            "courses": add_education,
            "photo": img_url.split('/')[-1]
        }

        return line

    except Exception as e:
        print(e)
        print(url)
        pass

try:
    with open("doctors_error.csv", mode="w", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter="|", lineterminator="\r")
        file_writer.writerow(
                ["fio","spec","exp","cat","clinic","tel","education","courses","photo"])

        # for i in range(1,51):
        #     driver.get(f"https://doctu.ru/msk/doctors?page={i}")
        #     sleep(2)
        #
        #     soup = BeautifulSoup(driver.page_source, "lxml")
        #     doctors_list = soup.find("section",{"id":"doctorList"}).findAll("section",{"class":"doctor_2_0"})
        #     for doctor in doctors_list:
        #         doctor_url = start_url + doctor.find("div",{"class":"doc-description"}).find("div",{"class":"name"}).find("a")["href"]
        for doctor_url in error_urls:
            line = get_line(doctor_url)
            file_writer.writerow(
                    [line["fio"], line["spec"], line["exp"], line["cat"], line["clinic"], line["tel"],
                     line["education"], line["courses"], line["photo"]])

                # if (doctor_url.split("/")[-1]+".jpg") not in doctor1_file["photo"].values:
                #     try:
                #         line = get_line(doctor_url)
                #         file_writer.writerow(
                #             [line["fio"], line["spec"], line["exp"], line["cat"], line["clinic"], line["tel"],
                #              line["education"], line["courses"], line["photo"]])
                #     except:
                #         pass



except:
    pass

finally:

    driver.close()
    driver.quit()