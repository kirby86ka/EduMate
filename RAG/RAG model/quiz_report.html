import os
import json
from datetime import datetime

# Try to import AI libraries (optional)
try:
    from langchain_ollama import ChatOllama
    HAS_OLLAMA = True
except ImportError:
    HAS_OLLAMA = False

# ==============================================================================
# LEARNING RESOURCES DATABASE
# ==============================================================================
LEARNING_RESOURCES = {
    "JavaScript Variables": {
        "youtube": [
            {"title": "JavaScript Variables - var, let, and const", "url": "https://www.youtube.com/watch?v=9WIJQDvt4Us", "channel": "Programming with Mosh"},
            {"title": "JavaScript Variables Explained", "url": "https://www.youtube.com/watch?v=edlFjlzxkSI", "channel": "freeCodeCamp"}
        ],
        "articles": [
            {"title": "MDN: JavaScript Variables", "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Grammar_and_types#declarations"},
            {"title": "JavaScript.info - Variables", "url": "https://javascript.info/variables"}
        ],
        "explanation": "JavaScript has three ways to declare variables: var (function-scoped, older), let (block-scoped, can be reassigned), and const (block-scoped, cannot be reassigned). Use const by default, let when you need to reassign, and avoid var in modern code.",
        "tip": "Practice declaring variables with const first, and only use let when you know the value will change."
    },
    "React Hooks": {
        "youtube": [
            {"title": "React Hooks Tutorial - useEffect", "url": "https://www.youtube.com/watch?v=0ZJgIjIuY7U", "channel": "Web Dev Simplified"},
            {"title": "Complete React Hooks Guide", "url": "https://www.youtube.com/watch?v=TNhaISOUy6Q", "channel": "Codevolution"}
        ],
        "articles": [
            {"title": "React Docs: useEffect", "url": "https://react.dev/reference/react/useEffect"},
            {"title": "Complete Guide to useEffect", "url": "https://overreacted.io/a-complete-guide-to-useeffect/"}
        ],
        "explanation": "useEffect is a React Hook for handling side effects in functional components. Side effects include data fetching, subscriptions, manually changing the DOM, and timers. It runs after the component renders and can optionally clean up when the component unmounts.",
        "tip": "Start by understanding the dependency array - empty [] runs once, [value] runs when value changes, and no array runs after every render."
    },
    "Data Structures": {
        "youtube": [
            {"title": "Data Structures Easy to Advanced", "url": "https://www.youtube.com/watch?v=RBSGKlAvoiM", "channel": "freeCodeCamp"},
            {"title": "Big O Notation Full Course", "url": "https://www.youtube.com/watch?v=Mo4vesaut8g", "channel": "freeCodeCamp"}
        ],
        "articles": [
            {"title": "Big O Cheat Sheet", "url": "https://www.bigocheatsheet.com/"},
            {"title": "GeeksforGeeks: Binary Search Tree", "url": "https://www.geeksforgeeks.org/binary-search-tree-data-structure/"}
        ],
        "explanation": "Binary Search Trees (BST) have O(log n) time complexity for search in balanced trees because each comparison eliminates half of the remaining nodes. However, in worst-case unbalanced trees (like a linked list), it degrades to O(n). Self-balancing trees like AVL and Red-Black trees maintain O(log n).",
        "tip": "Draw out a balanced BST and trace through a search operation to visualize why it's O(log n) - you're halving the search space at each step."
    },
    "CSS Flexbox": {
        "youtube": [
            {"title": "Flexbox CSS in 20 Minutes", "url": "https://www.youtube.com/watch?v=JJSoEo8JSnc", "channel": "Traversy Media"},
            {"title": "Learn Flexbox in 15 Minutes", "url": "https://www.youtube.com/watch?v=fYq5PXgSsbE", "channel": "Web Dev Simplified"}
        ],
        "articles": [
            {"title": "CSS Tricks: Complete Guide to Flexbox", "url": "https://css-tricks.com/snippets/css/a-guide-to-flexbox/"},
            {"title": "MDN: Flexbox", "url": "https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Flexbox"}
        ],
        "explanation": "Flexbox is a CSS layout model that makes it easier to align and distribute space among items in a container. The flex-direction property sets the main axis (row, row-reverse, column, column-reverse), determining how flex items are placed in the container.",
        "tip": "Use the Chrome DevTools flexbox inspector to visualize and experiment with different flex properties in real-time."
    },
    "Git Version Control": {
        "youtube": [
            {"title": "Git and GitHub for Beginners", "url": "https://www.youtube.com/watch?v=RGOj5yH7evk", "channel": "freeCodeCamp"},
            {"title": "Git Branching Tutorial", "url": "https://www.youtube.com/watch?v=e2IbNHi4uCI", "channel": "The Net Ninja"}
        ],
        "articles": [
            {"title": "Git Branching - Basic Branching", "url": "https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging"},
            {"title": "Atlassian Git Branching Tutorial", "url": "https://www.atlassian.com/git/tutorials/using-branches"}
        ],
        "explanation": "Git checkout -b branch-name creates a new branch and immediately switches to it in one command. It's shorthand for 'git branch branch-name' followed by 'git checkout branch-name'. This is the most common way to start working on a new feature.",
        "tip": "Name your branches descriptively (feature/login-page, bugfix/header-alignment) to make it clear what each branch is for."
    }
}

