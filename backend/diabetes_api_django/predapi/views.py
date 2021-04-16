from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
import pandas as pd
import numpy as np
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from predapi.apps import PredapiConfig

# Create your views here.
# Class based view to predict based on diabetes model
class Diabetes_Model_Predict(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        data_dict = request.data

        print("Recieved Data: ",data_dict)

        keys=[]
        values=[]
        for key in data_dict:
            keys.append(key)
            values.append(data_dict[key])
        
        values_nparray = np.array(values)
     
        # load scaler
        scaler = PredapiConfig.scaler
      
        scaled_data = scaler.transform(values_nparray.reshape(1,-1))
    

        prediction = PredapiConfig.classifier.predict(scaled_data)

        y_pred = pd.Series(prediction)
        target_map = {0: 'No Diabetes', 1: 'Diabetes Detected'}
        y_pred = y_pred.map(target_map).to_numpy()
        response_dict = {"Prediced Diabetes status": y_pred[0]}

        print("\nPrediction Result: ",response_dict)

        return Response(response_dict, status=200)