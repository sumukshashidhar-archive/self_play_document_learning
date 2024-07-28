"""
This script takes some pre-defined output text, and converts it into a standard user, assistant message format
"""
import sys, os; sys.path.append(os.getcwd()) if os.getcwd() not in sys.path else None
import re
import json
import argparse
import logging
import sys
from typing import List, Dict, Tuple

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

def extract_content(text: str, tag: str) -> Tuple[str, int]:
    pattern = rf'<{tag}>(.*?)</{tag}>'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip(), match.end()
    return "", -1

def process_exchange(exchange: str, logger: logging.Logger) -> List[Dict[str, str]]:
    exchange_data = []
    
    # Extract scenario
    scenario, pos = extract_content(exchange, 'scenario')
    if scenario:
        exchange_data.append({'role': 'system', 'content': scenario})
    else:
        logger.warning(f"Scenario not found in exchange: {exchange[:50]}...")
    
    # Extract questions and answers
    while pos < len(exchange):
        question, q_end = extract_content(exchange[pos:], 'question')
        if q_end == -1:
            break
        pos += q_end
        exchange_data.append({'role': 'user', 'content': question})
        
        answer, a_end = extract_content(exchange[pos:], 'answer')
        if a_end != -1:
            pos += a_end
            # Remove <thinking> tags from answer
            answer = re.sub(r'<thinking>.*?</thinking>', '', answer, flags=re.DOTALL).strip()
            exchange_data.append({'role': 'assistant', 'content': answer})
        else:
            logger.warning(f"Answer not found for question: {question[:50]}...")
    
    return exchange_data

def process_file(file_path: str, logger: logging.Logger) -> List[List[Dict[str, str]]]:
    logger.info(f"Processing file: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        logger.error(f"Input file not found: {file_path}")
        sys.exit(1)
    except IOError as e:
        logger.error(f"Error reading input file: {e}")
        sys.exit(1)

    all_exchanges = []
    exchanges = re.findall(r'<exchange\d+>(.*?)</exchange\d+>', content, re.DOTALL)
    
    if not exchanges:
        logger.warning("No exchanges found in the file.")
        return all_exchanges

    for i, exchange in enumerate(exchanges, 1):
        logger.info(f"Processing exchange {i}")
        exchange_data = process_exchange(exchange, logger)
        all_exchanges.append(exchange_data)

    logger.info(f"Processed {len(all_exchanges)} exchanges")
    return all_exchanges

def write_jsonl(data: List[List[Dict[str, str]]], output_file: str, logger: logging.Logger):
    logger.info(f"Writing output to: {output_file}")
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for exchange in data:
                f.write(json.dumps(exchange, ensure_ascii=False) + '\n')
    except IOError as e:
        logger.error(f"Error writing output file: {e}")
        sys.exit(1)
    logger.info("Conversion complete")

def main():
    parser = argparse.ArgumentParser(description="Convert structured text file to JSONL format with grouped exchanges")
    parser.add_argument("input_file", help="Path to the input text file")
    parser.add_argument("output_file", help="Path to the output JSONL file")
    args = parser.parse_args()

    logger = setup_logging()

    all_exchanges = process_file(args.input_file, logger)
    write_jsonl(all_exchanges, args.output_file, logger)

if __name__ == "__main__":
    main()