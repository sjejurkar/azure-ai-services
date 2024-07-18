import os
import json
from dotenv import load_dotenv
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult, AnalyzeDocumentRequest, DocumentAnalysisFeature
from azure.core.credentials import AzureKeyCredential


def get_document_data(doc_file: str) -> str:
    with open(doc_file, "rb") as f:
        doc_data = f.read()

    return doc_data


def analyze_document(doc_file: str):
    load_dotenv()
    ai_endpoint = os.getenv("AI_SERVICE_ENDPOINT")
    ai_key = os.getenv("AI_SERVICE_KEY")
    di_endpoint = os.environ["DOCUMENT_INTELLIGENCE_ENDPOINT"]
    di_key = os.environ["DOCUMENT_INTELLIGENCE_KEY"]

    document_intelligence_client = DocumentIntelligenceClient(
        endpoint=di_endpoint, credential=AzureKeyCredential(di_key))

    # If analyzing a local document, remove the comment markers (#) at the beginning of these 8 lines.
    # Delete or comment out the part of "Analyze a document at a URL" above.
    # Replace <path to your sample file>  with your actual file path.
    poller = None
    with open(doc_file, "rb") as f:
        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-layout", analyze_request=f, content_type="application/octet-stream",
            features=[DocumentAnalysisFeature.KEY_VALUE_PAIRS]
        )

    # poller = document_intelligence_client.begin_analyze_document(
    #     "prebuilt-layout",
    #     AnalyzeDocumentRequest(bytes_source=get_document_data(doc_file))
    # )

    result: AnalyzeResult = poller.result()

    for page in result.pages:
        print(f"----Analyzing layout from page #{page.page_number}----")
        print(
            f"Page has width: {page.width} and height: {page.height}, measured with unit: {page.unit}")

    for table_idx, table in enumerate(result.tables):
        print(
            f"Table # {table_idx} has {table.row_count} rows and {table.column_count} columns")

        for cell in table.cells:
            print(
                f"...Cell[{cell.row_index}][{cell.column_index}] has content '{cell.content.encode('utf-8')}'")


def main():
    doc_dir = "documents"
    doc_file = f"{doc_dir}/vessel_documents_1.pdf"

    analyze_document(doc_file)


if __name__ == "__main__":
    main()
