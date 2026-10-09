"""Reproducible multinomial Naive Bayes. Standard library only. No paid API."""
import collections, hashlib, json, math, pathlib, random, re, urllib.request, zipfile, io
ROOT=pathlib.Path(__file__).parent
URL='https://archive.ics.uci.edu/static/public/228/sms+spam+collection.zip'
def tokens(text): return re.findall(r'[a-z0-9]+', text.lower())
def train():
    raw=urllib.request.urlopen(URL).read()
    z=zipfile.ZipFile(io.BytesIO(raw))
    rows={}
    for line in z.read('SMSSpamCollection').decode('utf-8').splitlines():
        label,text=line.split('\t',1)
        key=' '.join(tokens(text))
        if key not in rows: rows[key]=(int(label=='spam'),text)
    groups=[[r for r in rows.values() if r[0]==k] for k in (0,1)]
    rng=random.Random(42); trainset=[];test=[]
    for g in groups:
        rng.shuffle(g); n=int(len(g)*.75);trainset+=g[:n];test+=g[n:]
    counts=[collections.Counter(),collections.Counter()]; sizes=[0,0]
    for label,text in trainset:
        counts[label].update(tokens(text));sizes[label]+=1
    vocab=sorted(set(counts[0])|set(counts[1]));v=len(vocab)
    totals=[sum(c.values()) for c in counts]
    weights={w:round(math.log((counts[1][w]+1)/(totals[1]+v))-math.log((counts[0][w]+1)/(totals[0]+v)),9) for w in vocab}
    prior=math.log(sizes[1]/sizes[0])
    model={'algorithm':'Multinomial Naive Bayes, Laplace alpha=1','prior':prior,'weights':weights,'threshold':.9}
    def infer(text):
        score=prior+sum(weights.get(w,0) for w in tokens(text));return 1/(1+math.exp(-max(-700,min(700,score))))
    tp=fp=tn=fn=0
    for label,text in test:
        pred=int(infer(text)>=.9)
        tp+=int(pred==1 and label==1);fp+=int(pred==1 and label==0)
        tn+=int(pred==0 and label==0);fn+=int(pred==0 and label==1)
    metrics={'dataset':'UCI SMS Spam Collection (2011)','source':URL,'source_sha256':hashlib.sha256(raw).hexdigest(),'seed':42,'split':'75/25 stratified after normalized-text deduplication','unique_messages':len(rows),'train_count':len(trainset),'test_count':len(test),'train_ham':sizes[0],'train_spam':sizes[1],'vocabulary':v,'threshold':.9,'true_positive':tp,'false_positive':fp,'true_negative':tn,'false_negative':fn,'precision':tp/(tp+fp),'recall':tp/(tp+fn),'f1':2*tp/(2*tp+fp+fn),'accuracy':(tp+tn)/len(test),'scope':'English historical SMS spam, NOT verified scams, modern phishing or Indian-language coverage.'}
    (ROOT/'model.json').write_text(json.dumps(model,separators=(',',':')))
    (ROOT/'metrics.json').write_text(json.dumps(metrics,indent=2))
    (ROOT/'DATASET_LICENSE.txt').write_bytes(z.read('readme'))
    print(json.dumps(metrics,indent=2))
if __name__=='__main__':train()
