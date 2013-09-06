#!/usr/bin/python
"""
    kenken.py op value numBoxes
    kenken.py -l op
       
Description:

    Calculates possible moves for kenken groups. The first use, without the -l
    option, calculates possibilities for a single box. It requires three arguments:
        1. (op) The mathematical operation (+,-,*,/)
        2. (value) The result for the operation
        3. (numBoxes) The number of boxes in this group
    Also useful are the -n and -d options, which specify the maximum digit
    (default 9) and maximum number of duplicates.
    
    When the -l option is specified, rather than giving possibilities for a
    specific group, possibilities for all groups of a given operator are output.
    The -b option is used to limit the number of boxes, and the -p option
    filters groups with large numbers of possibilities.

Credits:

    By Spencer Bliven <sbliven@ucsd.edu>. Copyright 2013."""

import sys
import math
import optparse

log=False #enable debug logging
indent=0 #for logging

class InputError(Exception): pass

def factor(n):
    """Brute-force factorization algorithm"""
    global indent,log
    if log: print "factoring %d" % n
    if n < 0:
        factors = [-1]
        factors.extend(factor(-n))
        return factors
    if n == 1: return [1]
    if n <= 3: return [1,n]
    
    factors = [1]
    x = 2
    while x*x <= n:
        if n%x == 0:
            if log: print "%d=%d*%d"%(n,x,n/x)
            factors.append(x)
            n /= x
        else:
            x += 1
    if n >= x:
        factors.append(n)
    return factors

def listBoxesMult(n, numBoxes, maxnum=9, maxRepeats=None):
    global indent
    if log: print("%slistBoxesMult(%d,%d)"%("  "*indent,n,numBoxes))

    # base cases
    if n < 1:
        raise InputError(n,"n must be positive")
    if numBoxes < 1:
        raise InputError(numBoxes, "numBoxes must be positive")
    if numBoxes == 1:
        if n <=maxnum:
            if log: print("%sreturn (%d,%d) [[%d]]"%("  "*indent,n,numBoxes,n))
            return [[n]]
        else:
            if log: print("%sreturn (%d,%d) []"%("  "*indent,n,numBoxes))
            return []
    if n == 1:
        if log: print("%sreturn (%d,%d) %s"%("  "*indent,n,numBoxes,[[1]*numBoxes]))
        return [[1]*numBoxes]

    # recursion
    allBoxes = []
    indent+=1
    for x in xrange(maxnum,1,-1):
        if n%x == 0:
            boxes = listBoxesMult(n/x,numBoxes-1,maxnum=x,maxRepeats=maxRepeats)
            for box in boxes:
                # append if sorted and doesn't violate maxRepeats
                if (maxRepeats is None or maxRepeats<1 or len(box)<maxRepeats or box[-maxRepeats] != x):
                    box.append(x)
                    allBoxes.append(box)
    indent-=1

    if log: print("%sreturn (%d,%d) %s"%("  "*indent,n,numBoxes,allBoxes))
    return allBoxes

def listBoxesAdd(n, numBoxes, maxnum=9, maxRepeats=None):
    global indent,log
    if log: print("%slistBoxesAdd(%d,%d)"%("  "*indent,n,numBoxes))

    # base cases
    if n < 1:
        raise InputError(n,"n must be positive")
    if numBoxes < 1:
        raise InputError(numBoxes, "numBoxes must be positive")
    if numBoxes == 1:
        if n <=maxnum:
            if log: print("%sreturn (%d,%d) [[%d]]"%("  "*indent,n,numBoxes,n))
            return [[n]]
        else:
            if log: print("%sreturn (%d,%d) []"%("  "*indent,n,numBoxes))
            return []
    if n == 0:
        if log: print("%sreturn (%d,%d) %s"%("  "*indent,n,numBoxes,[[1]*numBoxes]))
        return [[1]*numBoxes]

    # recursion
    allBoxes = []
    indent+=1
    for x in xrange(maxnum,0,-1):
        if n-x>0:
            boxes = listBoxesAdd(n-x,numBoxes-1,x,maxRepeats)
            for box in boxes:
                # append if sorted and doesn't violate maxRepeats
                if (maxRepeats is None or maxRepeats<1 or len(box)<maxRepeats or box[-maxRepeats] != x):
                    box.append(x)
                    allBoxes.append(box)
    indent-=1

    if log: print("%sreturn (%d,%d) %s"%("  "*indent,n,numBoxes,allBoxes))
    return allBoxes

