from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
import pymysql
# Create your views here.
def select(request):
    data=""
    con=pymysql.connect("localhost","root","","productdb")
    c=con.cursor()
    c.execute("select * from product_table")
    data=c.fetchall()
   
    return render(request,"select.html",{"data":data})
def cart(request):
    productid=request.GET.get("productid")
    print(productid)
    data=""
    con=pymysql.connect("localhost","root","","productdb")
    c=con.cursor()
    
    data1=""
    c.execute("select * from product_table  where productid ='"+productid+"'")
    data=c.fetchone()
    productname=data[1]
    description=data[2]
    price=data[3]
    c.execute("insert into cart_table(productname,description,price)values('"+str(productname)+"','"+str(description)+"','"+str(price)+"')")
    con.commit()
    c.execute("select * from cart_table")
    data1=c.fetchall()
    c.execute("select sum(price) from cart_table")
    data2=c.fetchone()
    return render(request,"productcart.html",{"data":data,"data1":data1,"data2":data2})
def addcart(request):
    data=""
    con=pymysql.connect("localhost","root","","productdb")
    c=con.cursor()
    productid=request.GET.get("productid")
    c.execute("select * from product_table  where productid ='"+productid+"'")
    data=c.fetchone()
    l=[]
    if(request.session.get("sdata")==""):
       
       dic={
       "productname":data[1],
       "decription":data[2],
       "price":data[3]
       }
       l.append(dic)
       request.session["sdata"]=l
       
    else:
         
       dic={
       "productname":data[1],
       "decription":data[2],
       "price":data[3]}
       u=request.session.get("sdata")
       print(u)
       for d in u:
          l.append(d) 
         
       l.append(dic)
       request.session["sdata"]=l
    data3=request.session.get("sdata")
    return render(request,"productcart.html",{"data":data3})