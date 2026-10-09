"""Expanded-data, group-disjoint train/validation/test. pip install scikit-learn"""
import csv,io,json,re,hashlib,pathlib,urllib.request,zipfile
import numpy as np
from sklearn.model_selection import GroupShuffleSplit
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix,precision_score,recall_score,f1_score,accuracy_score
R=pathlib.Path(__file__).parent
UCI='https://archive.ics.uci.edu/static/public/228/sms+spam+collection.zip'
IMC='https://raw.githubusercontent.com/reportsmishing/Smishing-Dataset-IMC25/main/dataset/final_dataset_output.csv'
def normalize(text):
 text=re.sub(r'<[^>]+>',' ',text.lower())
 text=re.sub(r'https?://\S+|www\.\S+',' urltoken ',text)
 return re.findall(r'[a-z]+',text)
def template(text):
 # Same normalized opening 8 words stays in one split. Deliberately conservative.
 ts=normalize(text);return ' '.join(ts[:8])
def stats(y,p):
 tn,fp,fn,tp=confusion_matrix(y,p,labels=[0,1]).ravel()
 return dict(true_positive=int(tp),false_positive=int(fp),true_negative=int(tn),false_negative=int(fn),precision=float(precision_score(y,p,zero_division=0)),recall=float(recall_score(y,p)),f1=float(f1_score(y,p)),accuracy=float(accuracy_score(y,p)))
def main():
 u=urllib.request.urlopen(UCI).read();z=zipfile.ZipFile(io.BytesIO(u));im=urllib.request.urlopen(IMC).read()
 raw=[]
 for line in z.read('SMSSpamCollection').decode().splitlines():
  label,text=line.split('\t',1);raw.append((text,int(label=='spam'),'UCI'))
 allim=list(csv.DictReader(io.StringIO(im.decode())))
 english=[x for x in allim if x['language']=='English' and x['text'].strip() and x['scam_type']]
 for x in english:raw.append((x['text'],1,'IMC2025'))
 bykey={};conflicts=set()
 for text,label,source in raw:
  key=' '.join(normalize(text))
  if not key:continue
  if key in bykey and bykey[key][1]!=label:conflicts.add(key)
  else:bykey.setdefault(key,(text,label,source))
 rows=[r for k,r in bykey.items() if k not in conflicts]
 X=np.array([r[0] for r in rows]);y=np.array([r[1] for r in rows]);sources=np.array([r[2] for r in rows]);groups=np.array([template(t) for t in X])
 split=GroupShuffleSplit(n_splits=1,test_size=.2,random_state=42)
 dev,test=next(split.split(X,y,groups));tr,va=next(GroupShuffleSplit(n_splits=1,test_size=.25,random_state=43).split(X[dev],y[dev],groups[dev]));train=dev[tr];val=dev[va]
 assert not set(groups[train])&set(groups[val]);assert not set(groups[dev])&set(groups[test])
 v=TfidfVectorizer(tokenizer=normalize,token_pattern=None,lowercase=False,min_df=2,max_features=20000,sublinear_tf=True)
 a=v.fit_transform(X[train]);b=v.transform(X[val]);c=v.transform(X[test]);candidates=[]
 for name,clf in [('tfidf_logistic',LogisticRegression(C=4,max_iter=1000,class_weight='balanced',random_state=42)),('tfidf_naive_bayes',MultinomialNB(alpha=.5))]:
  clf.fit(a,y[train]);prob=clf.predict_proba(b)[:,1]
  for threshold in [.5,.6,.7,.8,.85,.9,.95]:
   met=stats(y[val],prob>=threshold);fpr=met['false_positive']/max(1,met['false_positive']+met['true_negative'])
   candidates.append((fpr<=.01,met['f1'],name,threshold,clf,met))
 eligible=[r for r in candidates if r[0]];chosen=max(eligible or candidates,key=lambda r:r[1]);_,_,name,threshold,clf,valstats=chosen
 if name!='tfidf_logistic':raise RuntimeError('NB won; implement matching browser export before shipping')
 prob=clf.predict_proba(c)[:,1];teststats=stats(y[test],prob>=threshold)
 names=v.get_feature_names_out();model={'algorithm':'TF-IDF logistic regression','bias':float(clf.intercept_[0]),'weights':{w:float(co) for w,co in zip(names,clf.coef_[0])},'idf':{w:float(i) for w,i in zip(names,v.idf_)},'threshold':threshold}
 # Clean baseline: same Naive Bayes design trained only on UCI rows in NEW train split.
 import collections,math
 counts=[collections.Counter(),collections.Counter()];size=[0,0]
 for i in train:
  if sources[i]!='UCI':continue
  counts[y[i]].update(re.findall(r'[a-z0-9]+',X[i].lower()));size[y[i]]+=1
 vocab=set(counts[0])|set(counts[1]);totals=[sum(c.values()) for c in counts]
 w={t:math.log((counts[1][t]+1)/(totals[1]+len(vocab)))-math.log((counts[0][t]+1)/(totals[0]+len(vocab))) for t in vocab}
 def oldp(t):
  ts=re.findall(r'[a-z0-9]+',t.lower());score=math.log(size[1]/size[0])+sum(w.get(t,0) for t in ts);return score>=np.log(.9/.1)
 legacy=stats(y[test],[oldp(t) for t in X[test]])
 details=lambda ids:dict(count=int(len(ids)),ham=int(sum(y[ids]==0)),spam_or_smishing=int(sum(y[ids]==1)),sources={s:int(sum(sources[ids]==s)) for s in ['UCI','IMC2025']})
 metrics={'version':2,'dataset':'UCI SMS + IMC2025 English public smishing reports','source_urls':[UCI,IMC],'source_sha256':[hashlib.sha256(u).hexdigest(),hashlib.sha256(im).hexdigest()],'source_rows':{'UCI':len(raw)-len(english),'IMC_all_languages':len(allim),'IMC_English_eligible':len(english)},'unique_messages':len(rows),'conflicting_normalized_labels_dropped':len(conflicts),'split':'60/20/20 group-disjoint by normalized opening 8 words; seeds42/43','train':details(train),'validation':details(val),'test':details(test),'train_count':len(train),'test_count':len(test),'vocabulary':len(names),'threshold':threshold,'validation_metrics':valstats,**teststats,'uci_only_nb_clean_same_test':legacy,'scope':'Mixed English spam/public smishing reports versus historical benign SMS. Source/time imbalance, incomplete campaign grouping, no modern benign control, not representative Indian scam accuracy.','selection':'TF-IDF logistic vs TF-IDF NB, 7 thresholds each, select validation F1 subject to <=1% benign false-positive rate; final test untouched until selection.'}
 (R/'model.json').write_text(json.dumps(model,separators=(',',':')));(R/'metrics.json').write_text(json.dumps(metrics,indent=2));(R/'IMC2025_LICENSE.txt').write_bytes(urllib.request.urlopen('https://raw.githubusercontent.com/reportsmishing/Smishing-Dataset-IMC25/main/LICENSE.txt').read())
 print(json.dumps(metrics,indent=2))
 # Independent probability fixture to test JS export fidelity.
 fixtures=[{'text':str(X[i]),'prob':float(clf.predict_proba(v.transform([X[i]]))[0,1])} for i in test[:20]]
 pathlib.Path('/tmp/v2-fixtures.json').write_text(json.dumps(fixtures))
if __name__=='__main__':main()
