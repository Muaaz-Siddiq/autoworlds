from os import name
import re
import requests
import folium
from bson.codec_options import _RAW_BSON_DOCUMENT_MARKER
from flask import Flask, jsonify, render_template,request,Response
from flask import json
from flask.json import dumps
from flask_pymongo import PyMongo
from bson import json_util
from datetime import datetime



app = Flask(__name__)

app.secret_key ='projectdb'
app.config['MONGO_URI'] = "mongodb://localhost:27017/cars-db"
monogo = PyMongo(app)



#                            ------------------index.html / index--------------------------
@app.route('/')
@app.route('/index')
def home():
    return render_template('index.html')

#                              -----------------brand.html / Brands----------------------
@app.route('/Brands')
def brands():
    return render_template('Brands.html')

#                             -------------------------about.html--------------------------------
@app.route('/about')
def aboutus():
    return render_template('About.html')


#                   --------------------------Product.html / all-products-------------------

@app.route('/all-products/<company>')
def all_products(company):
    name_list=[]
    img_list=[]
    price_list =[]
    myvar = monogo.db.details.aggregate([
    {
        '$match': {
            'company': company
        }
    }, {
        '$group': {
            '_id': {
                'name': '$Name', 
                'image': '$image1',
                'price':"$price"
            }
        }
    }
])
    for records in myvar:
        records_id = records['_id']
        records_name = records_id['name']
        records_img = records_id['image']
        records_price = records_id['price']
        name_list.append(records_name)
        img_list.append(records_img)
        price_list.append(records_price)
    #print("name", name_list)
    #print("image", img_list)

    return render_template('Products.html',name1=name_list[0],name2=name_list[1],name3=name_list[2],name4=name_list[3],name5=name_list[4],
    img1=img_list[0],img2=img_list[1],img3=img_list[2],img4=img_list[3],img5=img_list[4],price1=price_list[0],
    price2=price_list[1],price3=price_list[2],price4=price_list[3],price5=price_list[4],comp=company)

#                    --------------------Car-details.html / details-------------------
@app.route('/detalis/<name>')
def details(name):
    mylist =[]
    mylist1 =[]
    relcarn_list=[]
    relcari_list=[]
    var_details = monogo.db.details.aggregate([ {
        '$match': {
            'Name': name
        }
    }])
    '''resp = json_util.dumps(test1)
    return Response(resp, mimetype='application/json')
    print(resp)'''
    for record in var_details:
        mylist.append(record['company'])
        mylist.append(record['Name'])
        mylist.append(record['engine'])
        mylist.append(record['description'])
        mylist.append(record['body_type'])
        mylist.append(record['image1'])
        mylist.append(record['image2'])
        mylist.append(record['image3'])
        mylist.append(record['image4'])
        mylist.append(record['image5'])
        mylist.append(record['price'])
    #print(mylist)


    star_avg = monogo.db.details.aggregate([
    {
        '$unwind': {
            'path': '$star'
        }
    }, {
        '$match': {
            'Name': name
        }
    }, {
        '$group': {
            '_id': '$Name', 
            'Rating': {
                '$avg': '$star'
            }, 
            'review': {
                '$sum': 1
            }
        }
    }
    ])

    for avgstars in star_avg:
        mylist1.append(round(avgstars['Rating'],1))
        mylist1.append(avgstars['review'])

    calc = monogo.db.details.aggregate([
    {
        '$match': {
            'Name': name
        }
    }, {
        '$group': {
            '_id': {
                'name': '$Name', 
                'tax': '$tax', 
                'reg_fees': '$reg_fees', 
                'plate_fees': '$plate_charge'
            }, 
            'On_road_price': {
                '$sum': {
                    '$add': [
                        '$price', '$tax', '$reg_fees', '$plate_charge'
                    ]
                }
            }
        }
    }
])

    for charges in calc:
        id = charges['_id']
        Tax = id['tax']
        Registartion_fees = id['reg_fees']
        Plate_fees = id['plate_fees']
        Tax = id['tax']
        total = charges['On_road_price']

    relcar = monogo.db.details.aggregate([
    {
        '$match': {
            'company': mylist[0]
        }
    }, {
        '$match': {
            'Name': {
                '$ne': mylist[1]
            }
        }
    }
])
    for relcars in relcar:
        relcarn_list.append(relcars['Name'])
        relcari_list.append(relcars['image1'])

    return render_template('car-detail.html', company = mylist[0],
    Name= mylist[1],
    engine = mylist[2],
    description = mylist[3],
    body_type = mylist[4],
    image1=mylist[5],
    image2=mylist[6],
    image3=mylist[7],
    image4=mylist[8],
    image5=mylist[9],
    price = mylist[10],
    avg_star = mylist1[0],
    reviews = mylist1[1],
    Tax = Tax,
    Registration_fees = Registartion_fees,
    Plate_fees = Plate_fees,
    total = total,
    name1=relcarn_list[0],name2=relcarn_list[1],name3=relcarn_list[2],name4=relcarn_list[3],
    img1=relcari_list[0],img2=relcari_list[1],img3=relcari_list[2],img4=relcari_list[3])

#          --------------------------------comparison----------------------------------
@app.route('/compare')
def compare():
    imgurl = "https://i.ibb.co/mzwD5H0/default.jpg"
    return render_template('compare.html',image=imgurl,image1=imgurl)


