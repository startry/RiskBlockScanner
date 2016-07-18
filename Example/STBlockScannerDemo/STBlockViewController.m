//
//  STBlockViewController.m
//  STBlockScannerDemo
//
//  Created by chenxing.cx on 16/7/18.
//  Copyright © 2016年 Startry. All rights reserved.
//

#import "STBlockViewController.h"
#import <libextobjc/EXTScope.h>

@implementation STBlockViewController

- (void) viewDidLoad {
    [super viewDidLoad];
    NSLog(@"Run risk_block_scanner.py by CMD");
}

- (void) blockFunc {
    NSLog(@"blockFunc has run");
    [self blockCallback:^(NSString *backStr) {
        [self doAnyThing];
    }];
}

- (void) blockNestFunc {
    NSLog(@"blockNestFunc has run");
    [self blockCallback:^(NSString *backStr) {
        [self doAnyThing];
        
        [self blockCallback:^(NSString *backStr) {
            [self doAnyThing];
        }];
    }];
}

- (void) safeFunc {
    NSLog(@"safeFunc has run");
    __weak __typeof(self) weakSelf = self;
    [self blockCallback:^(NSString *backStr) {
        __strong __typeof(self) strongSelf = weakSelf;
        [strongSelf doAnyThing];
    }];
}

- (void) safeMacroFunc {
    NSLog(@"safeMacroFunc has run");
    @weakify(self)
    [self blockCallback:^(NSString *backStr) {
        @strongify(self)
        [self doAnyThing];
    }];
    
    [self blockCallback:^(NSString *backStr) {
        @strongify(self)
        [self doAnyThing];
    }];
}

- (void) safeUseFunc {
    NSLog(@"safeUseFunc has run");
    [self blockCallback:^(NSString *backStr) {
        NSLog(@"Block havn't call self");
    }];
}

- (void) safeGCDFunc {
    NSLog(@"safeGCDFunc");
    dispatch_after(dispatch_time(DISPATCH_TIME_NOW, (int64_t)(1.0f * NSEC_PER_SEC)), dispatch_get_main_queue(), ^{
        [self doAnyThing];
    });
}

- (void) blockCallback:(void (^)(NSString * backStr)) callback {
    callback(@"test");
}

- (void) doAnyThing {
    NSLog(@"doAnyThing");
}

@end
