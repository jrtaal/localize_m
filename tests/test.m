@implementation ViewController 
- (void)viewDidLoad {
  self.label.text = @"Test String to Localize";
  self.label.text = 
NSLocalizedStringWithDefaultValue(@"test-string-to-auto-localize",
  kDefaultLocalizationsTable, kClassBundle,
  @"Test String to Auto Localize",
  @"Test String to Auto Localize"
);
}
@end