# ==============================================================================
# QUIZ QUESTIONS DATABASE
# ==============================================================================
QUIZ_QUESTIONS = [
    {
        "id": 1,
        "topic": "JavaScript Variables",
        "question": "What is the correct way to declare a constant variable in JavaScript?",
        "options": [
            "A) var PI = 3.14",
            "B) let PI = 3.14",
            "C) const PI = 3.14",
            "D) constant PI = 3.14"
        ],
        "correct_answer": "C",
        "explanation": "const is used to declare constants that cannot be reassigned"
    },
    {
        "id": 2,
        "topic": "React Hooks",
        "question": "Which React Hook is used for managing side effects?",
        "options": [
            "A) useState",
            "B) useEffect",
            "C) useContext",
            "D) useReducer"
        ],
        "correct_answer": "B",
        "explanation": "useEffect is used for side effects like API calls, subscriptions, and DOM manipulation"
    },
    {
        "id": 3,
        "topic": "Data Structures",
        "question": "What is the time complexity of searching in a balanced binary search tree?",
        "options": [
            "A) O(1)",
            "B) O(n)",
            "C) O(log n)",
            "D) O(n²)"
        ],
        "correct_answer": "C",
        "explanation": "Binary search trees have O(log n) search time when balanced"
    },
    {
        "id": 4,
        "topic": "CSS Flexbox",
        "question": "Which property changes the main axis direction in flexbox?",
        "options": [
            "A) flex-wrap",
            "B) flex-direction",
            "C) justify-content",
            "D) align-items"
        ],
        "correct_answer": "B",
        "explanation": "flex-direction changes the main axis (row or column)"
    },
    {
        "id": 5,
        "topic": "Git Version Control",
        "question": "What command creates a new branch and switches to it?",
        "options": [
            "A) git branch new-branch",
            "B) git checkout -b new-branch",
            "C) git new-branch",
            "D) git switch new-branch"
        ],
        "correct_answer": "B",
        "explanation": "git checkout -b creates and switches to a new branch in one command"
    }
]

