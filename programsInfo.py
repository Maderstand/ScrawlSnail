#-*-coding:utf-8-*-
#-*-encoding=utf-8

"""
This script is used for download programs info from the xxx.org

"""
import os
import sys
import requests,urllib
import re,math
from bs4 import BeautifulSoup
#from PIL import Image
#from pytesseract import image_to_string
from http import cookiejar

# -------------------------------------------------
# define function getProgInfo, getProgPDF
# -------------------------------------------------

def getProgInfo(progNum, progUrl, reviewState, market_filePath):
    #progS = requests.Session()
    #get_PI_req = progS.get(progUrl, cookies = cookies)
    prog_req = urllib.request.Request(progUrl)
    prog_resp = urllib.request.urlopen(prog_req)
    html_PI = BeautifulSoup(prog_resp.read(),'html.parser')

    # 1. find CEO info
    detail_CEO = html_PI.find('div',attrs={'class':'bmTable'})
    detail_CEO_Tr = detail_CEO.find_all('tr')
    detail_CEO_Gender = detail_CEO_Tr[0].find_all('td')[1].get_text()
    detail_CEO_BirthDate = detail_CEO_Tr[1].find_all('td')[2].get_text()
    detail_CEO_MaxEdu = detail_CEO_Tr[2].find_all('td')[0].get_text()
    detail_CEO_University = detail_CEO_Tr[2].find_all('td')[1].get_text()
    detail_CEO_Addr = detail_CEO_Tr[5].find_all('td')[0].get_text()

    # 2. find Company info
    detail_COM = html_PI.find('div',attrs={'class':'bmTable bmTable2'})
    detail_COM_Tr = detail_COM.find_all('tr')
        # .1 find tittle[1]
    detail_Tittle = html_PI.find_all('div',attrs={'class':'tittle'})[1].get_text()
                                                
    if len(detail_Tittle) == 4:
        detail_COM_Name = detail_COM_Tr[0].find_all('td')[0].get_text()
        detail_COM_RegiDate = detail_COM_Tr[1].find_all('td')[0].get_text()
        detail_COM_Field = detail_COM_Tr[1].find_all('td')[1].get_text()
        # .2 if not
    else:
        detail_COM_Name = detail_COM_Tr[0].find_all('td')[0].get_text()
        detail_COM_RegiDate = "企业成立时间：0000"
        detail_COM_Field = detail_COM_Tr[0].find_all('td')[2].get_text()
        
    # 3. find Program Score if reviewState is finished
    detail_SCO = html_PI.find('div',attrs={'class':'contTable'})
    detail_SCO_Tr = detail_SCO.find_all('tr')
    if reviewState == 1:
        detail_SCO_CeoAbility = detail_SCO_Tr[1].find_all('td')[4].get_text()\
                                .replace(" ","").replace("\n","").strip()
        detail_SCO_CeoKnow = detail_SCO_Tr[2].find_all('td')[4].get_text()\
                             .replace(" ","").replace("\n","").strip()
        detail_SCO_CeoLead = detail_SCO_Tr[3].find_all('td')[4].get_text()\
                             .replace(" ","").replace("\n","").strip()
        detail_SCO_CeoGroup = detail_SCO_Tr[4].find_all('td')[4].get_text()\
                              .replace(" ","").replace("\n","").strip()
        detail_SCO_Policy = detail_SCO_Tr[5].find_all('td')[4].get_text()\
                            .replace(" ","").replace("\n","").strip()
        detail_SCO_MarketGrow = detail_SCO_Tr[6].find_all('td')[4].get_text()\
                                .replace(" ","").replace("\n","").strip()
        detail_SCO_Product = detail_SCO_Tr[7].find_all('td')[4].get_text()\
                             .replace(" ","").replace("\n","").strip()
    else:
        detail_SCO_CeoAbility = '--'
        detail_SCO_CeoKnow = '--'
        detail_SCO_CeoLead = '--'
        detail_SCO_CeoGroup = '--'
        detail_SCO_Policy = '--'
        detail_SCO_MarketGrow = '--'
        detail_SCO_Product = '--'
    
    # 4. find the Market Info, then write into file
    detail_Market = html_PI.find('div',attrs={'class':'bmDl'}) 
    detail_Market_Dl = detail_Market.find_all('dl')
    if len(detail_Tittle) == 4:
        detail_Market_ProductTitle = detail_Market_Dl[0].find_all('dt')[0].get_text()
        detail_Market_ProductInfo = detail_Market_Dl[0].find_all('dd')[0].get_text()
        detail_Market_CustomerTitle = detail_Market_Dl[1].find_all('dt')[0].get_text()
        detail_Market_CustomerInfo = detail_Market_Dl[1].find_all('dd')[0].get_text()
        detail_Market_BusiModelTitle = detail_Market_Dl[2].find_all('dt')[0].get_text()
        detail_Market_BusiModelInfo = detail_Market_Dl[2].find_all('dd')[0].get_text()
        detail_Market_MarketGrowTitle = detail_Market_Dl[3].find_all('dt')[0].get_text()
        detail_Market_MarketGrowInfo = detail_Market_Dl[3].find_all('dd')[0].get_text()
        detail_Market_DriveTitle = detail_Market_Dl[4].find_all('dt')[0].get_text()
        detail_Market_DriveInfo = detail_Market_Dl[4].find_all('dd')[0].get_text()
        detail_Market_MarketComTitle = detail_Market_Dl[3].find_all('dt')[0].get_text()
        detail_Market_MarketComInfo = detail_Market_Dl[3].find_all('dd')[0].get_text()
        detail_Market_MarketStatusTitle = detail_Market_Dl[4].find_all('dt')[0].get_text()
        detail_Market_MarketStatusInfo = detail_Market_Dl[4].find_all('dd')[0].get_text()
        # 
    else: 
        detail_Market_ProductTitle = detail_Market_Dl[1].find_all('dt')[0].get_text()
        detail_Market_ProductInfo = detail_Market_Dl[1].find_all('dd')[0].get_text()
        detail_Market_CustomerTitle = detail_Market_Dl[2].find_all('dt')[0].get_text()
        detail_Market_CustomerInfo = detail_Market_Dl[2].find_all('dd')[0].get_text()
        detail_Market_BusiModelTitle = detail_Market_Dl[3].find_all('dt')[0].get_text()
        detail_Market_BusiModelInfo = detail_Market_Dl[3].find_all('dd')[0].get_text()
        detail_Market_MarketGrowTitle = detail_Market_Dl[4].find_all('dt')[0].get_text()
        detail_Market_MarketGrowInfo = detail_Market_Dl[4].find_all('dd')[0].get_text()
        detail_Market_DriveTitle = detail_Market_Dl[5].find_all('dt')[0].get_text()
        detail_Market_DriveInfo = detail_Market_Dl[5].find_all('dd')[0].get_text()
        detail_Market_MarketComTitle = detail_Market_Dl[6].find_all('dt')[0].get_text()
        detail_Market_MarketComInfo = detail_Market_Dl[6].find_all('dd')[0].get_text()
        detail_Market_MarketStatusTitle = detail_Market_Dl[7].find_all('dt')[0].get_text()
        detail_Market_MarketStatusInfo = detail_Market_Dl[7].find_all('dd')[0].get_text()
        # .1 write market info into file
    
    market_info_file = open(market_filePath,'a+',encoding='utf-8')
    try:
        market_info_file.write(str(progNum) + ' ' + detail_COM_Name + '\n' +
                               detail_COM_RegiDate + '\n' +
                               detail_COM_Field + '\n' + '\n' +
                               '1) ' + detail_Market_ProductTitle + '\n' +
                               detail_Market_ProductInfo + '\n' + '\n' +
                               '2) ' + detail_Market_CustomerTitle + '\n' +
                               detail_Market_CustomerInfo + '\n' + '\n' +
                               '3) ' + detail_Market_BusiModelTitle + '\n' +
                               detail_Market_BusiModelInfo + '\n' + '\n' +
                               '4) ' + detail_Market_MarketGrowTitle + '\n' +
                               detail_Market_MarketGrowInfo + '\n' + '\n' +
                               '5) ' + detail_Market_DriveTitle + '\n' +
                               detail_Market_DriveInfo + '\n' + '\n' +
                               '6) ' + detail_Market_MarketComTitle + '\n' +
                               detail_Market_MarketComInfo + '\n' + '\n' +
                               '7) '+ detail_Market_MarketStatusTitle + '\n' +
                               detail_Market_MarketStatusInfo + '\n' + '\n' )
        market_info_file.close()
        print (str(progNum) + detail_COM_Name + " market info has been writed into file")
    except:
        market_info_file.write('Info of this program has some format Error, please check it')
        market_info_file.close()
        print (str(progNum) + detail_COM_Name + " market info has some format Error")
        
    
    # 5. find the pdf, if exists, then download
    prog_pdf = html_PI.find('div',attrs={'class':'fujianBox fujianBox2'})
    exist_pdf = prog_pdf.find_all('a')
    #print(exist_pdf)
    
    if len(exist_pdf) != 0:
        pdf_rawUrl = prog_pdf.a['href']
        #print (pdf_rawUrl)
        pdf_URL = rootUrl + pdf_rawUrl
    else:
        pdf_URL = ''

    # 6. return a progInfo_List
    progInfo_List = [detail_CEO_Gender, detail_CEO_BirthDate, detail_CEO_MaxEdu,
                     detail_CEO_University, detail_CEO_Addr, 
                     detail_COM_RegiDate, detail_COM_Field,
                     detail_SCO_CeoAbility, detail_SCO_CeoKnow, detail_SCO_CeoLead,
                     detail_SCO_CeoGroup, detail_SCO_Policy,
                     detail_SCO_MarketGrow, detail_SCO_Product,
                     pdf_URL]
    return progInfo_List

