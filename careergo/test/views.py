from django.shortcuts import render,redirect,HttpResponse
from .models import StudentAssessment
from .models import course  # Import your Course model
import pandas as pd
#from sklearn.neighbors import KNeighborsClassifier 
import os
from django.conf import settings
import joblib
from home.models import CustomUser
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from sklearn.preprocessing import LabelEncoder
from django.contrib import messages
from sklearn.preprocessing import LabelEncoder
from collections import Counter
import sklearn
# import tabulate




def predict_and_recommend(input_data):
    df = pd.read_csv('model/courses_new_new.csv')
    college_df = pd.read_csv('model/Book1.csv')

    X = df[['Logical Reasoning', 'Communication Skills', 'Quantitative Skills', 'Analytical Skills', 'English', 'Maths', 'Physics', 'Biology', 'Chemistry', 'Accounting','Economics','Business Studies','History','Sociology','Politics','High School CGPA', 'Stream_Point']]
    y = df['Recommended Course']

    # Encode the target labels to numerical values
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    # Make predictions on the input data using individual classifiers
    xgb_classifier = joblib.load('model/xgb_classifier.pkl')
    knn_classifier = joblib.load('model/knn_classifier.pkl')
    svm_classifier = joblib.load('model/svm_classifier.pkl')
    new_data_predictions_xgb = xgb_classifier.predict(input_data)
    new_data_predictions_knn = knn_classifier.predict(input_data)
    new_data_predictions_svm = svm_classifier.predict(input_data)
    
    
    # Combine the predictions using majority voting for the new data
    ensemble_predictions = []
    for i in range(len(input_data)):
        predictions = [new_data_predictions_xgb[i], new_data_predictions_knn[i], new_data_predictions_svm[i]]
        majority_vote = Counter(predictions).most_common(1)[0][0]
        ensemble_predictions.append(majority_vote)

    # Convert the predicted label back to its original class label
    predictions = [new_data_predictions_xgb[0], new_data_predictions_knn[0], new_data_predictions_svm[0]]
    top_three = [x[0] for x in Counter(predictions).most_common(3)]

    predicted_courses = label_encoder.inverse_transform(top_three)
    # print(f"Recommended Course for new data: {predicted_course[0]}")

    # Get the predicted course from your model
    recommended_courses = list(predicted_courses)

    # Filter recommended colleges based on the predicted course
    recommended_colleges = []
    for predicted_course in recommended_courses:
        colleges_for_course = college_df[college_df['Recommended Course'] == predicted_course]
        recommended_colleges.append(colleges_for_course)
    # Optionally, sort the recommended colleges by NIRF ranking
    sorted_recommended_colleges = [colleges.sort_values(by='NIRF_Ranking_2023') for colleges in recommended_colleges]
    # Select only the college name and NIRF ranking columns
    
    # Take the top five recommended colleges
      

    # print(top_five_colleges)
    

    return recommended_courses,  sorted_recommended_colleges

def assessment(request):
    #predict_and_recommend = joblib.load('model/knn.pkl')
    user = request.user
    exist = StudentAssessment.objects.filter(student_id=user.id, assessment_status=True).exists()
    
    if request.method == 'POST':
        # Retrieve the assessment scores from the request (update these values accordingly)
        logical_reasoning_score = int(request.POST.get('category_logical_reasoning_score', 0))
        communication_skills_score = int(request.POST.get('category_communication_skills_score', 0))
        quantitative_aptitude_score = int(request.POST.get('category_quantitative_aptitude_score', 0))
        analytical_skills_score = int(request.POST.get('category_analytical_skills_score', 0))
        # Retrieve the stream and Plus Two CGPA from the request
        english = int(request.POST.get('english', 0))
        math = int(request.POST.get('math', 0))
        stream = request.POST.get('stream', None)
        science_physics = int(request.POST.get('science_physics', 0))
        science_chemistry = int(request.POST.get('science_chemistry', 0))
        science_biology = int(request.POST.get('science_biology', 0))
        commerce_accounting = int(request.POST.get('commerce_accounting', 0))
        commerce_economics = int(request.POST.get('commerce_economics', 0))
        commerce_business = int(request.POST.get('commerce_business', 0))
        humanities_history = int(request.POST.get('humanities_history', 0))
        humanities_sociology = int(request.POST.get('humanities_sociology', 0))
        humanities_political = int(request.POST.get('humanities_political', 0))
        #stream = request.POST.get('stream', None)
        plus_two_cgpa = float(request.POST.get('plus-two-cgpa', 0))
        total_score = int(request.POST.get('total_score', 0))

        print(logical_reasoning_score)
        print(total_score)

        # Map the stream to a numeric value
        stream_mapping = {
            'Science': 8,
            'Commerce': 6,
            'Humanities': 5,
        }
        stream_numeric = stream_mapping.get(stream, 0)

       
        input_data = [[logical_reasoning_score, communication_skills_score, quantitative_aptitude_score, analytical_skills_score,english,math,science_physics,science_biology, science_chemistry, commerce_accounting, commerce_economics, commerce_business,humanities_history,humanities_sociology,humanities_political, plus_two_cgpa, stream_numeric]]

        recommended_courses,  sorted_recommended_colleges = predict_and_recommend(input_data)


        top_five_colleges = {}
        for i, course in enumerate(recommended_courses):
            top_five_colleges[course] = sorted_recommended_colleges[i][['College', 'NIRF_Ranking_2023']].head(5).to_dict(orient='records')

        print(recommended_courses)
        # print( sorted_recommended_colleges)

        # df=recommended_colleges

        # html_table = df.to_html(classes='table table-bordered', border=5, index=False, escape=False)





        # Create or update the StudentAssessment record for the user
        assessment, created = StudentAssessment.objects.get_or_create(student=user)
        assessment.logical_reasoning_score = logical_reasoning_score
        assessment.communication_skills_score = communication_skills_score
        assessment.quantitative_aptitude_score = quantitative_aptitude_score
        assessment.analytical_skills_score = analytical_skills_score
        assessment.stream = stream
        assessment.plus_two_cgpa = plus_two_cgpa
        assessment.total_score = total_score
        assessment.assessment_status = True
        assessment.save()
    
        context = {
        'assessment_status': exist, 'recommended_course': recommended_courses, 'top_five_colleges':  top_five_colleges,'assessment': assessment,
    }
        

        return render(request, 'result.html', context)

    return render(request, 'assesment.html', {'assessment_status': exist})

    # return render(request, 'assesment.html')

def coursess(request):
    courses = course.objects.all() 
    return render(request, 'course.html', {'courses': courses})

def result(request):
    user = request.user  # Get the currently logged-in user
    assessment = StudentAssessment.objects.get(student=user)

    # Pass the assessment data to the template context
    context = {
        'assessment': assessment,
    }

    return render(request, 'result.html', context)