# ==============================================================================
# STEP 1: CONDUCT THE QUIZ
# ==============================================================================
def conduct_quiz():
    """
    Presents quiz questions to the student and records their answers.
    """
    print("\n" + "=" * 70)
    print("🎓 PROGRAMMING KNOWLEDGE QUIZ")
    print("=" * 70 + "\n")
    
    print("📋 Instructions:")
    print("   - Answer each question by typing A, B, C, or D")
    print("   - You will receive personalized learning resources based on your answers")
    print("   - Total Questions: 5\n")
    
    input("Press Enter to start the quiz... ")
    
    quiz_results = {
        "userId": input("\n👤 Enter your name: ").strip() or "Anonymous",
        "quizId": "programming_quiz_001",
        "dateTaken": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "totalQuestions": len(QUIZ_QUESTIONS),
        "correctAnswers": 0,
        "incorrectAnswers": 0,
        "incorrectlyAnswered": [],
        "correctlyAnswered": []
    }
    
    print("\n" + "=" * 70 + "\n")
    
    for idx, q in enumerate(QUIZ_QUESTIONS, 1):
        print(f"Question {idx}/{len(QUIZ_QUESTIONS)}")
        print(f"📚 Topic: {q['topic']}")
        print(f"\n{q['question']}\n")
        
        for option in q['options']:
            print(f"   {option}")
        
        while True:
            answer = input("\n✏️  Your answer (A/B/C/D): ").strip().upper()
            if answer in ['A', 'B', 'C', 'D']:
                break
            print("❌ Invalid input. Please enter A, B, C, or D.")
        
        # Check if answer is correct
        if answer == q['correct_answer']:
            print("✅ Correct!\n")
            quiz_results['correctAnswers'] += 1
            quiz_results['correctlyAnswered'].append({
                "questionId": q['id'],
                "topic": q['topic'],
                "questionText": q['question']
            })
        else:
            print(f"❌ Incorrect. The correct answer is {q['correct_answer']}")
            print(f"💡 {q['explanation']}\n")
            quiz_results['incorrectAnswers'] += 1
            quiz_results['incorrectlyAnswered'].append({
                "questionId": q['id'],
                "topic": q['topic'],
                "questionText": q['question'],
                "studentAnswer": answer,
                "correctAnswer": q['correct_answer'],
                "explanation": q['explanation']
            })
        
        print("-" * 70 + "\n")
    
    # Calculate score
    score_percentage = (quiz_results['correctAnswers'] / quiz_results['totalQuestions']) * 100
    quiz_results['score'] = f"{quiz_results['correctAnswers']}/{quiz_results['totalQuestions']} ({score_percentage:.0f}%)"
    
    # Display results
    print("=" * 70)
    print("📊 QUIZ RESULTS")
    print("=" * 70)
    print(f"✅ Correct Answers: {quiz_results['correctAnswers']}")
    print(f"❌ Incorrect Answers: {quiz_results['incorrectAnswers']}")
    print(f"📈 Score: {quiz_results['score']}")
    print("=" * 70 + "\n")
    
    # Save results to JSON
    with open('quiz_progress.json', 'w', encoding='utf-8') as f:
        json.dump(quiz_results, f, indent=2, ensure_ascii=False)
    
    print("💾 Quiz results saved to 'quiz_progress.json'\n")
    
    return quiz_results