def getProgPDF(pdfUrl,fileNum, fileName,pdfFormat):
    pdf_path = './/PDF//'+ fileName + pdfFormat
    try:
        f_pdf = open(pdf_path,'wb').write(urllib.request.urlopen(pdfUrl).read())
        print (fileName + " has been downloaded to your PDF dir")
    except:
        fileName = str(fileNum) +  "&Not_A_Normal_Name_Change_It_By_Yourself"
        pdf_path = './/PDF//'+fileName + pdfFormat
        f_pdf =  open(pdf_path,'wb').write(urllib.request.urlopen(pdfUrl).read())
        print("Warning: " + fileName +": file name is not applicable,please download it by yourself")
        
    #pdf = requests.get(pdfUrl)
    #file = dirPath  + fileName + '.pdf'
    #print
    #f = open(file,'wb')
    #f.write(pdf.content)
    #f.close()
    

def getProgNP(reviewUrl):
    page_html = urllib.request.Request(reviewUrl)
    page_resp = urllib.request.urlopen(page_html)
    page_soup = BeautifulSoup(page_resp.read(),'html.parser')
    #print (page_soup)
    page_div = page_soup.find('div',attrs={'class':'page'})
    page_div_txt = page_div.text
    page_div_re = re.compile("\d+.?<")
    page_div_re_part = page_div_re.findall(page_div_txt)
    page_num_re = re.compile("\d+")
    prog_num_list = page_num_re.findall(page_div_re_part[0])
    prog_num_max = int(prog_num_list[0])
    page_num_max = math.ceil(int(prog_num_max)/15)
    progNP = [prog_num_max, page_num_max]
    #print (progNP)
    return progNP
