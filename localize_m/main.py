#import rlcompleter
import gnureadline as readline

import argparse
import re
import sys
import slugify
import tokenize
import colored
import glob
import shutil


TEMPLATE =\
"""
NSLocalizedStringWithDefaultValue(@"{}",
  kDefaultLocalizationsTable, kClassBundle,
  @"{}",
  @"{}"
)"""

AUTOPREFIX = "__LOCALIZE"

class NoMatchException(Exception):
   pass

class ReplaceAction(Exception):
   pass

REPLACE = "[]"

slugify.ALLOWED_CHARS_PATTERN = re.compile(r'[^-a-z0-9[]]+')

def context_buf_readlines(infile, A=10, B=6):
   prebuf = []
   postbuf = []
   linenum = 0
   for line in infile.readlines():
      postbuf.append(line)
      if len(postbuf) < B:
         continue

      yield prebuf, postbuf[0], postbuf[1:], linenum
      linenum += 1   
      prebuf = prebuf[-A:] + postbuf[0:1]
      postbuf = postbuf[1:]

   for line in postbuf:
      yield prebuf, postbuf[0], postbuf[1:], linenum
      linenum += 1
      prebuf = prebuf[-A:] + postbuf[0:1]
      postbuf = postbuf[1:]
         

def parse(filename, infile, outfile, ask_all = True, comments = False, inplace = False):
   interactive = ask_all or comments
      
   string_re = re.compile(r'(.*?)@"([^"]+)"(.*)')
   prefix_re = re.compile(r"NSLocalized[a-zA-Z]String\(");
   fmt_re = re.compile(r"%[-0-9\.]*[l]?[difes\@]")

   def slug_from_string(sel, REPLACE = REPLACE):
      items = fmt_re.split(sel)
      newitems = map(lambda item:slugify.slugify(item), items)
      
      slug =  "-[]-".join(filter(lambda x:len(x), newitems))
      return slug
   

   w = sys.stdout.write
   fg = colored.fg
   attr = colored.attr

   quit_after = False
   linenum = 0

   replace_autoprefix = True
   
   #for line in infile.readlines():
   for prebuf, line, postbuf, linenum in context_buf_readlines(infile):

      try:
                  
         match =  string_re.match(line)
      
         if not match:
            raise NoMatchException
         
         prefix = match.group(1)
         sel = match.group(2)
         postfix = match.group(3)

         def _print_preamble():
            
            header = "%s (%d):" % (filename, linenum)
            data = [
               fg(2), attr(1), header, "_" * (60 - len(header) -5 ), attr(0), "\n",
               "  ", "  ".join(prebuf),
               fg(3), "> ", prefix, fg(4), '@"', fg(2), attr(1), sel, fg(4), '"', attr(0), '\n'
               "  ", "  ".join(postbuf)
            ]
            w("".join(data))
         print_preamble = _print_preamble
               
         if prefix_re.search(prefix):
            raise NoMatchException

         if prefix[-1] in "[":
            raise NoMatchException
         
         try:
            if replace_autoprefix and prefix.endswith(AUTOPREFIX):
               prefix = prefix[:-len(AUTOPREFIX)]
               raise ReplaceAction
               
            if ask_all:
                              
               print_preamble()
               print_preamble = lambda :None
               answer = raw_input(colored.fg(1) + colored.attr(1) + "Replace String? [N/y]" + colored.attr(0))
            
               if len(answer) > 0:
                  if  answer in "Yy":
                     raise ReplaceAction
                  elif answer in "qQ":
                     ask_all = False
                     comments = False
                     quit_after = True
                     replace_autoprefix = False
                  
         except ReplaceAction:
            
            slug = slug_from_string(sel)
               
            cmt = sel
            try:
               if comments:
                  print_preamble()
               
                  def hook():
                     readline.insert_text(slug)
                     readline.redisplay()
                  readline.set_pre_input_hook(hook)

                  if len(slug)>30:
                     w( fg(1) + attr(1) + ( "ID for translation:" ) + attr(0))
                     w("\n" + fg(1) )
                     newslug = raw_input("> ")
                     w(attr(0))
                  else:
                     w("\n" + fg(1) + attr(1))
                     newslug = raw_input( "ID for translation: ")
                     w(attr(0))
                  if newslug:
                     slug = newslug

                  
                  def hook():
                     readline.insert_text(sel)
                     readline.redisplay()
                  readline.set_pre_input_hook(hook)
               
                  cmt  = raw_input(colored.fg(1) + colored.attr(1) + "Comment for translator: " + colored.attr(0))
                  if not cmt:
                     cmt = sel
                  readline.set_pre_input_hook()
                     
            except KeyboardInterrupt:
               w("\n")
               
               raise
            else:

               rep = TEMPLATE.format(slug, sel, cmt )
               if comments or interactive:
                  w( "".join(prebuf[-3:] +
                             [
                                prefix, fg(4), rep, attr(0), postfix, "\n"
                             ] + postbuf[0:3]
                          ))
                     
               outfile.write("".join([prefix, rep, postfix, "\n"]))

            continue
               
         except KeyboardInterrupt:
            raise
         else:
            raise NoMatchException
            
      except KeyboardInterrupt:
         ask_all = False
         comments = False
         interactive = False
         replace_autoprefix = False
         if line:
            outfile.writelines([line])
         quit_after = True
            
      except NoMatchException:
         
         outfile.writelines([line])


   if quit_after:
      raise KeyboardInterrupt

def main():
   parser = argparse.ArgumentParser(description = "add Translation to .m files")

   parser.add_argument('-p', '--path', type = str)
   
   parser.add_argument('infile', metavar = 'infile', nargs = '?',
                       type=argparse.FileType('r'),
                       help='Input .m file')

   parser.add_argument('-o','--outfile', metavar = 'outfile', nargs = '?',
                       type=argparse.FileType('w'),
                       default=None,
                       help='Output file, otherwise stdout')

   parser.add_argument("-a", "--ask-all", help = "ask for all strings (interactive))", default = False, action = "store_true")

   parser.add_argument("-c", "--comments", help = "ask for comments and ids (interactive)", default = False, action = "store_true")

   parser.add_argument("--inplace", help = "edit inplace", default = False, action = "store_true")
   
   args = parser.parse_args()

   if not args.infile and not args.path:
      parser.print_help()
      return -1

   if args.ask_all:
      args.comments = True
   
   if args.inplace:
      
      from cStringIO import StringIO
      intext = StringIO(args.infile.read())
      fn = args.infile.name;
      args.infile.close()
      outfile = open(fn, "w")
      parse(fn, intext, outfile, args.ask_all, args.comments)
      
   else:
            
      try:
         if args.infile:
            if not args.outfile:
               args.outfile = sys.stdout
               if args.ask_all or not args.comments:
                  print "Output to stdout is only supported in non-interactive mode"
                  sys.exit(0)
            parse(args.infile.name, args.infile, args.outfile, args.ask_all, args.comments)

         elif args.path: # implies inplace
            from cStringIO import StringIO
            for fn in glob.glob(args.path):
               intext = StringIO(open(fn,"r").read())
               outfile = open(fn, "w")
               parse(fn, intext, outfile, args.ask_all, args.comments)
               
      except KeyboardInterrupt:
         sys.exit(1)
         