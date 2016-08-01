//
//  STRetainTestViewController.m
//  STBlockScannerDemo
//
//  Created by chenxing.cx on 16/8/1.
//  Copyright © 2016年 Startry. All rights reserved.
//

#import "STRetainTestViewController.h"

@interface STRetainTestViewController ()

@property (nonatomic, strong) NSArray *testArray;
@property (nonatomic, strong) NSAttributedString *attrString;

@end

@implementation STRetainTestViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    
    self.testArray = @[@1, @2, @3, @5, @1, @1231, @44];
    
    self.view.backgroundColor = [UIColor yellowColor];
    
    [self.testArray enumerateObjectsUsingBlock:^(id  _Nonnull obj, NSUInteger idx, BOOL * _Nonnull stop) {
        [self logArray];
    }];
    
    self.attrString = [[NSAttributedString alloc] initWithString:@"test"];
    
    [self.attrString enumerateAttribute:NSLinkAttributeName inRange:NSMakeRange(0, self.attrString.length) options:0 usingBlock:^(id value, __unused NSRange range, __unused BOOL *stop) {
        [self logArray];
    }];
}

- (void) logArray {
    NSLog(@"%@", self.testArray);
}

- (void) logAttrStr {
    NSLog(@"%@", self.attrString);
}

- (void)dealloc {
    NSLog(@"STRetainTestViewController delloc is Called!");
}

@end
