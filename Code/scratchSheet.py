import pandas

data = pandas.read_csv("../SMC Challenge 6/Trial Match Master File.csv")
patient = 1
nciList = []
nctList = []
saveFrame = pandas.DataFrame(columns=["PatientID", "NCI_ID", "NCT_ID"])
for i, _ in enumerate(data.values):
    if data.Patient_ID.values[i] == patient:
        nciList.append(data.NCI_ID.values[i])
        nctList.append(data.NCT_ID.values[i])
    if data.Patient_ID.values[i+1] != patient:
        saveFrame.at[patient - 1, "PatientID"] = patient
        saveFrame.at[patient - 1, "NCI_ID"] = nciList
        saveFrame.at[patient - 1, "NCT_ID"] = nctList
        patient += 1
        nciList = []
        nctList = []
        if patient > 100:
            break
saveFrame.to_csv("../SMC Challenge 6/Trial Match Simplified.csv", index=False)
