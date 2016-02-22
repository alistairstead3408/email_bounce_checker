# email-bounce-checker
Script to scan the rutherford bounces gmail account to check for DSN emails. Outputs a list of comma separated emails which are determined by:

1. Whether the email has a valid X-Failed-Recipients field
2. Whether the MIME type of the email is DSN
3. If the email contains text that matches some given phrases

In cases 2 and 3, the most frequently mentioned email is selected. 