# -------------------------------------------------------------
# Main function
# -------------------------------------------------------------

#if os.path.exists('F:\PyWork\xxx') == False:
#    os.mkdir('F:\PyWork\xxx');
# if program market info doc does not exists, then create it

login_url = 'http://xxx.org/account/review_login'
rootUrl = 'http://xxx.org'
review_url = 'http://xxx.org/review'
dirPDF_Path = './/PDF//'

# Set-Up auto Reco image code and login
imgUrl = 'http://pkucy.org/account/getCode'
img_save_path = './CodeImage/img_ID.png'
if os.path.exists('./CodeImage') == False:
    os.mkdir('./CodeImage')
    # .1 input the username and password for website pkucy.org/review
username = input('please enter the username, then press enter:')
password = input('please enter the password, then press enter:')
    # .2 Set up Cookie
cj = cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))  
opener.addheaders = [('User-agent','Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)')]  
urllib.request.install_opener(opener)
    # .3 retrieve the image code and recognise the image code
f = open(img_save_path,'wb').write(urllib.request.urlopen(imgUrl).read())
#img = urllib.request.urlretrieve(imgUrl,'/Users/apple/Documents/python/imageIdentify/imageID.png')
#imgID = Image.open(img_save_path)
#imgTxt = image_to_string(imgID).encode('utf-8')
imgTxt = input('please check the image code and enter, then press the enter: ')
#print (imgTxt)
    # .4 form data and login
user_data = {"email":username,"password":password,"code":imgTxt,"x":"0","y":"0"}
user_data_encode = urllib.parse.urlencode(user_data).encode(encoding='utf-8')
#print (user_data_encode)
login_req = urllib.request.Request(login_url, user_data_encode)  
login_resp = urllib.request.urlopen(login_req)  
#print (resp.read().decode('utf-8'))

# get ProgNum and PageNum
# page_html = urllib.request.Request(review_url)
# page_resp = urllib.request.urlopen(page_html)
page_soup = BeautifulSoup(login_resp.read(),'html.parser')
# print (page_soup)
[progMax, pageMax] = getProgNP(review_url)
print ("The number of programs are: " + str(progMax))

