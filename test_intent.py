#!/usr/bin/env python3
"""Test the semantic intent detection capabilities"""

import sys
sys.path.insert(0, 'src')

from cache_for_claude.intent_detector import IntentDetector

def test_intent_detection():
    """Test various user feedback phrases"""
    detector = IntentDetector()

    test_phrases = [
        # Clearly positive
        ("Perfect! That's exactly what I needed", "positive"),
        ("Thanks so much!", "positive"),
        ("That worked beautifully", "positive"),
        ("Fixed the issue", "positive"),
        ("Problem solved", "positive"),
        ("Great job", "positive"),

        # Implicit positive
        ("ok let's move on to the next thing", "positive"),
        ("alright, now we can continue", "positive"),
        ("good, what's next?", "positive"),
        ("I see how it works now", "positive"),
        ("makes sense", "positive"),

        # Subtle positive
        ("hmm interesting approach", "neutral/positive"),
        ("oh I see what you did there", "positive"),
        ("ah that explains it", "positive"),

        # Clearly negative
        ("That didn't work", "negative"),
        ("Still getting the same error", "negative"),
        ("No, that's not right", "negative"),
        ("Try something else", "negative"),

        # Neutral
        ("Ok", "neutral"),
        ("Let me check", "neutral"),
        ("Hold on", "neutral"),

        # Context-dependent
        ("Finally!", "positive"),  # Relief = positive
        ("Whatever", "neutral/negative"),  # Could be resignation
        ("Sure", "neutral"),  # Depends on context
    ]

    print("=" * 60)
    print("SEMANTIC INTENT DETECTION TEST")
    print("=" * 60)

    for phrase, expected in test_phrases:
        intent, confidence = detector.detect_intent(phrase)

        # Color code the output
        if intent == 'positive':
            color = '\033[92m'  # Green
        elif intent == 'negative':
            color = '\033[91m'  # Red
        else:
            color = '\033[93m'  # Yellow

        reset = '\033[0m'

        print(f"\nPhrase: \"{phrase}\"")
        print(f"Expected: {expected}")
        print(f"Detected: {color}{intent}{reset} (confidence: {confidence:.2f})")

    # Test conversation flow
    print("\n" + "=" * 60)
    print("CONVERSATION FLOW ANALYSIS")
    print("=" * 60)

    conversation = [
        {'role': 'user', 'content': 'Can you help me fix the login bug?'},
        {'role': 'assistant', 'content': 'I found the issue in auth.js...'},
        {'role': 'user', 'content': 'Let me try that'},
        {'role': 'assistant', 'content': 'The fix has been applied'},
        {'role': 'user', 'content': 'Still not working, same error'},
        {'role': 'assistant', 'content': 'Let me check the database connection...'},
        {'role': 'user', 'content': "Oh wait, it's working now! I just had to refresh"},
    ]

    analysis = detector.analyze_conversation_flow(conversation)

    print("\nConversation:")
    for msg in conversation:
        prefix = "User: " if msg['role'] == 'user' else "Assistant: "
        print(f"  {prefix}{msg['content'][:60]}...")

    print(f"\nOverall Intent: {analysis['overall_intent']}")
    print(f"Confidence: {analysis['confidence']:.2f}")
    print(f"Scores: {analysis['scores']}")

if __name__ == "__main__":
    test_intent_detection()