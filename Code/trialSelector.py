import pandas

hemoFile = pandas.read_excel("../SMC Challenge 6/eligibility criteria/Dataset1_Hemoglobin_Trials_First.xlsx")
hivFile = pandas.read_excel("../SMC Challenge 6/eligibility criteria/Dataset1_HIV_Trials_First.xlsx")
plateletFile = pandas.read_excel("../SMC Challenge 6/eligibility criteria/Dataset1_Platelets_Trials_First.xlsx")
therapyFile = pandas.read_excel("../SMC Challenge 6/eligibility criteria/Dataset1_Prior_Therapy_Trials_First.xlsx")
psFile = pandas.read_excel("../SMC Challenge 6/eligibility criteria/Dataset1_Performance_Status_Trials_First.xlsx")
wbcFile = pandas.read_excel("../SMC Challenge 6/eligibility criteria/Dataset1_WBC_Trials_First.xlsx")

patientTrialsSelected = pandas.DataFrame(columns=["Patient_ID", "Mode_Trial", "Unique_Trials"])
masterFile = pandas.read_csv("../SMC Challenge 6/Trial Match Master File.csv")
matchLoc = 0

for i in range(1, 101):
    print("Patient: ", i)
    patientSelect = masterFile[masterFile['Patient_ID'] == i]
    matchList = 0
    uniqueNCI = []
    for elem in patientSelect.NCI_ID.unique():
        if elem in hemoFile.nci_id.values:
            matchList += 1
        if elem in hivFile.nci_id.values:
            matchList += 1
        if elem in plateletFile.nci_id.values:
            matchList += 1
        if elem in therapyFile.nci_id.values:
            matchList += 1
        if elem in psFile.nci_id.values:
            matchList += 1
        if elem in wbcFile.nci_id.values:
            matchList += 1
        if matchList == 1:
            uniqueNCI.append(elem)
        matchList = 0
    nciCounts = patientSelect.NCI_ID.value_counts()

    patientTrialsSelected.at[matchLoc, "Patient_ID"] = i
    patientTrialsSelected.at[matchLoc, "Mode_Trial"] = nciCounts.index[0]
    patientTrialsSelected.at[matchLoc, "Unique_Trials"] = uniqueNCI
    matchLoc += 1

patientTrialsSelected.to_csv("../SMC Challenge 6/Selected Patient Trials.csv", index=False)


