"""LLM feedback generation service using Hugging Face."""
import os
from typing import Optional
from huggingface_hub import InferenceClient


class LLMService:
    """Service for generating feedback using Hugging Face API."""

    # Models verified to work on Hugging Face Inference API free tier
    # Now using Chat Completion API for better compatibility
    AVAILABLE_MODELS = {
        'llama-3.3': 'meta-llama/Llama-3.3-70B-Instruct',  # High quality, no thinking tags
        'mistral': 'mistralai/Mistral-7B-Instruct-v0.2',  # Fast and reliable
        'zephyr': 'HuggingFaceH4/zephyr-7b-beta',  # Instruction-tuned
        'deepseek-r1': 'deepseek-ai/DeepSeek-R1',  # Advanced reasoning (verbose)
        'flan-t5': 'google/flan-t5-base',  # Fallback option
    }
    
    # Default model (high quality, compact)
    DEFAULT_MODEL = 'llama-3.3'

    def __init__(self):
        """Initialize Hugging Face client."""
        api_key = os.getenv('HF_API_KEY', '')
        
        # Get model choice from env, default to FLAN-T5 (verified to work)
        model_choice = os.getenv('HF_MODEL', self.DEFAULT_MODEL).lower()
        self.model = self.AVAILABLE_MODELS.get(model_choice, self.AVAILABLE_MODELS[self.DEFAULT_MODEL])
        
        if not api_key:
            self.client = None
            self.use_mock = True
            print("[ℹ️  LLM Service] No HF_API_KEY found. Using mock feedback.")
        else:
            self.client = InferenceClient(api_key=api_key)
            self.use_mock = False
            print(f"[✅ LLM Service] Initialized with model: {self.model}")

    def generate_feedback(
        self,
        student_name: str,
        marks: float,
        category: str,
        course: str,
        max_marks: float = 100
    ) -> str:
        """
        Generate personalized feedback for a student.
        
        Args:
            student_name: Name of the student
            marks: Marks obtained
            category: Pass/Fail/Distinction
            course: Course/exam name
            max_marks: Total marks (default 100)
            
        Returns:
            Personalized feedback message
        """
        if self.use_mock:
            return self._generate_mock_feedback(student_name, marks, category, course, max_marks)

        try:
            return self._generate_llm_feedback(student_name, marks, category, course, max_marks)
        except Exception as e:
            print(f"[⚠️  LLM API Error] {str(e)[:100]}... Falling back to mock feedback")
            return self._generate_mock_feedback(student_name, marks, category, course, max_marks)

    def _generate_llm_feedback(
        self,
        student_name: str,
        marks: float,
        category: str,
        course: str,
        max_marks: float
    ) -> str:
        """Generate feedback using Hugging Face Inference API (Chat Completion)."""
        percentage = (marks / max_marks) * 100

        # Prompt for chat completion API - kept concise to avoid verbose outputs
        user_message = f"""Brief feedback only (1-2 sentences). Student {student_name} scored {percentage:.1f}% ({category}) in {course}. Constructive, encouraging, actionable."""

        try:
            # Use Chat Completion API (OpenAI-compatible format)
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": user_message}
                ],
                max_tokens=100,  # Reduced for compact responses
                temperature=0.5,  # Lower temp for more consistent output
            )

            # Extract feedback from standard chat completion response format
            feedback = response.choices[0].message.content.strip()
            
            # Remove thinking tags (used by reasoning models like DeepSeek-R1)
            if '<think>' in feedback:
                # Extract only the content after thinking tags
                parts = feedback.split('</think>')
                feedback = parts[-1].strip() if len(parts) > 1 else feedback
            
            # Cleanup: remove common unwanted prefixes/markup
            unwanted_prefixes = [
                "Feedback:", "feedback:", "**", "Here's the feedback:", 
                "Here's your feedback:", "Assistant:", "Student Feedback:"
            ]
            for prefix in unwanted_prefixes:
                while feedback.lower().startswith(prefix.lower()):
                    feedback = feedback[len(prefix):].strip()
            
            # Clean up markdown bold markers if any
            feedback = feedback.replace('**', '').strip()
            
            # Ensure single complete sentence range (80-150 chars)
            if len(feedback) > 150:
                # Truncate at last period or comma
                for sep in ['.', ',']:
                    idx = feedback.rfind(sep, 0, 150)
                    if idx > 80:
                        feedback = feedback[:idx+1].strip()
                        break
                if len(feedback) > 150:
                    feedback = feedback[:150].rsplit(' ', 1)[0] + '.'
            
            return feedback if feedback and len(feedback) > 10 else self._generate_mock_feedback(student_name, marks, category, course, max_marks)

        except Exception as e:
            print(f"[⚠️  Chat Completion Error] {str(e)[:100]}")
            raise

    def _generate_mock_feedback(
        self,
        student_name: str,
        marks: float,
        category: str,
        course: str,
        max_marks: float
    ) -> str:
        """Generate mock feedback for testing."""
        percentage = (marks / max_marks) * 100

        feedbacks = {
            'distinction': [
                f"Excellent performance, {student_name}! You scored {percentage:.1f}% in {course}. Keep up this outstanding work and consider exploring advanced topics to deepen your expertise.",
                f"Outstanding result, {student_name}! Your {percentage:.1f}% score in {course} demonstrates strong mastery. Explore supplementary materials to further enhance your knowledge.",
                f"Congratulations, {student_name}! Your exceptional performance ({percentage:.1f}%) in {course} shows excellent understanding. Consider peer tutoring to reinforce your leadership in academics.",
            ],
            'pass': [
                f"Good effort, {student_name}! You scored {percentage:.1f}% in {course}. Focus on the challenging concepts and practice regularly to improve further.",
                f"Well done, {student_name}! Your {percentage:.1f}% score in {course} shows satisfactory understanding. Review the difficult sections and solve more practice problems.",
                f"Nice work, {student_name}! You've passed {course} with {percentage:.1f}%. Identify weak areas and dedicate extra time to strengthen your fundamentals.",
            ],
            'fail': [
                f"Don't worry, {student_name}. Your {percentage:.1f}% score in {course} suggests you need more practice. Review the fundamentals and seek additional support.",
                f"Encouragement to you, {student_name}. Your {percentage:.1f}% in {course} indicates challenging areas. Focus on core concepts and consider forming study groups.",
                f"Keep learning, {student_name}! Your {percentage:.1f}% score in {course} shows opportunity for growth. Start with basic concepts and build progressively.",
            ],
        }

        import random
        category_key = category.lower() if category.lower() in feedbacks else 'pass'
        return random.choice(feedbacks[category_key])


# Global instance
_llm_service = None


def get_llm_service() -> LLMService:
    """Get or create LLM service instance."""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service
