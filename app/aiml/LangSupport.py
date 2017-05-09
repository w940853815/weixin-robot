# -*- coding: utf-8 -*-

import jieba as jb
import re
a=u"([\u4e00-\u9fa5]+)( +)" 
b=u"( +)([\u4e00-\u9fa5]+)"

pa = re.compile(a)
pb = re.compile(b)

def isChinese(c):
    # http://www.iteye.com/topic/558050

    r = [
        # 标准CJK文字
        (0x3400, 0x4DB5), (0x4E00, 0x9FA5), (0x9FA6, 0x9FBB), (0xF900, 0xFA2D),
        (0xFA30, 0xFA6A), (0xFA70, 0xFAD9), (0x20000, 0x2A6D6), (0x2F800, 0x2FA1D),
        # 全角ASCII、全角中英文标点、半宽片假名、半宽平假名、半宽韩文字母
        (0xFF00, 0xFFEF),
        # CJK部首补充
        (0x2E80, 0x2EFF),
        # CJK标点符号
        (0x3000, 0x303F),
        # CJK笔划
        (0x31C0, 0x31EF)]
    return any(s <= ord(c) <= e for s, e in r)


def splitUnicode(s):
    assert type(s) == unicode, "string must be a unicode"
    segs = s.split()
    result = []
    for seg in segs:
        if any(map(isChinese, seg)):
            result.extend(splitChinese(seg))
        else:
            result.append(seg)
    return result

def splitChinese(s):
    
    result = jb.cut(s)
    ret = '|'.join(result)
    return ret.split("|")

def mergeChineseSpace(s):
    assert type(s) == unicode, "string must be a unicode"
    if len(s) == 0 :
        return s
    sa = pa.sub(r"\1",s)
    sb = pb.sub(r"\2",sa)
    return sb
