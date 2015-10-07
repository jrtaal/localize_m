@implementation ViewController 
- (void)viewDidLoad {
  self.label.text = @"Test String to Localize";
  self.label.text = __LOCALIZE@"Test String to Auto Localize";
}
@end
