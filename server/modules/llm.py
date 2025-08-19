from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
from langchain.callbacks import StdOutCallbackHandler
from langchain.memory import ConversationSummaryBufferMemory
import os
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class MediCoreConfig:
    """Configuration class for MediCore AI"""
    
    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.model_name = os.getenv("GROQ_MODEL", "llama3-70b-8192")
        self.temperature = float(os.getenv("LLM_TEMPERATURE", "0.1"))
        self.max_tokens = int(os.getenv("MAX_TOKENS", "4096"))
        self.top_p = float(os.getenv("TOP_P", "0.95"))
        
        # Validate required configurations
        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
    
    def get_llm_params(self) -> Dict[str, Any]:
        """Get LLM parameters"""
        return {
            "groq_api_key": self.groq_api_key,
            "model_name": self.model_name,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
            "streaming": True,
            "verbose": True
        }

class MediCorePrompts:
    """Advanced prompt templates for MediCore AI"""
    
    @staticmethod
    def get_main_prompt() -> PromptTemplate:
        """Main conversation prompt for MediCore AI"""
        template = """
🧬 **MediCore AI - Advanced Healthcare Intelligence**

You are **MediCore AI**, a state-of-the-art medical AI assistant with advanced healthcare intelligence. You specialize in providing evidence-based medical information with precision and clarity.

**Core Principles:**
• Evidence-based responses only from provided context
• Clear, professional medical communication
• Patient safety and ethical considerations first
• Acknowledge limitations and recommend professional consultation

---

📚 **Medical Knowledge Context**:
{context}

🔍 **Patient/User Inquiry**:
{question}

---

🧬 **MediCore AI Response Guidelines**:

**ANALYSIS FRAMEWORK:**
1. **Context Review**: Analyze provided medical literature/documents
2. **Evidence Assessment**: Identify relevant, peer-reviewed information
3. **Risk Evaluation**: Consider safety implications and contraindications
4. **Clarity Check**: Ensure response is understandable for the target audience

**RESPONSE STRUCTURE:**
💡 **Key Information**: [Main medical facts from context]
⚠️ **Important Considerations**: [Safety warnings, limitations, contraindications]
📋 **Evidence Level**: [Strength of evidence from provided sources]
🏥 **Professional Consultation**: [When to seek medical advice]

**SAFETY PROTOCOLS:**
• If insufficient context: "Based on the available information, I cannot provide a complete answer. Please consult a healthcare professional."
• For emergency symptoms: "This appears to be a medical emergency. Seek immediate medical attention."
• For drug interactions: Always emphasize checking with pharmacist/doctor
• For diagnostic questions: Never provide definitive diagnoses

**RESPONSE TONE:**
• Professional and empathetic
• Scientifically accurate
• Appropriately cautious
• Encouraging of professional medical care

Remember: You are providing educational information to support informed healthcare decisions, not replacing professional medical consultation.

Generate a comprehensive, evidence-based response following these guidelines.
"""
        return PromptTemplate(
            input_variables=["context", "question"],
            template=template
        )
    
    @staticmethod
    def get_emergency_prompt() -> PromptTemplate:
        """Emergency response prompt"""
        template = """
🚨 **EMERGENCY PROTOCOL ACTIVATED**

You are MediCore AI detecting a potential medical emergency.

Context: {context}
Emergency Query: {question}

IMMEDIATE RESPONSE:
⚠️ **URGENT**: This appears to be a medical emergency situation.

🆘 **IMMEDIATE ACTION REQUIRED**:
• Call emergency services (911/local emergency number) immediately
• If unconscious: Check breathing and pulse, consider CPR if trained
• Do not delay seeking professional medical care

📋 **Based on Available Information**:
{context}

🏥 **Next Steps**:
1. Contact emergency services immediately
2. Follow dispatcher instructions
3. Have medical history/medications ready if possible
4. Stay calm and provide clear information to emergency responders

⚠️ **DISCLAIMER**: This is an emergency situation requiring immediate professional medical intervention. Do not rely solely on AI advice for emergency medical care.
"""
        return PromptTemplate(
            input_variables=["context", "question"],
            template=template
        )
    
    @staticmethod
    def get_drug_interaction_prompt() -> PromptTemplate:
        """Specialized prompt for drug interactions"""
        template = """
💊 **MediCore AI - Pharmaceutical Intelligence Module**

You are analyzing potential drug interactions and pharmaceutical information.

**Pharmaceutical Context**: {context}
**Drug Inquiry**: {question}

**PHARMACEUTICAL ANALYSIS FRAMEWORK**:

🔬 **Drug Profile Analysis**:
• Mechanism of action
• Therapeutic class
• Known interactions
• Contraindications

⚠️ **Safety Assessment**:
• Interaction severity levels
• Risk factors
• Patient populations at risk
• Monitoring requirements

📊 **Evidence Review**:
• Clinical study data
• FDA warnings/alerts
• Professional guidelines
• Case reports

**RESPONSE FORMAT**:
💊 **Drug Information**: [Key pharmaceutical facts]
⚠️ **Interaction Risks**: [Potential interactions and severity]
🩺 **Clinical Considerations**: [Monitoring, dosing, timing]
🏥 **Professional Guidance**: [When to consult pharmacist/physician]

**MANDATORY DISCLAIMERS**:
• Always verify with pharmacist or physician
• Individual responses may vary
• Consider all medications, supplements, and health conditions
• Never stop prescribed medications without medical consultation

Provide evidence-based pharmaceutical information with appropriate safety warnings.
"""
        return PromptTemplate(
            input_variables=["context", "question"],
            template=template
        )

