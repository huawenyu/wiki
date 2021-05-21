# pass a hash to a function

http://perldoc.perl.org/perlfaq7.html#How-can-I-pass%2freturn-a-%7bFunction%2c-FileHandle%2c-Array%2c-Hash%2c-Method%2c-Regex%7d%3f

Pass the reference instead of the hash itself. As in
```perl
PrintAA("abc", \%fooHash);

sub PrintAA
{
  my $test = shift;
  my $aaRef = shift;

  print $test, "\n";
  foreach (keys %{$aaRef})
  {
    print $_, " : ", $aaRef->{$_}, "\n";
  }
}
```

# hash

http://perl101.org/hashes.html

# array

http://www.informit.com/articles/article.aspx?p=2271909&seqNum=3

