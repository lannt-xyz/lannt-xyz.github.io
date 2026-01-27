# permission

## DashboardAndAlarmManagement

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "DashboardAndAlarmManagement",
            "Effect": "Allow",
            "Action": [
                "cloudwatch:PutDashboard",
                "cloudwatch:DeleteDashboards",
                "cloudwatch:ListDashboards",
                "cloudwatch:GetDashboard",
                "cloudwatch:GetMetricData",
                "cloudwatch:GetMetricStatistics",
                "cloudwatch:ListMetrics",
                "cloudwatch:DescribeAlarms",
                "cloudwatch:DescribeAlarmHistory",
                "cloudwatch:PutMetricAlarm",
                "logs:PutMetricFilter",
                "logs:PutRetentionPolicy",
                "logs:DescribeMetricFilters",
                "sns:CreateTopic",
                "sns:ListTopics",
                "sns:Subscribe",
                "sns:GetTopicAttributes",
                "sns:ListSubscriptions",
                "sns:ListSubscriptionsByTopic"
            ],
            "Resource": "*"
        }
    ]
}
```

## EC2WritingAndLogging

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "EC2WritingAndLogging",
            "Effect": "Allow",
            "Action": [
                "cloudwatch:PutMetricData",
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "logs:DescribeLogStreams",
                "logs:DescribeLogGroups",
                "xray:PutTraceSegments",
                "xray:PutTelemetryRecords",
                "xray:GetSamplingRules",
                "xray:GetSamplingTargets",
                "xray:GetSamplingStatisticSummaries",
                "ec2:DescribeTags",
                "ec2:DescribeInstances",
                "ec2:DescribeVolumes"
            ],
            "Resource": "*"
        }
    ]
}
```
