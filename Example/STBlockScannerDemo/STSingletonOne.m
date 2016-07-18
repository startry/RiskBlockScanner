//
//  STSingletonOne.m
//  STBlockScannerDemo
//
//  Created by chenxing.cx on 16/7/18.
//  Copyright © 2016年 Startry. All rights reserved.
//

#import "STSingletonOne.h"

@implementation STSingletonOne

static STSingletonOne *_STSingletonOne_sharedInstance = nil;

+ (STSingletonOne *)sharedInstance {
    
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        _STSingletonOne_sharedInstance = [[STSingletonOne alloc] init];
    });
    return _STSingletonOne_sharedInstance;
}

+ (id)allocWithZone:(struct _NSZone *)zone{
    @synchronized(self){
        if (_STSingletonOne_sharedInstance == nil) {
            _STSingletonOne_sharedInstance = [super allocWithZone:zone];
        }
    }
    return _STSingletonOne_sharedInstance;
}

- (void) blockFunc {
    NSLog(@"blockFunc has run");
    [self blockCallback:^(NSString *backStr) {
        [self doAnyThing];
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

- (void) blockCallback:(void (^)(NSString * backStr)) callback {
    callback(@"test");
}

- (void) doAnyThing {
    NSLog(@"doAnyThing");
}

@end
