import pandas

patientData = pandas.read_csv("../SMC Challenge 6/Dataset 2 Simplified.csv")
eligibilityFile = pandas.read_excel("../SMC Challenge 6/eligibility criteria/Dataset1_WBC_Trials_First.xlsx")
eligibilityFile.NCIT = eligibilityFile.NCIT.astype(str)
matchResults = pandas.DataFrame(columns=["NCI_ID", "NCT_ID", "Patient_ID"])
matchRow = 0

for i, _ in enumerate(patientData.values[0:2]):
    for j, _ in enumerate(eligibilityFile.values):
        if eligibilityFile.NCIT.values[j].count("(") > 1:
            continue
        if "C51948" in eligibilityFile.NCIT.values[j]:
            patientWBC = patientData.WBC.values[i]
            if ">=" in eligibilityFile.NCIT.values[j]:
                eligibleWBC = eligibilityFile.NCIT.values[j].split("=")[1].split("/")[0]
                if patientWBC >= int(eligibleWBC):
                    matchResults.at[matchRow, "NCI_ID"] = "WBC_" + eligibilityFile.nci_id.values[j]
                    matchResults.at[matchRow, "NCT_ID"] = "WBC_" + eligibilityFile.nct_id.values[j]
                    matchResults.at[matchRow, "Patient_ID"] = patientData.PatientID.values[i]
                    matchRow += 1
            elif "<=" in eligibilityFile.NCIT.values[j]:
                eligibleWBC = eligibilityFile.NCIT.values[j].split("=")[1].split("/")[0]
                if patientWBC <= int(eligibleWBC):
                    matchResults.at[matchRow, "NCI_ID"] = "WBC_" + eligibilityFile.nci_id.values[j]
                    matchResults.at[matchRow, "NCT_ID"] = "WBC_" + eligibilityFile.nct_id.values[j]
                    matchResults.at[matchRow, "Patient_ID"] = patientData.PatientID.values[i]
                    matchRow += 1

matchResults.to_csv("../SMC Challenge 6/WBC Match Test.csv", index=False)
