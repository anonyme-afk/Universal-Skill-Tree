import argparse
import sys
import os
from ust import get_registry, enable_branch

def cmd_list(args):
    registry = get_registry()
    if args.branch:
        if args.branch != "all":
            enable_branch(args.branch)
        else:
            # We don't have enable_all, so list from loaded or try to load all
            from ust import _BRANCH_MODULES
            for b in _BRANCH_MODULES.keys():
                enable_branch(b)
    
    skills = registry.list_all()
    if not skills:
        print("No skills loaded. Try specifying a branch: `ust list --branch system`")
        return
        
    print(f"Loaded {len(skills)} skills:")
    for skill in skills:
        print(f" - {skill.name} [{skill.branch}]: {skill.description}")

def cmd_run(args):
    # args.skill might be "system.run_command" or just "run_command"
    parts = args.skill.split('.')
    skill_name = parts[-1]
    branch = parts[0] if len(parts) > 1 else None
    
    if branch:
        enable_branch(branch)
        
    registry = get_registry()
    skill = registry.get(skill_name)
    if not skill:
        print(f"Error: Skill '{skill_name}' not found. Did you forget to specify the branch or enable it?")
        sys.exit(1)
        
    import json
    kwargs = {}
    for arg in args.args:
        if "=" in arg:
            k, v = arg.split("=", 1)
            # Try to decode json or fallback to string
            try:
                v = json.loads(v)
            except json.JSONDecodeError:
                pass
            kwargs[k] = v
            
    print(f"Running {skill_name} with {kwargs}...")
    try:
        # Since we just want to run directly, we call the fn
        result = skill.fn(**kwargs)
        print("Result:")
        print(result)
    except Exception as e:
        print(f"Execution Error: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Universal Skill Tree CLI")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # LIST command
    parser_list = subparsers.add_parser("list", help="List available skills")
    parser_list.add_argument("--branch", "-b", type=str, help="Load a specific branch before listing (or 'all')", default=None)
    
    # RUN command
    parser_run = subparsers.add_parser("run", help="Run a specific skill")
    parser_run.add_argument("skill", type=str, help="Name of the skill to run (e.g. system.get_cpu_usage)")
    parser_run.add_argument("args", nargs="*", help="Arguments in key=value format (e.g. command=\"echo hello\")")
    
    # CHECK command
    parser_check = subparsers.add_parser("check", help="Check configured environment variables")
    
    args = parser.parse_args()
    
    if args.command == "list":
        cmd_list(args)
    elif args.command == "run":
        cmd_run(args)
    elif args.command == "check":
        print("Checking environment variables in .env.ust is not fully implemented yet.")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
