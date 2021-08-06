import numpy as np
import pandas as pd
from flask import Flask,render_template,request
import pickle
from sklearn.model_selection import train_test_split



app = Flask(__name__)

# list of locations 
location_list_data = pd.read_csv("location.csv") 

# data loading for model 
df = pd.read_csv('clean_data.csv') 

# Split data 
x = df.drop('price',axis=1)
y = df['price']
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=1)

# Column list to check index for columns 
column_list = x.columns.tolist()

def area_type_index(area):
    area_type_index_var = column_list.index('area_type_'+area)
    return area_type_index_var

def locatio_index(location):
    location_index_var = column_list.index('location_'+location)
    return location_index_var


# load Model 
hpp_model = pickle.load(open("hpp.pickle","rb")) 




@app.route('/')
def index():
    locations = sorted(location_list_data['location'].unique())
    return render_template('index.html',locations=locations)

    
    
@app.route('/predict', methods=["POST"])
def predict():

#############################################################################
    if request.method =="POST":
        location = ' Dollar Scheme Colony'
        area = request.form.get('area_type')
        BHK = request.form.get('bhk')
        balcony = request.form.get('balcony')
        bathroom = request.form.get('bathroom')
        sqft  = request.form.get('sqft')
        print(f"User Form Data:{location=},{area=},{BHK=},{balcony=},{bathroom=},{sqft=}")
    else:
        return render_template("index.html")
###################################################################################
    # create null dataframe for data mapping 
    user_input_data = np.zeros(len(x.columns))
    print(x.columns[0:10])
    # adding user values to features
    try:
        user_input_data[0] = sqft
        user_input_data[1] = bathroom
        user_input_data[2] = balcony
        user_input_data[3] = BHK
    
        index_area = area_type_index(area)
        index_location = locatio_index(location)
        user_input_data[index_area] = 1
        user_input_data[index_location] = 1
    except:
        pass
    predicted_price= hpp_model.predict([user_input_data])[0]
    
    print(f"{predicted_price=}")

    # return price
    return render_template('index.html', prediction_text='Predicted Price of Bangalore House is {}'.format(predicted_price))
 
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port="8080")
     

    


if __name__=='__main__':
    app.run(debug=False)