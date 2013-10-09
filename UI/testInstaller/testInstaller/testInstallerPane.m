//
//  testInstallerPane.m
//  testInstaller
//
//  Created by echeng on 10/9/13.
//  Copyright (c) 2013 echeng. All rights reserved.
//

#import "testInstallerPane.h"

@implementation testInstallerPane

- (NSString *)title
{
	return [[NSBundle bundleForClass:[self class]] localizedStringForKey:@"PaneTitle" value:nil table:nil];
}

@end