progNum = 0
progDict = {}

if os.path.exists('./PDF') == False:
    os.mkdir('./PDF')
market_file_path = './Program_Market_Info.doc'
# if market file exists, then clean
if os.path.exists(market_file_path) ==True:
    f = open(market_file_path,'wb')
    f.truncate()
    f.close()
f = open('./pkucy_InfoList.txt','w');

for pageNum in range(1, pageMax+1):

    pageUrl = review_url + '?page=' + str(pageNum)

    get_req = urllib.request.Request(pageUrl)
    get_resp = urllib.request.urlopen(get_req)
    #print (get_resp.read())

    html = BeautifulSoup(get_resp.read(), 'html.parser')

    #print (html)

    programInfo = html.find('div',attrs={'class':'listTable'})

    #print (programInfo)

    progLine = programInfo.find_all('tr')
    

    for progTr in progLine:
        progTd = progTr.find_all('td')
        
        if len(progTd) >1:
            progNum = progNum + 1
            print ('----***----')
            print (str(progNum) + "is downloading: ")
            rawProgUrl = progTd[0].a['href']
            progURL = rootUrl + rawProgUrl

            # get program general info
            progDict['progHref'] = progURL
            progDict['progNum'] = str(progNum)
            progDict['progName'] = progTd[0].get_text()
            progDict['progCEO'] = progTd[1].get_text()
            progDict['progDate'] = str(progTd[2].get_text())
            progDict['progScore'] = str(progTd[3].get_text())
            progDict['progState'] = progTd[4].get_text()
        
            # get program detail info
            # .1 if review finished, set status 1
            if progDict['progScore'] == '--':
                reviewState = 0
            else:
                reviewState = 1
            # .2 get progCEO and Company Info
            
            progInfo = getProgInfo(progNum, progURL, reviewState, market_file_path)
            progDict['progCEO_Gender'] = progInfo[0]
            progDict['progCEO_BirthDate'] = progInfo[1]
            progDict['progCEO_MaxEdu'] = progInfo[2]
            progDict['progCEO_University'] = progInfo[3]
            progDict['progCEO_Addr'] = progInfo[4]
            progDict['progCOM_RegiDate']= progInfo[5]
            progDict['progCOM_Field'] = progInfo[6]
            progDict['progSCO_CeoAbility']= progInfo[7]
            progDict['progSCO_CeoKnow'] = progInfo[8]
            progDict['progSCO_CeoLead']= progInfo[9]
            progDict['progSCO_CeoGroup']= progInfo[10]
            progDict['progSCO_Policy']= progInfo[11]
            progDict['progSCO_MarketGrow']= progInfo[12]
            progDict['progSCO_Product']= progInfo[13]

            # print process state
            
            #print (progDict['progHref'])
            
            # write info into text
            f.write(progDict['progNum'] + ';' + progDict['progName'] + ';' +
                    progDict['progScore'] + ';' + progDict['progCEO'] + ';' +
                    progDict['progCEO_Gender'] + ';' +
                    progDict['progCEO_BirthDate'] + ';' + progDict['progCEO_MaxEdu'] + ';' +
                    progDict['progCEO_University'] + ';' + progDict['progCEO_Addr'] + ';' +
                    progDict['progCOM_RegiDate'] + ';' + progDict['progCOM_Field'] + ';' +
                    progDict['progSCO_CeoAbility'] + ';' + progDict['progSCO_CeoKnow'] + ';' +
                    progDict['progSCO_CeoLead'] + ';' + progDict['progSCO_CeoGroup'] + ';' +
                    progDict['progSCO_Policy'] + ';' + progDict['progSCO_MarketGrow'] + ';' +
                    progDict['progSCO_Product'] + ';' + 
                    progDict['progHref'] + '\n')
            #if progNum == 116:
                #continue

            # download PDF if exists
            pdf_Url = progInfo[14]
            pdfName = progDict['progNum'] + '&' + progDict['progName']
            
            if pdf_Url !='':
                pdf_format_re = re.compile('\.[A-Za-z]+[A-Za-z]$')
                pdf_format = pdf_format_re.findall(pdf_Url)[0]
                if os.path.exists(dirPDF_Path +  pdfName + pdf_format):
                    print(pdfName + " has already exists")
                    
                else:
                    getProgPDF(pdf_Url,progNum, pdfName,pdf_format)
            else:
                print(pdfName + " does not have pdf file")
            

print ("Scraw Finished");
f.close()
            

    
