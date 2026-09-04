import json
import logging
import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from app.models.analyses import Analysis
from app.models.conversations import Conversation
from app.engine.embedder import Embedder

logger = logging.getLogger(__name__)

class Document:
    def __init__(self, conversation_id: str, text: str, validation_status: str, metadata: dict):
        self.conversation_id = conversation_id
        self.text = text
        self.validation_status = validation_status
        self.metadata = metadata

class VectorStoreBase:
    async def load(self, session: AsyncSession):
        raise NotImplementedError
        
    async def search(self, query: str, top_k: int = 5, validation_status_in: list[str] = None, metadata_filters: dict = None) -> list[Document]:
        raise NotImplementedError

def cosine_similarity(a, b):
    # a is 1D array, b is 2D array
    dot = np.dot(b, a)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b, axis=1)
    # avoid division by zero
    norms = norm_a * norm_b
    norms[norms == 0] = 1e-10
    return dot / norms

class NumPyVectorStore(VectorStoreBase):
    def __init__(self):
        self.documents = []
        self.embeddings = None
        self.embedder = Embedder()
        self.is_loaded = False
        
    async def load(self, session: AsyncSession):
        """Loads all embeddings from the database into memory."""
        result = await session.execute(
            select(Analysis)
            .options(joinedload(Analysis.conversation).joinedload(Conversation.source))
            .where(Analysis.embedding.is_not(None))
        )
        analyses = result.scalars().all()
        
        self.documents = []
        embeddings_list = []
        
        for a in analyses:
            if not a.conversation:
                continue
                
            metadata = {
                "source_url": a.conversation.source_url,
                "primary_barrier_category": a.primary_barrier_category,
                "primary_barrier_detail": a.primary_barrier_detail,
                "purchase_intent": a.purchase_intent,
                "shopping_stage": a.shopping_stage,
                "wishlist_behavior": a.wishlist_intent,
                "uncertainty": a.uncertainty,
                "behavior_type": a.behavior,
                "comparison_behavior": a.comparison_behavior,
                "external_research": a.external_research,
                "unmet_need": a.unmet_need,
                "occasion": a.occasion,
                "product_category": a.product_category,
                "ai_confidence": a.ai_confidence
            }
            
            doc = Document(
                conversation_id=str(a.conversation.id),
                text=a.conversation.raw_content,
                validation_status=a.validation_status,
                metadata=metadata
            )
            
            self.documents.append(doc)
            # Embedding is stored as JSON array of floats
            emb = a.embedding if isinstance(a.embedding, list) else json.loads(a.embedding)
            embeddings_list.append(emb)
            
        if embeddings_list:
            self.embeddings = np.array(embeddings_list, dtype=np.float32)
        else:
            self.embeddings = np.array([])
            
        self.is_loaded = True
        logger.info(f"Loaded {len(self.documents)} documents into NumPyVectorStore.")
        
    async def search(self, query: str, top_k: int = 5, validation_status_in: list[str] = None, metadata_filters: dict = None) -> list[Document]:
        if not self.is_loaded or len(self.documents) == 0:
            return []
            
        # 1. Embed query
        query_embedding = await self.embedder.generate_embedding(query)
        q_vec = np.array(query_embedding, dtype=np.float32)
        
        # 2. Compute similarity
        similarities = cosine_similarity(q_vec, self.embeddings)
        
        # Evidence Ranking: Boost validated records
        for i, doc in enumerate(self.documents):
            if doc.validation_status in ['validated_relevant', 'ai_direct_evidence']:
                similarities[i] += 0.15
            elif doc.validation_status in ['indirect_pre_purchase', 'ai_indirect_evidence']:
                similarities[i] += 0.05
            elif doc.validation_status.startswith('excluded'):
                similarities[i] -= 0.50 # Heavily penalize excluded
                
        # 3. Sort by boosted similarity (no arbitrary cutoff, let the Relevance Gate decide)
        valid_indices = np.argsort(similarities)[::-1]
        
        # 4. Filter by metadata / status
        results = []
        for idx in valid_indices:
            doc = self.documents[idx]
            
            # Apply validation_status filter
            if validation_status_in and doc.validation_status not in validation_status_in:
                continue
                
            # Apply metadata filters (exact match)
            if metadata_filters:
                match = True
                for k, v in metadata_filters.items():
                    # Handle special SQL-like filters here if needed, 
                    # for now just simple exact match on truthy presence or exact value
                    doc_v = doc.metadata.get(k)
                    if v == "__not_null__":
                        if not doc_v:
                            match = False
                            break
                    elif doc_v != v:
                        match = False
                        break
                if not match:
                    continue
                    
            # Check a minimum similarity threshold if desired? (0.5?)
            if similarities[idx] < 0.3:
                continue
                
            # Add similarity score to metadata for transparency
            doc.metadata['retrieval_score'] = float(similarities[idx])
            results.append(doc)
            
            if len(results) >= top_k:
                break
                
        return results
