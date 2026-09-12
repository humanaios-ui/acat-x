#!/usr/bin/env python3
"""
ACAT-X Phase A: Consist/Drift extractor
Scores error recovery patterns and thrashing detection
Feeds: state vector (ρ=0.65 vs self ρ=-0.573 from blind-rating test)
       Detects when practices are error-recovering cleanly vs thrashing

Key insight from blind-rating: self-report on state is INVERSE predictive (ρ -0.573)
Practitioners underestimate their own error recovery. Tool-use patterns are more accurate.
"""
from dataclasses import dataclass
from typing import List, Dict, Tuple
import re

@dataclass
class ErrorEvent:
    turn: int
    error_text: str
    error_type: str  # "file_not_found", "syntax_error", "timeout", "permission", "other"
    recovered: bool  # did recovery happen in next 3 turns?
    recovery_turn: int  # turn number of recovery

def categorize_error(text: str) -> Tuple[str, bool]:
    """Categorize error type and whether it looks recoverable."""
    text_lower = text.lower()
    
    patterns = {
        "file_not_found": (r"not found|no such file", True),
        "syntax_error": (r"syntax error|SyntaxError", True),
        "timeout": (r"timeout|Connection terminated", True),
        "permission": (r"permission denied|EACCES", True),
        "type_error": (r"TypeError|Cannot use import", True),
        "module_error": (r"ModuleNotFoundError|ImportError", True),
        "thrashing": (r"repeated|again|retry|loop|stack|overflow", False),
    }
    
    for error_type, (pattern, is_recoverable) in patterns.items():
        if re.search(pattern, text, re.IGNORECASE):
            return error_type, is_recoverable
    
    return "other", True

def extract_errors(transcript: List[dict]) -> List[ErrorEvent]:
    """Extract error events from transcript."""
    errors = []
    
    for i, turn in enumerate(transcript):
        if turn.get("role") != "assistant":
            continue
        
        tool_results = turn.get("tool_results", [])
        for result in tool_results:
            if result.get("is_error"):
                content = result.get("content", "")
                error_type, _ = categorize_error(content)
                
                # Check if recovered in next 3 turns
                recovered = False
                recovery_turn = -1
                for j in range(i+1, min(i+4, len(transcript))):
                    next_turn = transcript[j]
                    if next_turn.get("role") == "assistant":
                        next_results = next_turn.get("tool_results", [])
                        for nr in next_results:
                            if not nr.get("is_error"):
                                # Found a successful command nearby
                                recovered = True
                                recovery_turn = j
                                break
                    if recovered:
                        break
                
                errors.append(ErrorEvent(
                    turn=i,
                    error_text=content[:100],
                    error_type=error_type,
                    recovered=recovered,
                    recovery_turn=recovery_turn
                ))
    
    return errors

def score_consistency(transcript: List[dict]) -> dict:
    """
    Score consistency/state dimension: error recovery patterns.
    
    Formula: clean_run = no errors, some_errors_recovered = recovery within 3 turns, thrashing = repeated errors without recovery
    
    Scale:
    - 1.0: clean run (0-1 errors in ~50 turns, all recovered)
    - 0.5: some errors, recovered consistently
    - 0.0: thrashing (repeated errors, no recovery pattern)
    
    Returns: {score, n, evidence, tier, confidence}
    """
    errors = extract_errors(transcript)
    
    if not errors:
        # Clean run
        return {
            "dimension": "consistency",
            "score": 1.0,
            "n": len(transcript),
            "clean_run": True,
            "errors_found": 0,
            "tier": "deterministic",
            "confidence": 0.9,
            "evidence": [
                {"rule": "zero-errors", "count": 0, "detail": "No errors in transcript"},
            ]
        }
    
    # Count recovery patterns
    recovered_count = sum(1 for e in errors if e.recovered)
    unrecovered_count = len(errors) - recovered_count
    
    # Detect thrashing: repeated same-type errors without recovery
    error_types = [e.error_type for e in errors]
    repeated_errors = sum(1 for t in error_types if error_types.count(t) > 1)
    
    if unrecovered_count > len(errors) * 0.5:
        # More than half unrecovered = thrashing
        score = 0.0
        confidence = 0.85
    elif recovered_count == len(errors):
        # All recovered = clean
        score = 0.8 if len(errors) <= 2 else 0.6
        confidence = 0.85
    else:
        # Mixed: some recovered, some not
        score = 0.4
        confidence = 0.7
    
    return {
        "dimension": "consistency",
        "score": score,
        "n": len(errors),
        "errors_found": len(errors),
        "recovered": recovered_count,
        "unrecovered": unrecovered_count,
        "repeated_error_types": repeated_errors,
        "tier": "deterministic",
        "confidence": confidence,
        "evidence": [
            {"rule": "error-recovery", "count": recovered_count, "detail": f"{recovered_count} errors with recovery"},
            {"rule": "error-thrashing", "count": unrecovered_count, "detail": f"{unrecovered_count} errors without recovery"},
            {"rule": "repeated-errors", "count": repeated_errors, "detail": f"{repeated_errors} repeated error types"},
        ]
    }

if __name__ == "__main__":
    # Example
    mock_transcript = [
        {"role": "assistant", "content": "Running install...", "tool_results": [
            {"tool": "Bash", "content": "error: permission denied", "is_error": True}
        ]},
        {"role": "assistant", "content": "Trying with sudo...", "tool_results": [
            {"tool": "Bash", "content": "installed successfully", "is_error": False}
        ]},
        {"role": "assistant", "content": "Running tests...", "tool_results": [
            {"tool": "Bash", "content": "tests passed", "is_error": False}
        ]},
    ]
    
    result = score_consistency(mock_transcript)
    print(f"Consistency score: {result}")