class MediCoreChainBuilder:
    """Advanced chain builder for MediCore AI"""
    
    def __init__(self, config: MediCoreConfig):
        self.config = config
        self.prompts = MediCorePrompts()
        
    def _create_llm(self) -> ChatGroq:
        """Create and configure the LLM"""
        try:
            llm = ChatGroq(**self.config.get_llm_params())
            logger.info(f"✅ MediCore AI LLM initialized with model: {self.config.model_name}")
            return llm
        except Exception as e:
            logger.error(f"❌ Failed to initialize LLM: {str(e)}")
            raise
    
    def _detect_query_type(self, question: str) -> str:
        """Detect the type of medical query to use appropriate prompt"""
        emergency_keywords = [
            "emergency", "urgent", "chest pain", "heart attack", "stroke", 
            "bleeding", "unconscious", "severe pain", "difficulty breathing",
            "allergic reaction", "overdose", "suicide", "trauma"
        ]
        
        drug_keywords = [
            "drug", "medication", "prescription", "pill", "interaction", 
            "side effect", "dosage", "pharmacy", "antibiotic", "painkiller"
        ]
        
        question_lower = question.lower()
        
        if any(keyword in question_lower for keyword in emergency_keywords):
            return "emergency"
        elif any(keyword in question_lower for keyword in drug_keywords):
            return "drug"
        else:
            return "general"
    
    def _get_prompt_by_type(self, query_type: str) -> PromptTemplate:
        """Get appropriate prompt based on query type"""
        prompt_map = {
            "emergency": self.prompts.get_emergency_prompt(),
            "drug": self.prompts.get_drug_interaction_prompt(),
            "general": self.prompts.get_main_prompt()
        }
        return prompt_map.get(query_type, self.prompts.get_main_prompt())
    
    def create_retrieval_chain(self, retriever, query_type: str = "general") -> RetrievalQA:
        """Create enhanced retrieval QA chain"""
        try:
            llm = self._create_llm()
            prompt = self._get_prompt_by_type(query_type)
            
            # Create callback handlers for monitoring
            callbacks = [StdOutCallbackHandler()]
            
            chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=retriever,
                chain_type_kwargs={
                    "prompt": prompt,
                    "verbose": True
                },
                return_source_documents=True,
                callbacks=callbacks
            )
            
            logger.info(f"✅ MediCore AI chain created successfully with {query_type} prompt")
            return chain
            
        except Exception as e:
            logger.error(f"❌ Failed to create retrieval chain: {str(e)}")
            raise

class MediCoreAI:
    """Main MediCore AI class with enhanced functionality"""
    
    def __init__(self):
        self.config = MediCoreConfig()
        self.chain_builder = MediCoreChainBuilder(self.config)
        self.session_start = datetime.now()
        
    def get_chain(self, retriever, question: str = None) -> RetrievalQA:
        """Get optimized chain based on question type"""
        query_type = "general"
        if question:
            query_type = self.chain_builder._detect_query_type(question)
            
        return self.chain_builder.create_retrieval_chain(retriever, query_type)
    
    def process_query(self, chain: RetrievalQA, question: str) -> Dict[str, Any]:
        """Process query with enhanced error handling and logging"""
        try:
            start_time = datetime.now()
            logger.info(f"🧬 MediCore AI processing query: {question[:100]}...")
            
            # Detect query type for appropriate handling
            query_type = self.chain_builder._detect_query_type(question)
            logger.info(f"📋 Query classified as: {query_type}")
            
            # Process the query
            result = chain({"query": question})
            
            # Calculate processing time
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # Format response
            response_data = {
                "answer": result.get("result", ""),
                "sources": [doc.metadata.get("source", "Unknown") for doc in result.get("source_documents", [])],
                "query_type": query_type,
                "processing_time": processing_time,
                "confidence": self._calculate_confidence(result),
                "timestamp": datetime.now().isoformat(),
                "session_duration": (datetime.now() - self.session_start).total_seconds()
            }
            
            logger.info(f"✅ Query processed in {processing_time:.2f}s with confidence: {response_data['confidence']}")
            return response_data
            
        except Exception as e:
            logger.error(f"❌ Error processing query: {str(e)}")
            return {
                "answer": "I apologize, but I encountered an error processing your query. Please try again or contact support if the issue persists.",
                "sources": [],
                "query_type": "error",
                "processing_time": 0,
                "confidence": 0,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _calculate_confidence(self, result: Dict[str, Any]) -> float:
        """Calculate confidence score based on sources and content"""
        try:
            source_count = len(result.get("source_documents", []))
            answer_length = len(result.get("result", ""))
            
            # Basic confidence calculation
            confidence = min(0.95, (source_count * 0.2) + (min(answer_length, 1000) / 1000 * 0.5) + 0.3)
            return round(confidence, 2)
        except:
            return 0.5

# Legacy function for backward compatibility
def get_llm_chain(retriever):
    """Legacy function - use MediCoreAI class for enhanced functionality"""
    logger.warning("⚠️ Using legacy get_llm_chain function. Consider upgrading to MediCoreAI class.")
    medicore = MediCoreAI()
    return medicore.get_chain(retriever)

# Factory function for easy initialization
def create_medicore_ai() -> MediCoreAI:
    """Create and initialize MediCore AI instance"""
    return MediCoreAI()

# Example usage and testing
if __name__ == "__main__":
    # Test configuration
    try:
        config = MediCoreConfig()
        print("✅ MediCore AI configuration loaded successfully")
        print(f"📋 Model: {config.model_name}")
        print(f"🌡️ Temperature: {config.temperature}")
        print(f"🎯 Max Tokens: {config.max_tokens}")
        
        # Test MediCore AI initialization
        medicore = create_medicore_ai()
        print("🧬 MediCore AI initialized successfully!")
        
    except Exception as e:
        print(f"❌ Configuration test failed: {str(e)}")