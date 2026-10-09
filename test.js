const assert=require('node:assert/strict');const fs=require('node:fs');const {analyze,inspectLinks}=require('./engine');const m=JSON.parse(fs.readFileSync('model.json'));
let n=0;function test(name,fn){fn();n++;console.log('PASS',name)}
test('normal message never declared safe',()=>assert.equal(analyze('Study group meets in the library at four. Bring your notes and we can revise together.',m).level,'No strong signals found'));
test('KYC+OTP pressure high caution',()=>assert.equal(analyze('Your bank KYC expires today. Account blocked within 2 hours. Update Aadhaar at https://bank-kyc-check.example/verify and share your OTP immediately.',m).level,'High caution'));
test('family impersonation high caution',()=>assert.equal(analyze('This is dad on my new number. Transfer money by UPI urgently.',m).level,'High caution'));
test('non-English abstains',()=>assert.equal(analyze('आपका खाता बंद हो रहा है',m).supported,false));
test('short text abstains',()=>assert.equal(analyze('urgent',m).supported,false));
test('unseen vocabulary abstains',()=>assert.equal(analyze('zxyq abcdefgh qwertyas zzzzyy',m).supported,false));
test('empty rejected',()=>assert.throws(()=>analyze('',m)));
test('too long rejected',()=>assert.throws(()=>analyze('x'.repeat(10001),m)));
test('hostname username trick',()=>assert.equal(inspectLinks('https://bank.example@evil.example/pay')[0].host,'evil.example'));
test('HTTP flagged',()=>assert.ok(inspectLinks('http://example.org')[0].signals.includes('Unencrypted HTTP')));
test('short URL flagged',()=>assert.ok(inspectLinks('https://bit.ly/test')[0].signals.some(s=>s.includes('Shortened'))));
test('never returns a clickable URL HTML',()=>assert.ok(!JSON.stringify(analyze('<script>alert(1)</script> http://evil.example',m)).includes('<a')));
test('probability finite',()=>assert.ok(Number.isFinite(analyze('hello friends here is a note',m).spamScore)));
console.log(`${n} tests passed`);
