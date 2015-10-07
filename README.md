# localize_m

A script which helps in localizing your objc .m files. It has two modes:
1. Interactively parse your file, and ask for each string whether it should be localized  ( `--ask-all` option)
2. Parse your file and replace each `@"..."` string with `NSLocalizedStringWithDefaultValue(<slug>, kDefaultLocalizationTable, kClassBundle, @"...", @"...")` 
   If you use the -c option, localize_m will ask you to edit the slug and to provide a comment for the translator




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

