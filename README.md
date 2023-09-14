# pygmsender

This is a minimalistic package for dispatch of emails
from your gmail account.

### Requirements
You need to activate 2FA on your gmail account and to generate an app password.
You can find more information [here](https://support.google.com/accounts/answer/185833?hl=en).

### Installation
```bash 
```

### Example
I am assuming that you have the environment variables 
`MY_GMAIL_USERNAME` and `MY_GMAIL_APP_PASSWORD` set on your machine.
The former is your gmail username and the latter is the app password you generated
using the instructions above.

The snippet below illustrates how to send
an email to `test12345@some.another` with 
subject `Test email!` and body `Hello World!`:


```python
import os
from pygmsender.gmail_sender import GmailSender

sender = GmailSender(
    os.environ['MY_GMAIL_USERNAME'], 
    os.environ['MY_GMAIL_APP_PASSWORD']
)   
sender.send_email(
    l_str_recipients=["test12345@some.another"],
    str_subject='Test email!',
    str_body='Hello World!'    
)
```   
