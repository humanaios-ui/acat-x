#!/usr/bin/env python3
"""
ACAT-X Phase A: Service extractor
Scores task outcome turns (tests run, files delivered) vs user's stated ask
Feeds: do vector (task completion ρ=0.668 vs self ρ=0.5 from blind-rating test)
       impact vector (low confidence unless receipts present)
"""
from dataclasses import dataclass
from typing import List, Optional, Tuple

@dataclass
class TaskAsk:
    turn: int
    text: str
    ask_type: str  # "implement", "fix", "test", "document", "verify"

@dataclass
class TaskOutcome:
    turn: int
    text: str
    outcome_type: str  # "test_pass", "test_fail", "file_delivered", "build_success", "verified"
    receipt_present: bool

def extract_task_asks(transcript: List[dict]) -> List[TaskAsk]:
    """Extract task outcomes stated by the user."""
    asks = []
    
    ask_keywords = {
        "implement": ["implement", "write", "build", "create", "add"],
        "fix": ["fix", "fix", "resolve", "patch"],
        "test": ["test", "run tests", "pytest"],
        "document": ["document", "write docs", "explain"],
        "verify": ["verify", "check", "validate", "confirm"],
    }
    
    for i, turn in enumerate(transcript):
        if turn.get("role") != "user":
            continue
        
        text = turn.get("content", "").lower()
        for ask_type, keywords in ask_keywords.items():
            if any(kw in text for kw in keywords):
                asks.append(TaskAsk(
                    turn=i,
                    text=turn.get("content", ""),
                    ask_type=ask_type
                ))
                break
    
    return asks

def extract_task_outcomes(transcript: List[dict]) -> List[TaskOutcome]:
    """Extract outcomes: test passes, file deliverables, builds, verified state."""
    outcomes = []
    
    for i, turn in enumerate(transcript):
        if turn.get("role") != "assistant":
            continue
        
        tool_results = turn.get("tool_results", [])
        for result in tool_results:
            tool_name = result.get("tool", "")
            is_error = result.get("is_error", False)
            content = result.get("content", "")
            
            if not is_error:
                if "test" in tool_name.lower() or "pytest" in content.lower():
                    if "pass" in content.lower():
                        outcomes.append(TaskOutcome(
                            turn=i,
                            text=f"Tests passed: {content[:100]}",
                            outcome_type="test_pass",
                            receipt_present=True
                        ))
                
                elif tool_name == "Write":
                    outcomes.append(TaskOutcome(
                        turn=i,
                        text="File delivered",
                        outcome_type="file_delivered",
                        receipt_present=True
                    ))
                
                elif "build" in content.lower() and "success" in content.lower():
                    outcomes.append(TaskOutcome(
                        turn=i,
                        text=f"Build succeeded: {content[:100]}",
                        outcome_type="build_success",
                        receipt_present=True
                    ))
            
            else:
                # Error = unverified outcome
                if "test" in content.lower():
                    outcomes.append(TaskOutcome(
                        turn=i,
                        text=f"Test failed: {content[:100]}",
                        outcome_type="test_fail",
                        receipt_present=False
                    ))
    
    return outcomes

def match_tasks_to_outcomes(asks: List[TaskAsk], outcomes: List[TaskOutcome]) -> Tuple[int, int]:
    """
    Match user asks to outcomes: completed (ask + outcome with receipt), unverified.
    Returns (completed_with_receipt, unverified_or_missing).
    """
    completed = 0
    unverified = 0
    
    expected_outcomes_by_ask = {
        "implement": ["file_delivered", "build_success"],
        "fix": ["test_pass", "build_success"],
        "test": ["test_pass"],
        "document": ["file_delivered"],
        "verify": ["test_pass"],
    }
    
    matched_outcome_turns = set()
    
    for ask in asks:
        expected_types = expected_outcomes_by_ask.get(ask.ask_type, [])
        found_verified = False
        
        for outcome in outcomes:
            if (abs(outcome.turn - ask.turn) <= 10 and
                outcome.outcome_type in expected_types and
                outcome.receipt_present and
                outcome.turn not in matched_outcome_turns):
                completed += 1
                found_verified = True
                matched_outcome_turns.add(outcome.turn)
                break
        
        if not found_verified:
            unverified += 1
    
    return completed, unverified

def score_service(transcript: List[dict]) -> dict:
    """
    Score service dimension: task outcome receipts vs stated ask.
    Formula: completed_with_receipt / (completed + unverified)
    Returns: {score, n, evidence, tier, confidence}
    """
    asks = extract_task_asks(transcript)
    outcomes = extract_task_outcomes(transcript)
    
    completed, unverified = match_tasks_to_outcomes(asks, outcomes)
    
    total = completed + unverified
    if total == 0:
        score = None
        n = 0
        confidence = 0.0
    else:
        score = completed / total
        n = total
        confidence = 0.85 if completed > 0 else 0.3
    
    return {
        "dimension": "service",
        "score": score,
        "n": n,
        "completed_with_receipt": completed,
        "unverified_or_missing": unverified,
        "tier": "deterministic",
        "confidence": confidence,
        "evidence": [
            {"rule": "task-outcome-verified", "count": completed, "detail": f"{completed} asks with verified outcomes"},
            {"rule": "task-unverified", "count": unverified, "detail": f"{unverified} asks without verification"},
        ]
    }

if __name__ == "__main__":
    # Example
    mock_transcript = [
        {"role": "user", "content": "Implement the auth middleware"},
        {"role": "assistant", "content": "Writing the middleware...", "tool_results": [
            {"tool": "Write", "content": "File created", "is_error": False}
        ]},
        {"role": "user", "content": "Run the tests"},
        {"role": "assistant", "content": "Running tests...", "tool_results": [
            {"tool": "Bash", "content": "pytest auth_test.py ... PASSED", "is_error": False}
        ]},
    ]
    
    result = score_service(mock_transcript)
    print(f"Service score: {result}")
