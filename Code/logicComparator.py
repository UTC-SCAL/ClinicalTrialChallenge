import pandas

# Read in the patient data
patientData = pandas.read_csv("../SMC Challenge 6/Dataset 2 Simplified.csv")
# The eligibility file you want to compare against the patient data
# eligibilityFile = pandas.read_excel("../SMC Challenge 6/eligibility criteria/Dataset1_WBC_Trials_First.xlsx")
eligibilityFile = pandas.read_excel("../SMC Challenge 6/eligibility criteria/Dataset1_Prior_Therapy_Trials_First.xlsx")
# eligibilityFile = pandas.read_excel("../SMC Challenge 6/eligibility criteria/Dataset1_Platelets_Trials_First.xlsx")
eligibilityFile.NCIT = eligibilityFile.NCIT.astype(str)
# Dataframe to save any matches
matchResults = pandas.DataFrame(columns=["NCI_ID", "NCT_ID", "Patient_ID"])
# Position marker for the match dataframe
matchRow = 0

for i, _ in enumerate(patientData.values[0:1]):
    print("Patient " + str(i+1) + "/" + str(len(patientData)))
    for j, _ in enumerate(eligibilityFile.values):
        # Skip over our empties
        if eligibilityFile.NCIT.values[j] != "nan":
            # LogicList is going to be the eligibility identifier for our patients
            logicNum = 0
            logicList = []
            ncitString = eligibilityFile.NCIT.values[j]
            # Iterate through the file's NCIT value, which contain the logical operators for seeing if a patient
            # is eligible for a treatment
            # Basically, we want a list version of the eligibility logic, with each cell in the list being it's
            # own fragment of the logical statement
            for word in ncitString.split():
                if "(" in word:
                    logicList.append(word)
                elif "AND" or "OR" in word:
                    logicList.append(word)
                else:
                    logicList[logicNum] = logicList[logicNum] + word
                    logicNum += 1
            for k in range(0, len(logicList)):
                if 'and' in logicList[k] or 'or' in logicList[k]:
                    continue
                # Keep beginning and ending parenthesis values for assisting in logical ordering later
                beginParenth = ""
                endParenth = ""
                # Have these two statement to remove the parenthesis of the values we cover in the logic list
                # We remove the parenthesis at first for the individual value comparisons (each cell in the logicList),
                # then add them later for the evaluation of the whole statement (the whole logicList)
                if "(" in logicList[k]:
                    openParenthCounter = logicList[k].count("(")
                    logicList[k] = logicList[k].replace("(", "")
                    beginParenth = "(" * openParenthCounter
                if ")" in logicList[k]:
                    closeParenthCounter = logicList[k].count(")")
                    logicList[k] = logicList[k].replace(")", "")
                    endParenth = ")" * closeParenthCounter
                # Code is the medical code for the eligibility file that represents some value
                # (age, treatment type, etc)
                # Value is the numerical value associated with the code
                # compOp is the <, >, <=, >=, or = present in the statement
                code = ""
                value = ""
                compOp = ""
                if ">=" in logicList[k]:
                    code = logicList[k].split(">=")[0]
                    value = logicList[k].split(">=")[1]
                    compOp = ">="
                elif "<=" in logicList[k]:
                    code = logicList[k].split("<=")[0]
                    value = logicList[k].split("<=")[1]
                    compOp = "<="
                elif "<" in logicList[k]:
                    code = logicList[k].split("<")[0]
                    value = logicList[k].split("<")[1]
                    compOp = "<"
                elif ">" in logicList[k]:
                    code = logicList[k].split(">")[0]
                    value = logicList[k].split(">")[1]
                    compOp = ">"
                elif "=" in logicList[k]:
                    code = logicList[k].split("=")[0]
                    value = logicList[k].split("=")[1]
                    compOp = "=="
                # After we get the logical operator, the code, and the value, we get into the meat and potatoes
                # These 6 if/elif statements are used to check values according to the 5 static codes in the patient
                # records (age, wbc, gender, hb count, & platelet count)
                # Because those variables always use the same codes, we can simply hard code the conditionals for them
                # print(logicList)
                if "C25150" in code:  # age
                    if eval(str(patientData.AGE.values[i]) + compOp + str(value)):
                        logicList[k] = beginParenth + "True" + endParenth
                    else:
                        logicList[k] = beginParenth + "False" + endParenth
                elif "C51948" in code:  # WBC
                    if eval(str(patientData.WBC.values[i]) + compOp + str(value)):
                        logicList[k] = beginParenth + "True" + endParenth
                    else:
                        logicList[k] = beginParenth + "False" + endParenth
                elif "C46110" in code:  # Gender = Female
                    if "C46110" in patientData.Gender_Bool.values[i]:
                        logicList[k] = beginParenth + "True" + endParenth
                    else:
                        logicList[k] = beginParenth + "False" + endParenth
                elif "C46109" in code:  # Gender = Male
                    if "C46109" in patientData.Gender_Bool.values[i]:
                        logicList[k] = beginParenth + "True" + endParenth
                    else:
                        logicList[k] = beginParenth + "False" + endParenth
                elif "C64848" in code:  # HB Count
                    if eval(str(patientData.HB_Count.values[i]) + compOp + str(value)):
                        logicList[k] = beginParenth + "True" + endParenth
                    else:
                        logicList[k] = beginParenth + "False" + endParenth
                elif "C51951" in code:  # Platelet Count
                    if eval(str(patientData.Platelet_Count.values[i]) + compOp + str(value)):
                        logicList[k] = beginParenth + "True" + endParenth
                    else:
                        logicList[k] = beginParenth + "False" + endParenth
                else:
                    # Now, we have to check the other 4 variables in the patient records used for trial matching
                    # (Cancer_Site_Bool, Cancer_Stage_Bool, Treatment_History_Bool, and PS_Bool)
                    # Create termCheck to see if the current logicList has the code we're looking at
                    codeFound = False
                    line_copy = list(patientData.values[i].copy())
                    if str(code) in line_copy:
                        colName = ''
                        colList = list(patientData.columns)
                        for elem in line_copy:
                            if str(code) in str(elem):
                                codeFound = True
                                colNum = line_copy.index(elem)
                                colName = colList[colNum]
                                break
                        if codeFound is True:
                            if 'Cancer_Site_Bool' in str(colName):
                                if str(code) in str(patientData.Cancer_Site_Bool.values[i]):
                                    logicList[k] = beginParenth + "True" + endParenth
                                else:
                                    logicList[k] = beginParenth + "False" + endParenth
                            elif 'Cancer_Stage_Bool' in str(colName):
                                if str(code) in str(patientData.Cancer_Stage_Bool.values[i]):
                                    logicList[k] = beginParenth + "True" + endParenth
                                else:
                                    logicList[k] = beginParenth + "False" + endParenth
                            elif 'Treatment_History_Bool' in str(colName):
                                if str(code) in str(patientData.Treatment_History_Bool.values[i]):
                                    logicList[k] = beginParenth + "True" + endParenth
                                else:
                                    logicList[k] = beginParenth + "False" + endParenth
                            elif 'PS_Bool' in str(colName):
                                if (str(code) + compOp + str(value)) is str(patientData.Treatment_History_Bool.values[i]):
                                    logicList[k] = beginParenth + "True" + endParenth
                                else:
                                    logicList[k] = beginParenth + "False" + endParenth
                            else:
                                print("Finding the column name went wrong")
                                print("List:", logicList)
                                print("Col Name: ", colName)
                                exit()
                    else:
                        logicList[k] = beginParenth + "False" + endParenth

            # How do we want to go about joining all of the different trials? Since some of the different eligibility
            # datasets have the same trial ID, do we want to differentiate per trial?
            # patientTrialEvaluation = eval(" ".join(logicList))
            patientTrialEvaluation = " ".join(logicList)
            print("Row: ", j, ":", patientTrialEvaluation)
            patientTrialEvaluation = eval(patientTrialEvaluation)
            if patientTrialEvaluation and ("Inclusion" in eligibilityFile.inclusion_indicator.values[j]):
                matchResults.at[matchRow, "NCI_ID"] = eligibilityFile.nci_id.values[j]
                matchResults.at[matchRow, "NCT_ID"] = eligibilityFile.nct_id.values[j]
                matchResults.at[matchRow, "Patient_ID"] = patientData.PatientID.values[i]
                matchRow += 1

matchResults.to_csv("../SMC Challenge 6/Prior Therapy Match Test 2.csv", index=False)
