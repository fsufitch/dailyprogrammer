## Problem description

Word search puzzles are a very common free time pastime. They are fairly simple in concept (though can be quite challenging to solve): given a grid of letters, find as many words as you can that run vertically down, horizontally left to right, or diagonally to the right. For example, for the following grid:

    FDHQYABZ
    ASIGASDG
    HFDGNPGA
    FAERIENP
    PQXBFMAE
    XCNAAADS
    FWZSAONG
    GAZDCZSS

You can find the words:

 - FAERIE (horizontal)
 - HIDE, ASP, GAPES (vertical)
 - DIG, FAN (diagonal down/right)
 - PAD, CODE (diagonal up/right)

Programs to solve word search puzzles have been done before, though. Instead, let's take a different angle on it: find the largest rectangular block of letters with no words in it!

## Formal Input

The input is a rectangular word search puzzle. All the letters are capital case, and there is no punctuation/whitespace in any of them. You may also want to take the [enable1.txt](https://github.com/fsufitch/dailyprogrammer/raw/master/common/enable1.txt) word list as an input so you have a dictionary to work from.

**Sample input:**

    FDHQYABZ
    ASIGASDG
    HFDGNPGA
    FAERIENP
    PQXBFMAE
    XCNAAADS
    FWZSAONG
    GAZDCZSS


## Formal output

The output consists of two things: first, a count of the total area (number of letters) in the largest rectangular region without any words, then a print-out of the rectangular region itself.

**Sample output**:

    12
    QXB
    CNA
    WZS
    AZD

**Explanation:** Here is the input with `.` substituted for letters that are part of a word. You can see the output block near the bottom left.

    F..QY.BZ
    AS.GA.D.
    HF..N.G.
    ......N.
    .QXB.MA.
    XCNAA...
    FWZSA..G
    GAZD.ZSS

Solutions may not be unique. Another valid solution for this input would be:

    12
    XCNA
    FWZS
    GAZD

## Challenge input 1

    CSXECOMEMBANKMEDTSHTEHGXI
    NNHUTFMILDBTTSWDUSPSTNRMX
    ZINGARIONDEXADSEUCKIAQUCQ
    BECROWDULUNESRTBNTKGPSFNR
    MFHFUTURISMMSVNEITEIEEENT
    LRSNMSJTLRYPXEMUNKSANKFYC
    GARFBZIAERERUYLKQDPVMGEID
    DTIKLCWDEEGQOAYVEOBFQIEIS
    REDUAGNFTBOLHWIEEDBUUCHON
    RRSPZEESDLPRTOWNNROYNEONG
    QNOXLLUOIEEDWDYDTPOELBWQM
    AIRSUANNDCPONZEKNYRXVTYAE
    YTOZOYGEFIUOGTFEJEIGHTERH
    HYWSTARTSMPSSGKNFENTOOTTG
    MARRMMYIZPYOIBPSEOOJFNNRD
    HTCUXAHELURHXTNQYSSZAAAOU
    ZHIRRSRSXDEJYATQTYQIHCRPL
    YHVGYAKEEOXSRPQHOKJNTTSOL
    MTQDUZLDHSMTTWOFRMRWCGLUR
    RETIBRAVUSAAVOFDHNOEHEIRC
    ORTROXJLSELCRRCBOSARBOLEA
    PEPAGPCOVRCDUUCKHREIPDSRP
    SNZPGZEGIHRZCHARMINGFHIXR
    QAYEOEDNSHOUURLWRNLCANTYN
    OTFTTTPCMZUFMCSCLBGZLVIMA

## Challenge input 2 (big)

Use this 2000x2000 grid here: https://github.com/fsufitch/dailyprogrammer/raw/master/ideas/wordsearch/big.txt
