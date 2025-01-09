var _ps = [];
var fn_arg0 = "irisctf{funny_bunny_was_a_hare_funny_bunny_had_nice_hair}";

// globals
var gbl_bitLengths;
//
var gbl_enchuff_stream;
var gbl_enchuff_currentByte;
var gbl_enchuff_bitCount;


// start m, main()
var fm_compa, fm_compb;
fm_compa = btoa("jumpjumpj"); // anVtcGp1bXBq
fm_compb = btoa("pjumpjumpjumpjumpj").substring(3); // 1bXBqdW1wanVtcGp1bXBq

_ps.push(null);

_ps.push("dW1wQtXNWGp");
_ps.push(0x0a252d34);
_ps.push("dW1xKn9ucGp");
_ps.push(0x0a11242b);
_ps.push("dW1xKPZtcGp");
_ps.push(0x080e191f);
_ps.push("dW1waXVv+mp");
_ps.push(0x05060837);
_ps.push("dW1wQnBtaGp");
_ps.push(0x03162530);
_ps.push("dW1x6nVFcH5");
_ps.push(0x07172f33);
_ps.push("dW1xL3ZtcGp");
_ps.push(0x06151f2e);
_ps.push("dW1x6PVtWGp");
_ps.push(0x0e1c1e2e);
_ps.push("dW1xKnVFcS9");
_ps.push(0x12141928);
_ps.push("dW1wCnVt1Wp");
_ps.push(0x051b262c);
_ps.push("dW1xKhU9cGp");
_ps.push(0x021d2432);
_ps.push("dW1xKtVtdmp");
_ps.push(0x09202d33);
_ps.push("dW1wCnVFcG9");
_ps.push(0x11183538);
_ps.push("dW1wfnVtEG9");
_ps.push(0x0f203138);
_ps.push("dW1wanVtEGp");
_ps.push(0x0c122329);
_ps.push("dW1wcn89cGp");
_ps.push(0x00041a31);
_ps.push("dW1wOnVsMAp");
_ps.push(0x030c292c);
_ps.push("dW1xKnVucSp");
_ps.push(0x01141c2a);
_ps.push("dW1wanfucH5");
_ps.push(0x071c2237);
_ps.push("dW1wanVrcGp");
_ps.push(0x090f2026);
_ps.push("dW1wanZtcGp");
_ps.push(0x0a11212f);
_ps.push("dW1xLHXNcGp");
_ps.push(0x171b2b35);
_ps.push("dW1xKnVFWH5");
_ps.push(0x13142237);
_ps.push("dW1xL3VucGp");
_ps.push(0x0b10152a);
_ps.push("dW1wahVtcGp");
_ps.push(0x00023036);
_ps.push("dW1x6nVtcGp");
_ps.push(0x0d192a33);
_ps.push("dW1x6zVv8Gp");
_ps.push(0x04131927);
_ps.push("dW1xKiVtdmp");
_ps.push(0x091d1e26);

/**@cndjmp (_ps[_ps.length-1] === null) success*/ //: fm_toploop
/**@call sliceStr*/
/**@call buildCanonicalHuffmanTree*/
/**@call getEncodedHuffmanTree*/
/**@cndjmp (!_ps.pop().startsWith(fm_compa + _ps.pop() + fm_compb)) failure*/
/**@jmp fm_toploop*/

return true //: success
return false //: failure
// end main



// enjoy quality chatgpt output :)
// start a, buildCanonicalHuffmanTree(str[-1])
var fa_str;
fa_str = _ps[_ps.length-1]; //: buildCanonicalHuffmanTree
_ps[_ps.length-1] = ""; // hide input string

// calculate frequency of each character
var fa_freq, fa_freqI;
fa_freq = {};
fa_freqI = 0;
/**@cndjmp (fa_freqI >= fa_str.length) fa_loop1_exit*/ //: fa_loop1_top
    fa_freq[fa_str[fa_freqI]] = (fa_freq[fa_str[fa_freqI]] || 0) + 1;
    fa_freqI++;
/**@jmp fa_loop1_top*/

fa_str = ""; // hide other input string //: fa_loop1_exit

// create a priority queue of nodes
var fa_heap;
fa_heap = Object.entries(fa_freq).map(([c, f]) => ({c: c, f: f, x: null, y: null}));
fa_heap.sort((a, b) => a.f - b.f);

// build the huffman tree
var fa_left, fa_right, fa_merged;
/**@cndjmp (fa_heap.length <= 1) fa_loop2_exit*/ //: fa_loop2_top
    fa_left = fa_heap.shift();
    fa_right = fa_heap.shift();
    fa_merged = {c: null, f: fa_left.f + fa_right.f, x: null, y: null};
    fa_merged.x = fa_left;
    fa_merged.y = fa_right;
    fa_heap.push(fa_merged);
    fa_heap.sort((a, b) => a.f - b.f);
/**@jmp fa_loop2_top*/

var fa_root;
fa_root = fa_heap[0]; //: fa_loop2_exit

// assign bit lengths to each character
gbl_bitLengths = {};
_ps.push(0);
_ps.push(fa_root);
/**@call assignBitLengths*/

var fa_sortedChars, fa_codes, fa_code, fa_prevLength, fa_sortedCharsI;
fa_sortedChars = Object.entries(gbl_bitLengths).sort((a, b) => a[1] - b[1] || a[0].localeCompare(b[0]));
fa_codes = {};
fa_code = 0;
fa_prevLength = 0;

