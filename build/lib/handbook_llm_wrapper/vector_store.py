from langchain_community.document_loaders import DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.text_splitter import MarkdownTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
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

    def __load_documents(self):
        return DirectoryLoader(self.path, glob="**/*.md").load()

    def __get_chunks(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        elements = partition_text(text=content)
        doc_text = "\n".join([str(element) for element in elements])
        text_splitter = MarkdownTextSplitter(
            chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
        )

        return text_splitter.split_text(doc_text)

    def __process_document(self, doc):
        chunks = self.__get_chunks(doc.metadata["source"])

        return [Document(page_content=chunk) for chunk in chunks]

    def __create_index(self):
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.index = VectorstoreIndexCreator(embedding=embeddings).from_documents(
            self.documents
        )

        return self.index

    def build_vector_store(self):
        docs = self.__load_documents()
        for doc in docs:
            self.documents.extend(self.__process_document(doc))

        return self.__create_index()
