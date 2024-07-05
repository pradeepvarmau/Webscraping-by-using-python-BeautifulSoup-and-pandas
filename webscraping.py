#WEBSCRAPING IN PYTHON USING FLIPKART WEBSITE
#import section
import requests
import pandas
from bs4 import BeautifulSoup
response=requests.get("https://www.flipkart.com/search?q=iphone+13&sid=tyy%2C4io&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_3_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_3_na_na_na&as-pos=1&as-type=RECENT&suggestionId=iphone+13%7CMobiles&requestId=dc4bfcff-051b-479f-81c5-c53672f43f6f&as-searchtext=iph")

#print(response)

soup=BeautifulSoup(response.content,"html.parser")
#print(soup)
#NAMES
names=soup.find_all("div",class_="_KzDlHZ")
name=[]
for i in names[0:5]:
    d=i.get_text()
    name.append(d)
print(name)
#PRICES
prices=soup.find_all("div",class_="_KzDlHZ")
price=[]
for i in prices[0:5]:
    d=i.get_text()
    price.append(d)
#print(price)
#RATING
ratings=soup.find_all("div",class_="_KzDlHZ")
rate=[]
for i in ratings[0:5]:
    d=i.get_text()
    rate.append(float(d))
#print(rate)
#REVIEWS
reviews=soup.find_all("li",class_="_KzDlHZ")
review=[]
for i in reviews[0:5]:
    d=i.get_text()
    review.append(d)
#print(review)
#features
features=soup.find_all("li",class_="_KzDlHZ")
feature=[]
for i in features[0:5]:
    d=i.get_text()
    feature.append(d)
#print(feature)
#LINKS
links=soup.find_all("a",class_="_KzDlHZ")
link=[]
for i in links[0:5]:
    d="https://www.flipkart.com/"+i["href"]
    link.append(d)
#print(link)
#IMAGES
images=soup.find_all("img",class_="_KzDlHZ")
image=[]
for i in images[0:5]:
    d=i["src"]
    #d=i.div.img["src"]
    image.append(d)
#print(image)
            #PANDAS
df=pandas.DataFrame()#dataframe consists of rows and columns
#print(df)
data={'names':name, #if getting error "names":pandas.series(names)
      "prices":price,
      "ratings":rate,
      "reviews":review,
      "features":feature,
      "links":link,
      "images":image
      }
#print(data)
df=pandas.DataFrame(data)
#print(df)
df.to_csv("mobiles_data.csv")
    
    
