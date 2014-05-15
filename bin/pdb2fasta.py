#!/usr/bin/python

import string
from sys import stdout
from os import popen,system
from os.path import exists
from amino_acids import longer_names
import optparse

if __name__ == "__main__":
    parser = optparse.OptionParser( usage="usage: python %prog [options]" )
    parser.add_option("-1","--onechain", help="Only output one chain",
        dest="onechain",default=False, action="store_true")
    parser.add_option("--nochain", help="Remove chain number from output pdb [disabled]",
        dest="removechain",default=False, action="store_true")
    (options, pdbnames) = parser.parse_args()



    #chainid = ' '
    #if len(argv)>2:
    #    chainid = argv[2]

    for pdbname in pdbnames:
    #    if (pdbname[-4:] != '.pdb'):
    #        pdbname += '.pdb'

        outfile = pdbname

        netpdbname = pdbname
        assert( exists(netpdbname))
        #print 'Reading ... '+netpdbname

        lines = open(netpdbname,'r').readlines()

        #outid = open( outfile, 'w')
        #print 'Writing ... '+pdbname

        #fastafile = pdbname+'.fasta'
        #fastaid = open( fastafile, 'w')
        #print 'Writing ... '+fastafile

        fastaid = stdout

        fastaid.write('>'+pdbname+'\n');

        oldresnum = '   '
        count = 0;
        for line in lines:
            if (len(line)>6): # and (chainid == line[21]):
                line_edit = line
                if line[0:3] == 'TER':
                    if options.onechain:
                        break
                    else:
                        fastaid.write('\n') 
                elif line[0:6] == 'ENDMDL':
                    break
                elif (line[0:6] == 'HETATM') & (line[17:20]=='MSE'): #Selenomethionine
                    line_edit = 'ATOM  '+line[6:17]+'MET'+line[20:]
                    if (line_edit[12:14] == 'SE'):
                        line_edit = line_edit[0:12]+' S'+line_edit[14:]
                    if len(line_edit)>75:
                        if (line_edit[76:78] == 'SE'):
                            line_edit = line_edit[0:76]+' S'+line_edit[78:]

                elif line_edit[0:4] == 'ATOM':
                    resnum = line_edit[23:26]
                    if not resnum == oldresnum:
                        count = count + 1
                        longname = line_edit[17:20]
                        if longer_names.has_key(longname):
                            fastaid.write( longer_names[longname] );
                        else:
                            fastaid.write( 'X')
                    oldresnum = resnum

                    newnum = '%3d' % count
                    line_edit = line_edit[0:23] + newnum + line_edit[26:]
                    if options.removechain:
                        line_edit = line_edit[0:21]+' '+line_edit[22:]

                    #outid.write(line_edit)
        fastaid.write('\n')


        #outid.close()
        #fastaid.close()
