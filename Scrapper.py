import os
import sys
import requests
import re
import time
import xlrd
import urllib
from selenium import webdriver
from bs4 import BeautifulSoup
from linkedin_scraper import Person
import pandas as pd

Username = ''
Password = ''
#print(df.head(5))  
browser = webdriver.Chrome(executable_path=r"chromedriver.exe")
browser.get('https://www.linkedin.com/')
browser.find_element_by_id('login-email').send_keys(Username)
browser.find_element_by_id ('login-password').send_keys(Password)
#time.sleep(5); 
#browser.findElement(By.xpath('//*[@id="memberlogin"]/div[1]/input[3]')).click();
browser.find_element_by_id ('login-submit').click();
#time.sleep(20)
#browser.find_element_by_id ('nav-search-bar').send_keys(search)
file_name =  "C:\\Users\\imedia27\\AppData\\Local\\Programs\\Python\\Python37-32\\doc list.xlsx";
sheet =  "Sheet1";


for h in range(1,6):
	
	print("h",h)
	df = pd.read_excel(io=file_name, sheet_name=sheet)
	Name = (df['DrName'].tolist())
	Address =  (df['AddressClinic'].tolist())
	search = Name[h] + ' ' + Address[h]
	print("Name",search)
	browser.find_element_by_xpath('//input[@placeholder="Search"]').send_keys(search);
	#time.sleep(5);
	browser.find_element_by_xpath('//input[@placeholder="Search"]').send_keys(u'\ue007')
	time.sleep(10);
	html = browser.page_source
	soup1 = BeautifulSoup(html, "lxml")
	if soup1.find_all("div", {"class": "search-no-results__image-container"}):
		print("inside if")
		browser.find_element_by_xpath('//input[@placeholder="Search"]').clear();
		continue
	else:
		print("insid else")
		browser.find_element_by_class_name('search-result__image').click();
		time.sleep(10);
		print (browser.current_url)
		url = browser.current_url;
		print("*******************************************Scrolling Start ********************************************")
		browser.execute_script("window.scrollTo(0, 1500)") 
		time.sleep(20)
		html = browser.page_source
		soup = BeautifulSoup(html, "lxml")

