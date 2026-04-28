"""Student classification service."""
from typing import List, Dict, Any


def classify_students(
    students: List[Dict[str, Any]],
    pass_threshold: float,
    fail_threshold: float,
    distinction_threshold: float
) -> List[Dict[str, Any]]:
    """
    Classify students as Pass, Fail, or Distinction based on marks and thresholds.
    
    Classification logic:
    - Distinction: marks >= distinction_threshold
    - Pass: marks >= pass_threshold and marks < distinction_threshold
    - Fail: marks < fail_threshold
    
    Args:
        students: List of student dictionaries with 'Marks' key
        pass_threshold: Minimum marks for pass (typically 40)
        fail_threshold: Minimum marks for distinction (typically 40)
        distinction_threshold: Minimum marks for distinction (typically 70)
        
    Returns:
        List of students with 'Status' and 'Category' keys added
    """
    classified = []
    
    for student in students:
        marks = student['Marks']
        
        if marks >= distinction_threshold:
            status = 'Distinction'
            category = 'distinction'
        elif marks >= pass_threshold:
            status = 'Pass'
            category = 'pass'
        else:
            status = 'Fail'
            category = 'fail'
        
        classified.append({
            **student,
            'Status': status,
            'Category': category,
        })
    
    return classified


def get_category_color(category: str) -> str:
    """Get Bootstrap color for category."""
    colors = {
        'distinction': 'success',
        'pass': 'info',
        'fail': 'danger'
    }
    return colors.get(category, 'secondary')
