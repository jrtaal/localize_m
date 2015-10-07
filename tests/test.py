from nose.tools import eq_
import os, sys

mfile = u"""
@implementation ViewController 
- (void)viewDidLoad {
  self.label.text = @"Test String to Localize";
  self.label.text = __LOCALIZE@"Test String to Auto Localize";
  self.label.text = __LOCALIZE@"Test String to Auto %20@ Localize with %02d = 2 formatting arguments";
}
@end
"""

mfile_custom = u"""
@implementation ViewController 
- (void)viewDidLoad {
  self.label.text = @"Test String to Localize";
  self.label.text = __LOCALIZE_ME_PLEASE@"Test String to Auto Localize";
}
@end
"""

correct_output = u"""
@implementation ViewController 
- (void)viewDidLoad {
  self.label.text = @"Test String to Localize";
  self.label.text = NSLocalizedStringWithDefaultValue(@"test-string-to-auto-localize", kDefaultLocalizationsTable, kClassBundle, 
@"Test String to Auto Localize",@"Test String to Auto Localize");
  self.label.text = NSLocalizedStringWithDefaultValue(@"test-string-to-auto-[]-localize-with-[]-2-formatting-arguments", kDefaultLocalizationsTable, kClassBundle,
@"Test String to Auto %20@ Localize with %02d = 2 formatting arguments",@"Test String to Auto %20@ Localize with %02d = 2 formatting arguments");
}
@end
"""

correct_output_custom = u"""
@implementation ViewController 
- (void)viewDidLoad {
  self.label.text = @"Test String to Localize";
  self.label.text = NSLocalizedStringWithDefaultValue(@"test-string-to-auto-localize", mytable, mybundle, 
@"Test String to Auto Localize",@"Test String to Auto Localize");
}
@end
"""

import re
from localize_m.main import parse
from io import StringIO
import codecs
 
w_re = re.compile(r"\s+")
def prepare(text):
   return w_re.sub('', text)


def test_file():
    infile = StringIO(mfile)
    outfile = StringIO()

    config = dict(ask_all = False,
                  comments = False,
               )

    parse("testfile", infile, outfile, **config)
    eq_(prepare(outfile.getvalue()),prepare(correct_output)) 

def test_custom():
    infile = StringIO(mfile_custom)
    outfile = StringIO()

    config = dict(ask_all = False,
                  comments = False,
                  autoreplace_prefix = "__LOCALIZE_ME_PLEASE",
                  bundle = "mybundle",
                  table = "mytable")

    parse("testfile", infile, outfile, **config)
    eq_(prepare(outfile.getvalue()),prepare(correct_output_custom)) 


def test_cli():
   infile = codecs.open(os.path.join(os.path.dirname(__file__),"test.m"),"r")
   from localize_m.main import main
   sys.argv = ["-i", "tests/test.m"]
   try:
      main()
   except SystemExit:
      raise "Failed"


