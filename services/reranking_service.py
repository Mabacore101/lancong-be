from sentence_transformers import CrossEncoder
from typing import List, Dict, Any

class RerankingService:
    """
    Service untuk melakukan reranking hasil pencarian menggunakan cross-encoder model.
    Model ini akan menghitung semantic similarity antara query dan setiap hasil,
    kemudian mengurutkan ulang hasil berdasarkan skor relevansi yang lebih akurat.
    """
    
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        """
        Initialize reranker dengan model cross-encoder.
        Model default: ms-marco-MiniLM-L-6-v2 (ringan, cepat, akurat untuk search relevance)
        
        Args:
            model_name: Nama model cross-encoder dari Hugging Face
        """
        self.model = CrossEncoder(model_name)
        self.model_name = model_name
    
    def rerank(
        self, 
        query: str, 
        results: List[Dict[str, Any]], 
        text_field: str = "name",
        top_k: int = None
    ) -> List[Dict[str, Any]]:
        """
        Rerank hasil pencarian berdasarkan semantic similarity dengan query.
        
        Args:
            query: Query pencarian dari user
            results: List hasil pencarian (dict dengan field yang akan direrank)
            text_field: Field dalam dict yang akan dibandingkan dengan query (default: "name")
            top_k: Jumlah hasil teratas yang akan dikembalikan (None = semua hasil)
        
        Returns:
            List hasil yang sudah direrank berdasarkan relevance score (tertinggi ke terendah)
        """
        if not results:
            return []
        
        # Siapkan pasangan (query, document) untuk scoring
        query_doc_pairs = []
        for result in results:
            # Extract text dari result berdasarkan text_field
            doc_text = self._extract_text(result, text_field)
            query_doc_pairs.append([query, doc_text])
        
        # Hitung relevance scores menggunakan cross-encoder
        scores = self.model.predict(query_doc_pairs)
        
        # Tambahkan rerank_score ke setiap result
        for i, result in enumerate(results):
            result['rerank_score'] = float(scores[i])
        
        # Sort berdasarkan rerank_score (descending)
        reranked_results = sorted(results, key=lambda x: x['rerank_score'], reverse=True)
        
        # Return top_k results jika dispesifikasi
        if top_k is not None:
            return reranked_results[:top_k]
        
        return reranked_results
    
    def _extract_text(self, result: Dict[str, Any], text_field: str) -> str:
        """
        Extract text dari result untuk digunakan dalam reranking.
        Bisa handle nested fields dan multiple fields.
        
        Args:
            result: Dictionary hasil pencarian
            text_field: Field name atau path (bisa nested dengan dot notation)
        
        Returns:
            Text yang akan digunakan untuk reranking
        """
        # Handle nested fields (e.g., "place.name")
        if '.' in text_field:
            parts = text_field.split('.')
            value = result
            for part in parts:
                if isinstance(value, dict) and part in value:
                    value = value[part]
                else:
                    return ""
            return str(value) if value else ""
        
        # Handle direct field access
        if text_field in result:
            text = str(result[text_field])
        # Fallback: coba ambil dari nested 'place' object jika ada
        elif 'place' in result and isinstance(result['place'], dict):
            text = str(result['place'].get(text_field, ""))
        else:
            text = ""
        
        return text
    
    def rerank_with_description(
        self,
        query: str,
        results: List[Dict[str, Any]],
        name_field: str = "name",
        description_field: str = "description",
        top_k: int = None,
        description_weight: float = 0.3
    ) -> List[Dict[str, Any]]:
        """
        Advanced reranking yang mempertimbangkan baik nama maupun deskripsi.
        Berguna untuk query yang lebih deskriptif.
        
        Args:
            query: Query pencarian
            results: List hasil pencarian
            name_field: Field untuk nama/judul
            description_field: Field untuk deskripsi
            top_k: Jumlah hasil teratas
            description_weight: Bobot untuk deskripsi (0-1), sisanya untuk nama
        
        Returns:
            List hasil yang sudah direrank
        """
        if not results:
            return []
        
        # Score berdasarkan nama
        name_pairs = [[query, self._extract_text(r, name_field)] for r in results]
        name_scores = self.model.predict(name_pairs)
        
        # Score berdasarkan deskripsi
        desc_pairs = [[query, self._extract_text(r, description_field)] for r in results]
        desc_scores = self.model.predict(desc_pairs)
        
        # Combine scores dengan weighted average
        for i, result in enumerate(results):
            name_score = float(name_scores[i])
            desc_score = float(desc_scores[i])
            
            combined_score = (
                (1 - description_weight) * name_score + 
                description_weight * desc_score
            )
            
            result['rerank_score'] = combined_score
            result['name_score'] = name_score
            result['description_score'] = desc_score
        
        # Sort dan return
        reranked_results = sorted(results, key=lambda x: x['rerank_score'], reverse=True)
        
        if top_k is not None:
            return reranked_results[:top_k]
        
        return reranked_results


# Singleton instance untuk reuse model
_reranker_instance = None

def get_reranker() -> RerankingService:
    """
    Get atau create singleton instance dari RerankingService.
    Ini mencegah loading model berulang kali.
    """
    global _reranker_instance
    if _reranker_instance is None:
        _reranker_instance = RerankingService()
    return _reranker_instance
