#from crypt import methods
import os
from uuid import uuid4
from flask import Flask, render_template, request,send_from_directory
##import tensorflow as tf
global graph,model
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
##graph = tf.get_default_graph()
##import detection

# define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('helloworld.json', scope)

# authorize the clientsheet 
client = gspread.authorize(creds)


# get the instance of the Spreadsheet
sheet = client.open('PneumoniaDataCollection')
# get the first sheet of the Spreadsheet
sheet_instance = sheet.get_worksheet(0)


result = 0

##ml = detection.detectp()
     
app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    return render_template("upload.html")

#@app.route("/upload",methods=["GET","POST"])
#def upload():
#    form = uploadform()
#    if form.is_submitted():
#        result= request.form
#        return render_template('user.html',result=result)
#    return render_template('upload.html',form=form)


@app.route("/upload", methods=["POST"])
def upload():
    paitentname = request.form.get("paitentname")
    print(paitentname)
    paitentage = request.form.get("paitentage")
    print(paitentage)
    gender = request.form.get("gender")
    print(gender)
    imageid= request.form.get("imageid")
    print(imageid)
    clinicname=request.form.get("clinicname")
    print(clinicname)
    
    
    # Image folder 
    target = os.path.join(APP_ROOT, 'images/')
    # target = os.path.join(APP_ROOT, 'static/')
    
    if not os.path.isdir(target):
            os.mkdir(target)

    # print(request.files.getlist("file"))

    for upload in request.files.getlist("file"):
        file_name = str(uuid4())

        print(file_name)

        destination = "/".join([target, f'{file_name}.png'])
        
        upload.save(destination)
    
    elements=[file_name,paitentname,paitentage,gender,imageid,clinicname]
    data=pd.DataFrame.from_dict(elements)
    # get all the records of the data
    #records_data = sheet_instance.get_all_records()
    # convert the json to dataframe
    #records_df = pd.DataFrame.from_dict(records_data)

    # view the top records
    #recordhead=records_df.head()

    sheet_instance.insert_cols(data.values.tolist())
    ##result = ml.detect(destination)
    

    return render_template("complete.html",result=round(result*100,3))

@app.route("/upload")
def send_image():
    return send_from_directory("images", "heatmap.png")

if __name__ == "__main__":
    app.run(port=80)