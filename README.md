# Crawling code for downloading the picture and picture's tag from  www.zappos.com.
## Configuration instructions
### Basic environment
* Python 3.5
* Pip3
* Mysql 5.7
### Libs
* beautifulsoup4
    > sudo pip3 install beautifulsoup4
* html5lib
    > sudo pip3 install python3-html5lib
* selenium
    > sudo pip3 install selenium
* PhantomJS

    * 下载地址：https://npm.taobao.org/mirrors/phantomjs
    * you need to download the 2.1.1 version for your os(windows/linux/macOS)
    * after install,please modify the following variable in the code(Zappos.py & GetImg.py)
        <pre><cpde>browserPath = 'C:\\Program Files (x86)\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe'</pre></code>
### Mysql
* the default user,password,datebase are "root","root","zappos",if your config is not same.please modify following variable in the code(Zappos.py & GetImg.py & FindSamePhoto.py)
        <pre><code>db = pymysql.connect("localhost", "root", "root", "zappos")</pre></code>
* table 1 : picture_with_tag
    * show the tags for each picture
* table 2 : id_imgurl
    * the download url for each picture
* table 3 : tag_scan
    * which tag has been scanned for each category
    * 0 : not be scaned yet
    * 1 : has been scanned
### Means of "outputDir" variable 
* "outputDir" means the loaction for downloading picture,you can modify it.
    <pre><code>outputDir = 'C:\\Users\\zapposPhoto'</pre></code>
### Means of the figures(isdownload = 0,1,2,3) in database table(id_imgurl) :
   * 0 : Not been downloaded
   * 1 : Has been downloaded
   * 2 : Wrong URL(There is no picture on the server)
   * 3 : Repeated picture
### Steps:
1. install the libs
2. modify the variabs(browserPath,outputDir)
3. modify the parameter of database connection(user,password,database)
4. import db data from backup(zappos/db_backup),there are two tables
5. run application