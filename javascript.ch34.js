#!/usr/bin/env node
var k = new Array(176,214,205,246,264,255,227,237,242,244,265,270,283);
var u = 'administrator';
var p = '';
for (i=0; i<k.length; i++) { 
	p += String.fromCharCode(k[i] - i*10 - u.charCodeAt(i)); 
}
console.log(u, p);
