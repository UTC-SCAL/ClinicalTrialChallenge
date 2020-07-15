#!/usr/bin/env python
# coding: utf-8

# In[34]:


import pandas as pd
import json
import texthero as hero
from texthero import preprocessing
from sklearn.cluster import AgglomerativeClustering
import numpy as np
import seaborn as sns
import nltk, string, numpy as np


# In[ ]:


filename =r'C:\Users\Sree\Documents\clinical_challange\APIResponse_401_500.json'


# In[ ]:


with open(filename, 'r', encoding='utf-8') as f:
  
    # returns JSON object as  
    # a dictionary 
    data = json.load(f) 


# In[ ]:


output_dict={}


# In[ ]:


for key,val in data['FullStudiesResponse'].items():
#     for studies in fstudy['FullStudies']:
    if key=='FullStudies':
        for row in val:
            for rkey, rval in row.items():
                if rkey=='Study':
                    for irow, ival in rval.items():
                        for iirow, iival in ival.items():
                            if iirow =='EligibilityModule':
                                output_dict[ival['IdentificationModule']['NCTId']]=iival['EligibilityCriteria']
                    


# In[ ]:


df = pd.DataFrame(output_dict.items())


# In[ ]:


df = df.rename(columns={0:'NCTId'})


# In[ ]:


df= pd.merge(df, df[1].str.split('\n\n', n=3, expand=True), right_index=True, left_index=True,suffixes=('','_y'))


# In[ ]:


df= df[df[0]=='Inclusion Criteria:']


# In[ ]:


df= df[df[2]=='Exclusion Criteria:']


# In[ ]:


df = df.drop(['1',0,2], axis=1)


# In[ ]:


df = df.rename(columns={'1_y':'Inclusion', 3:'Exclusion'})


# In[ ]:


df['description'] = df['Inclusion'] + df['Exclusion']


# In[ ]:


df.to_csv('trials_401_500.csv', index=False)


# In[3]:


trial1=pd.read_csv('trials_1_100.csv')


# In[4]:


trial2=pd.read_csv('trials_101_200.csv')


# In[5]:


trial3=pd.read_csv('trials_201_300.csv')


# In[6]:


trial4=pd.read_csv('trials_301_400.csv')


# In[7]:


trial5=pd.read_csv('trials_401_500.csv')


# In[8]:


description=pd.concat([trial1,trial2,trial3,trial4,trial5]).reset_index()


# In[9]:


description.tail()


# In[10]:


description.drop(['Inclusion', 'Exclusion','index'],axis=1)


# https://towardsdatascience.com/natural-language-processing-count-vectorization-with-scikit-learn-e7804269bb5e
# 
# https://sites.temple.edu/tudsc/2017/03/30/measuring-similarity-between-texts-in-python/ (cosin similarity)
# 
# https://towardsdatascience.com/machine-learning-text-processing-1d5a2d638958
# 
# https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4119097/
# 
# https://dataconomy.com/2015/04/implementing-the-five-most-popular-similarity-measures-in-python/  (jaccard similarity)
# 
# https://machinelearningmastery.com/clean-text-machine-learning-python/#:~:text=Python%20offers%20a%20function%20called,set%20of%20characters%20to%20another.&text=We%20can%20put%20all%20of,word%20to%20remove%20the%20punctuation. (remove puntuations)
# 
# https://nlp.stanford.edu/IR-book/html/htmledition/hierarchical-agglomerative-clustering-1.html#:~:text=Bottom%2Dup%20hierarchical%20clustering%20is,until%20individual%20documents%20are%20reached.(aggolmatarive algoritm steps)
# 
# http://rstudio-pubs-static.s3.amazonaws.com/265632_3ad9e0b981244e15887677f8dffb39a0.html (methods for optimal clusters)

# # Text Hero

# Text cleaning

# In[11]:


custom_pipeline = [preprocessing.fillna,
                   preprocessing.lowercase,
                   preprocessing.remove_whitespace,
                  preprocessing.remove_punctuation,
                  preprocessing.remove_angle_brackets,
                  preprocessing.remove_brackets,
                  preprocessing.remove_round_brackets,
                  preprocessing.remove_html_tags,
                  preprocessing.remove_stopwords
                  ]
description['clean_text'] = description['description'].pipe(hero.clean,custom_pipeline)


# In[13]:


#Normalize by lemmatization:

nltk.download('wordnet') # first-time use only
lemmer = nltk.stem.WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


# Jaccard Similarity

# In[14]:


from sklearn.metrics import pairwise_distances
from sklearn.feature_extraction.text import TfidfVectorizer
TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
def jaccard_similarity(textlist):
    tfidf = TfidfVec.fit_transform(textlist)
    tfidf =tfidf.toarray()
    return pairwise_distances(tfidf,metric='jaccard')
X=jaccard_similarity(description['clean_text'])


# In[15]:


description['tfidf'] = pd.Series(list(X))


# In[16]:


test = [1,2,3,4,5,6,7]
[i for i in test if i >5]


# ## Threshold is set to0.8 lenght of list is not the same in each row in the fig.so unbale to apply this to clusters

# In[17]:


def get_threshold_list(x):
    x = x[x>0.8]
    return x


# In[18]:


description ['tfidf_threshold'] = pd.Series(description['tfidf'].apply(get_threshold_list))


# In[19]:


description


# In[20]:


type(description['tfidf'].values)


# In[21]:


type(X)


# aggolmorative algorithm

# In[22]:


hc = AgglomerativeClustering(n_clusters = 15, affinity = 'euclidean', linkage ='ward')
# Lets try to fit the hierarchical clustering algorithm  to dataset #X while creating the clusters vector that tells for each customer #which cluster the customer belongs to.
y_hc=hc.fit_predict(X)


# In[23]:




description['cluster']=y_hc.astype(str)


# In[24]:


description.groupby(['cluster']).count()


# Principal conponant analysis for dimentionality reduction. we have 331 value but cannot plot 331 valyes. so reducing it to 2 dimentional plot by keeping the meaning same

# In[29]:


description['pca'] = description['tfidf'].pipe(hero.pca)


# In[32]:


hero.scatterplot(description, 'pca', color='cluster', title="Clinical trial clusters",hover_data=['NCTId'])


# In[33]:


description.to_csv('clusteroutput.csv', index=False)


# In[42]:


patient=pd.read_csv('Trial Match Master File.csv')


# In[43]:


patient.head()


# In[47]:


patient_new=patient.rename({'NCT_ID':'NCTId'}, axis=1)


# In[48]:


patient_new.head()


# In[52]:


df_patient = pd.merge(patient_new, description, on='NCTId')


# In[54]:


df_patient.head(10)


# In[56]:


given_data=pd.read_csv('Dataset1_Hemoglobin_Trials_First.csv')


# In[61]:


given_data.head()


# In[64]:


given_data_new=given_data.rename({'nct_id':'NCTId'}, axis=1)
given_data_new.head()


# In[66]:


df_patient_new = pd.merge(patient_new, given_data_new, on='NCTId')


# In[68]:


given_data_new


# In[ ]:




