#!/usr/bin/env node

const cdk = require('aws-cdk-lib');
const { CdkprojectStack } = require('../lib/cdkproject-stack');

const app = new cdk.App();
new CdkprojectStack(app, 'CdkprojectStack', {});
