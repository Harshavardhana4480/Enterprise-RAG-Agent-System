from langchain_text_splitters import RecursiveCharacterTextSplitter

def create_splitter():
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200,
        separators = ["\n\n", "\n",". "," ",""]
    )
    return splitter
