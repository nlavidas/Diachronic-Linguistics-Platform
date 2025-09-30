def chunk_text(text, chunk_size=5000, overlap=500):
    """
    Split large text into overlapping chunks
    """
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        # Find end point
        end = start + chunk_size
        
        # Try to break at sentence end
        if end < len(text):
            # Look for period, !, or ?
            for punct in ['. ', '! ', '? ', '\n']:
                last_punct = text.rfind(punct, start, end)
                if last_punct != -1:
                    end = last_punct + 1
                    break
        
        chunks.append(text[start:end])
        start = end - overlap  # Overlap for context
    
    return chunks

def process_large_text(text, processor_func):
    """
    Process large text in chunks
    """
    chunks = chunk_text(text)
    results = []
    
    for i, chunk in enumerate(chunks):
        print(f"Processing chunk {i+1}/{len(chunks)}...")
        try:
            result = processor_func(chunk)
            results.append(result)
        except Exception as e:
            print(f"Error in chunk {i+1}: {e}")
            results.append({'error': str(e)})
    
    return combine_results(results)

def combine_results(results):
    """
    Combine results from multiple chunks
    """
    combined = {
        'tokens': [],
        'sentences': [],
        'errors': []
    }
    
    for r in results:
        if 'error' in r:
            combined['errors'].append(r['error'])
        else:
            combined['tokens'].extend(r.get('tokens', []))
            combined['sentences'].extend(r.get('sentences', []))
    
    return combined