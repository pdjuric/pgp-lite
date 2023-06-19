from ske.algorithm import SymmetricKeyAlgorithm
from ske.AES128 import AES128
from ske.TripleDES import TripleDES
from codes import Code

SymmetricKeyAlgorithm.map[Code.AES128.value] = AES128()
SymmetricKeyAlgorithm.map[Code.TripleDES.value] = TripleDES()
