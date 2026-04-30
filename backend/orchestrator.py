import json
import logging
from agents import CodeAgent, TestAgent, FixAgent
from runner import run_tests
from config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_requirement(requirement: str):
    if not requirement or not requirement.strip():
        yield f"data: {json.dumps({'status': 'error', 'message': 'Requirement cannot be empty'})}\n\n"
        return
    
    code_agent = CodeAgent()
    test_agent = TestAgent()
    fix_agent = FixAgent()
    
    try:
        yield f"data: {json.dumps({'status': 'start', 'message': 'Starting...'})}\n\n"
        
        yield f"data: {json.dumps({'status': 'generate', 'message': 'Generating code...'})}\n\n"
        files = code_agent.generate(requirement)
        logger.info(f"Generated {len(files)} files")
        
        yield f"data: {json.dumps({'status': 'generate', 'message': 'Generating tests...'})}\n\n"
        tests = test_agent.generate(files)
        logger.info(f"Generated {len(tests)} test files")
        
        for i in range(settings.max_fix_attempts):
            yield f"data: {json.dumps({'status': 'test', 'message': f'Running tests (attempt {i+1})...'})}\n\n"
            success, log = run_tests(files, tests)
            
            if success:
                yield f"data: {json.dumps({'status': 'done', 'message': 'All tests passed!', 'files': files})}\n\n"
                return
            
            if i < settings.max_fix_attempts - 1:
                yield f"data: {json.dumps({'status': 'fix', 'message': 'Fixing code...'})}\n\n"
                try:
                    files = fix_agent.fix(files, tests, log)
                except Exception as e:
                    logger.error(f"Fix failed: {e}")
                    yield f"data: {json.dumps({'status': 'error', 'message': f'Fix failed: {str(e)}'})}\n\n"
                    break
        
        yield f"data: {json.dumps({'status': 'done', 'message': 'Failed after max attempts', 'files': files})}\n\n"
        
    except Exception as e:
        logger.error(f"Process failed: {e}")
        yield f"data: {json.dumps({'status': 'error', 'message': str(e)})}\n\n"
