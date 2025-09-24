import requests
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

class SearchEngine:
    def __init__(self):
        self.base_urls = {
            'arxiv': 'http://export.arxiv.org/api/query',
            'doaj': 'https://doaj.org/api/v2/search/articles',
            'pubmed': 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi',
            'crossref': 'https://api.crossref.org/works'
        }
    
    def search(self, query: str, subject_areas: List[str] = None, 
               language: str = '', date_from: str = '', date_to: str = '',
               min_word_count: int = 0, max_word_count: int = 0) -> List[Dict[str, Any]]:
        """
        Search for open access texts across multiple sources
        """
        results = []
        
        # Search ArXiv
        arxiv_results = self._search_arxiv(query, subject_areas, date_from, date_to)
        results.extend(arxiv_results)
        
        # Search DOAJ
        doaj_results = self._search_doaj(query, subject_areas, language, date_from, date_to)
        results.extend(doaj_results)
        
        # Search PubMed for open access articles
        pubmed_results = self._search_pubmed(query, subject_areas, date_from, date_to)
        results.extend(pubmed_results)
        
        # Filter by word count if specified
        if min_word_count > 0 or max_word_count > 0:
            results = self._filter_by_word_count(results, min_word_count, max_word_count)
        
        return results
    
    def _search_arxiv(self, query: str, subject_areas: List[str] = None,
                      date_from: str = '', date_to: str = '') -> List[Dict[str, Any]]:
        """Search ArXiv for papers"""
        try:
            params = {
                'search_query': f'all:{query}',
                'start': 0,
                'max_results': 20,
                'sortBy': 'relevance',
                'sortOrder': 'descending'
            }
            
            if subject_areas:
                # Map subject areas to ArXiv categories
                category_map = {
                    'computer science': 'cs',
                    'mathematics': 'math',
                    'physics': 'physics',
                    'biology': 'q-bio',
                    'economics': 'econ',
                    'statistics': 'stat'
                }
                categories = []
                for area in subject_areas:
                    if area.lower() in category_map:
                        categories.append(f"cat:{category_map[area.lower()]}*")
                
                if categories:
                    params['search_query'] = f"({' OR '.join(categories)}) AND all:{query}"
            
            response = requests.get(self.base_urls['arxiv'], params=params, timeout=10)
            response.raise_for_status()
            
            # Parse XML response (simplified)
            results = self._parse_arxiv_xml(response.text)
            return results
            
        except Exception as e:
            print(f"Error searching ArXiv: {e}")
            return []
    
    def _search_doaj(self, query: str, subject_areas: List[str] = None,
                     language: str = '', date_from: str = '', date_to: str = '') -> List[Dict[str, Any]]:
        """Search Directory of Open Access Journals"""
        try:
            params = {
                'q': query,
                'pageSize': 20
            }
            
            if subject_areas:
                params['subject'] = ','.join(subject_areas)
            
            if language:
                params['language'] = language
            
            if date_from:
                params['fromDate'] = date_from
            
            if date_to:
                params['toDate'] = date_to
            
            response = requests.get(self.base_urls['doaj'], params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            results = self._parse_doaj_json(data)
            return results
            
        except Exception as e:
            print(f"Error searching DOAJ: {e}")
            return []
    
    def _search_pubmed(self, query: str, subject_areas: List[str] = None,
                       date_from: str = '', date_to: str = '') -> List[Dict[str, Any]]:
        """Search PubMed for open access articles"""
        try:
            # First, search for article IDs
            search_params = {
                'db': 'pubmed',
                'term': f'{query} AND open access[Filter]',
                'retmax': 20,
                'retmode': 'json'
            }
            
            if date_from and date_to:
                search_params['term'] += f' AND {date_from}:{date_to}[dp]'
            
            response = requests.get(self.base_urls['pubmed'], params=search_params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if 'esearchresult' not in data or not data['esearchresult'].get('idlist'):
                return []
            
            # Get article details
            ids = ','.join(data['esearchresult']['idlist'])
            fetch_params = {
                'db': 'pubmed',
                'id': ids,
                'retmode': 'xml'
            }
            
            fetch_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi'
            fetch_response = requests.get(fetch_url, params=fetch_params, timeout=10)
            fetch_response.raise_for_status()
            
            results = self._parse_pubmed_xml(fetch_response.text)
            return results
            
        except Exception as e:
            print(f"Error searching PubMed: {e}")
            return []
    
    def _parse_arxiv_xml(self, xml_content: str) -> List[Dict[str, Any]]:
        """Parse ArXiv XML response"""
        # Simplified XML parsing - in production, use proper XML parser
        results = []
        # This is a simplified implementation
        # In practice, you'd use xml.etree.ElementTree or lxml
        return results
    
    def _parse_doaj_json(self, data: dict) -> List[Dict[str, Any]]:
        """Parse DOAJ JSON response"""
        results = []
        
        if 'results' in data:
            for article in data['results']:
                result = {
                    'title': article.get('bibjson', {}).get('title', ''),
                    'authors': self._extract_authors(article.get('bibjson', {}).get('author', [])),
                    'abstract': article.get('bibjson', {}).get('abstract', ''),
                    'url': article.get('bibjson', {}).get('link', [{}])[0].get('url', ''),
                    'doi': article.get('bibjson', {}).get('identifier', [{}])[0].get('id', ''),
                    'source': 'DOAJ',
                    'publication_date': article.get('created_date', ''),
                    'subject_areas': article.get('bibjson', {}).get('subject', []),
                    'language': article.get('bibjson', {}).get('language', ['en'])[0],
                    'keywords': article.get('bibjson', {}).get('keywords', [])
                }
                results.append(result)
        
        return results
    
    def _parse_pubmed_xml(self, xml_content: str) -> List[Dict[str, Any]]:
        """Parse PubMed XML response"""
        # Simplified XML parsing - in production, use proper XML parser
        results = []
        # This is a simplified implementation
        return results
    
    def _extract_authors(self, authors: List[dict]) -> str:
        """Extract author names from various formats"""
        if not authors:
            return ''
        
        author_names = []
        for author in authors:
            if isinstance(author, dict):
                name = author.get('name', '')
                if not name:
                    # Try to construct name from parts
                    first = author.get('first_name', '')
                    last = author.get('last_name', '')
                    name = f"{first} {last}".strip()
                if name:
                    author_names.append(name)
            elif isinstance(author, str):
                author_names.append(author)
        
        return '; '.join(author_names)
    
    def _filter_by_word_count(self, results: List[Dict[str, Any]], 
                             min_count: int, max_count: int) -> List[Dict[str, Any]]:
        """Filter results by word count"""
        filtered = []
        
        for result in results:
            text = f"{result.get('title', '')} {result.get('abstract', '')}"
            word_count = len(text.split())
            
            if min_count > 0 and word_count < min_count:
                continue
            if max_count > 0 and word_count > max_count:
                continue
            
            result['word_count'] = word_count
            filtered.append(result)
        
        return filtered