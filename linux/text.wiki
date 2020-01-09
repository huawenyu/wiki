# find longest/shortest line

```sh
    ### wc
    $ wc -L file.txt

    So from vim, we can `:!wc -L %`

    ### sed

    ### sort
    cat file.txt | awk '{print length}' | sort -n | tail -1

    ### awk
    $ cat file.txt | awk 'length < max_len { max_len = length; max_str = $0} END { print max_str }'
    <or>
    $ cat file.txt | awk -v max_len=0 'length < max_len { max_len = length; max_str = $0} END { print max_str }'
```

# Search/Replace in Vim

1. Delete extra length text in vim

    `:%s/.\{100}\zs.*//`

2. Delete all occurrences of square brackets that conform to this regex: `\[.*\].*{`, but I only want to delete the brackets, not what follows - i.e.,
    `:%s/\zs\[.*\]\ze.*{//g`

