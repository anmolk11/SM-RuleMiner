import openpyxl
import datetime
import os

cutoff = 0.5

testing = ["Time","P_avg","P_best","N_avg","N_best"]

rules = ["Date Time", "Pregnancies_flag" ,"Pregnancies_lb","Pregnancies_ub","Glucose_flag","Glucose_lb","Glucose_ub","BP_flag","BP_lb","BP_ub","SkinThickness_flag","SkinThickness_lb","SkinThickness_ub","Insulin_flag","Insulin_lb","Insulin_ub","BMI_flag","BMI_lb","BMI_ub","DPF_flag","DPF_lb","DPF_ub","Age_flag","Age_lb","Age_ub","Class","Hit Ratio"]

def logTesting(p_ave,p_best,n_ave,n_best,file_name):
    file_name = "Logs/" + file_name + ".xlsx"

    if os.path.exists(file_name) == False:
       workbook = openpyxl.Workbook()
       sheet = workbook.active
       sheet.append(testing) 
    else:
        workbook = openpyxl.load_workbook(file_name)
        sheet = workbook.active
    
    now = datetime.datetime.now()
    current_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    sheet.append([current_date_time, p_ave,p_best,n_ave,n_best])
    workbook.save(file_name)

def logRules(attr,sign,hit_ratio,file_name):
    file_name = "Logs/" + file_name + ".xlsx"


    if os.path.exists(file_name) == False:
       workbook = openpyxl.Workbook()
       sheet = workbook.active
       sheet.append(rules) 
    else:
        workbook = openpyxl.load_workbook(file_name)
        sheet = workbook.active

    now = datetime.datetime.now()
    current_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    
    for i in range(len(attr)):
        if i % 3 == 0:
            if attr[i] >= cutoff:
                attr[i] = 1
            else:
                attr[i] = 0
    for i in range(1,len(attr),3):
        mx = max(attr[i],attr[i + 1])
        mn = min(attr[i],attr[i + 1])
        attr[i] = mn
        attr[i + 1] = mx
        
    sheet.append([current_date_time] + attr + [sign,hit_ratio])
    workbook.save(file_name)