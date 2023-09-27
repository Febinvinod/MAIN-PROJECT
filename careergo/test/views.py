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




# Create your views here.
def assessment(request):

    model = joblib.load('model/naive_bayessss.pkl')
    user = request.user
    exist=StudentAssessment.objects.filter(student_id=user.id,assessment_status=True).exists()
    print(user)
    print(exist)
    
    if request.method == 'POST':
        # Get the logged-in user (assuming you're using authentication)
        

        # Retrieve the assessment scores from the request (update these values accordingly)
        logical_reasoning_score = int(request.POST.get('category_logical_reasoning_score', 0))
        communication_skills_score = int(request.POST.get('category_communication_skills_score', 0))
        quantitative_aptitude_score = int(request.POST.get('category_quantitative_aptitude_score', 0))
        analytical_skills_score = int(request.POST.get('category_analytical_skills_score', 0))
        # Retrieve the stream and Plus Two CGPA from the request
        stream = request.POST.get('stream', None)
        plus_two_cgpa = request.POST.get('plus-two-cgpa', None)

        # label_encoder = LabelEncoder()
        
        # stream_encoded = label_encoder.fit_transform([stream])
        stream_mapping = {
            'Science': 8,
            'Commerce': 6,
            'Humanities': 5,
        }
        stream_numeric = stream_mapping.get(stream, 0)

        input_data = pd.DataFrame({
        'Logical Reasoning': [logical_reasoning_score],
        'Communication Skills': [communication_skills_score],
        'Quantitative Skills': [quantitative_aptitude_score],
        'Analytical Skills': [analytical_skills_score],
        'High School CGPA': [plus_two_cgpa],
        'Stream_Point' : [stream_numeric],
    })
        print({logical_reasoning_score})
        print({quantitative_aptitude_score})
        print({stream_numeric})

       

        # Create or update the StudentAssessment record for the user
        assessment, created = StudentAssessment.objects.get_or_create(student=user)
        assessment.logical_reasoning_score = logical_reasoning_score
        assessment.communication_skills_score = communication_skills_score
        assessment.quantitative_aptitude_score = quantitative_aptitude_score
        assessment.analytical_skills_score = analytical_skills_score
        assessment.stream = stream
        assessment.plus_two_cgpa = plus_two_cgpa
        assessment.assessment_status = True
        assessment.save()

        # predicted_course = model.predict(input_data)[0]
        # print(f"Predicted Course: {predicted_course}")
        # response_data = {'predicted_course': predicted_course}
        # return JsonResponse(response_data)
        N = 3
        predicted_probabilities = model.predict_proba(input_data)[0]
        sorted_courses = sorted(zip(model.classes_, predicted_probabilities), key=lambda x: -x[1])
        top_n_recommendations = [course for course, _ in sorted_courses[:N]]
        response_data = {'recommended_courses': top_n_recommendations, }
        #return render(request, 'assesment.html', context=response_data)
        return JsonResponse(response_data)
    


    return render(request, 'assesment.html',{'assessment_status':exist}) # Replace 'assessment_success' with your success page URL

    # return render(request, 'assesment.html')

def coursess(request):
    courses = course.objects.all() 
    return render(request, 'course.html', {'courses': courses})




