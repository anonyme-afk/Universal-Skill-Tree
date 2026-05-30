import os
import json
import importlib.util

def type_mapper(t):
    if 'str' in t: return 'string'
    if 'int' in t: return 'integer'
    if 'float' in t: return 'number'
    if 'bool' in t: return 'boolean'
    if 'list' in t: return 'array'
    if 'dict' in t: return 'object'
    return 'string'

def parse_params(params):
    properties = {}
    required = []
    
    for k, v in params.items():
        v_base = v.split('=')[0].strip()
        has_default = '=' in v
        
        properties[k] = {"type": type_mapper(v_base)}
        if not has_default:
            required.append(k)
            
    res = {}
    if properties:
        res["properties"] = properties
    if required:
        res["required"] = required
    return res

def import_catalog():
    spec = importlib.util.spec_from_file_location("skills_catalog", "skills_catalog.py")
    cat = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cat)
    
    skills = []
    for var in dir(cat):
        if var.endswith("_SKILLS") and isinstance(getattr(cat, var), list):
            skills.extend(getattr(cat, var))
            
    by_cat = {}
    for s in skills:
        category = s.get("category", "misc")
        if category not in by_cat:
            by_cat[category] = {}
        by_cat[category][s.get('name')] = s
        
    for category, cat_dict in by_cat.items():
        cat_skills = list(cat_dict.values())
        dir_path = f"ust/skills/{category}"
        os.makedirs(dir_path, exist_ok=True)
        
        init_path = os.path.join(dir_path, "__init__.py")
        if not os.path.exists(init_path):
            with open(init_path, "w", encoding="utf-8") as f:
                f.write("from .skills import *\\n")
                
        skills_path = os.path.join(dir_path, "skills.py")
        with open(skills_path, "w", encoding="utf-8") as f:
            f.write(f'\"\"\" ust.skills.{category} \"\"\"\\n')
            f.write('from __future__ import annotations\\n')
            f.write('import os\\n')
            f.write('import json\\n')
            f.write('from ust.core.registry import skill\\n\\n')
            
            for s in cat_skills:
                name = s.get("name")
                desc = s.get("description", "").replace('"', '\\\\"')
                params = s.get("parameters", {})
                code = s.get("code", "").strip()
                reqs = s.get("requires", [])
                env_vars = s.get("env_vars", [])
                
                parsed_params = parse_params(params)
                
                f.write(f'@skill(\\n')
                f.write(f'    name="{name}",\\n')
                f.write(f'    branch="{category}",\\n')
                f.write(f'    description="{desc}",\\n')
                if parsed_params:
                    f.write(f'    parameters={json.dumps(parsed_params, indent=4)},\\n')
                else:
                    f.write(f'    parameters={{}},\\n')
                f.write(f')\\n')
                
                lines = code.split('\n')
                f.write(f'{lines[0]}\n') # def ...
                
                f.write('    # --- P&P Checks ---\n')
                for env in env_vars:
                    f.write(f'    if not os.getenv("{env}"):\n')
                    f.write(f'        return "Erreur Plug & Play : clé API manquante ({env}). Ajoutez-la dans .env.ust puis réessayez."\n')
                
                f.write('    try:\n')
                for line in lines[1:]:
                    if line.strip():
                        f.write(f'    {line}\n')
                f.write('    except ImportError as e:\n')
                f.write('        reqs_str = " ".join(' + str(reqs) + ') if ' + str(reqs) + ' else str(e)\n')
                f.write('        return "Erreur Plug & Play : package manquant. Demandez a utilisateur de lancer : pip install " + reqs_str\n')
                f.write('    except Exception as e:\n')
                f.write('        return f"Erreur inattendue : {e}"\n')
                f.write('\n\n')

                
    # Also update ust/__init__.py _BRANCH_MODULES map to include any new categories
    init_file = "ust/__init__.py"
    with open(init_file, "r") as f:
        content = f.read()
        
    for category in by_cat.keys():
        line = f'    "{category}": "ust.skills.{category}.skills",'
        if f'"{category}":' not in content:
            # find where to insert
            content = content.replace('_BRANCH_MODULES: dict[str, str] = {', f'_BRANCH_MODULES: dict[str, str] = {{\n{line}')
            
    with open(init_file, "w") as f:
        f.write(content)
        
if __name__ == "__main__":
    import_catalog()
    print("DONE building skills from catalog.")
