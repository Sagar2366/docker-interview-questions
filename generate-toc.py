#!/usr/bin/env python3
"""
Generate Table of Contents for Docker Interview Questions
"""

import os
import re
from pathlib import Path

def extract_questions_from_file(file_path):
    """Extract question titles from README.md files"""
    questions = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Find all questions (## followed by number)
        pattern = r'^## (\d+)\.\s+(.+?)$'
        matches = re.findall(pattern, content, re.MULTILINE)
        
        for num, title in matches:
            questions.append(f"{num}. {title}")
            
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    
    return questions

def generate_toc():
    """Generate comprehensive table of contents"""
    base_dir = Path('.')
    
    sections = {
        'basic-concepts': 'Basic Concepts',
        'docker-architecture': 'Docker Architecture', 
        'docker-networking': 'Docker Networking',
        'docker-security': 'Docker Security',
        'docker-compose': 'Docker Compose',
        'dockerfile-best-practices': 'Dockerfile Best Practices',
        'latest-features': 'Latest Features',
        'advanced-topics': 'Advanced Topics',
        'practical-scenarios': 'Practical Scenarios'
    }
    
    toc_content = "# Complete Table of Contents\n\n"
    toc_content += "## Overview\n\n"
    toc_content += "This document provides a comprehensive overview of all Docker interview questions organized by category.\n\n"
    
    total_questions = 0
    
    for folder, title in sections.items():
        readme_path = base_dir / folder / 'README.md'
        
        if readme_path.exists():
            questions = extract_questions_from_file(readme_path)
            
            if questions:
                toc_content += f"## {title}\n\n"
                toc_content += f"**Location**: [`{folder}/README.md`]({folder}/README.md)\n\n"
                
                for question in questions:
                    toc_content += f"- {question}\n"
                
                toc_content += f"\n**Total Questions**: {len(questions)}\n\n"
                total_questions += len(questions)
    
    # Add examples section
    toc_content += "## Examples and References\n\n"
    toc_content += "- [Dockerfile Examples](examples/Dockerfile-examples.md)\n"
    toc_content += "- [Docker Compose Examples](examples/docker-compose-examples.md)\n"
    toc_content += "- [Docker Commands Reference](quick-reference/docker-commands.md)\n\n"
    
    # Add summary
    toc_content += f"## Summary\n\n"
    toc_content += f"**Total Questions**: {total_questions}\n"
    toc_content += f"**Categories**: {len(sections)}\n"
    toc_content += f"**Difficulty Levels**: Beginner to Expert\n\n"
    
    toc_content += "---\n\n"
    toc_content += "*Generated automatically by generate-toc.py*\n"
    
    # Write TOC file
    with open('TABLE_OF_CONTENTS.md', 'w', encoding='utf-8') as f:
        f.write(toc_content)
    
    print(f"✅ Generated TABLE_OF_CONTENTS.md with {total_questions} questions")

if __name__ == "__main__":
    generate_toc()