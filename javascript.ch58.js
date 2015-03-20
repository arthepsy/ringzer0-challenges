#!/usr/bin/env node
src = 'abcd-efgh-ijkl-mnop-qrtu';
dst = 'ubcq-pfgm-ljki-hnoe-drta';
adst = 'TBG8-Jjep-jM2L-KL23-Hr1A';
asrc = adst;

for (i=0; i<src.length; i++) {
	p = dst.indexOf(src[i]);
	tmp = asrc.split('');
	tmp[p] = adst[i];
	asrc = tmp.join('');
}

console.log(asrc);