#with open("output1.html", "wb") as file:
#   file.write(str(soup).encode("utf-8"))
#browser.find_element_by_value ('START ADS').click();
#browser.findElement(By.xpath('//*[@id="main"]/h2[2]/div/input')).click();
#browser.findElement(By.xpath('//input[@value="START WATCHING PAYED ADS"')).click();
#browser.find_element_by_xpath("//input[@value='START WATCHING PAYED ADS' and @type='button']").click()
#WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@value='START WATCHING PAYED ADS' and @type='button']"))).click()

		name = soup.findAll("h1", {"class": "pv-top-card-section__name inline t-24 t-black t-normal"})
		print("**********************************FULL NAME**********************************")
		Name_Deatil = []
		for i in name:
			Name = re.sub('\n+',' ', i.text)
			Name_Deatil.append(Name)
		print (Name_Deatil)

		summary = soup.findAll("p", {"class": "pv-top-card-section__summary-text mt4 ember-view"})
		print("**********************************SUMMARY**********************************")
		Summary_Detail = []
		for i in summary:
			Summary = re.sub('\n+',' ', i.text) 	
			if not Summary:
				Summary_Detail = ['NA']
			else:
				Summary_Detail.append(Summary)
		print(Summary_Detail)

		header_articles = soup.findAll("h2", {"class":"pv-recent-activity-section-v2__headline t-20 t-black t-normal"})
		print("**********************************ARTICLES HEADER**********************************")
		Article_Title = []
		for i in header_articles:
			Header_Articles = str(re.sub('\s+',' ', i.text))
			if "Articles" in Header_Articles:
				articles = soup.findAll("h3", {"class": "t-16 t-black t-bold"})
				for articles1 in articles:
					try:	
						harsh = articles1.find("div",{"class": "lt-line-clamp lt-line-clamp--multi-line ember-view"})
						Articles = re.sub('\n+',' ', harsh.text)
						Article_Title.append(Articles)	
					except:
						pass
				print(Article_Title)
			else:
				Article_Title = []

		header_experience = soup.findAll("h2",{"class":"pv-profile-section__card-heading t-20 t-black t-normal"})
		print("**********************************EXPERINCE HEADER**********************************")
		Experience = []
		for j in header_experience:
			Header_Experience = str(re.sub('\s+',' ', j.text))
	#print("Header_Experience",Header_Experience)
			if "Experience" in Header_Experience:
		#print("true")
				experience = soup.findAll("li", {"class": "pv-profile-section__card-item-v2 pv-profile-section pv-position-entity ember-view"})
				for experience1 in experience:
					try:	
						title = experience1.find("h3",{"class": "t-16 t-black t-bold"})
						company = experience1.find("h4",{"class": "t-16 t-black t-normal"})
						time_period = experience1.find("div",{"class":"display-flex"})
						location = experience1.find("h4",{"class":"pv-entity__location t-14 t-black--light t-normal block"})
						Title = re.sub('\n+',' ', title.text)
						Company = re.sub('\n+',' ', company.text)
						Time_Period = re.sub('\n+',' ', time_period.text)
						Location = re.sub('\n+',' ', location.text)
						Experience.append(Title+Company+Time_Period+Location)
					except:
						pass
				print("Experience list",Experience)
			else:
				Experience = []

		header_education = soup.findAll("h2",{"class":"pv-profile-section__card-heading t-20 t-black t-normal"})
		print("**********************************EDUCATION HEADER**********************************")
		Education_Details = []
		for j in header_education:
			Header_Education = str(re.sub('\s+',' ', j.text))
			if "Education" in Header_Education:
				education = soup.findAll("li", {"class": "pv-profile-section__sortable-item pv-profile-section__section-info-item relative pv-profile-section__sortable-item--v2 sortable-item ember-view"})
		
				for education1 in education:
					try:	
						education_title = education1.find("h3",{"class": "pv-entity__school-name t-16 t-black t-bold"})
						education_degree = education1.find("div",{"class": "pv-entity__degree-info"})
						education_time_period = education1.find("p",{"class":"pv-entity__dates t-14 t-black--light t-normal"})
						Education_Title = re.sub('\n+',' ', education_title.text)
						Education_Degree = re.sub('\n+',' ', education_degree.text)
						Education_Time_Period = re.sub('\n+',' ', education_time_period.text)
						Education_Details.append(Education_Title+Education_Degree+Education_Time_Period)
					except:
						pass
				print(Education_Details)
				break
			else:
				Education_Details = []

		header_skill = soup.findAll("h2",{"class":"pv-profile-section__card-heading t-20 t-black t-normal"})
		print("**********************************SKILL HEADER**********************************")
		Skills_Details = []
		for j in header_skill:
			Header_Skill = str(re.sub('\s+',' ', j.text))
			if "Skills & Endorsements" in Header_Skill:
				skill = soup.findAll("li", {"class": "pv-skill-category-entity__top-skill pv-skill-category-entity pb3 pt4 pv-skill-endorsedSkill-entity relative ember-view"})	
				for skill1 in skill:
					try:	
						skill_title = skill1.find("span",{"class": "t-16 t-black t-bold"})
						Skill_Title = re.sub('\n+',' ', skill_title.text)
						Skills_Details.append(Skill_Title)
					except:
						pass
				print(Skills_Details)
				break
			else:
				Skills_Details = []


		header_accomplishments = soup.findAll("h2",{"class":"card-heading t-20 t-black t-normal fl"})
		print("**********************************ACCOMPLISHMENTS HEADER**********************************")
		Accomplishments = []
		for j in header_accomplishments:
			Header_Accomplishments = str(re.sub('\s+',' ', j.text))
			if "Accomplishments" in Header_Accomplishments:
				accomplishments = soup.findAll("div", {"class": "pv-accomplishments-block__content break-words"})
				
				for accomplishments1 in accomplishments:
					try:	
						accomplishments_title = accomplishments1.find("div",{"class": "pv-accomplishments-block__list-container"})
						Accomplishments_Title = re.sub('\n+',' ', accomplishments_title.text)
						main_title = accomplishments1.find("h3",{"class":"pv-accomplishments-block__title"})
						Main_Title = re.sub('\n+',' ', main_title.text)
						Accomplishments.append(Main_Title+Accomplishments_Title)
					except:
						pass
				print(Accomplishments)
			else:
				Accomplishments = []

		header_interests = soup.findAll("h2",{"class":"card-heading t-20 t-black t-normal"})
		print("**********************************INTERESTS HEADER**********************************")
		Interests = []
		for j in header_interests:
			Header_Interests = str(re.sub('\s+',' ', j.text))
			if "Interests" in Header_Interests:
				interests = soup.findAll("li", {"class": "pv-interest-entity pv-profile-section__card-item ember-view"})
				
				for interests1 in interests:
					try:	
						interests_title = interests1.find("h3",{"class": "pv-entity__summary-title t-16 t-black t-bold"})
						Interests_Title = re.sub('\n+',' ', interests_title.text)
						Interests.append(Interests_Title)
					except:
						pass
				print(Interests)
			else:
				Interests = []
		
			
		writer = pd.ExcelWriter('result.xlsx', engine='openpyxl') 
		wb  = writer.book
		df = pd.DataFrame({'Name': pd.Series(Name),
								'Education': pd.Series(Education_Details),
			                  'Skills': pd.Series(Skills_Details),
			                  'Summary': pd.Series(Summary_Detail),
			                  'Articles': pd.Series(Article_Title),
			                  'Experience': pd.Series(Experience),
			                  'Accomplishments': pd.Series(Accomplishments),
			                  'Interests': pd.Series(Interests),

			                  })

		df.to_excel(writer)
			
		wb.save('result.xlsx')
		