complist1 =[]
@app.route('/compare/<car1>')
def comparison(car1):
    complist1.clear()
    carc1 = monogo.db.details.aggregate([ {
        '$match': {
            'Name': car1
        }
    }])
    for record5 in carc1:
        complist1.append(record5['Name'])
        complist1.append(record5['engine'])
        complist1.append(record5['body_type'])
        complist1.append(record5['image1'])
        complist1.append(record5['price'])
    #print("c1",complist1)
    
    star_avg1 = monogo.db.details.aggregate([
    {
        '$unwind': {
            'path': '$star'
        }
    }, {
        '$match': {
            'Name': car1
        }
    }, {
        '$group': {
            '_id': '$Name', 
            'Rating': {
                '$avg': '$star'
            }, 
            'review': {
                '$sum': 1
            }
        }
    }
    ])
    '''resp = json_util.dumps(test2)
    return Response(resp, mimetype='application/json')
    print(resp)'''

    for avgstars1 in star_avg1:
        complist1.append(round(avgstars1['Rating'],1))
    return("",204)


complist2=[]
@app.route('/compares/<car2>')
def comparisons(car2):
    complist2.clear()
    carc2 = monogo.db.details.aggregate([ {
        '$match': {
            'Name': car2
        }
    }])
    for record6 in carc2:
        complist2.append(record6['Name'])
        complist2.append(record6['engine'])
        complist2.append(record6['body_type'])
        complist2.append(record6['image1'])
        complist2.append(record6['price'])
    #print("c2",complist2)

        star_avg2 = monogo.db.details.aggregate([
    {
        '$unwind': {
            'path': '$star'
        }
    }, {
        '$match': {
            'Name': car2
        }
    }, {
        '$group': {
            '_id': '$Name', 
            'Rating': {
                '$avg': '$star'
            }, 
            'review': {
                '$sum': 1
            }
        }
    }
    ])
    '''resp = json_util.dumps(test2)
    return Response(resp, mimetype='application/json')
    print(resp)'''

    for avgstars2 in star_avg2:
        complist2.append(round(avgstars2['Rating'],1))
    return("",204)

@app.route('/comparebutton')
def result():
    return render_template('compare.html',Name=complist1[0],engine=complist1[1],
    bodytype=complist1[2],image=complist1[3],price=complist1[4],star=complist1[5], Name1=complist2[0],
    engine1=complist2[1],
    bodytype1=complist2[2],image1=complist2[3],price1=complist2[4],star1=complist2[5])

#          ----------------------------News---------------------------------------
@app.route('/News', methods=['GET'])
def news():
    authorlist=[]
    titlelist=[]
    descrpitlist=[]
    publishedlist=[]
    contentlist=[]

    dt = datetime.date(datetime.now())
    req = requests.get(f'https://newsapi.org/v2/everything?q=tesla&from={dt}&sortBy=publishedAt&apiKey=fe645105a0204f9aa35038d8c68b8e25')
    data = json.loads(req.content)
    for key,values in data.items():
        if key == 'articles':
            for i in range(1,6):
                authorlist.append(values[i]['author'])
                titlelist.append(values[i]['title'])
                descrpitlist.append(values[i]['description'])
                publishedlist.append(values[i]['publishedAt'])
                contentlist.append(values[i]['content'])
    return render_template("news.html",author=authorlist[0],title=titlelist[0],descript=descrpitlist[0],
    published=publishedlist[0],content=contentlist[0],author1=authorlist[1],title1=titlelist[1],descript1=descrpitlist[1],
    published1=publishedlist[1],content1=contentlist[1],author2=authorlist[2],title2=titlelist[2],descript2=descrpitlist[2],
    published2=publishedlist[2],content2=contentlist[2],
    author3=authorlist[3],title3=titlelist[3],descript3=descrpitlist[3],
    published3=publishedlist[3],content3=contentlist[3],
    author4=authorlist[4],title4=titlelist[4],descript4=descrpitlist[4],
    published4=publishedlist[4],content4=contentlist[4])

#      ------------------------------------ maps -----------------------------------------
@app.route('/map/<loc>')
def map(loc):

    if loc == 'BMW':
        lon=30.6880702
        lat=-96.8858575
    elif loc == 'Audi':
        lon=28.3382283
        lat=-96.8825097
    elif loc == 'Honda':
        lon=32.6880702
        lat=-96.8858575
    elif loc == 'Toyota':
        lon=33.8797612
        lat=-113.8126791
    elif loc == 'Nissan':
        lon=42.2316003
        lat=-96.8858575
    elif loc == 'Lamborghini':
        lon=40.6932866
        lat=-113.8775378
    elif loc == 'KIA':
        lon=39.1015302
        lat=-116.4560085
    elif loc == 'Hyundai':
        lon=37.6137496
        lat=-116.5134254
    elif loc == 'chevrolet':
        lon=35.8084869
        lat=-96.5979544

 
    maps = folium.Map(
        location=[lon,lat],
        zoom_start=9
        #tiles='Stamen Terrain'
    )
    
    folium.Marker(
    location=[lon,lat],
    popup=loc
    ).add_to(maps)

    return maps._repr_html_()



if __name__ == "__main__":
    app.run(debug=False, port = 8000)