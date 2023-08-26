import csv
import requests
from bs4 import BeautifulSoup

class Tenders:
    def __init__(self, url):
        self.url = url
        self.rows_list = [["Number", "Description", "Condition", "Type",
              "1- Nasher", "1- Desc", "1- Date", "1- Info", "1- Download",
              "2- Nasher", "2- Desc", "2- Date", "2- Info", "2- Download",
              "3- Nasher", "3- Desc", "3- Date", "3- Info", "3- Download",
              "4- Nasher", "4- Desc", "4- Date", "4- Info", "4- Download"]]
    
    def get_tenders(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.content, 'html.parser')
        tenders = soup.find_all(class_="tenderContainer")
        return tenders
    
    def parse_tenders_details(self,rows, row_list):
        for row in rows:
            if row["style"] != "display:none":
                tender_detail_date = "".join(row.find(class_="txtsmall_colorB").find('br').next_siblings).strip()
                row_list.append(tender_detail_date)

                td_elements = row.find_all('td')
                tender_detail_announcement = td_elements[1].text.strip()
                row_list.append(tender_detail_announcement)

                start_close = td_elements[2].contents
                text_components = []
                for content in start_close:
                    to_save = content.text.strip()
                    if to_save:
                        text_components.append(to_save)
                row_list.append(" ".join(text_components))
                
                tender_detail_info_title = td_elements[3].find(class_="popModal")["title"].strip()
                tender_detail_info = td_elements[3].find(class_="popModal")["data-heading"].strip()
                if tender_detail_info_title:
                    tender_detail_info = f"{tender_detail_info_title} : {tender_detail_info}"
                row_list.append(tender_detail_info)
                
                link = td_elements[4].find(class_="btn")
                tender_detail_link = None
                if link:
                    tender_detail_link = f"https://www.pahw.gov.kw{link['href']}"
                row_list.append(tender_detail_link)

        self.rows_list.append(row_list)
        
    def parse_tenders(self, tenders):
        for tender in tenders:
            row_list = []
            cells = tender.find_all(class_="cell")

            tender_title = cells[0].h2.text
            row_list.append(tender_title)

            tender_description = cells[0].p.text
            row_list.append(tender_description)

            tender_condition = cells[1].span.text
            row_list.append(tender_condition)

            tender_type = ''.join(
                cells[2].find('br').next_siblings)  # object is a generator so need to unpack it using an iterator
            row_list.append(tender_type)

            table_element = tender.find('table', class_='blueTable')
            rows = table_element.find_all('tr')

            self.parse_tenders_details(rows=rows,row_list=row_list)
            
    
    def write_to_csv(self):
        with open('tenders.csv', 'w', newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(self.rows_list)

    def run(self):
        tenders = self.get_tenders()
        self.parse_tenders(tenders=tenders)
        self.write_to_csv()

t1 = Tenders(url='https://www.pahw.gov.kw/Tenders_arabic')
t1.run()