from flask import Flask, request, render_template
from flask_cors import cross_origin
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import pyodbc


#connection to database
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=LAPTOP-0F19FF79;'
                      'Database=Hotel_management__;'
                      'Trusted_Connection=yes;');

app = Flask(__name__)

@app.route("/")
@cross_origin()
def home():
    return render_template("index.html")

@app.route("/datareport", methods = ["GET", "POST"])
@cross_origin()
def data():
    option = request.form['exampleRadios']
    if option == 'option1':
        data = pd.read_sql("SELECT * FROM Hotel", conn)
        result=data.to_html()

    elif option == 'option2':
        data = pd.read_sql("SELECT * FROM Customers", conn)
        result=data.to_html()
        sns.countplot(x='city',data=data)
        plt.xlabel('City')
        plt.ylabel('No. of customers from the cities')
        plt.title('No. of customers from the cities')
        plt.savefig('static/cust1.jpg')

        #sns.kdeplot(data=data['score'])
        #plt.xlabel('Client Score')
        #plt.title('Score data separation')
        #plt.savefig('static/client2.jpg')
        result=append_html(result,['cust1.jpg'])

    elif option == 'option3':
        data = pd.read_sql("SELECT * FROM Food", conn)
        result=data.to_html()
        fig = plt.figure(figsize=(9,9))
        ax = sns.barplot(y=data.cost_per_item,x=data.food_type,data=data)
        #sns.barplot(y=data.cost_per_item,x=data.food_type,data=data)
        plt.xlabel('Food type')
        plt.ylabel('Cost per item')
        plt.title('Food type and their price per item')
        plt.savefig('static/food1.jpg')
        result=append_html(result,['food1.jpg'])
        print()

        sns.countplot(x='food_type',data=data)
        plt.xlabel('Food type')
        plt.ylabel('No. of customers who ordered the food types')
        plt.title('Food type and the no. of orders')
        plt.savefig('static/food2.jpg')
        result=append_html(result,['food2.png'])


    elif option == 'option4':
        data = pd.read_sql("SELECT * FROM Rooms", conn)
        result=data.to_html()
        sns.barplot(y=data.price_per_night,x=data.room_type,data=data)
        plt.xlabel('Room type')
        plt.ylabel('Price per night')
        plt.title('Room type and their price per night')
        plt.savefig('static/room1.png')
        result=append_html(result,['room1.png'])
        print()
        sns.countplot(x='room_type',data=data)
        plt.xlabel('Room type')
        plt.ylabel('No. of customers who booked the different room types')
        plt.title('Room type and the no. of bookings')
        plt.savefig('static/room2.jpg')
        result=append_html(result,['room2.png'])

        print()
        
        

    elif option == 'option5':
        data = pd.read_sql("SELECT * FROM Bills", conn).sort_values(by='bill_date')
        result=data.to_html()
        sns.countplot(x='payment_method',data=data)
        plt.xlabel('Payment method')
        plt.ylabel('No. of customers who opted the payment methods')
        plt.title('Payments methods and the no. of customers who opted it')
        plt.savefig('static/bill1.jpg')
        result=append_html(result,['bill1.png'])
        print()
        
        sns.barplot(y=data.no_of_items,x=data.cust_id,data=data)
        plt.xlabel('Customer ID')
        plt.ylabel('No. of food items ordered')
        plt.title('Number of Food items ordered by the customers')
        plt.savefig('static/bill2.png')
        result=append_html(result,['bill2.png'])
        print()

        sns.barplot(y=data.amount,x=data.cust_id,data=data)
        plt.xlabel('Customer ID')
        plt.ylabel('Amount spent')
        plt.title('Amount spent by the customers')
        plt.savefig('static/bill3.png')
        result=append_html(result,['bill3.png'])
        print()

        fig = plt.figure(figsize=(15,15))
        pt=pd.pivot_table(data,index=['bill_date'],values=['amount'])
        pt.plot()
        plt.savefig('static/bill4.png')
        result=append_html(result,['bill4.png'])
        
        



    return result



def append_html(result,image_names):
    for i in image_names:
        result=result+" <img src=\"static/"+i+"\" width=\"600\" height=\"500\">"
    return result


if __name__ == "__main__":
    app.run(debug=True)
