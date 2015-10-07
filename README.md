# localize_m

A script which helps in localizing your objc .m files. It has two modes:

1. Interactively parse your file, and ask for each string whether it should be localized  ( `--ask-all` option)
2. Parse your file and replace each `__LOCALIZE@"..."` string with:
   `NSLocalizedStringWithDefaultValue(<slug>, kDefaultLocalizationTable, kClassBundle, @"...", @"...")` .
   If you use the -c option, localize_m will ask you to edit the slug and to provide a comment for the translator

## Localization ID's
Localize_m automatically generates slugs from you strings to act as lookup keys for your translations. 
Formatting codes `%@`, `%d`, etc are replaced by `[]` in  your slugs, for ease of reading. Why do we use slugs as id?

1. slugs should uniquely describe the string. Even if you have the same @"Example" string at multiple place 
   in your code, you may want to be able to translate to Dutch with @"Voorbeeld", and with @"Bijv." at another 
   place. So if you use slugs `example-long-form` and `example-short-form`, you can discriminiate between the two
2. To help you resist the temptation to edit the ID. Never edit the ID, when your strings have been translated.


## Tip:
In your project.pch precompiled header define:
```
#define __LOCALIZE
#define kClassBundle [NSBundle bundleForClass:[self class]]
#define kDefaultLocalizationsTable nil
```

This makes sure that your project compiles, even when you have put `__LOCALIZE`s in your code, and haven't run the localize_m script yet. We use `[NSBundle bundleForClass:[self class]]` so that your project is framework compatible. You can manually override the kDefaultLocalizationsTable with a string, when you want to use another table than the default Localizations.strings file.


## Usage

```
usage: localize_m [-h] [-p PATH] [-o [outfile]] [-a] [-c] [--inplace] [infile]

add Translation to .m files

positional arguments:
  infile                Input .m file

optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH
  -o [outfile], --outfile [outfile]
                        Output file, otherwise stdout
  -a, --ask-all         ask for all strings (interactive))
  -c, --comments        ask for comments and ids (interactive)
  --inplace             edit inplace
```

## installation

Localize_m uses python, which is installed on every Mac by default.

```
# pip install localize_m
Collecting localize-m
  Downloading Localize_M-1.0.tar.gz
Collecting colored (from localize-m)
  Using cached colored-1.2.1.tar.gz
Collecting slugify (from localize-m)
  Using cached slugify-0.0.1.tar.gz
Collecting gnureadline (from localize-m)
  Using cached gnureadline-6.3.3-cp27-none-macosx_10_6_intel.whl
Installing collected packages: colored, slugify, gnureadline, localize-m
  Running setup.py install for colored
  Running setup.py install for slugify
  Running setup.py install for localize-m
Successfully installed colored-1.2.1 gnureadline-6.3.3 localize-m-1.0 slugify-0.0.1

#
```
# Examples

## One file
```

# cd project/src
# localize_m MainViewController.m --comments --inplace

```

## All m files
```
localize_m -p "./*.m" --comments
```
You can go through all files. Press CTRL-C to save your changes and quit. Just start localize_m again to resume where you left.