// assign canonical codes based on bit lengths
fa_sortedCharsI = 0;
/**@cndjmp (fa_sortedCharsI >= fa_sortedChars.length) fa_loop3_exit*/ //: fa_loop3_top
    /**@cndjmp (fa_sortedChars[fa_sortedCharsI][1] === fa_prevLength) fa_len_is_prevlen*/
        fa_code <<= (fa_sortedChars[fa_sortedCharsI][1] - fa_prevLength);
        fa_prevLength = fa_sortedChars[fa_sortedCharsI][1];
    fa_codes[fa_sortedChars[fa_sortedCharsI][0]] = fa_code.toString(2).padStart(fa_sortedChars[fa_sortedCharsI][1], "0"); //: fa_len_is_prevlen
    fa_code++;
    fa_sortedCharsI++;
/**@jmp fa_loop3_top*/

// fix stack
_ps.pop(); //: fa_loop3_exit
//
// return result
_ps.push(fa_codes);
//
/**@ret */
// end buildCanonicalHuffmanTree



// start b, assignBitLengths(node[-1], depth[-2])
var fb_tmpNode, fb_tmpDepth;
fb_tmpNode = _ps[_ps.length-1]; //: assignBitLengths
fb_tmpDepth = _ps[_ps.length-2];
/**@cndjmp (!!fb_tmpNode) fb_dontreturn*/
    // fix stack
    _ps.pop();
    _ps.pop();
    //
    /**@ret */

/**@cndjmp (fb_tmpNode.c === null) fb_dontsetbitlen*/ //: fb_dontreturn
    gbl_bitLengths[fb_tmpNode.c] = _ps[_ps.length-2];

_ps.push(fb_tmpDepth + 1); //: fb_dontsetbitlen
_ps.push(fb_tmpNode.x);
/**@call assignBitLengths*/

fb_tmpNode = _ps[_ps.length-1];
fb_tmpDepth = _ps[_ps.length-2];
_ps.push(fb_tmpDepth + 1);
_ps.push(fb_tmpNode.y);
/**@call assignBitLengths*/

// fix stack
_ps.pop();
_ps.pop();
//
/**@ret */
// end assignBitLengths



// start c, getEncodedHuffmanTree(str[-1])
var fc_inp, fc_inpstr, fc_mainI, fc_mainJ;
fc_inp = _ps[_ps.length-1]; //: getEncodedHuffmanTree
//console.log("fc_inp", fc_inp);
fc_inpstr = Object.keys(fc_inp).reduce((arr, key) => {arr[key.charCodeAt(0)] = fc_inp[key].length; return arr;}, []);
//console.log("fc_inpstr", fc_inpstr);
gbl_enchuff_stream = [];
gbl_enchuff_currentByte = 0;
gbl_enchuff_bitCount = 0;
fc_mainI = 0;
/**@cndjmp (fc_mainI >= 256) fc_loop1_exit*/ //: fc_loop1_top
    /**@cndjmp ((fc_inpstr[fc_mainI]||0) <= 0) fc_char_not_used*/
        _ps.push(1);
        /**@call addBitEncodedHuffmanTree*/
        fc_inpstr[fc_mainI] <<= 1;
        //
        _ps.push((fc_inpstr[fc_mainI] >>= 1) & 1);
        /**@call addBitEncodedHuffmanTree*/
        _ps.push((fc_inpstr[fc_mainI] >>= 1) & 1);
        /**@call addBitEncodedHuffmanTree*/
        _ps.push((fc_inpstr[fc_mainI] >>= 1) & 1);
        /**@call addBitEncodedHuffmanTree*/
        _ps.push((fc_inpstr[fc_mainI] >>= 1) & 1);
        /**@call addBitEncodedHuffmanTree*/
        /**@jmp fc_char_used_end*/
    // else
        _ps.push(0); //: fc_char_not_used
        /**@call addBitEncodedHuffmanTree*/
    fc_mainI++; //: fc_char_used_end
/**@jmp fc_loop1_top*/

/**@cndjmp (gbl_enchuff_bitCount == 0) fc_bit_count_is_0*/ //: fc_loop1_exit
    gbl_enchuff_stream.push((gbl_enchuff_currentByte << (8 - gbl_enchuff_bitCount)) ^ "jump".charCodeAt(gbl_enchuff_stream.length % 4));

// fix stack
_ps.pop(); //: fc_bit_count_is_0
//
// return result
_ps.push(btoa(String.fromCharCode(...gbl_enchuff_stream)));
//
/**@ret */
// end getEncodedHuffmanTree



// start d, addBitEncodedHuffmanTree(bit[-1])
gbl_enchuff_currentByte = (gbl_enchuff_currentByte << 1) | _ps[_ps.length-1]; //: addBitEncodedHuffmanTree
gbl_enchuff_bitCount++;
/**@cndjmp (gbl_enchuff_bitCount !== 8) fd_bitcount_not_8*/
    gbl_enchuff_stream.push(gbl_enchuff_currentByte ^ "jump".charCodeAt(gbl_enchuff_stream.length % 4));
    gbl_enchuff_currentByte = 0;
    gbl_enchuff_bitCount = 0;

// fix stack
_ps.pop(); //: fd_bitcount_not_8
//
/**@ret */



// start e, sliceStr(encNum[-1])
var fe_encNum, fe_res;
fe_encNum = _ps[_ps.length-1]; //: sliceStr

fe_res = "";
fe_res += fn_arg0[(fe_encNum & 0xff)];
fe_res += fn_arg0[((fe_encNum >> 8) & 0xff)];
fe_res += fn_arg0[((fe_encNum >> 16) & 0xff)];
fe_res += fn_arg0[((fe_encNum >> 24) & 0xff)];

// fix stack
_ps.pop();
//
// return result
_ps.push(fe_res);
//
/**@ret */


return Array(-1);