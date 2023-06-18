from ske.algorithm import SymmetricKeyAlgorithm
from ske.AES128 import AES128
from ske.TripleDES import TripleDes
from codes import Code

SymmetricKeyAlgorithm.map[Code.AES128] = AES128()
SymmetricKeyAlgorithm.map[Code.TripleDES] = TripleDes()
