from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.staticfiles.storage import staticfiles_storage
from .forms import ContactUsForm, CreateUserForm
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
import os


def home(request):
    context = {}
    context['contact_form'] = ContactUsForm()
    context['anchor'] = None
    context['contact_error'] = None
    context['prediction_error'] = None
    context['can_give_loan'] = None
    context['login_error'] = None
    context['register_error'] = None

    if request.method == 'POST':
        if request.POST.get('form_name') == "contact_form":
            context['anchor'] = "Contact"
            contact_form = ContactUsForm(request.POST)
            if contact_form.is_valid():
                contact_form.save()
                context['contact_error'] = False
            else:
                context['contact_error'] = True
        elif request.POST.get('form_name') == "predicton_form":
            context['anchor'] = "Predictor"
            result, error = predict(request.POST)
            context['prediction_error'] = True if result == None else False
            context['can_give_loan'] = result
        elif request.POST.get('form_name') == "register":
            user = CreateUserForm(request.POST)
            if user.is_valid():
                user.save()
                username = request.POST.get('username')
                password = request.POST.get('password1')

                user = authenticate(
                    request, username=username, password=password)
                login(request, user)
                context['anchor'] = ""
            else:
                context['register_error'] = True
        elif request.POST.get('form_name') == "login":
            username = request.POST.get('username1')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                context['anchor'] = ""
            else:
                context['login_error'] = True

    return render(request, 'index.html', context)


def logOut(request):
    logout(request)
    return redirect('home')


def predict(request):
    # df = pd.read_csv("data.csv")
    # df = df.dropna()
    # df = df.iloc[:, 1:]
    # df.to_csv('cleanedDataset.csv', index = False, header = True)
    df = pd.read_csv(staticfiles_storage.path("cleanedDataset.csv"))

    # OneHotEncoder part
    headers = ["Gender", "Married", "Dependents", "Education", "Self_Employed", "ApplicantIncome",
               "CoapplicantIncome", "LoanAmount", "Loan_Amount_Term", "Credit_History", "Property_Area"]
    categoricalHeaders = ["Gender", "Married",
                          "Education", "Self_Employed", "Property_Area"]
    X = df.iloc[:, :-1]
    columnTransformer = ColumnTransformer(
        [('encoder', OneHotEncoder(), categoricalHeaders)], remainder='passthrough')
    X = np.array(columnTransformer.fit_transform(X))
    y = df["Loan_Status"].map({'Y': 1, 'N': 0})
    # StandardScaler part
    sc = StandardScaler()
    X = sc.fit_transform(X)
    # DecisionTreeClassifier part
    classifier = DecisionTreeClassifier(criterion='entropy', random_state=0)
    classifier.fit(X, y)

    try:
        arr = [request["gender"], request["married"], request["dependents"], request["education"], request["self_Employed"],
               request["applicant_income"], request["coapplicant_income"], request["loan_amount"], request["loan_amount_term"],
               request["credit_history"], request["property_area"]]
        X_test = pd.DataFrame(np.array([arr]), columns=headers)
        X_test = np.array(columnTransformer.transform(X_test))
        X_test = sc.transform(X_test)
        y_pred = classifier.predict(X_test)
        return True if y_pred == 1 else False, None
    except:
        return None, 'Give the correct values for the respective category'
