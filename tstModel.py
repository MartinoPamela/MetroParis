from database.DAO import DAO
from model.modello import Model

myLinee = DAO.getAllLinee()

mymodel = Model()
mymodel.buildGraph()

print(f"The graph has {mymodel.getNumNodes()} nodes.")
print(f"The graph has {mymodel.getNumEdges()} edges.")
