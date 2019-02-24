from Accountadmin import Accoutadmin
from Bookadmin import Bookadmin

account = Accoutadmin()
while True:
    select = input("1.注册。2.登入。3.修改\n")
    if(select=="1"):
        account.regist()
    elif(select=="2"):
        account.login()
    elif(select == "3"):
        account.changepassword()
        continue
    while account.is_login:
        book = Bookadmin()
        select_b = input("1.查询所有书籍。2.通过书名查询一本书。3.通过价格查询书籍。4.添加一本书"
                         "5.删除一本书。6.修改一本书。7.退出系统\n")
        if (select_b == "1"):
            book.selectAllbook()
        elif(select_b == "2"):
            bookname = input("请输入书名：")
            book.selectOneBookByName(bookName=bookname)
        elif (select_b == "3"):
            minprice = input("请输入最低价：")
            maxprice = input("请输入最高价：")
            try:
                int(minprice)
                int(maxprice)
            except BaseException:
                print("请输入数字")
                continue
            book.selectBooksByPrice(minPrice=minprice,maxPrice=maxprice)
        elif (select_b == "4"):
            bookname = input("请输入书名：")
            author = input("请输入作者：")
            category = input("请输入类型：")
            price = input("请输入价格：")
            descs = input("请输入描述：")
            book.addOneBook(bookname=bookname,author=author,category=category,price=price,descs=descs)
        elif (select_b == "5"):
            bookname = input("请输入书名：")
            book.deleteOneBookByName(bookname=bookname)
        elif (select_b == "6"):
            bookname = input("请输入书名：")
            author = input("请输入作者：")
            category = input("请输入类型：")
            price = input("请输入价格：")
            descs = input("请输入描述：")
            book.modifyOneBookByName(bookname=bookname,author=author,category=category,price=price,descs=descs)
        elif (select_b == "7"):
            exit()


