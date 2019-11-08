#!/usr/bin/awk -f

# actions before reading text stream - initiate counters
BEGIN{
    wcnt = bllinecnt = 0;
    wmin = wmax = "";
}

# at every line ruleblock
{
    print FILENAME
    if (FILENAME ~ /names\.py/)
        print "wilson001"
    # count the words
    wcnt += NF;
    # count blank/empty lines
    if (NF == 0)
        bllinecnt++;
    # update maximum and minimum word count variables
    if( (NF>(wmax+0)) || (NR==1))
        wmax = NF;
    if( (NF<(wmin+0)) || (NR==1))
        wmin = NF;
}

# final text stream statistics
END{
    printf("Total %d words on %d lines. (average/min/max %.2f/%s/%s words per line; %d blank lines)\n",
           wcnt, NR, wcnt / NR, wmin, wmax, bllinecnt);
    print " - DONE -"
}