def listBoxes(op, n, numBoxes, maxnum=9, maxRepeats=None):
    if op=="+":
        return listBoxesAdd(n, numBoxes, maxnum, maxRepeats)
    elif op=="*":
        return listBoxesMult(n, numBoxes, maxnum, maxRepeats)
    else:
        raise InputError(op,"Unsupported operation")
        
def listAllBoxes(op, maxpossibilities=None, boxes=None, maxnum=9, maxRepeats=1):
    """listAllBoxes(...) -> {box: {n:[possibilites]} }
    Returns a two-level dictionary mapping box->n->[possibilities] such that
    len(possibilities) < maxpossibilities
    """
    if boxes is None:
        boxes=xrange(2,maxnum)
       
    # helper function to calculate possible n. Returns generator
    if op=="+":
        # anything possible up to boxNum*maxnum
        possibleN = lambda box: xrange(1,box*maxnum+1)
    elif op=="*":
        # product of any digits
        # emits duplicates
        def possibleN(box,min=1):
            if box == 0:
                yield 1
                return
            for i in xrange(min,maxnum+1):
                for j in possibleN(box-1,i):
                    yield i*j
        
    else:
        raise InputError(op,"Unsupported operation")
 
    result = {}
    for box in boxes:
        #print "%d boxes:" % box
        boxresult = {}
        for n in possibleN(box):
            allPossible = listBoxes(op,n,box,maxnum)
            if maxpossibilities is None or maxpossibilities <1 or 0 < len(allPossible) <= maxpossibilities:
                #print "  % 3d: %s" % (n, "\n      ".join([" ".join([str(a) for a in add]) for add in alladds]))
                boxresult[n]=allPossible
        result[box] = boxresult
    return result

def printPossibilities(possibilities,boxes=None,maxnum=9):
    if boxes is None:
        boxes=xrange(2,maxnum)
    if len(possibilities) != len(boxes):
        raise InputError("Unexpected number of groups. Ensure possibilities and boxes have the same length.")
    
    for box in boxes:
        print "%d boxes:" % box
        if not possibilities.has_key(box): continue
        
        for n in sorted(possibilities[box].keys()):
            poss = possibilities[box][n]
            print "%6d: %s" % (n, "\n        ".join([" ".join([str(a) for a in p]) for p in poss]))

## Unit tests
def assertEquals(expected,result):
    if expected != result:
        raise AssertionError("Test failed. Expected:<%s>, Actual:<%s>"%(expected,result))
  
def test():
    testMult()
    testFactor()
    testAdd()
              
def testMult():
    result = listBoxesMult(100,1)
    expected = []
    assertEquals(expected,result)
    
    result = listBoxesMult(1,3)
    expected = [[1,1,1]]
    assertEquals(expected,result)
    
    result = listBoxesMult(9,1)
    expected = [[9]]
    assertEquals(expected,result)

    result = listBoxesMult(12,3)
    expected = [[1,2,6],[1,3,4],[2,2,3]]
    assertEquals(expected,result)

    result = listBoxesMult(12,3)
    expected = [[1,2,6],[1,3,4],[2,2,3]]
    assertEquals(expected,result)

    result = listBoxesMult(12,3,maxRepeats=1)
    expected = [[1,2,6],[1,3,4]]
    assertEquals(expected,result)

