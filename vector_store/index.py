from langchain_community.document_loaders import DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.text_splitter import MarkdownTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
from unstructured.partition.text import partition_text
from langchain.docstore.document import Document
from config import CHUNK_SIZE, CHUNK_OVERLAP


class VectorStore:
    def __init__(self, path, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP):
        self.path = path
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.documents = []
        self.index = None

    def load_documents(self):
        loader = DirectoryLoader(self.path, glob="**/*.md")

        return loader.load()

    def process_document(self, doc):
        file_path = doc.metadata["source"]
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        elements = partition_text(text=content)
        doc_text = "\n".join([str(element) for element in elements])
        text_splitter = MarkdownTextSplitter(
            chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
        )
        doc_chunks = text_splitter.split_text(doc_text)

        return [Document(page_content=chunk) for chunk in doc_chunks]

    def create_index(self):
        embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        self.index = VectorstoreIndexCreator(embedding=embeddings).from_documents(
            self.documents
        )

        return self.index

    def build_vector_store(self):
        docs = self.load_documents()
        for doc in docs:
            self.documents.extend(self.process_document(doc))

        return self.create_index()
