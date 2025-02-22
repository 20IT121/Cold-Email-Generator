import pandas as pd
import chromadb
import uuid

class Portfolio:
    def __init__(self, file_path='./resource/my_portfolio.csv'):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.chroma_client = chromadb.Client()
        self.collection = self.chroma_client.get_or_create_collection(name = "portfolio")

    
    def load_portfolio(self):
    # iterrows() is a pandas method that returns an iterator yielding index and row data for each row.
    # The underscore (_) is used as a placeholder for the index, which is not being used in this loop.
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(
                    documents = row["Techstack"],
                    metadatas = {"links" : row["Links"]},
                    ids = [str(uuid.uuid4())]
                )

    def query_links(self, skills):
        return self.collection.query(query_texts=skills , n_results=2).get('metadatas' , [])