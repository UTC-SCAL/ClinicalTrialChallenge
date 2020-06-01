import pandas

# Read in the patient data
patientData = pandas.read_csv("../SMC Challenge 6/Dataset 2 Simplified.csv")
# The eligibility file you want to compare against the patient data
eligibilityFile = pandas.read_excel("../SMC Challenge 6/eligibility criteria/Dataset1_WBC_Trials_First.xlsx")
eligibilityFile.NCIT = eligibilityFile.NCIT.astype(str)
# Dataframe to save any matches
matchResults = pandas.DataFrame(columns=["NCI_ID", "NCT_ID", "Patient_ID"])
# Position marker for the match dataframe
matchRow = 0

for i, _ in enumerate(patientData.values):
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
            # print(logicList)
            for k in range(0, len(logicList)):
                # Keep beginning and ending parenthesis values for assisting in logical ordering later
                beginParenth = ""
                endParenth = ""
                # Have these two statement to remove the parenthesis of the values we cover in the logic list
                # We remove the parenthesis at first for the individual value comparisons (each cell in the logicList),
                # then add them later for the evaluation of the whole statement (the whole logicList)
                if "(" in logicList[k]:
                    logicList[k] = logicList[k].replace("(", "")
                    beginParenth = "("
                if ")" in logicList[k]:
                    logicList[k] = logicList[k].replace(")", "")
                    endParenth = ")"
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
                elif 'AND' in logicList[k] or "OR" in logicList[k]:
                    # convert uppercase ands and ors to lowercase for logical use later
                    logicList[k] = logicList[k].lower()
                # After we get the logical operator, the code, and the value, we get into the meat and potatoes
                if "C25150" in code:  # age
                    if eval(str(patientData.AGE.values[i]) + compOp + str(value)):
                        logicList[k] = beginParenth + "True" + endParenth
                    else:
                        logicList[k] = beginParenth + "False" + endParenth
                elif "C8644" in code:  # B Acute Lymphoblastic Leukemia
                    if "C8644" in str(patientData.Cancer_Site_Bool.values[i]):
                        logicList[k] = beginParenth + "True" + endParenth
                    else:
                        logicList[k] = beginParenth + "False" + endParenth
                elif "C51948" in code:  # WBC
                    if eval(str(patientData.WBC.values[i]) + compOp + str(value)):
                        logicList[k] = beginParenth + "True" + endParenth
                    else:
                        logicList[k] = beginParenth + "False" + endParenth
                elif "C5440" in code:  # Central Nervous System Leukemia
                    if "C5440" in str(patientData.Cancer_Site_Bool.values[i]):
                        logicList[k] = beginParenth + "True" + endParenth
                    else:
                        logicList[k] = beginParenth + "False" + endParenth
                elif "C9277" in code:  # Testicular Leukemia
                    if "C9277" in str(patientData.Cancer_Site_Bool.values[i]):
                        logicList[k] = beginParenth + "True" + endParenth
                    else:
                        logicList[k] = beginParenth + "False" + endParenth
                elif "C15370" in code:  # Steroid Therapy
                    if "C15370" in str(patientData.Treatment_History_Boolean.values[i]):
                        logicList[k] = beginParenth + "True" + endParenth
                    else:
                        logicList[k] = beginParenth + "False" + endParenth
            # How do we want to go about joining all of the different trials? Since some of the different eligibility
            # datasets have the same trial ID, do we want to differentiate per trial?
            patientTrialEvaluation = eval(" ".join(logicList))
            if patientTrialEvaluation and ("Inclusion" in eligibilityFile.inclusion_indicator.values[j]):
                matchResults.at[matchRow, "NCI_ID"] = "WBC_" + eligibilityFile.nci_id.values[j]
                matchResults.at[matchRow, "NCT_ID"] = "WBC_" + eligibilityFile.nct_id.values[j]
                matchResults.at[matchRow, "Patient_ID"] = patientData.PatientID.values[i]
                matchRow += 1

# matchResults.to_csv("../SMC Challenge 6/WBC Match Test.csv", index=False)