def testFactor():
    global indent,log

    result = factor(7)
    expected = [1,7]
    assertEquals(expected,result)
    
    result = factor(9)
    expected = [1,3,3]
    assertEquals(expected,result)
    
    result = factor(2**3 * 3**2 * 7)
    expected = [1,2,2,2,3,3,7]
    assertEquals(expected,result)
        
    result = factor(22)
    expected = [1,2,11]
    assertEquals(expected,result)
    
def testAdd():
    result = listBoxesAdd(9,1)
    expected = [[9]]
    assertEquals(expected,result)

    result = listBoxesAdd(10,1)
    expected = []
    assertEquals(expected,result)

    result = listBoxesAdd(4,2)
    expected = [[1,3],[2,2]]
    assertEquals(expected,result)

    result = listBoxesAdd(4,2,maxRepeats=1)
    expected = [[1,3]]
    assertEquals(expected,result)
    
    result = listBoxesAdd(17,2)
    expected = [[8,9]]
    assertEquals(expected,result)

    result = listBoxesAdd(8,3)
    expected = [[1,1,6],[1,2,5],[1,3,4],[2,2,4],[2,3,3]]
    assertEquals(expected,result)
    
    result = listBoxesAdd(8,3,maxRepeats=1)
    expected = [[1,2,5],[1,3,4]]
    assertEquals(expected,result)


if __name__ == "__main__":
    #usage = "\n".join(__doc__.split("\n")[:-3])
    usage = __doc__
    
    parser = optparse.OptionParser( usage=usage)
    # Normal mode
    parser.add_option("-n","--digits", help="Maximum digit used (default 9)",
        dest="digits",default=9, type="int")
    parser.add_option("-d","--duplicates", help="Maximum number of duplicates to allow (default unlimited)",
        dest="duplicates",default=None, type="int")
    # List mode
    parser.add_option("-l","--list", help="List all possibilities",
        dest="list",default=False, action="store_true")
    parser.add_option("-b","--boxes", help="When used with -l, the number of boxes "
        "per group. Accepts a comma delimeted list or an inclusive range (eg 1:9)",
        dest="boxes",default=None, type="str")
    parser.add_option("-p","--possibilities", help="When used with -l, the maximum "
        "number of possibilities to print. Boxes with more possibilities are "
        "ignored. (default unlimited)",
        dest="possibilities",default=None, type="int")
    # Flags
    parser.add_option("-v","--verbose", help="Enable debugging output",
        dest="verbose",default=False, action="store_true")
    parser.add_option("-t","--test", help="Run tests and exit",
        dest="test",default=False, action="store_true")
    
    (options, args) = parser.parse_args()


    if options.verbose:
        log=True
    if options.test:
        test()
        print "All tests passed"
        sys.exit(0)
   
    # List mode
    if options.list:
        if len(args) != 1:
            parser.print_usage()
            parser.exit("Error: Expected 1 argument with -l option, but found %d"%len(args) )
        
        op = args[0]
        #parse boxes
        if options.boxes is None:
            boxes = range(1,options.digits+1)
        elif options.boxes.find(":")>0:
            boxrange=options.boxes.split(":")
            if len(boxrange) != 2:
                parser.exit("Error: invalid argument for -b. (\"%s\")"%options.boxes)
            
            start = int(boxrange[0]) if boxrange[0] != '' else 1
            end   = int(boxrange[1]) if boxrange[1] != '' else options.digits
            
            boxes=range(start,end+1)
        else:
            boxes = [int(i) for i in options.boxes.split(",")]
        
        l = listAllBoxes(op, maxpossibilities=options.possibilities, boxes=boxes,
            maxnum=options.digits,
            maxRepeats=options.duplicates or 1)
        printPossibilities(l,boxes)

    # Normal mode
    else:
        if len(args) != 3:
            parser.print_usage()
            parser.exit("Error: Expected 3 arguments, but found %d"%len(args) )        
    
        op = args[0]
        n = int(args[1])
        numBoxes = int(args[2])
        
        possibilities = listBoxes(op,n,numBoxes,maxnum=options.digits,maxRepeats=options.duplicates)

        print "\n".join([str(b) for b in possibilities])
