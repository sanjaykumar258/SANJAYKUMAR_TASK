import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

def task1_basic_vector_search():
    print("=== Task 1: Basic Vector Search using IndexFlatL2 ===")
    d = 64                           # dimension
    nb = 100                         # database size
    nq = 5                           # nb of queries
    np.random.seed(1234)             # make reproducible
    
    # Generate random vectors
    xb = np.random.random((nb, d)).astype('float32')
    xq = np.random.random((nq, d)).astype('float32')
    
    # Initialize index
    index = faiss.IndexFlatL2(d)
    print("Is index trained?", index.is_trained)
    index.add(xb)
    print("Total vectors in index:", index.ntotal)
    
    # Search
    k = 4                          # we want to see 4 nearest neighbors
    D, I = index.search(xq, k)     # actual search
    
    print(f"Indices of top {k} neighbors for {nq} queries:")
    print(I)
    print(f"Distances to top {k} neighbors:")
    print(D)
    print()

def task2_semantic_similarity_search():
    print("=== Task 2: Semantic Similarity Search (all-MiniLM-L6-v2) ===")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    sentences = [
        "The quick brown fox jumps over the lazy dog.",
        "A fast, dark-colored fox leaps over a sleepy hound.",
        "Artificial Intelligence is transforming the world.",
        "Machine learning models are getting better every day.",
        "It's raining heavily outside.",
    ]
    
    # Generate embeddings
    embeddings = model.encode(sentences)
    
    d = embeddings.shape[1]
    index = faiss.IndexFlatL2(d)
    index.add(embeddings)
    
    query = "A speedy fox jumps over a dog that is resting."
    query_embedding = model.encode([query])
    
    k = 2
    D, I = index.search(query_embedding, k)
    
    print(f"Query: '{query}'")
    for i, idx in enumerate(I[0]):
        print(f"Rank {i+1}: '{sentences[idx]}' (Distance: {D[0][i]:.4f})")
    print()

def task3_context_aware_retrieval():
    print("=== Task 3: Context-aware Document Retrieval System ===")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    documents = [
        {"id": "doc1", "context": "Science", "text": "Photosynthesis is the process used by plants, algae and certain bacteria to harness energy from sunlight."},
        {"id": "doc2", "context": "Science", "text": "Gravity is a fundamental interaction which causes mutual attraction between all things with mass or energy."},
        {"id": "doc3", "context": "History", "text": "The Industrial Revolution was the transition to new manufacturing processes in Great Britain, continental Europe, and the United States."},
        {"id": "doc4", "context": "Technology", "text": "Cloud computing is the on-demand availability of computer system resources, especially data storage and computing power."},
    ]
    
    texts = [doc["text"] for doc in documents]
    embeddings = model.encode(texts)
    
    d = embeddings.shape[1]
    index = faiss.IndexFlatL2(d)
    index.add(embeddings)
    
    def retrieve(query, expected_context=None, k=2):
        query_emb = model.encode([query])
        D, I = index.search(query_emb, len(documents)) # get all to filter by context optionally
        
        results = []
        for i, idx in enumerate(I[0]):
            doc = documents[idx]
            if expected_context and doc["context"] != expected_context:
                continue
            results.append((doc, D[0][i]))
            if len(results) == k:
                break
        return results

    q1 = "How do plants get their energy?"
    print(f"Retrieving for query: '{q1}' with no context filter")
    res1 = retrieve(q1)
    for doc, dist in res1:
        print(f" - [{doc['context']}] {doc['text']} (Dist: {dist:.4f})")
        
    q2 = "Tell me about manufacturing changes."
    print(f"Retrieving for query: '{q2}' with expected context 'History'")
    res2 = retrieve(q2, expected_context="History")
    for doc, dist in res2:
        print(f" - [{doc['context']}] {doc['text']} (Dist: {dist:.4f})")
    print()

def task4_near_duplicate_detection():
    print("=== Task 4: Near-duplicate Detection Engine (L2 distance thresholding) ===")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    dataset = [
        "The company reported a significant increase in Q3 revenue.",
        "The company saw a massive jump in third quarter profits.", # duplicate of 0
        "We are opening a new office in London next month.",
        "A new branch in London will be operational next month.", # duplicate of 2
        "I need to buy some groceries later today.",
        "The sky is very clear tonight.",
    ]
    
    embeddings = model.encode(dataset)
    d = embeddings.shape[1]
    index = faiss.IndexFlatL2(d)
    index.add(embeddings)
    
    # Threshold for L2 distance (needs to be tuned based on the model and use case)
    # L2 distance with sentence-transformers can be relatively small for similar sentences. 
    threshold = 1.0 
    
    # Perform a search for each item to find its nearest neighbor (excluding itself)
    k = 2 # Best match is itself (dist=0), second best is the potential duplicate
    D, I = index.search(embeddings, k)
    
    duplicates = set()
    for i in range(len(dataset)):
        # I[i][0] is always 'i' because dist to itself is 0
        # I[i][1] is the nearest neighbor
        nn_idx = I[i][1]
        dist = D[i][1]
        
        if dist < threshold:
            # We sort to avoid recording both (i, j) and (j, i)
            pair = tuple(sorted([i, nn_idx]))
            duplicates.add((pair, dist))
            
    print(f"Detected {len(duplicates)} near-duplicate pairs (Threshold: L2 < {threshold}):")
    for (i, j), dist in duplicates:
        print(f" - Pair: (Dist: {dist:.4f})")
        print(f"   1: '{dataset[i]}'")
        print(f"   2: '{dataset[j]}'")
    print()

if __name__ == "__main__":
    task1_basic_vector_search()
    task2_semantic_similarity_search()
    task3_context_aware_retrieval()
    task4_near_duplicate_detection()
