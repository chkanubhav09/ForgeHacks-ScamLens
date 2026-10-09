/* Local inference only. Messages never leave this module. */
(function(root){
'use strict';
function tokenize(text){return text.toLowerCase().match(/[a-z0-9]+/g)||[];}
const rules=[
 {id:'secret',rx:/\b(otp|one[ -]?time password|pin|password|cvv|verification code)\b/i,label:'Sensitive credential or code',explain:'Never share an OTP, PIN, password or CVV with someone who contacted you.'},
 {id:'urgency',rx:/\b(urgent|immediately|within\s+\d+|expire[sd]?|suspend(?:ed)?|blocked|last chance|act now)\b/i,label:'Pressure to act quickly',explain:'Urgency can stop you checking the request independently.'},
 {id:'authority',rx:/\b(bank|police|arrest|court|customs|rbi|income tax|cyber ?crime|government)\b/i,label:'Claimed authority',explain:'A name or logo does not verify a sender. Use an independently found official contact.'},
 {id:'payment',rx:/\b(upi|pay|payment|transfer|deposit|fee|refund|bank account|money|rupees|rs\.?|gift card|crypto)\b/i,label:'Money or payment request',explain:'Check who receives the money before paying. A refund should not require your UPI PIN.'},
 {id:'reward',rx:/\b(prize|lottery|winner|won|reward|cashback|guaranteed|free money|investment return)\b/i,label:'Reward or too-good-to-be-true claim',explain:'Unexpected rewards or guaranteed returns deserve independent checks.'},
 {id:'remote',rx:/\b(anydesk|teamviewer|screen ?shar(?:e|ing)|remote access|install.*(?:apk|app)|download.*apk)\b/i,label:'Remote access or installation',explain:'Do not install an APK or share your screen at an unknown caller\'s request.'},
 {id:'identity',rx:/\b(kyc|aadhaar|aadhar|pan card|verify.*(?:identity|account)|update.*kyc)\b/i,label:'Identity or account verification',explain:'Open the official app yourself. Do not use the link in an unexpected KYC message.'},
 {id:'impersonation',rx:/\b(new number|lost my phone|this is.*(?:dad|mum|mom|boss)|(?:dad|mum|mom|boss).*new number)\b/i,label:'Possible personal impersonation',explain:'Call the person on a number you already know before sending money.'}
];
function inspectLinks(text){
 let links=(text.match(/(?:https?:\/\/|www\.)[^\s<>"']+/gi)||[]).slice(0,12);
 return links.map(raw=>{let url;try{url=new URL(raw.startsWith('www.')?'https://'+raw:raw.replace(/[).,;!?]+$/,''));}catch(e){return{raw,host:'unparseable',signals:['Could not parse this link']};}
 let flags=[];let host=url.hostname;
 if(url.protocol==='http:')flags.push('Unencrypted HTTP');
 if(host.startsWith('xn--')||host.includes('.xn--'))flags.push('Punycode hostname: inspect spelling carefully');
 if(/^\d{1,3}(\.\d{1,3}){3}$/.test(host))flags.push('Numeric IP address instead of a domain');
 if(url.username||url.password)flags.push('Username part can disguise the real host');
 if(/(^|\.)(bit\.ly|tinyurl\.com|t\.co|is\.gd|cutt\.ly)$/.test(host))flags.push('Shortened link hides its destination');
 return{raw,host,signals:flags};});
}
function analyze(text,model){
 text=String(text||'').trim(); if(!text)throw Error('Paste a message first.');if(text.length>10000)throw Error('Keep the message under 10,000 characters.');
 let ts=tokenize(text),known=ts.filter(t=>Object.prototype.hasOwnProperty.call(model.weights,t)),unique=[...new Set(known)];
 let score=model.prior+known.reduce((s,t)=>s+model.weights[t],0);
 let probability=1/(1+Math.exp(-Math.max(-700,Math.min(700,score))));
 let evidence=rules.filter(r=>r.rx.test(text)).map(({id,label,explain})=>({id,label,explain}));let links=inspectLinks(text);
 let coverage=ts.length?known.length/ts.length:0; let supported=ts.length>=4&&coverage>=.45&&!/[^\x00-\x7F]/.test(text);
 let modelFlag=supported&&probability>=model.threshold;
 let strong=evidence.some(e=>['secret','remote','impersonation'].includes(e.id))&&(evidence.length>=2||links.length>0);
 let risky=strong||(evidence.length>=3)||(links.some(l=>l.signals.length)&&evidence.length>=1);
 let level=(modelFlag||risky)?'High caution':(!supported||evidence.length||links.length?'Check independently':'No strong signals found');
 return {level,supported,modelFlag,ruleFlag:risky,spamScore:probability,coverage,tokenCount:ts.length,evidence,links,
  contributors:unique.map(token=>({token,weight:model.weights[token]*known.filter(t=>t===token).length})).sort((a,b)=>b.weight-a.weight).filter(x=>x.weight>0).slice(0,6),
  warning:'This is not proof of fraud or safety. The model learned historical English SMS spam, not modern scams or sender identity.'};
}
const api={tokenize,analyze,inspectLinks};if(typeof module!=='undefined'&&module.exports)module.exports=api;root.ScamLens=api;
})(typeof globalThis!=='undefined'?globalThis:this);
