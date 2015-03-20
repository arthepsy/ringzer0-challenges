#!/usr/bin/env node
var CryptoJS = require("crypto-js");

function hex2str(d) {
	return unescape(('' + d).replace(/(..)/g, '%$1'))
}

u = "\x68\x34\x78\x30\x72";
var k = CryptoJS.SHA256("\x93\x39\x02\x49\x83\x02\x82\xf3\x23\xf8\xd3\x13\x37");
key = CryptoJS.enc.Hex.parse(k.toString().substring(0,32));
iv = CryptoJS.enc.Hex.parse(k.toString().substring(32,64));
pb = "ob1xQz5ms9hRkPTx+ZHbVg==";

p = CryptoJS.AES.decrypt(pb, key, {iv: iv})
t = CryptoJS.AES.encrypt(p, key, { iv: iv })
// console.log(t.toString())
// console.log(pb)

console.log(u, hex2str(p));
