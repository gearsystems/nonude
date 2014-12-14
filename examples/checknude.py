import nude
from nude import Nude

# Example of usage
# n = Nude('./images/filename.extension')
# n.parse()
# print(n.result, n.inspect())

n = Nude('./images/')
n.parse()
print(n.result, n.inspect())
