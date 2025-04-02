# card-vulnerabilities
In this repository we study the vulnerabilities of physical cards and offer some potential protections

# Usage 
use [nfc-mfclassic](https://www.mankier.com/1/nfc-mfclassic) from libnfc


# References
paper:
fairly sure the paper conceps won't work directly for our tags as they are type 2 (meaning no hidden blocks)
- ie any hash chain written to the card could be easily cloned
https://www.cs.ru.nl/~wouter/papers/2008-thebest.pdf

Security details:
https://security.stackexchange.com/questions/234637/hardening-nfc-tags-for-authentication
https://security.stackexchange.com/questions/63483/how-do-nfc-tags-prevent-copying

https://electronics.stackexchange.com/questions/103741/is-it-possible-to-provide-security-in-passive-rfid-tags

https://forum.arduino.cc/t/prevent-nfc-tag-cloning/276786

https://seritag.com/learn/using-nfc/nfc-tag-authentication-explained