# ==============================================================================
# STEP 2: GENERATE RECOMMENDATIONS
# ==============================================================================
def generate_recommendations(quiz_data):
    """
    Generates learning recommendations based on incorrect answers using curated resources.
    """
    incorrect_answers = quiz_data.get("incorrectlyAnswered", [])
    
    if not incorrect_answers:
        print("🎉 Perfect Score! No recommendations needed.\n")
        return None
    
    print("=" * 70)
    print("🎯 GENERATING PERSONALIZED LEARNING PLAN")
    print("=" * 70 + "\n")
    
    recommendations = []
    
    for idx, ans in enumerate(incorrect_answers, 1):
        topic = ans['topic']
        question = ans['questionText']
        
        print(f"📚 Topic {idx}: {topic}")
        print("   ✅ Generating recommendations...\n")
        
        # Get curated resources for this topic
        resources = LEARNING_RESOURCES.get(topic, {})
        
        if not resources:
            print(f"   ⚠️  No pre-loaded resources for '{topic}'\n")
            continue
        
        rec = {
            "topic": topic,
            "question": question,
            "resources": resources
        }
        
        recommendations.append(rec)
    
    # Display recommendations in terminal
    print("\n" + "╔" + "═" * 68 + "╗")
    print("║" + " 📋 YOUR PERSONALIZED LEARNING RECOMMENDATIONS ".center(68) + "║")
    print("╚" + "═" * 68 + "╝\n")
    
    for idx, rec in enumerate(recommendations, 1):
        topic_resources = rec['resources']
        
        # Topic Header
        print("┌" + "─" * 68 + "┐")
        print("│ " + f"📚 TOPIC {idx}: {rec['topic']}".ljust(67) + "│")
        print("└" + "─" * 68 + "┘")
        
        # Question
        print(f"\n❓ Question: {rec['question']}\n")
        
        # YouTube Videos Section
        print("╔" + "═" * 68 + "╗")
        print("║" + " 📹 YOUTUBE TUTORIALS ".center(68) + "║")
        print("╚" + "═" * 68 + "╝\n")
        
        for video_idx, video in enumerate(topic_resources.get('youtube', []), 1):
            print(f"  [{video_idx}] {video['title']}")
            print(f"      👤 Channel: {video['channel']}")
            print(f"      🔗 {video['url']}\n")
        
        # Articles Section
        print("╔" + "═" * 68 + "╗")
        print("║" + " 📄 ARTICLES & DOCUMENTATION ".center(68) + "║")
        print("╚" + "═" * 68 + "╝\n")
        
        for article_idx, article in enumerate(topic_resources.get('articles', []), 1):
            print(f"  [{article_idx}] {article['title']}")
            print(f"      🔗 {article['url']}\n")
        
        # Explanation Box
        explanation = topic_resources.get('explanation', 'No explanation available')
        print("╔" + "═" * 68 + "╗")
        print("║" + " 💡 EXPLANATION ".center(68) + "║")
        print("╚" + "═" * 68 + "╝")
        print(f"\n{explanation}\n")
        
        # Study Tip Box
        tip = topic_resources.get('tip', 'Practice regularly')
        print("╔" + "═" * 68 + "╗")
        print("║" + " ✅ STUDY TIP ".center(68) + "║")
        print("╚" + "═" * 68 + "╝")
        print(f"\n{tip}\n")
        
        print("═" * 70 + "\n")
    
    # Save recommendations
    output = {
        "student": quiz_data['userId'],
        "date": quiz_data['dateTaken'],
        "score": quiz_data['score'],
        "recommendations": recommendations
    }
    
    with open('recommendations.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print("\n╔" + "═" * 68 + "╗")
    print("║" + " ✅ RECOMMENDATIONS SAVED ".center(68) + "║")
    print("╚" + "═" * 68 + "╝")
    print(f"📄 File: recommendations.json")
    print(f"📄 File: quiz_progress.json\n")
    
    return recommendations

# ==============================================================================
# STEP 3: GENERATE HTML REPORT
# ==============================================================================
def generate_html_report(quiz_data, recommendations):
    """
    Generates a beautiful HTML report of the quiz results and recommendations.
    """
    if not recommendations:
        return
    
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quiz Results - {quiz_data['userId']}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }}
        .container {{ 
            max-width: 1000px; 
            margin: 0 auto; 
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}
        h1 {{ 
            color: #667eea; 
            margin-bottom: 10px;
            font-size: 2.5em;
        }}
        .header {{ 
            text-align: center; 
            margin-bottom: 40px;
            border-bottom: 3px solid #667eea;
            padding-bottom: 20px;
        }}
        .score {{ 
            display: flex;
            justify-content: space-around;
            margin: 30px 0;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
        }}
        .score-item {{ text-align: center; }}
        .score-value {{ 
            font-size: 2.5em; 
            font-weight: bold;
            color: #667eea;
        }}
        .topic {{ 
            margin: 30px 0;
            padding: 25px;
            background: #f8f9fa;
            border-radius: 15px;
            border-left: 5px solid #667eea;
        }}
        .topic h2 {{ 
            color: #667eea; 
            margin-bottom: 15px;
            font-size: 1.8em;
        }}
        .question {{ 
            font-style: italic; 
            color: #666;
            margin-bottom: 20px;
            padding: 10px;
            background: white;
            border-radius: 5px;
        }}
        .resource-section {{ margin: 20px 0; }}
        .resource-section h3 {{ 
            color: #764ba2; 
            margin-bottom: 10px;
            font-size: 1.3em;
        }}
        .resource {{ 
            margin: 10px 0; 
            padding: 15px;
            background: white;
            border-radius: 8px;
            transition: transform 0.2s;
        }}
        .resource:hover {{ 
            transform: translateX(5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        .resource a {{ 
            color: #667eea; 
            text-decoration: none;
            font-weight: 500;
        }}
        .resource a:hover {{ 
            text-decoration: underline; 
        }}
        .channel {{ 
            color: #999; 
            font-size: 0.9em;
            margin-left: 10px;
        }}
        .explanation {{ 
            padding: 15px;
            background: #e3f2fd;
            border-radius: 8px;
            margin: 15px 0;
            border-left: 4px solid #2196f3;
        }}
        .tip {{ 
            padding: 15px;
            background: #e8f5e9;
            border-radius: 8px;
            margin: 15px 0;
            border-left: 4px solid #4caf50;
        }}
        .emoji {{ font-size: 1.2em; }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #e0e0e0;
            color: #999;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎓 Quiz Results & Learning Plan</h1>
            <p style="color: #666; font-size: 1.2em;">Student: {quiz_data['userId']}</p>
            <p style="color: #999;">Date: {quiz_data['dateTaken']}</p>
        </div>
        
        <div class="score">
            <div class="score-item">
                <div class="score-value">{quiz_data['correctAnswers']}/{quiz_data['totalQuestions']}</div>
                <div>Score</div>
            </div>
            <div class="score-item">
                <div class="score-value">{int((quiz_data['correctAnswers']/quiz_data['totalQuestions'])*100)}%</div>
                <div>Accuracy</div>
            </div>
            <div class="score-item">
                <div class="score-value">{len(recommendations)}</div>
                <div>Topics to Review</div>
            </div>
        </div>
        
        <h2 style="color: #667eea; margin: 30px 0 20px 0;">📚 Your Personalized Learning Resources</h2>
"""
    
    for idx, rec in enumerate(recommendations, 1):
        topic_resources = rec['resources']
        html_content += f"""
        <div class="topic">
            <h2>{idx}. {rec['topic']}</h2>
            <div class="question">
                <strong>Question:</strong> {rec['question']}
            </div>
            
            <div class="resource-section">
                <h3>📹 YouTube Tutorials</h3>
"""
        for video in topic_resources.get('youtube', []):
            html_content += f"""
                <div class="resource">
                    <a href="{video['url']}" target="_blank">{video['title']}</a>
                    <span class="channel">by {video['channel']}</span>
                </div>
"""
        
        html_content += """
            </div>
            
            <div class="resource-section">
                <h3>📄 Articles & Documentation</h3>
"""
        for article in topic_resources.get('articles', []):
            html_content += f"""
                <div class="resource">
                    <a href="{article['url']}" target="_blank">{article['title']}</a>
                </div>
"""
        
        html_content += f"""
            </div>
            
            <div class="explanation">
                <strong>💡 Explanation:</strong><br>
                {topic_resources.get('explanation', 'No explanation available')}
            </div>
            
            <div class="tip">
                <strong>✅ Study Tip:</strong><br>
                {topic_resources.get('tip', 'Practice regularly')}
            </div>
        </div>
"""
    
    html_content += """
        <div class="footer">
            <p>Keep practicing and reviewing these resources! 💪</p>
            <p>Generated by Smart Quiz Recommender System</p>
        </div>
    </div>
</body>
</html>
"""
    
    with open('quiz_report.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("📄 HTML Report: quiz_report.html (Open in browser!)\n")

# ==============================================================================
# MAIN PROGRAM
# ==============================================================================
def main():
    """
    Main function that runs the complete quiz and recommendation system.
    """
    print("\n" + "█" * 70)
    print("█" + " " * 68 + "█")
    print("█" + "  🎓 SMART QUIZ & LEARNING RECOMMENDER SYSTEM 🎓  ".center(68) + "█")
    print("█" + " " * 68 + "█")
    print("█" * 70 + "\n")
    
    # Step 1: Conduct Quiz
    quiz_results = conduct_quiz()
    
    # Step 2: Check if recommendations are needed
    if quiz_results['incorrectAnswers'] == 0:
        print("🌟 Congratulations! You got a perfect score!")
        print("🎉 No additional study needed. Great job!\n")
        return
    
    # Step 3: Generate recommendations
    recommendations = generate_recommendations(quiz_results)
    
    print("\n" + "╔" + "═" * 68 + "╗")
    print("║" + " ✅ ALL DONE! ".center(68) + "║")
    print("╚" + "═" * 68 + "╝")
    print("\n📚 Your learning materials are ready!")
    print("📄 recommendations.json - Detailed data")
    print("📄 quiz_progress.json - Quiz results")
    print("\n💡 All YouTube links and articles are shown above!")
    print("=" * 70 + "\n")

# ==============================================================================
# RUN THE PROGRAM
# ==============================================================================
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Quiz interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()