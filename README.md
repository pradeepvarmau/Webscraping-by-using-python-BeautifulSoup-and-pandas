# Web Scraping with Beautiful Soup and Pandas



Web scraping is the process of using bots to extract content and data from a website.

Unlike screen scraping, which only copies pixels displayed onscreen, web scraping extracts underlying HTML code and, with it, data stored in a database. The scraper can then replicate entire website content elsewhere.

Web scraping is used in a variety of digital businesses that rely on data harvesting. Legitimate use cases include:

- Search engine bots crawling a site, analyzing its content and then ranking it.
- Price comparison sites deploying bots to auto-fetch prices and product descriptions for allied seller websites.
- Market research companies using scrapers to pull data from forums and social media (e.g., for sentiment analysis).

## Table of Contents
[1. Making Database From Scratch With Beautiful Soup](#I.-Making-Database-From-Scratch-With-Beautiful-Soup) <br>
- [Scrape The Data](#Scrape-The-Data) 
- [Make A Database](#Make-A-Database)

[2. Web Scraping Using Pandas](#II.-Web-Scraping-Using-Pandas) <br>
- [Get The URL](#Get-The-URL) 
- [Read The HTML Webpage Into Pandas](#Read-The-HTML-Webpage-Into-Pandas)
- [Data Cleaning](#Data-Cleaning) 
- [Quick Exploratory Data Analysis](#Quick-Exploratory-Data-Analysis)<br>


## I. Making Database From Scratch With Beautiful Soup

There are a number of different packages available for web scraping, and one of the most popular is [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/). Beautiful Soup parses web content into a Python object and makes the [DOM](https://en.wikipedia.org/wiki/Document_Object_Model) queryable element by element. Used in conjunction with a requests package, it makes web scraping very easy!

---
### Installation of Beautiful Soup (if haven't done so)
In the `bash` terminal or `Anaconda Prompt`,run:
```bash
conda install beautifulsoup4
```
---


```python
# Standard imports
import pandas as pd

# For web scraping
import requests
import urllib.request
from bs4 import BeautifulSoup

# For performing regex operations
import re

# Data visualization
import seaborn as sns
import matplotlib.pyplot as plt

```

For this tutorial, we'll be scraping the **random functions names and usages** from Python documentation from the website [docs.python.org](https://docs.python.org/).

### Scrape The Data



```python
# Save the URL of the webpage we want to scrape to a variable
url = 'https://docs.python.org/3/library/random.html#module-random'
```

When web scraping, the first step is to pull down the content of the page into a Python (string) variable. For simpler webscraping tasks you can do this with the `requests` package, which is what we'll use here. For more complex tasks (involving, e.g., webpages with lots of Javascript or other elements that are rendered by the web browser) you may need to use something more advanced, like `urllib` or [Selenium](https://selenium-python.readthedocs.io/index.html).


```python
# Send a get request and assign the response to a variable
response = requests.get(url)
```

Let's take a look at what we have!


```python
response
```




    <Response [200]>




```python
response.content
```




<<<<<<< HEAD
    b'\n<!DOCTYPE html>\n\n<html xmlns="http://www.w3.org/1999/xhtml">\n  <head>\n    <meta charset="utf-8" />\n    <title>random \xe2\x80\x94 Generate pseudo-random numbers &#8212; Python 3.9.2 documentation</title>\n    <link rel="stylesheet" href="../_static/pydoctheme.css" type="text/css" />\n    <link rel="stylesheet" href="../_static/pygments.css" type="text/css" />\n    \n    <script id="documentation_options" data-url_root="../" src="../_static/documentation_options.js"></script>\n    <script src="../_static/jquery.js"></script>\n    <script src="../_static/underscore.js"></script>\n    <script src="../_static/doctools.js"></script>\n    <script src="../_static/language_data.js"></script>\n    \n    <script src="../_static/sidebar.js"></script>\n    \n    <link rel="search" type="application/opensearchdescription+xml"\n          title="Search within Python 3.9.2 documentation"\n          href="../_static/opensearch.xml"/>\n    <link rel="author" title="About these documents" href="../about.html" />\n    <link rel="index" title="Index" href="../genindex.html" />\n    <link rel="search" title="Search" href="../search.html" />\n    <link rel="copyright" title="Copyright" href="../copyright.html" />\n    <link rel="next" title="statistics \xe2\x80\x94 Mathematical statistics functions" href="statistics.html" />\n    <link rel="prev" title="fractions \xe2\x80\x94 Rational numbers" href="fractions.html" />\n    <link rel="canonical" href="https://docs.python.org/3/library/random.html" />\n    \n      \n      \n    \n\n    \n    <style>\n      @media only screen {\n        table.full-width-table {\n            width: 100%;\n        }\n      }\n    </style>\n\n    <link rel="shortcut icon" type="image/png" href="../_static/py.png" />\n    \n    <script 




That's a lot to look at! It's also pretty unreadable. This is where Beautiful Soup comes in. What Beautiful Soup does is helps us parse the page content properly, into a form that we can more easily use.


```python
# Turn the undecoded content into a Beautiful Soup object and assign it to a variable
soup = BeautifulSoup(response.content)
type(soup)
```




    bs4.BeautifulSoup



**Now let's take a look at this.**


```python
# Check soup variable

soup
```




    <!DOCTYPE html>
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head>
    <meta charset="utf-8"/>
    <title>random — Generate pseudo-random numbers — Python 3.9.2 documentation</title>
    <link href="../_static/pydoctheme.css" rel="stylesheet" type="text/css"/>
    <link href="../_static/pygments.css" rel="stylesheet" type="text/css"/>
    <script data-url_root="../" id="documentation_options" src="../_static/documentation_options.js"></script>
    <script src="../_static/jquery.js"></script>



```python
# Other way to load the html code using 'urllib.request.urlopen()'

#url = urllib.request.urlopen("https://docs.python.org/3/library/random.html#module-random")
#soup = BeautifulSoup(url)
#soup
```

    
**Still very long, but a little easier to take in.**

The real advantage of Beautiful Soup, however, is that it *parses* our webpage according to its structure and allows us to *search for* and *extract* elements within it. This is because it transforms the webpage from a string into a special Beautiful Soup object.

To extract HTML elements from our webpage, we can call the `.find()` method on our Beautiful Soup object. This method finds the first element that matches the criterion that we pass in. The criterion may be an element `id`, `class`, tag `name`, or even a function. (For a full list of search elements, see [this page](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#searching-the-tree).)

But how do we know what element to search for? This is where your browser's `Inspect` or `Inspect Element` feature comes in handy. Simply right click on an object of interest on the web page and click `Inspect` on Chrome or `Inspect Element` on Firefox. This will then show you the corresponding place in the HTML code where the element appears. From there you should be able to find an id or class name that will allow you to locate the element with Beautiful Soup.

**In this case, we want to target the tag/ element `dt` as below picture:**

<br>
<br>
<img src = "https://docs.google.com/uc?export=download&id=1Mj9K4QnhS5mFMK4Ddx_6OHFUIN-xpR9X" />

<br>
<br>

**So it looks like we're looking for a `dt` element with `id='random.___'`. We can easily retrieve this with Beautiful Soup's `.findAll` command.**


```python
# Find all function names - we specify the name of the element in this case is 'dt'

names = soup.body.findAll('dt')

print(names)
```

    [<dt id="random.seed">
    <code class="sig-prename descclassname">random.</code><code class="sig-name descname">seed</code><span class="sig-paren">(</span><em class="sig-param">a=None</em>, <em class="sig-param">version=2</em><span class="sig-paren">)</span><a class="headerlink" href="#random.seed" title="Permalink to this definition">¶</a></dt>, <dt id="random.getstate">
    <code class="sig-prename descclassname">random.</code><code class="sig-name descname">getstate</code><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#random.getstate" title="Permalink to this definition">¶</a></dt>, <dt id="random.setstate">
    <code class="sig-prename descclassname">random.</code><code class="sig-name descname">setstate</code><span class="sig-paren">(</span><em class="sig-param">state</em><span class="sig-paren">)</span><a class="headerlink" href="#random.setstate" title="Permalink to this definition">¶</a></dt>, <dt id="random.randbytes">


**There are still some works to do! This is when regex kicks in.**



```python
# Find all the information we're looking for with regex
# In this case, it would be every string at starts with id='random.'

function_names = re.findall('id="random.\w+' , str(names)) # '\w+' which means the string should end with the function name

# Let print the results
print(function_names)
```

    ['id="random.seed', 'id="random.getstate', 'id="random.setstate', 'id="random.randbytes', 'id="random.randrange', 'id="random.randint', 'id="random.getrandbits', 'id="random.choice', 'id="random.choices', 'id="random.shuffle', 'id="random.sample', 'id="random.random', 'id="random.uniform', 'id="random.triangular', 'id="random.betavariate', 'id="random.expovariate', 'id="random.gammavariate', 'id="random.gauss', 'id="random.lognormvariate', 'id="random.normalvariate', 'id="random.vonmisesvariate', 'id="random.paretovariate', 'id="random.weibullvariate', 'id="random.Random', 'id="random.SystemRandom']


**We are almost there! We just need to remove the first few characters from each string.**


```python
# Using list comprehension to edit our values:

function_names = [item[4:] for item in function_names]

# Let print the results
print(function_names)
```

    ['random.seed', 'random.getstate', 'random.setstate', 'random.randbytes', 'random.randrange', 'random.randint', 'random.getrandbits', 'random.choice', 'random.choices', 'random.shuffle', 'random.sample', 'random.random', 'random.uniform', 'random.triangular', 'random.betavariate', 'random.expovariate', 'random.gammavariate', 'random.gauss', 'random.lognormvariate', 'random.normalvariate', 'random.vonmisesvariate', 'random.paretovariate', 'random.weibullvariate', 'random.Random', 'random.SystemRandom']


**Perfect! Now we need to do the same with the function description.
We have to target the description details with tag - `dd`**

<br>


<img src = "https://docs.google.com/uc?export=download&id=169-W93jfnmbwHejyP4QV4sDQm9LgriwB" />

<br>
<br>


```python
# Find all the function description

description = soup.body.findAll('dd')

#print(description)
```

**Wow it looks very complicated! There are lots of tags here (`<em>` tags). These unnecessary elements from the above method would take a long time to get rid of manually.**
    
Luckily, BeautifulSoup is not only beautiful, it's also smart. Let's look at the `.text` method:


```python
# Create a list

function_usage = []

# Create a loop

for item in description:
    item = item.text      #  Save the extracted text to a variable
    item = item.replace('\n', ' ')     # to get rid of the next line operator which is `\n` 
    function_usage.append(item)
    
#print(function_usage)  # Don't get overwhelmed! they are just all the function description from the above function names
```


```python
# Let's check the length of the function_names and function_usage

print(f' Length of function_names: {len(function_names)}')
print(f' Length of function_usage: {len(function_usage)}')
```

     Length of function_names: 25
     Length of function_usage: 25


### Make A Database


```python
# Create a dataframe since the length of both variables are equal!

data = pd.DataFrame( {  'function name': function_names, 
                      'function usage' : function_usage  } )

data
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
    
    
    ........
    
    
      <th>21</th>
      <td>random.paretovariate</td>
      <td>Pareto distribution.  alpha is the shape param...</td>
    </tr>
    <tr>
      <th>22</th>
      <td>random.weibullvariate</td>
      <td>Weibull distribution.  alpha is the scale para...</td>
    </tr>
    <tr>
      <th>23</th>
      <td>random.Random</td>
      <td>Class that implements the default pseudo-rando...</td>

</div>



```python
# Let make a CSV file from the dataframe

data.to_csv('random_function.csv')
```

**BONUS: if you want to target a specific attributes, for example `id="bookeeping-functions"` you can use the following code:**


```python
# Target specific attributes

#example = soup.body.findAll ('div', attrs = {'id' : 'bookeeping-functions'})
#print(example)    # you can get very specific result with BeautifulSoup
```

## II. Web Scraping Using Pandas 

Pandas is very useful! We can easily scrape data using the pandas `read_html()` function for your data science project. 

We will be web scraping NBA player stats data and perform a quick data exploration from the website [basketball-reference.com](https://www.basketball-reference.com).

### Get The URL

First, we want to check out the specific [URL](https://www.basketball-reference.com/leagues/NBA_2020_per_game.html) that we are going to scrape the data - the NBA Player Stats of season 2019-2020.




```python
# Method 1: only 1 year

# URL of the player stats in 2020

url = 'https://www.basketball-reference.com/leagues/NBA_2020_per_game.html'
url
```




    'https://www.basketball-reference.com/leagues/NBA_2020_per_game.html'




```python
# Method 2: multiple years

years = ['2016', '2017', '2018', '2019', '2020']
str = 'https://www.basketball-reference.com/leagues/NBA_{}_per_game.html'

for year in years:
    url = str.format(year)
    print(url)
```

    https://www.basketball-reference.com/leagues/NBA_2016_per_game.html
    https://www.basketball-reference.com/leagues/NBA_2017_per_game.html
    https://www.basketball-reference.com/leagues/NBA_2018_per_game.html
    https://www.basketball-reference.com/leagues/NBA_2019_per_game.html
    https://www.basketball-reference.com/leagues/NBA_2020_per_game.html


### Read The HTML Webpage Into Pandas


```python
# Let check URL of the player stats in 2020

url = 'https://www.basketball-reference.com/leagues/NBA_2020_per_game.html'

# Using pd.read_html()

df = pd.read_html(url, header = 0)

print(df)
```

    [      Rk                    Player Pos Age   Tm   G  GS    MP   FG   FGA  ...  \
    0      1              Steven Adams   C  26  OKC  63  63  26.7  4.5   7.6  ...   
    1      2               Bam Adebayo  PF  22  MIA  72  72  33.6  6.1  11.0  ...   
    2      3         LaMarcus Aldridge   C  34  SAS  53  53  33.1  7.4  15.0  ...   
    3      4            Kyle Alexander   C  23  MIA   2   0   6.5  0.5   1.0  ...   
    4      5  Nickeil Alexander-Walker  SG  21  NOP  47   1  12.6  2.1   5.7  ...   
    ..   ...                       ...  ..  ..  ...  ..  ..   ...  ...   ...  ...   
    672  525                Trae Young  PG  21  ATL  60  60  35.3  9.1  20.8  ...   
    673  526               Cody Zeller   C  27  CHO  58  39  23.1  4.3   8.3  ...   
    674  527              Tyler Zeller   C  30  SAS   2   0   2.0  0.5   2.0  ...   
    675  528                Ante Žižić   C  23  CLE  22   0  10.0  1.9   3.3  ...   
    676  529               Ivica Zubac   C  22  LAC  72  70  18.4  3.3   5.3  ...   
    
          FT%  ORB  DRB   TRB  AST  STL  BLK  TOV   PF   PTS  
    0    .582  3.3  6.0   9.3  2.3  0.8  1.1  1.5  1.9  10.9  
    1    .691  2.4  7.8  10.2  5.1  1.1  1.3  2.8  2.5  15.9  
    2    .827  1.9  5.5   7.4  2.4  0.7  1.6  1.4  2.4  18.9  
    3     NaN  1.0  0.5   1.5  0.0  0.0  0.0  0.5  0.5   1.0  
    4    .676  0.2  1.6   1.8  1.9  0.4  0.2  1.1  1.2   5.7  
    ..    ...  ...  ...   ...  ...  ...  ...  ...  ...   ...  
    672  .860  0.5  3.7   4.3  9.3  1.1  0.1  4.8  1.7  29.6  
    673  .682  2.8  4.3   7.1  1.5  0.7  0.4  1.3  2.4  11.1  
    674   NaN  1.5  0.5   2.0  0.0  0.0  0.0  0.0  0.0   1.0  
    675  .737  0.8  2.2   3.0  0.3  0.3  0.2  0.5  1.2   4.4  
    676  .747  2.7  4.8   7.5  1.1  0.2  0.9  0.8  2.3   8.3  
    
    [677 rows x 30 columns]]


**It looks a little bit messy. What we actually have here is a list of DataFrames. We can beautify this object using Pandas (without any additional libraries!)**


```python
# Check number of DataFrames in this list

print(f'number of tables in df: {len(df)}') 

print('================')

# Since there is only 1, pull out the 0th element:
df[0].head(20)
```

    number of tables in df: 1
    ================





<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Rk</th>
      <th>Player</th>
      <th>Pos</th>
      <th>Age</th>
      <th>Tm</th>
      <th>G</th>
      <th>GS</th>
      <th>MP</th>
      <th>FG</th>
      <th>FGA</th>
      <th>...</th>
      <th>FT%</th>
      <th>ORB</th>
      <th>DRB</th>
      <th>TRB</th>
      <th>AST</th>
      <th>STL</th>
      <th>BLK</th>
      <th>TOV</th>
      <th>PF</th>
      <th>PTS</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>Steven Adams</td>
      <td>C</td>
      <td>26</td>
      <td>OKC</td>
      <td>63</td>
      <td>63</td>
      <td>26.7</td>
      <td>4.5</td>
      <td>7.6</td>
      <td>...</td>
      <td>.582</td>
      <td>3.3</td>
      <td>6.0</td>
      <td>9.3</td>
      <td>2.3</td>
      <td>0.8</td>
      <td>1.1</td>
      <td>1.5</td>
      <td>1.9</td>
      <td>10.9</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>Bam Adebayo</td>
      <td>PF</td>
      <td>22</td>
      <td>MIA</td>
      <td>72</td>
      <td>72</td>
      <td>33.6</td>
      <td>6.1</td>
      <td>11.0</td>
      <td>...</td>
      <td>.691</td>
      <td>2.4</td>
      <td>7.8</td>
      <td>10.2</td>
      <td>5.1</td>
      <td>1.1</td>
      <td>1.3</td>
      <td>2.8</td>
      <td>2.5</td>
      <td>15.9</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>LaMarcus Aldridge</td>
      <td>C</td>
      <td>34</td>
      <td>SAS</td>
      <td>53</td>
      <td>53</td>
      <td>33.1</td>
      <td>7.4</td>
      <td>15.0</td>
      <td>...</td>
      <td>.827</td>
      <td>1.9</td>
      <td>5.5</td>
      <td>7.4</td>
      <td>2.4</td>
      <td>0.7</td>
      <td>1.6</td>
      <td>1.4</td>
      <td>2.4</td>
      <td>18.9</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>Kyle Alexander</td>
      <td>C</td>
      <td>23</td>
      <td>MIA</td>
      <td>2</td>
      <td>0</td>
      <td>6.5</td>
      <td>0.5</td>
      <td>1.0</td>
      <td>...</td>
      <td>NaN</td>
      <td>1.0</td>
      <td>0.5</td>
      <td>1.5</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.5</td>
      <td>0.5</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>Nickeil Alexander-Walker</td>
      <td>SG</td>
      <td>21</td>
      <td>NOP</td>
      <td>47</td>
      <td>1</td>
      <td>12.6</td>
      <td>2.1</td>
      <td>5.7</td>
      <td>...</td>
      <td>.676</td>
      <td>0.2</td>
      <td>1.6</td>
      <td>1.8</td>
      <td>1.9</td>
      <td>0.4</td>
      <td>0.2</td>
      <td>1.1</td>
      <td>1.2</td>
      <td>5.7</td>
    </tr>
    <tr>
      <th>5</th>
      <td>6</td>
      <td>Grayson Allen</td>
      <td>SG</td>
      <td>24</td>
      <td>MEM</td>
      <td>38</td>
      <td>0</td>
      <td>18.9</td>
      <td>3.1</td>
      <td>6.6</td>
      <td>...</td>
      <td>.867</td>
      <td>0.2</td>
      <td>2.0</td>
      <td>2.2</td>
      <td>1.4</td>
      <td>0.3</td>
      <td>0.1</td>
      <td>0.9</td>
      <td>1.4</td>
      <td>8.7</td>
    </tr>
    <tr>
      <th>6</th>
      <td>7</td>
      <td>Jarrett Allen</td>
      <td>C</td>
      <td>21</td>
      <td>BRK</td>
      <td>70</td>
      <td>64</td>
      <td>26.5</td>
      <td>4.3</td>
      <td>6.6</td>
      <td>...</td>
      <td>.633</td>
      <td>3.1</td>
      <td>6.5</td>
      <td>9.6</td>
      <td>1.6</td>
      <td>0.6</td>
      <td>1.3</td>
      <td>1.1</td>
      <td>2.3</td>
      <td>11.1</td>
    </tr>
    <tr>
      <th>7</th>
      <td>8</td>
      <td>Kadeem Allen</td>
      <td>PG</td>
      <td>27</td>
      <td>NYK</td>
      <td>10</td>
      <td>0</td>
      <td>11.7</td>
      <td>1.9</td>
      <td>4.4</td>
      <td>...</td>
      <td>.636</td>
      <td>0.2</td>
      <td>0.7</td>
      <td>0.9</td>
      <td>2.1</td>
      <td>0.5</td>
      <td>0.2</td>
      <td>0.8</td>
      <td>0.7</td>
      <td>5.0</td>
    </tr>
    <tr>
      <th>8</th>
      <td>9</td>
      <td>Al-Farouq Aminu</td>
      <td>PF</td>
      <td>29</td>
      <td>ORL</td>
      <td>18</td>
      <td>2</td>
      <td>21.1</td>
      <td>1.4</td>
      <td>4.8</td>
      <td>...</td>
      <td>.655</td>
      <td>1.3</td>
      <td>3.5</td>
      <td>4.8</td>
      <td>1.2</td>
      <td>1.0</td>
      <td>0.4</td>
      <td>0.9</td>
      <td>1.5</td>
      <td>4.3</td>
    </tr>
    <tr>
      <th>9</th>
      <td>10</td>
      <td>Justin Anderson</td>
      <td>SG</td>
      <td>26</td>
      <td>BRK</td>
      <td>10</td>
      <td>1</td>
      <td>10.7</td>
      <td>1.0</td>
      <td>3.8</td>
      <td>...</td>
      <td>.500</td>
      <td>0.1</td>
      <td>2.0</td>
      <td>2.1</td>
      <td>0.8</td>
      <td>0.0</td>
      <td>0.6</td>
      <td>0.4</td>
      <td>1.3</td>
      <td>2.8</td>
    </tr>
    <tr>
      <th>10</th>
      <td>11</td>
      <td>Kyle Anderson</td>
      <td>SF</td>
      <td>26</td>
      <td>MEM</td>
      <td>67</td>
      <td>28</td>
      <td>19.9</td>
      <td>2.3</td>
      <td>4.9</td>
      <td>...</td>
      <td>.667</td>
      <td>0.9</td>
      <td>3.4</td>
      <td>4.3</td>
      <td>2.4</td>
      <td>0.8</td>
      <td>0.6</td>
      <td>1.0</td>
      <td>1.7</td>
      <td>5.8</td>
    </tr>
    <tr>
      <th>11</th>
      <td>12</td>
      <td>Ryan Anderson</td>
      <td>C</td>
      <td>31</td>
      <td>HOU</td>
      <td>2</td>
      <td>0</td>
      <td>7.0</td>
      <td>1.0</td>
      <td>3.5</td>
      <td>...</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>3.5</td>
      <td>3.5</td>
      <td>1.0</td>
      <td>0.5</td>
      <td>0.0</td>
      <td>0.5</td>
      <td>0.5</td>
      <td>2.5</td>
    </tr>
    <tr>
      <th>12</th>
      <td>13</td>
      <td>Giannis Antetokounmpo</td>
      <td>PF</td>
      <td>25</td>
      <td>MIL</td>
      <td>63</td>
      <td>63</td>
      <td>30.4</td>
      <td>10.9</td>
      <td>19.7</td>
      <td>...</td>
      <td>.633</td>
      <td>2.2</td>
      <td>11.4</td>
      <td>13.6</td>
      <td>5.6</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>3.7</td>
      <td>3.1</td>
      <td>29.5</td>
    </tr>
    <tr>
      <th>13</th>
      <td>14</td>
      <td>Kostas Antetokounmpo</td>
      <td>PF</td>
      <td>22</td>
      <td>LAL</td>
      <td>5</td>
      <td>0</td>
      <td>4.0</td>
      <td>0.6</td>
      <td>0.6</td>
      <td>...</td>
      <td>.500</td>
      <td>0.4</td>
      <td>0.2</td>
      <td>0.6</td>
      <td>0.4</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.2</td>
      <td>0.4</td>
      <td>1.4</td>
    </tr>
    <tr>
      <th>14</th>
      <td>15</td>
      <td>Thanasis Antetokounmpo</td>
      <td>SF</td>
      <td>27</td>
      <td>MIL</td>
      <td>20</td>
      <td>2</td>
      <td>6.5</td>
      <td>1.2</td>
      <td>2.4</td>
      <td>...</td>
      <td>.412</td>
      <td>0.6</td>
      <td>0.6</td>
      <td>1.2</td>
      <td>0.8</td>
      <td>0.4</td>
      <td>0.1</td>
      <td>0.6</td>
      <td>0.9</td>
      <td>2.8</td>
    </tr>
    <tr>
      <th>15</th>
      <td>16</td>
      <td>Carmelo Anthony</td>
      <td>PF</td>
      <td>35</td>
      <td>POR</td>
      <td>58</td>
      <td>58</td>
      <td>32.8</td>
      <td>5.8</td>
      <td>13.5</td>
      <td>...</td>
      <td>.845</td>
      <td>1.2</td>
      <td>5.1</td>
      <td>6.3</td>
      <td>1.5</td>
      <td>0.8</td>
      <td>0.5</td>
      <td>1.7</td>
      <td>2.9</td>
      <td>15.4</td>
    </tr>
    <tr>
      <th>16</th>
      <td>17</td>
      <td>OG Anunoby</td>
      <td>SF</td>
      <td>22</td>
      <td>TOR</td>
      <td>69</td>
      <td>68</td>
      <td>29.9</td>
      <td>4.1</td>
      <td>8.2</td>
      <td>...</td>
      <td>.706</td>
      <td>1.2</td>
      <td>4.1</td>
      <td>5.3</td>
      <td>1.6</td>
      <td>1.4</td>
      <td>0.7</td>
      <td>1.1</td>
      <td>2.4</td>
      <td>10.6</td>
    </tr>
    <tr>
      <th>17</th>
      <td>18</td>
      <td>Ryan Arcidiacono</td>
      <td>PG</td>
      <td>25</td>
      <td>CHI</td>
      <td>58</td>
      <td>4</td>
      <td>16.0</td>
      <td>1.6</td>
      <td>3.8</td>
      <td>...</td>
      <td>.711</td>
      <td>0.3</td>
      <td>1.6</td>
      <td>1.9</td>
      <td>1.7</td>
      <td>0.5</td>
      <td>0.1</td>
      <td>0.6</td>
      <td>1.7</td>
      <td>4.5</td>
    </tr>
    <tr>
      <th>18</th>
      <td>19</td>
      <td>Trevor Ariza</td>
      <td>SF</td>
      <td>34</td>
      <td>TOT</td>
      <td>53</td>
      <td>21</td>
      <td>28.2</td>
      <td>2.7</td>
      <td>6.1</td>
      <td>...</td>
      <td>.838</td>
      <td>0.6</td>
      <td>4.0</td>
      <td>4.6</td>
      <td>1.7</td>
      <td>1.3</td>
      <td>0.3</td>
      <td>1.1</td>
      <td>2.1</td>
      <td>8.0</td>
    </tr>
    <tr>
      <th>19</th>
      <td>19</td>
      <td>Trevor Ariza</td>
      <td>SF</td>
      <td>34</td>
      <td>SAC</td>
      <td>32</td>
      <td>0</td>
      <td>24.7</td>
      <td>2.0</td>
      <td>5.2</td>
      <td>...</td>
      <td>.778</td>
      <td>0.7</td>
      <td>3.9</td>
      <td>4.6</td>
      <td>1.6</td>
      <td>1.1</td>
      <td>0.2</td>
      <td>0.9</td>
      <td>2.0</td>
      <td>6.0</td>
    </tr>
    <tr>
      <th>20</th>
      <td>19</td>
      <td>Trevor Ariza</td>
      <td>SF</td>
      <td>34</td>
      <td>POR</td>
      <td>21</td>
      <td>21</td>
      <td>33.4</td>
      <td>3.7</td>
      <td>7.6</td>
      <td>...</td>
      <td>.872</td>
      <td>0.6</td>
      <td>4.1</td>
      <td>4.8</td>
      <td>2.0</td>
      <td>1.6</td>
      <td>0.4</td>
      <td>1.3</td>
      <td>2.3</td>
      <td>11.0</td>
    </tr>
    <tr>
      <th>21</th>
      <td>20</td>
      <td>D.J. Augustin</td>
      <td>PG</td>
      <td>32</td>
      <td>ORL</td>
      <td>57</td>
      <td>13</td>
      <td>24.9</td>
      <td>3.2</td>
      <td>8.1</td>
      <td>...</td>
      <td>.890</td>
      <td>0.4</td>
      <td>1.8</td>
      <td>2.1</td>
      <td>4.6</td>
      <td>0.6</td>
      <td>0.0</td>
      <td>1.5</td>
      <td>1.3</td>
      <td>10.5</td>
    </tr>
    <tr>
      <th>22</th>
      <td>Rk</td>
      <td>Player</td>
      <td>Pos</td>
      <td>Age</td>
      <td>Tm</td>
      <td>G</td>
      <td>GS</td>
      <td>MP</td>
      <td>FG</td>
      <td>FGA</td>
      <td>...</td>
      <td>FT%</td>
      <td>ORB</td>
      <td>DRB</td>
      <td>TRB</td>
      <td>AST</td>
      <td>STL</td>
      <td>BLK</td>
      <td>TOV</td>
      <td>PF</td>
      <td>PTS</td>
    </tr>
    <tr>
      <th>23</th>
      <td>21</td>
      <td>Deandre Ayton</td>
      <td>C</td>
      <td>21</td>
      <td>PHO</td>
      <td>38</td>
      <td>32</td>
      <td>32.5</td>
      <td>8.2</td>
      <td>14.9</td>
      <td>...</td>
      <td>.753</td>
      <td>3.9</td>
      <td>7.6</td>
      <td>11.5</td>
      <td>1.9</td>
      <td>0.7</td>
      <td>1.5</td>
      <td>2.1</td>
      <td>3.1</td>
      <td>18.2</td>
    </tr>
    <tr>
      <th>24</th>
      <td>22</td>
      <td>Dwayne Bacon</td>
      <td>SG</td>
      <td>24</td>
      <td>CHO</td>
      <td>39</td>
      <td>11</td>
      <td>17.6</td>
      <td>2.2</td>
      <td>6.3</td>
      <td>...</td>
      <td>.660</td>
      <td>0.4</td>
      <td>2.2</td>
      <td>2.6</td>
      <td>1.3</td>
      <td>0.6</td>
      <td>0.1</td>
      <td>0.9</td>
      <td>1.3</td>
      <td>5.7</td>
    </tr>
  </tbody>
</table>
<p>25 rows × 30 columns</p>
</div>



Wow! You'll notice that there are some missing values (NaN) and multiple occurences of some player names because they have been a part of different teams in the same year.

### Data Cleaning

**We can see on the website that the header repeats itself in every 20 players. We'll have to remove the subsequent headers and keep only the first header:**

<br>
<br>
<img src = "https://docs.google.com/uc?export=download&id=1CEQs7TNFr4Nak0sQK10QYXl06uXcvrLN" />

<br>
<br>


```python
# Assigns the table in a variable df_2020

df_2020 = df[0]

# Let check the table header which is presented multiple times in several rows

df_2020[df_2020.Age == 'Age'].head() #  All the subsequent table header selected for this entire dataframe!

```




<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Rk</th>
      <th>Player</th>
      <th>Pos</th>
      <th>Age</th>
      <th>Tm</th>
      <th>G</th>
      <th>GS</th>
      <th>MP</th>
      <th>FG</th>
      <th>FGA</th>
      <th>...</th>
      <th>FT%</th>
      <th>ORB</th>
      <th>DRB</th>
      <th>TRB</th>
      <th>AST</th>
      <th>STL</th>
      <th>BLK</th>
      <th>TOV</th>
      <th>PF</th>
      <th>PTS</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>22</th>
      <td>Rk</td>
      <td>Player</td>
      <td>Pos</td>
      <td>Age</td>
      <td>Tm</td>
      <td>G</td>
      <td>GS</td>
      <td>MP</td>
      <td>FG</td>
      <td>FGA</td>
      <td>...</td>
      <td>FT%</td>
      <td>ORB</td>
      <td>DRB</td>
      <td>TRB</td>
      <td>AST</td>
      <td>STL</td>
      <td>BLK</td>
      <td>TOV</td>
      <td>PF</td>
      <td>PTS</td>
    </tr>
    <tr>
      <th>53</th>
      <td>Rk</td>
      <td>Player</td>
      <td>Pos</td>
      <td>Age</td>
      <td>Tm</td>
      <td>G</td>
      <td>GS</td>
      <td>MP</td>
      <td>FG</td>
      <td>FGA</td>
      <td>...</td>
      <td>FT%</td>
      <td>ORB</td>
      <td>DRB</td>
      <td>TRB</td>
      <td>AST</td>
      <td>STL</td>
      <td>BLK</td>
      <td>TOV</td>
      <td>PF</td>
      <td>PTS</td>
    </tr>
    <tr>
      <th>76</th>
      <td>Rk</td>
      <td>Player</td>
      <td>Pos</td>
      <td>Age</td>
      <td>Tm</td>
      <td>G</td>
      <td>GS</td>
      <td>MP</td>
      <td>FG</td>
      <td>FGA</td>
      <td>...</td>
      <td>FT%</td>
      <td>ORB</td>
      <td>DRB</td>
      <td>TRB</td>
      <td>AST</td>
      <td>STL</td>
      <td>BLK</td>
      <td>TOV</td>
      <td>PF</td>
      <td>PTS</td>
    </tr>
    <tr>
      <th>101</th>
      <td>Rk</td>
      <td>Player</td>
      <td>Pos</td>
      <td>Age</td>
      <td>Tm</td>
      <td>G</td>
      <td>GS</td>
      <td>MP</td>
      <td>FG</td>
      <td>FGA</td>
      <td>...</td>
      <td>FT%</td>
      <td>ORB</td>
      <td>DRB</td>
      <td>TRB</td>
      <td>AST</td>
      <td>STL</td>
      <td>BLK</td>
      <td>TOV</td>
      <td>PF</td>
      <td>PTS</td>
    </tr>
    <tr>
      <th>130</th>
      <td>Rk</td>
      <td>Player</td>
      <td>Pos</td>
      <td>Age</td>
      <td>Tm</td>
      <td>G</td>
      <td>GS</td>
      <td>MP</td>
      <td>FG</td>
      <td>FGA</td>
      <td>...</td>
      <td>FT%</td>
      <td>ORB</td>
      <td>DRB</td>
      <td>TRB</td>
      <td>AST</td>
      <td>STL</td>
      <td>BLK</td>
      <td>TOV</td>
      <td>PF</td>
      <td>PTS</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 30 columns</p>
</div>




```python
# Checking the length for how many header we have:

print(f' total numbers of redundant headers: {len(df_2020[df_2020.Age == "Age"])} ')

# Drop the redundant headers in the dataframe:
df_2020_new = df_2020.drop(df_2020[df_2020.Age == 'Age'].index)

# Compare before and after dropping redundant headers with numbers of rows:

print(f' total rows of df_2020:     {df_2020.shape[0]} ')
print(f' total rows of df_2020_new: {df_2020_new.shape[0]} ')
print('===========================================')

df_2020_new.head(20)
```

     total numbers of redundant headers: 26 
     total rows of df_2020:     677 
     total rows of df_2020_new: 651 
    ===========================================





<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Rk</th>
      <th>Player</th>
      <th>Pos</th>
      <th>Age</th>
      <th>Tm</th>
      <th>G</th>
      <th>GS</th>
      <th>MP</th>
      <th>FG</th>
      <th>FGA</th>
      <th>...</th>
      <th>FT%</th>
      <th>ORB</th>
      <th>DRB</th>
      <th>TRB</th>
      <th>AST</th>
      <th>STL</th>
      <th>BLK</th>
      <th>TOV</th>
      <th>PF</th>
      <th>PTS</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>Steven Adams</td>
      <td>C</td>
      <td>26</td>
      <td>OKC</td>
      <td>63</td>
      <td>63</td>
      <td>26.7</td>
      <td>4.5</td>
      <td>7.6</td>
      <td>...</td>
      <td>.582</td>
      <td>3.3</td>
      <td>6.0</td>
      <td>9.3</td>
      <td>2.3</td>
      <td>0.8</td>
      <td>1.1</td>
      <td>1.5</td>
      <td>1.9</td>
      <td>10.9</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>Bam Adebayo</td>
      <td>PF</td>
      <td>22</td>
      <td>MIA</td>
      <td>72</td>
      <td>72</td>
      <td>33.6</td>
      <td>6.1</td>
      <td>11.0</td>
      <td>...</td>
      <td>.691</td>
      <td>2.4</td>
      <td>7.8</td>
      <td>10.2</td>
      <td>5.1</td>
      <td>1.1</td>
      <td>1.3</td>
      <td>2.8</td>
      <td>2.5</td>
      <td>15.9</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>LaMarcus Aldridge</td>
      <td>C</td>
      <td>34</td>
      <td>SAS</td>
      <td>53</td>
      <td>53</td>
      <td>33.1</td>
      <td>7.4</td>
      <td>15.0</td>
      <td>...</td>
      <td>.827</td>
      <td>1.9</td>
      <td>5.5</td>
      <td>7.4</td>
      <td>2.4</td>
      <td>0.7</td>
      <td>1.6</td>
      <td>1.4</td>
      <td>2.4</td>
      <td>18.9</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>Kyle Alexander</td>
      <td>C</td>
      <td>23</td>
      <td>MIA</td>
      <td>2</td>
      <td>0</td>
      <td>6.5</td>
      <td>0.5</td>
      <td>1.0</td>
      <td>...</td>
      <td>NaN</td>
      <td>1.0</td>
      <td>0.5</td>
      <td>1.5</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.5</td>
      <td>0.5</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>Nickeil Alexander-Walker</td>
      <td>SG</td>
      <td>21</td>
      <td>NOP</td>
      <td>47</td>
      <td>1</td>
      <td>12.6</td>
      <td>2.1</td>
      <td>5.7</td>
      <td>...</td>
      <td>.676</td>
      <td>0.2</td>
      <td>1.6</td>
      <td>1.8</td>
      <td>1.9</td>
      <td>0.4</td>
      <td>0.2</td>
      <td>1.1</td>
      <td>1.2</td>
      <td>5.7</td>
    </tr>
    <tr>
      <th>5</th>
      <td>6</td>
      <td>Grayson Allen</td>
      <td>SG</td>
      <td>24</td>
      <td>MEM</td>
      <td>38</td>
      <td>0</td>
      <td>18.9</td>
      <td>3.1</td>
      <td>6.6</td>
      <td>...</td>
      <td>.867</td>
      <td>0.2</td>
      <td>2.0</td>
      <td>2.2</td>
      <td>1.4</td>
      <td>0.3</td>
      <td>0.1</td>
      <td>0.9</td>
      <td>1.4</td>
      <td>8.7</td>
    </tr>
    <tr>
      <th>6</th>
      <td>7</td>
      <td>Jarrett Allen</td>
      <td>C</td>
      <td>21</td>
      <td>BRK</td>
      <td>70</td>
      <td>64</td>
      <td>26.5</td>
      <td>4.3</td>
      <td>6.6</td>
      <td>...</td>
      <td>.633</td>
      <td>3.1</td>
      <td>6.5</td>
      <td>9.6</td>
      <td>1.6</td>
      <td>0.6</td>
      <td>1.3</td>
      <td>1.1</td>
      <td>2.3</td>
      <td>11.1</td>
    </tr>
    <tr>
      <th>7</th>
      <td>8</td>
      <td>Kadeem Allen</td>
      <td>PG</td>
      <td>27</td>
      <td>NYK</td>
      <td>10</td>
      <td>0</td>
      <td>11.7</td>
      <td>1.9</td>
      <td>4.4</td>
      <td>...</td>
      <td>.636</td>
      <td>0.2</td>
      <td>0.7</td>
      <td>0.9</td>
      <td>2.1</td>
      <td>0.5</td>
      <td>0.2</td>
      <td>0.8</td>
      <td>0.7</td>
      <td>5.0</td>
    </tr>
    <tr>
      <th>8</th>
      <td>9</td>
      <td>Al-Farouq Aminu</td>
      <td>PF</td>
      <td>29</td>
      <td>ORL</td>
      <td>18</td>
      <td>2</td>
      <td>21.1</td>
      <td>1.4</td>
      <td>4.8</td>
      <td>...</td>
      <td>.655</td>
      <td>1.3</td>
      <td>3.5</td>
      <td>4.8</td>
      <td>1.2</td>
      <td>1.0</td>
      <td>0.4</td>
      <td>0.9</td>
      <td>1.5</td>
      <td>4.3</td>
    </tr>
    <tr>
      <th>9</th>
      <td>10</td>
      <td>Justin Anderson</td>
      <td>SG</td>
      <td>26</td>
      <td>BRK</td>
      <td>10</td>
      <td>1</td>
      <td>10.7</td>
      <td>1.0</td>
      <td>3.8</td>
      <td>...</td>
      <td>.500</td>
      <td>0.1</td>
      <td>2.0</td>
      <td>2.1</td>
      <td>0.8</td>
      <td>0.0</td>
      <td>0.6</td>
      <td>0.4</td>
      <td>1.3</td>
      <td>2.8</td>
    </tr>
    <tr>
      <th>10</th>
      <td>11</td>
      <td>Kyle Anderson</td>
      <td>SF</td>
      <td>26</td>
      <td>MEM</td>
      <td>67</td>
      <td>28</td>
      <td>19.9</td>
      <td>2.3</td>
      <td>4.9</td>
      <td>...</td>
      <td>.667</td>
      <td>0.9</td>
      <td>3.4</td>
      <td>4.3</td>
      <td>2.4</td>
      <td>0.8</td>
      <td>0.6</td>
      <td>1.0</td>
      <td>1.7</td>
      <td>5.8</td>
    </tr>
    <tr>
      <th>11</th>
      <td>12</td>
      <td>Ryan Anderson</td>
      <td>C</td>
      <td>31</td>
      <td>HOU</td>
      <td>2</td>
      <td>0</td>
      <td>7.0</td>
      <td>1.0</td>
      <td>3.5</td>
      <td>...</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>3.5</td>
      <td>3.5</td>
      <td>1.0</td>
      <td>0.5</td>
      <td>0.0</td>
      <td>0.5</td>
      <td>0.5</td>
      <td>2.5</td>
    </tr>
    <tr>
      <th>12</th>
      <td>13</td>
      <td>Giannis Antetokounmpo</td>
      <td>PF</td>
      <td>25</td>
      <td>MIL</td>
      <td>63</td>
      <td>63</td>
      <td>30.4</td>
      <td>10.9</td>
      <td>19.7</td>
      <td>...</td>
      <td>.633</td>
      <td>2.2</td>
      <td>11.4</td>
      <td>13.6</td>
      <td>5.6</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>3.7</td>
      <td>3.1</td>
      <td>29.5</td>
    </tr>
    <tr>
      <th>13</th>
      <td>14</td>
      <td>Kostas Antetokounmpo</td>
      <td>PF</td>
      <td>22</td>
      <td>LAL</td>
      <td>5</td>
      <td>0</td>
      <td>4.0</td>
      <td>0.6</td>
      <td>0.6</td>
      <td>...</td>
      <td>.500</td>
      <td>0.4</td>
      <td>0.2</td>
      <td>0.6</td>
      <td>0.4</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.2</td>
      <td>0.4</td>
      <td>1.4</td>
    </tr>
    <tr>
      <th>14</th>
      <td>15</td>
      <td>Thanasis Antetokounmpo</td>
      <td>SF</td>
      <td>27</td>
      <td>MIL</td>
      <td>20</td>
      <td>2</td>
      <td>6.5</td>
      <td>1.2</td>
      <td>2.4</td>
      <td>...</td>
      <td>.412</td>
      <td>0.6</td>
      <td>0.6</td>
      <td>1.2</td>
      <td>0.8</td>
      <td>0.4</td>
      <td>0.1</td>
      <td>0.6</td>
      <td>0.9</td>
      <td>2.8</td>
    </tr>
    <tr>
      <th>15</th>
      <td>16</td>
      <td>Carmelo Anthony</td>
      <td>PF</td>
      <td>35</td>
      <td>POR</td>
      <td>58</td>
      <td>58</td>
      <td>32.8</td>
      <td>5.8</td>
      <td>13.5</td>
      <td>...</td>
      <td>.845</td>
      <td>1.2</td>
      <td>5.1</td>
      <td>6.3</td>
      <td>1.5</td>
      <td>0.8</td>
      <td>0.5</td>
      <td>1.7</td>
      <td>2.9</td>
      <td>15.4</td>
    </tr>
    <tr>
      <th>16</th>
      <td>17</td>
      <td>OG Anunoby</td>
      <td>SF</td>
      <td>22</td>
      <td>TOR</td>
      <td>69</td>
      <td>68</td>
      <td>29.9</td>
      <td>4.1</td>
      <td>8.2</td>
      <td>...</td>
      <td>.706</td>
      <td>1.2</td>
      <td>4.1</td>
      <td>5.3</td>
      <td>1.6</td>
      <td>1.4</td>
      <td>0.7</td>
      <td>1.1</td>
      <td>2.4</td>
      <td>10.6</td>
    </tr>
    <tr>
      <th>17</th>
      <td>18</td>
      <td>Ryan Arcidiacono</td>
      <td>PG</td>
      <td>25</td>
      <td>CHI</td>
      <td>58</td>
      <td>4</td>
      <td>16.0</td>
      <td>1.6</td>
      <td>3.8</td>
      <td>...</td>
      <td>.711</td>
      <td>0.3</td>
      <td>1.6</td>
      <td>1.9</td>
      <td>1.7</td>
      <td>0.5</td>
      <td>0.1</td>
      <td>0.6</td>
      <td>1.7</td>
      <td>4.5</td>
    </tr>
    <tr>
      <th>18</th>
      <td>19</td>
      <td>Trevor Ariza</td>
      <td>SF</td>
      <td>34</td>
      <td>TOT</td>
      <td>53</td>
      <td>21</td>
      <td>28.2</td>
      <td>2.7</td>
      <td>6.1</td>
      <td>...</td>
      <td>.838</td>
      <td>0.6</td>
      <td>4.0</td>
      <td>4.6</td>
      <td>1.7</td>
      <td>1.3</td>
      <td>0.3</td>
      <td>1.1</td>
      <td>2.1</td>
      <td>8.0</td>
    </tr>
    <tr>
      <th>19</th>
      <td>19</td>
      <td>Trevor Ariza</td>
      <td>SF</td>
      <td>34</td>
      <td>SAC</td>
      <td>32</td>
      <td>0</td>
      <td>24.7</td>
      <td>2.0</td>
      <td>5.2</td>
      <td>...</td>
      <td>.778</td>
      <td>0.7</td>
      <td>3.9</td>
      <td>4.6</td>
      <td>1.6</td>
      <td>1.1</td>
      <td>0.2</td>
      <td>0.9</td>
      <td>2.0</td>
      <td>6.0</td>
    </tr>
  </tbody>
</table>
<p>20 rows × 30 columns</p>
</div>



### Quick Exploratory Data Analysis


```python
# Making a simple histogram

plt.figure(figsize=(10,8))

sns.distplot(df_2020_new.PTS,    # Checking frequency of the player points
            kde= False,          # Should be False because we want to retain the original frequency ( "kde=True" => it will be the probability)
            hist_kws = dict( edgecolor = 'black', linewidth=2))  

plt.title('HISTOGRAM OF PLAYER POINTS PER GAME IN THE 2020 NBA SEASON')
plt.ylabel('NUMBERS OF PLAYERS')
plt.xlabel('POINTS PER GAME')
plt.show()
```


    
![image](https://drive.google.com/uc?export=view&id=1JJQTnoOwjaJE-sWpi7TMj9PB7B5sTGo8)

    


From the histogram, we can see: 
- There are about 57 players having between 0 and 1 point.
- There are less than 10 players who had 30 points.
