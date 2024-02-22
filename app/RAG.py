from haystack.nodes import PreProcessor, PromptModel, PromptTemplate, PromptNode
from haystack import Pipeline, Document
from haystack.nodes import BM25Retriever
from haystack.document_stores import InMemoryDocumentStore


from config import PROMPT, HF_TOKEN

def create_document(text_dict):
    documents = []
    for title, text in text_dict.items():
        for values in text:
          if not values == "":


            documents.append(Document(content=values, meta={"name": title or ""}))
    return documents

def processing_document(documents):
    processor = PreProcessor(
        clean_empty_lines=True,
        clean_whitespace=True,
        clean_header_footer=True,
        split_by="word",
        split_length=500,
        split_respect_sentence_boundary=True,
        split_overlap=0,
        language="it",
    )

    # Processa la lista di documenti
    preprocessed_docs = processor.process(documents)

    document_store = InMemoryDocumentStore(use_bm25=True)
    document_store.write_documents(preprocessed_docs)

    retriever = BM25Retriever(document_store, top_k=5)
    qa_template = PromptTemplate(prompt_text=PROMPT, name="prompt_node")

    prompt_node = PromptNode(
        model_name_or_path="mistralai/Mixtral-8x7B-Instruct-v0.1",
        api_key=HF_TOKEN,
        default_prompt_template=qa_template,
        max_length=500,
        model_kwargs={"model_max_length": 5000}
    )

    rag_pipeline = Pipeline()
    rag_pipeline.add_node(component=retriever, name="retriever", inputs=["Query"])
    rag_pipeline.add_node(component=prompt_node, name="prompt_node", inputs=["retriever"])

    return rag_pipeline


def question_answering(question: str, model_pipeline):
    return model_pipeline.run(query=question)
