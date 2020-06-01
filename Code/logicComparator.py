import pandas
from distutils.util import strtobool

patientData = pandas.read_csv("../SMC Challenge 6/Dataset 2 Simplified.csv")
eligibilityFile = pandas.read_excel("../SMC Challenge 6/eligibility criteria/Dataset1_WBC_Trials_First.xlsx")
eligibilityFile.NCIT = eligibilityFile.NCIT.astype(str)
matchResults = pandas.DataFrame(columns=["NCI_ID", "NCT_ID", "Patient_ID"])
matchRow = 0

for i, _ in enumerate(patientData.values[0:1]):
    for j, _ in enumerate(eligibilityFile.values):
        if eligibilityFile.NCIT.values[j] != "nan":
            logicNum = 0
            logicList = []
            my_string = eligibilityFile.NCIT.values[j]
            for word in my_string.split():
                # print(word)
                if "(" in word:
                    logicList.append(word)
                elif "AND" or "OR" in word:
                    logicList.append(word)
                else:
                    logicList[logicNum] = logicList[logicNum] + word
                    logicNum += 1
            print(logicList)
            for k in range(0, len(logicList)):
                # Keep beginning and ending parenthesis values for assisting in logical ordering later
                beginParenth = ""
                endParenth = ""
                # Have these two statement to remove the parenthesis of the values we cover in the logic list
                if "(" in logicList[k]:
                    logicList[k] = logicList[k].replace("(", "")
                    beginParenth = "("
                if ")" in logicList[k]:
                    logicList[k] = logicList[k].replace(")", "")
                    endParenth = ")"
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
                if "C25150" in code:
                    if eval(str(patientData.AGE.values[i]) + compOp + str(value)):
                        logicList[k] = beginParenth + "True" + endParenth
                    else:
                        logicList[k] = beginParenth + "False" + endParenth
                elif "C8644" in code:
                    if "C8644" in str(patientData.Cancer_Site_Bool.values[i]):
                        logicList[k] = beginParenth + "True" + endParenth
                    else:
                        logicList[k] = beginParenth + "False" + endParenth
                elif "C51948" in code:
                    if eval(str(patientData.WBC.values[i]) + compOp + str(value)):
                        logicList[k] = beginParenth + "True" + endParenth
                    else:
                        logicList[k] = beginParenth + "False" + endParenth
                elif "C5440" in code:
                    if "C5440" in str(patientData.Cancer_Site_Bool.values[i]):
                        logicList[k] = beginParenth + "True" + endParenth
                    else:
                        logicList[k] = beginParenth + "False" + endParenth
                elif "C9277" in code:
                    if "C9277" in str(patientData.Cancer_Site_Bool.values[i]):
                        logicList[k] = beginParenth + "True" + endParenth
                    else:
                        logicList[k] = beginParenth + "False" + endParenth
                elif "C15370" in code:
                    if "C15370" in str(patientData.Treatment_History_Boolean.values[i]):
                        logicList[k] = beginParenth + "True" + endParenth
                    else:
                        logicList[k] = beginParenth + "False" + endParenth
            print(eval(" ".join(logicList)))
            # exit()
                # s1 = "0"
                # s2 = "1"
                # print(strtobool(s1) or strtobool(s2))

        # if "C51948" in eligibilityFile.NCIT.values[j]:
        #     patientWBC = patientData.WBC.values[i]
        #     if ">=" in eligibilityFile.NCIT.values[j]:
        #         eligibleWBC = eligibilityFile.NCIT.values[j].split("=")[1].split("/")[0]
        #         if patientWBC >= int(eligibleWBC):
        #             matchResults.at[matchRow, "NCI_ID"] = "WBC_" + eligibilityFile.nci_id.values[j]
        #             matchResults.at[matchRow, "NCT_ID"] = "WBC_" + eligibilityFile.nct_id.values[j]
        #             matchResults.at[matchRow, "Patient_ID"] = patientData.PatientID.values[i]
        #             matchRow += 1
        #     elif "<=" in eligibilityFile.NCIT.values[j]:
        #         eligibleWBC = eligibilityFile.NCIT.values[j].split("=")[1].split("/")[0]
        #         if patientWBC <= int(eligibleWBC):
        #             matchResults.at[matchRow, "NCI_ID"] = "WBC_" + eligibilityFile.nci_id.values[j]
        #             matchResults.at[matchRow, "NCT_ID"] = "WBC_" + eligibilityFile.nct_id.values[j]
        #             matchResults.at[matchRow, "Patient_ID"] = patientData.PatientID.values[i]
        #             matchRow += 1

# matchResults.to_csv("../SMC Challenge 6/WBC Match Test.csv", index=False)
