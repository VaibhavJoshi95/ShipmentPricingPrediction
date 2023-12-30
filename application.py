from flask import Flask,request,render_template,jsonify
from src.pipeline.prediction_pipeline import CustomData,PredictPipeline


application=Flask(__name__)
app=application


@app.route('/')
def home_page():
    return render_template('index.html ')

@app.route('/predict',methods=['GET','POST'])

def predict_datapoint():
    if request.method =='GET':
        return render_template('form.html')
    
    else:
        data=CustomData(
            Country  = request.form.get('Country'),
            Shipment_Mode = request.form.get('Shipment_Mode'),    
            Qauntity_of_pack = int(request.form.get('Qauntity_of_pack')),
            Pack_Price = float(request.form.get('Pack_Price')),         
            Weight_Kg = int(request.form.get('Weight_Kg')),       
            Product_Insurance_USD = float(request.form.get('Product_Insurance_USD'))
        )
        final_new_data=data.get_data_as_dataframe()
        predict_pipeline=PredictPipeline()
        pred=predict_pipeline.predict(final_new_data)

        results=pred

        return render_template('results.html',final_result=results)
    
    




if __name__=='__main__':
    app.run(host='0.0.0.0')