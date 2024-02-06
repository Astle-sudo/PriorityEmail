from rank import rankedEmails

N = int(input("Number of recent emails: "))
Emails = rankedEmails(N)
Emails = sorted(Emails, key=lambda x: x.rank, reverse=True)

class EmailTemplate :

    def __init__(self, emailObject):
        self.EO = emailObject
    
    def render (self) :
        print()
        print("--------------------------------------------------------")
        print()
        print("From [" + str(self.EO.sender) + "]")
        print()
        print("Subject [" + str(self.EO.subject) + "]")
        print()
        print()
        print(self.EO.summary)
        print()

for i in Emails :
    e = EmailTemplate(i)
    e.render()