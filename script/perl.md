# Basic

## prgma keywords

https://www.perlmonks.org/?node=use%20strict%20warnings%20and%20diagnostics%20or%20die

Perl has three pragmas specifically designed to make your life easier:
```perl
use strict;
use warnings;
use diagnostics;
```

# Howtos

## OOP
http://www.tutorialspoint.com/perl/perl_oo_perl.htm

## Create a Perl Module for code reuse

Assume we already have env var, if not, please add the following line to our .zshrc

    export PERL5LIB="$HOME/perl5/lib:$PERL5LIB";

### @INC

A note on @INC
When you issue a use MyModule; directive perl searchs the @INC array for a module with the correct name. @INC usually contains:
```sh
/perl/lib 
/perl/site/lib
.
```
The . directory (dot dir) is the current working directory. CORE modules are installed under perl/lib whereas non-CORE modules install under perl/site/lib. You can add directories to the module search path in @INC like this:
```perl
BEGIN { push @INC, '/my/dir' }
# or
BEGIN { unshift @INC, '/my/dir' }
# or
use lib '/my/dir';
```
We need to use a BEGIN block to shift values into @INC at compile time as this is when perl checks for modules. If you wait until the script is comiled it is too late and perl will throw an exception saying it can't find MyModule in @INC... The difference between pushing a value and unshifting a value into @INC is that perl searches the @INC array for the module starting with the first dir in that array. Thus is you have a MyModule in /perl/lib/ and another in /perl/site/lib/ and another in ./ the one in /perl/lib will be found first and thus the one used. The use lib pragma effectively does the same as the BEGIN { unshift @INC, $dir } block - see perlman:lib:lib for full specifics.

### Module

The module `My::Math` come from the file `$HOME/perl5/lib/My/Math.pm`

```perl
package My::Math;
use strict;
use warnings;

use Exporter qw(import);

our @EXPORT_OK = qw(add multiply);

sub add {
  my ($x, $y) = @_;
  return $x + $y;
}

sub multiply {
  my ($x, $y) = @_;
  return $x * $y;
}

1;
```

### Using Module

The script
```perl
    #!/usr/bin/perl
    use strict;
    use warnings;

    use My::Math qw(add);

    print add(19, 23);
```

### Run

    $ perl -I$HOME/perl5/lib/ app.pl
    $ perl app.pl

