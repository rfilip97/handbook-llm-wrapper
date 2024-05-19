from langchain_community.document_loaders import DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.text_splitter import MarkdownTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
from unstructured.partition.text import partition_text
from langchain.docstore.document import Document


def load_data(path):
    loader = DirectoryLoader(path, glob="**/*.md")

    text_splitter = MarkdownTextSplitter()

    documents = []
    for doc in loader.load():
        file_path = doc.metadata["source"]
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        elements = partition_text(text=content)
        doc_text = "\n".join([str(element) for element in elements])
        doc_chunks = text_splitter.split_text(doc_text)
        documents.extend([Document(page_content=chunk) for chunk in doc_chunks])

    embeddings = SentenceTransformerEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    return VectorstoreIndexCreator(embedding=embeddings).from_documents(documents)
